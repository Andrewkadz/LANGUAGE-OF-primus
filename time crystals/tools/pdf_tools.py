import argparse
import os
import sys
from typing import Optional, Tuple, List


def _choose_backend():
    """Try to import PDF libraries, return (name, module_or_tuple).

    Preferred order: pypdf, PyPDF2, pdfminer.six
    """
    # pypdf
    try:
        import pypdf  # type: ignore
        return ("pypdf", pypdf)
    except Exception:
        pass

    # PyPDF2
    try:
        import PyPDF2  # type: ignore
        return ("PyPDF2", PyPDF2)
    except Exception:
        pass

    # pdfminer.six
    try:
        from pdfminer.high_level import extract_text  # type: ignore
        from pdfminer.pdfpage import PDFPage  # type: ignore
        return ("pdfminer", (extract_text, PDFPage))
    except Exception:
        pass

    return (None, None)


def get_metadata(path: str) -> dict:
    name, mod = _choose_backend()
    meta = {}
    if name is None:
        return meta

    try:
        if name == "pypdf":
            pypdf = mod
            reader = pypdf.PdfReader(path)
            try:
                if getattr(reader, "is_encrypted", False):
                    try:
                        reader.decrypt("")  # type: ignore[attr-defined]
                    except Exception:
                        pass
            except Exception:
                pass
            md = getattr(reader, "metadata", None) or {}
            # pypdf returns an object that behaves like a dict
            def _get(k):
                return md.get(k) if hasattr(md, "get") else getattr(md, k, None)

            meta = {
                "Title": _get("/Title") or _get("Title"),
                "Author": _get("/Author") or _get("Author"),
                "Subject": _get("/Subject") or _get("Subject"),
                "Creator": _get("/Creator") or _get("Creator"),
                "Producer": _get("/Producer") or _get("Producer"),
                "CreationDate": _get("/CreationDate") or _get("CreationDate"),
                "ModDate": _get("/ModDate") or _get("ModDate"),
                "Pages": len(reader.pages),
            }
        elif name == "PyPDF2":
            PyPDF2 = mod
            reader = PyPDF2.PdfReader(path)
            try:
                if getattr(reader, "is_encrypted", False):
                    try:
                        reader.decrypt("")
                    except Exception:
                        pass
            except Exception:
                pass
            md = getattr(reader, "metadata", None) or {}
            def _get(k):
                return md.get(k) if hasattr(md, "get") else getattr(md, k, None)

            meta = {
                "Title": _get("/Title") or _get("Title"),
                "Author": _get("/Author") or _get("Author"),
                "Subject": _get("/Subject") or _get("Subject"),
                "Creator": _get("/Creator") or _get("Creator"),
                "Producer": _get("/Producer") or _get("Producer"),
                "CreationDate": _get("/CreationDate") or _get("CreationDate"),
                "ModDate": _get("/ModDate") or _get("ModDate"),
                "Pages": len(reader.pages),
            }
        else:  # pdfminer
            extract_text, PDFPage = mod
            # pdfminer doesn't expose metadata easily here; provide basic info
            # We'll estimate pages by iterating PDFPage.get_pages
            pages = 0
            try:
                with open(path, "rb") as f:
                    for _ in PDFPage.get_pages(f):
                        pages += 1
            except Exception:
                pages = None  # type: ignore[assignment]
            meta = {
                "Title": None,
                "Author": None,
                "Subject": None,
                "Creator": None,
                "Producer": None,
                "CreationDate": None,
                "ModDate": None,
                "Pages": pages,
            }
    except Exception:
        # On any failure, return what we have (possibly empty)
        pass

    return {k: v for k, v in meta.items() if v is not None}


def extract_pages_text(path: str, max_pages: Optional[int] = None) -> Tuple[List[str], Optional[int]]:
    """Return (page_texts, total_pages or None). If max_pages is set, only extract up to that many pages.
    """
    name, mod = _choose_backend()
    texts: List[str] = []
    total_pages: Optional[int] = None
    if name is None:
        raise RuntimeError("No PDF parser available. Install 'pypdf' or 'PyPDF2' or 'pdfminer.six'.")

    if name == "pypdf":
        pypdf = mod
        reader = pypdf.PdfReader(path)
        try:
            if getattr(reader, "is_encrypted", False):
                try:
                    reader.decrypt("")  # type: ignore[attr-defined]
                except Exception:
                    pass
        except Exception:
            pass
        total_pages = len(reader.pages)
        page_indices = range(total_pages) if max_pages is None else range(min(total_pages, max_pages))
        for i in page_indices:
            page = reader.pages[i]
            try:
                t = page.extract_text() or ""
            except Exception:
                t = ""
            texts.append(t)

    elif name == "PyPDF2":
        PyPDF2 = mod
        reader = PyPDF2.PdfReader(path)
        try:
            if getattr(reader, "is_encrypted", False):
                try:
                    reader.decrypt("")
                except Exception:
                    pass
        except Exception:
            pass
        total_pages = len(reader.pages)
        page_indices = range(total_pages) if max_pages is None else range(min(total_pages, max_pages))
        for i in page_indices:
            page = reader.pages[i]
            try:
                t = page.extract_text() or ""
            except Exception:
                t = ""
            texts.append(t)

    else:  # pdfminer
        extract_text, PDFPage = mod
        # We can only easily get full text or specific pages by number
        # Let's estimate total pages first
        try:
            with open(path, "rb") as f:
                total_pages = sum(1 for _ in PDFPage.get_pages(f))
        except Exception:
            total_pages = None
        pages_to_get = None
        if max_pages is not None:
            pages_to_get = list(range(max_pages))
        try:
            if pages_to_get is None:
                # full doc (can be heavy)
                full_text = extract_text(path) or ""
                texts = full_text.split("\f") if full_text else [""]
            else:
                # pdfminer uses 0-based in this API via page_numbers
                part = extract_text(path, page_numbers=pages_to_get) or ""
                texts = part.split("\f") if part else [""]
        except Exception:
            texts = [""]

    return texts, total_pages


def cmd_peek(path: str, pages: int, per_page_chars: int) -> int:
    print(f"File: {path}")
    md = get_metadata(path)
    if md:
        for k in ["Title", "Author", "Subject", "Creator", "Producer", "CreationDate", "ModDate", "Pages"]:
            if k in md:
                print(f"{k}: {md[k]}")
    else:
        print("Metadata: (unavailable)")

    print("\nPreview:")
    texts, total = extract_pages_text(path, max_pages=pages)
    count = len(texts)
    for i in range(count):
        body = texts[i] or ""
        body = body.replace("\r\n", "\n").replace("\r", "\n")
        if per_page_chars and len(body) > per_page_chars:
            body = body[:per_page_chars] + "\n… [truncated]"
        print(f"\n--- Page {i+1} ---\n{body}")
    if total is not None and pages < total:
        print(f"\n(Showing {count} of {total} pages)")
    return 0


def cmd_extract(path: str, out_path: Optional[str]) -> int:
    if out_path is None:
        base = os.path.basename(path)
        name, _ = os.path.splitext(base)
        out_dir = os.path.join(os.path.dirname(path), "extracted")
        os.makedirs(out_dir, exist_ok=True)
        out_path = os.path.join(out_dir, f"{name}.txt")

    texts, _ = extract_pages_text(path, max_pages=None)
    # Join pages with clear separators
    sep = "\n\n\f\n\n"  # form feed markers between pages
    try:
        with open(out_path, "w", encoding="utf-8", newline="\n") as f:
            f.write(sep.join(texts))
    except Exception as e:
        print(f"Failed to write output: {e}", file=sys.stderr)
        return 1

    print(f"Wrote: {out_path}")
    return 0


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="PDF utilities: peek and extract text")
    sub = parser.add_subparsers(dest="cmd", required=False)

    p_peek = sub.add_parser("peek", help="Print metadata and first pages")
    p_peek.add_argument("path", help="Path to PDF")
    p_peek.add_argument("--pages", type=int, default=2, help="Number of pages to preview")
    p_peek.add_argument("--per-page-chars", type=int, default=2000, help="Max characters per page")

    p_ext = sub.add_parser("extract", help="Extract full text to file")
    p_ext.add_argument("path", help="Path to PDF")
    p_ext.add_argument("-o", "--out", dest="out_path", help="Output text file path")

    args = parser.parse_args(argv)
    if args.cmd in (None, "peek"):
        return cmd_peek(args.path, getattr(args, "pages", 2), getattr(args, "per_page_chars", 2000))
    elif args.cmd == "extract":
        return cmd_extract(args.path, args.out_path)
    else:
        parser.print_help()
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

