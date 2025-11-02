(function(){
  const textarea = document.getElementById('inputText');
  const runBtn = document.getElementById('runBtn');
  const modeSelect = document.getElementById('modeSelect');
  const traceView = document.getElementById('traceView');
  const xiCount = document.getElementById('xiCount');
  const tickCount = document.getElementById('tickCount');
  const xiBar = document.getElementById('xiBar');
  const motifsEl = document.getElementById('motifs');

  const symbols = ['Σ','Δ','Ψ','→','+',' : ','/','|','^','=','(',')','[',']',',','Π','Λ','Ξ','ζ'];
  const pad = document.getElementById('symbolPad');
  symbols.forEach(sym => {
    const b = document.createElement('button');
    b.className = 'symbol-btn';
    b.textContent = sym.trim();
    b.addEventListener('click', () => insertAtCursor(textarea, sym));
    pad.appendChild(b);
  });

  function insertAtCursor(el, text){
    const [start, end] = [el.selectionStart, el.selectionEnd];
    const before = el.value.substring(0, start);
    const after = el.value.substring(end);
    el.value = before + text + after;
    const cursor = start + text.length;
    el.selectionStart = el.selectionEnd = cursor;
    el.focus();
  }

  function mockRun(){
    // Static scaffold: generate a few placeholder Λ entries.
    const input = textarea.value.trim() || '(empty)';
    const mode = modeSelect.value;
    const now = new Date().toLocaleTimeString();
    const steps = [
      `Λ[ Λ, input=${input}, output=Π(${input}), context=Φ, loop=Σ([Δ:Ψ]), tick=Σ(ζ) ]`,
      `Λ[ →, input=${input}, output=${input} → Λ, context=Φ, loop=Σ([Δ:Ψ],[Δ:Ψ]), tick=Σ(ζ, ζ) ]`,
      `Λ[ Ξ, input=${input}, output=Ξ(${input}), context=Φ, loop=Σ([Δ:Ψ],[Δ:Ψ],[Δ:Ψ]), tick=Σ(ζ, ζ, ζ) ]`
    ];
    steps.forEach(s => appendTrace(`${now}  ${s}`));

    // Update meters
    const currentXi = parseInt(xiCount.dataset.xi || '0', 10) + 1;
    xiCount.dataset.xi = String(currentXi);
    xiCount.textContent = `Ξ: ${currentXi}`;
    const currentTick = parseInt(tickCount.dataset.t || '0', 10) + 3;
    tickCount.dataset.t = String(currentTick);
    tickCount.textContent = `ζ: ${currentTick}`;
    xiBar.style.width = Math.min(100, currentXi * 10) + '%';
    // Motifs
    motifsEl.innerHTML = '';
    for (let i=0;i<currentXi;i++){
      const chip = document.createElement('span');
      chip.className = 'motif-chip';
      chip.textContent = '[Δ:Ψ]';
      motifsEl.appendChild(chip);
    }
  }

  function appendTrace(line){
    const div = document.createElement('div');
    div.textContent = line;
    traceView.appendChild(div);
    traceView.scrollTop = traceView.scrollHeight;
  }

  runBtn.addEventListener('click', mockRun);
})();
