import pandas as pd
import json

df = pd.read_excel('3000.xlsx')

words = []
for _, row in df.iterrows():
    word = str(row['Word']).strip() if pd.notna(row['Word']) else ''
    uk = str(row['UK Phonetics']).strip() if pd.notna(row['UK Phonetics']) else ''
    us = str(row['US Phonetics']).strip() if pd.notna(row['US Phonetics']) else ''
    p_cn = str(row['Paraphrase']).strip() if pd.notna(row['Paraphrase']) else ''
    p_pos = str(row['Paraphrase (w/ POS)']).strip() if pd.notna(row['Paraphrase (w/ POS)']) else ''
    p_en = str(row['Paraphrase (English)']).strip() if pd.notna(row['Paraphrase (English)']) else ''
    if word:
        words.append({
            'w': word,
            'uk': uk,
            'us': us,
            'cn': p_cn,
            'pos': p_pos,
            'en': p_en
        })

js_data = json.dumps(words, ensure_ascii=False)

html_template = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
<title>GRE 3000 Words - Fast Navigator</title>
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #0f1117; color: #e1e4e8; height: 100vh; display: flex; flex-direction: column; }
.header { background: #161b22; border-bottom: 1px solid #30363d; padding: 12px 20px; }
.header h1 { font-size: 18px; color: #58a6ff; margin-bottom: 10px; }
.controls { display: flex; gap: 8px; flex-wrap: wrap; align-items: center; }
.controls input[type="text"], .controls input[type="number"] { background: #0d1117; border: 1px solid #30363d; color: #e1e4e8; padding: 7px 10px; border-radius: 6px; font-size: 14px; outline: none; }
.controls input:focus { border-color: #58a6ff; }
#searchInput { width: 200px; }
#jumpInput { width: 70px; }
.btn { background: #21262d; border: 1px solid #30363d; color: #c9d1d9; padding: 7px 12px; border-radius: 6px; cursor: pointer; font-size: 12px; white-space: nowrap; }
.btn:hover { background: #30363d; }
.btn.active { background: #1f6feb; border-color: #1f6feb; color: #fff; }
.btn.danger { border-color: #f85149; color: #f85149; }
.btn.danger:hover { background: #f8514920; }
.btn.flag-active { background: #d29922; border-color: #d29922; color: #000; }
.alpha-nav { display: flex; gap: 2px; flex-wrap: wrap; margin-top: 8px; }
.alpha-nav button { background: #21262d; border: 1px solid #30363d; color: #8b949e; padding: 3px 7px; border-radius: 4px; cursor: pointer; font-size: 12px; min-width: 26px; }
.alpha-nav button:hover { background: #30363d; color: #e1e4e8; }
.alpha-nav button.active { background: #1f6feb; border-color: #1f6feb; color: #fff; }
.toolbar { display: flex; gap: 6px; flex-wrap: wrap; margin-top: 8px; align-items: center; }
.toolbar .label { color: #8b949e; font-size: 12px; }
.stats { color: #8b949e; font-size: 12px; margin-left: auto; }
.main { flex: 1; overflow-y: auto; padding: 10px 20px; min-height: 0; }
.header-row { display: grid; grid-template-columns: 30px 30px 160px 1fr 2fr 2fr; gap: 10px; padding: 6px 12px; font-size: 11px; color: #484f58; border-bottom: 1px solid #21262d; margin-bottom: 4px; }
.word-list { display: flex; flex-direction: column; gap: 3px; }
.word-item { display: grid; grid-template-columns: 30px 30px 160px 1fr 2fr 2fr; gap: 10px; padding: 8px 12px; background: #161b22; border-radius: 6px; border: 1px solid #21262d; align-items: center; font-size: 13px; cursor: pointer; }
.word-item:hover { border-color: #30363d; background: #1c2128; }
.word-item.highlighted { border-color: #1f6feb; background: #1c2128; }
.word-item.selected { border-color: #3fb950; background: #3fb95010; }
.word-item input[type="checkbox"] { width: 16px; height: 16px; cursor: pointer; accent-color: #3fb950; }
.flag-btn { background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.1); cursor: pointer; font-size: 16px; padding: 4px 8px; opacity: 0.4; transition: all 0.15s; border-radius: 4px; color: #8b949e; }
.flag-btn:hover { opacity: 0.8; background: rgba(210, 168, 34, 0.15); border-color: rgba(210, 168, 34, 0.3); color: #d2a8ff; }
.flag-btn.flagged { opacity: 1; background: rgba(210, 168, 34, 0.25); border-color: #d2a8ff; color: #f0c674; box-shadow: 0 0 8px rgba(210, 168, 34, 0.3); }
.word-index { color: #484f58; font-size: 11px; font-family: monospace; }
.word-name { color: #58a6ff; font-weight: 600; font-size: 14px; }
.word-phonetic { color: #8b949e; font-size: 11px; }
.word-phonetic .label { color: #484f58; font-size: 10px; margin-right: 3px; }
.word-pos { color: #d2a8ff; font-size: 12px; }
.word-en { color: #7ee787; font-size: 12px; }
.shortcuts { background: #161b22; border-top: 1px solid #30363d; padding: 6px 20px; display: flex; gap: 14px; font-size: 11px; color: #484f58; flex-wrap: wrap; }
.shortcuts kbd { background: #21262d; border: 1px solid #30363d; padding: 1px 4px; border-radius: 3px; font-family: monospace; color: #8b949e; font-size: 10px; }
#flagFileInput { display: none; }
.mobile-view { display: none; }
.desktop-view { display: flex; flex-direction: column; flex: 1; min-height: 0; }

@media (max-width: 768px) {
  .header { padding: 10px 12px; }
  .header h1 { font-size: 15px; margin-bottom: 6px; }
  .controls { gap: 6px; }
  #searchInput { width: 100%; order: -1; }
  .main { padding: 8px 10px; }
  .desktop-view { display: none !important; }
  .mobile-view { display: flex; flex-direction: column; flex: 1; overflow: hidden; }
  .shortcuts { display: none; }
  .header-row { display: none; }

  .mobile-tabs { display: flex; gap: 0; background: #161b22; border-bottom: 1px solid #30363d; }
  .mobile-tabs button { flex: 1; padding: 10px; background: none; border: none; border-bottom: 2px solid transparent; color: #8b949e; font-size: 13px; cursor: pointer; }
  .mobile-tabs button.active { color: #58a6ff; border-bottom-color: #58a6ff; }

  .flashcard-container { flex: 1; display: flex; flex-direction: column; overflow: hidden; }
  .flashcard-container.hidden { display: none; }
  .flashcard-area { flex: 1; display: flex; align-items: center; justify-content: center; padding: 20px; perspective: 1000px; }
  .flashcard { width: 100%; max-width: 360px; min-height: 240px; position: relative; transform-style: preserve-3d; transition: transform 0.4s ease; cursor: pointer; }
  .flashcard.flipped { transform: rotateY(180deg); }
  .flashcard-face { position: absolute; inset: 0; backface-visibility: hidden; border-radius: 12px; padding: 24px; display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center; }
  .flashcard-front { background: #161b22; border: 1px solid #30363d; }
  .flashcard-back { background: #1c2128; border: 1px solid #30363d; transform: rotateY(180deg); }
  .flashcard-front .fc-word { font-size: 28px; font-weight: 700; color: #58a6ff; margin-bottom: 12px; }
  .flashcard-front .fc-phonetic { font-size: 14px; color: #8b949e; line-height: 1.6; }
  .flashcard-front .fc-index { position: absolute; top: 12px; left: 16px; font-size: 11px; color: #484f58; }
  .flashcard-front .fc-flag { position: absolute; top: 10px; right: 14px; }
  .flashcard-back .fc-pos { font-size: 15px; color: #d2a8ff; margin-bottom: 12px; }
  .flashcard-back .fc-en { font-size: 15px; color: #7ee787; line-height: 1.5; }
  .flashcard-back .fc-cn { font-size: 14px; color: #f0883e; margin-top: 10px; }
  .flashcard-nav { display: flex; gap: 10px; padding: 12px 20px; justify-content: center; align-items: center; background: #161b22; border-top: 1px solid #30363d; }
  .flashcard-nav .btn { padding: 10px 20px; font-size: 14px; }
  .flashcard-nav .fc-counter { color: #8b949e; font-size: 13px; min-width: 80px; text-align: center; }

  .quicklist-container { flex: 1; overflow-y: auto; }
  .quicklist-container.hidden { display: none; }
  .quicklist-item { display: flex; align-items: center; gap: 10px; padding: 10px 14px; border-bottom: 1px solid #21262d; cursor: pointer; }
  .quicklist-item:active { background: #1c2128; }
  .quicklist-item .ql-flag { font-size: 14px; opacity: 0.3; flex-shrink: 0; }
  .quicklist-item .ql-flag.flagged { opacity: 1; }
  .quicklist-item .ql-word { color: #58a6ff; font-weight: 600; font-size: 15px; flex: 1; }
  .quicklist-item .ql-pos { color: #8b949e; font-size: 12px; }
}
</style>
</head>
<body>
<div class="header">
<h1>GRE 3000 Words</h1>
<div class="controls">
<input type="text" id="searchInput" placeholder="Search..." autocomplete="off">
<input type="number" id="jumpInput" placeholder="#" min="1" max="__WORD_COUNT__">
<button class="btn" onclick="jumpToIndex()">Go</button>
<button class="btn" id="filterFlagBtn" onclick="toggleFlagFilter()">&#9873; Flagged</button>
<span class="stats" id="stats">__WORD_COUNT__ words</span>
</div>
<div class="alpha-nav" id="alphaNav"></div>
<div class="toolbar">
<span class="label">Select:</span>
<button class="btn" onclick="selectAll()">All</button>
<button class="btn" onclick="selectNone()">None</button>
<button class="btn" onclick="selectVisible()">Visible</button>
<span class="label" style="margin-left:8px">Flag:</span>
<button class="btn" onclick="exportFlags()">&#9873; Export .flag</button>
<button class="btn" onclick="document.getElementById('flagFileInput').click()">&#128194; Import .flag</button>
<input type="file" id="flagFileInput" accept=".flag,.json" onchange="importFlags(event)">
<span class="label" style="margin-left:8px">Export:</span>
<button class="btn" onclick="exportSelected()">Export Selected</button>
<button class="btn danger" onclick="clearSelection()" id="clearSelBtn" style="display:none">Clear (0)</button>
</div>
</div>

<div class="desktop-view" id="desktopView">
<div class="main" id="main">
<div class="header-row">
<span>&#9744;</span><span>&#9873;</span><span>Word</span><span>Phonetics</span><span>POS</span><span>English</span>
</div>
<div class="word-list" id="wordList"></div>
</div>
</div>

<div class="mobile-view" id="mobileView">
<div class="mobile-tabs">
<button class="active" onclick="switchMobileTab('flashcard')">Flashcard</button>
<button onclick="switchMobileTab('quicklist')">Quick List</button>
</div>
<div class="flashcard-container" id="flashcardContainer">
<div class="flashcard-area">
<div class="flashcard" id="flashcard" onclick="flipCard()">
<div class="flashcard-face flashcard-front">
<span class="fc-index" id="fcIndex"></span>
<button class="flag-btn fc-flag" id="fcFlag" onclick="event.stopPropagation(); toggleFlagCard()">&#9873;</button>
<div class="fc-word" id="fcWord"></div>
<div class="fc-phonetic" id="fcPhonetic"></div>
</div>
<div class="flashcard-face flashcard-back">
<div class="fc-pos" id="fcPos"></div>
<div class="fc-en" id="fcEn"></div>
<div class="fc-cn" id="fcCn"></div>
</div>
</div>
</div>
<div class="flashcard-nav">
<button class="btn" onclick="cardPrev()">&#9664; Prev</button>
<span class="fc-counter" id="fcCounter"></span>
<button class="btn" onclick="cardNext()">Next &#9654;</button>
</div>
</div>
<div class="quicklist-container hidden" id="quicklistContainer">
<div id="quicklist"></div>
</div>
</div>

<div class="shortcuts">
<span><kbd>/</kbd> Search</span>
<span><kbd>Enter</kbd> Jump</span>
<span><kbd>Esc</kbd> Clear</span>
<span><kbd>&#8593;&#8595;</kbd> Nav</span>
<span><kbd>Space</kbd> Select</span>
<span><kbd>F</kbd> Flag</span>
</div>

<script>
const WORDS = WORD_DATA_PLACEHOLDER;
const TOTAL_WORDS = WORDS.length;
let filteredWords = WORDS.map((w, i) => ({ ...w, idx: i }));
let highlightedIdx = -1;
let selectedSet = new Set();
let flaggedIdx = -1;
let showFlaggedOnly = false;
let cardIdx = 0;
let cardFlipped = false;

const wordList = document.getElementById('wordList');
const searchInput = document.getElementById('searchInput');
const jumpInput = document.getElementById('jumpInput');
const stats = document.getElementById('stats');
const main = document.getElementById('main');
const alphaNav = document.getElementById('alphaNav');

const savedFlag = localStorage.getItem('gre_flag');
if (savedFlag) {
  try { flaggedIdx = parseInt(savedFlag); } catch(e) {}
}

function saveFlag() {
  localStorage.setItem('gre_flag', flaggedIdx.toString());
}

const letters = 'abcdefghijklmnopqrstuvwxyz'.split('');
letters.forEach(l => {
  const btn = document.createElement('button');
  btn.textContent = l.toUpperCase();
  btn.onclick = () => {
    searchInput.value = l;
    filterWords(true);
    document.querySelectorAll('.alpha-nav button').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
  };
  alphaNav.appendChild(btn);
});

function renderWords() {
  const fragment = document.createDocumentFragment();
  filteredWords.forEach((w, i) => {
    const div = document.createElement('div');
    const isSel = selectedSet.has(w.idx);
    const isFlag = flaggedIdx === w.idx;
    div.className = 'word-item' + (i === highlightedIdx ? ' highlighted' : '') + (isSel ? ' selected' : '');
    div.dataset.index = i;
    div.innerHTML = `
      <input type="checkbox" ${isSel ? 'checked' : ''} onclick="event.stopPropagation(); toggleSelect(${w.idx})">
      <button class="flag-btn ${isFlag ? 'flagged' : ''}" onclick="event.stopPropagation(); toggleFlag(${w.idx})" title="Flag">&#9873;</button>
      <div><div class="word-name">${w.w}</div></div>
      <div class="word-phonetic">
        <div><span class="label">UK</span> ${w.uk}</div>
        <div><span class="label">US</span> ${w.us}</div>
      </div>
      <div><div class="word-pos">${w.pos}</div></div>
      <div class="word-en">${w.en}</div>
    `;
    div.onclick = () => { highlightedIdx = i; renderWords(); };
    fragment.appendChild(div);
  });
  wordList.innerHTML = '';
  wordList.appendChild(fragment);
  updateStats();
}

function updateStats() {
  let s = filteredWords.length + ' / ' + WORDS.length + ' words';
  if (selectedSet.size > 0) s += ' | ' + selectedSet.size + ' selected';
  if (flaggedIdx >= 0) s += ' | 1 flagged';
  stats.textContent = s;
  const btn = document.getElementById('clearSelBtn');
  if (selectedSet.size > 0) { btn.style.display = ''; btn.textContent = 'Clear (' + selectedSet.size + ')'; }
  else { btn.style.display = 'none'; }
}

function filterWords(prefixOnly = false) {
  const query = searchInput.value.toLowerCase().trim();
  let base = WORDS.map((w, i) => ({ ...w, idx: i }));
  if (showFlaggedOnly && flaggedIdx >= 0) base = base.filter(w => w.idx === flaggedIdx);
  if (!query) {
    filteredWords = base;
  } else {
    filteredWords = base.filter(w =>
      prefixOnly ? w.w.toLowerCase().startsWith(query) : w.w.toLowerCase().includes(query)
    );
  }
  highlightedIdx = -1;
  renderWords();
  if (main) main.scrollTop = 0;
  cardIdx = 0;
  cardFlipped = false;
  renderMobile();
}

function jumpToIndex() {
  const idx = parseInt(jumpInput.value);
  if (idx >= 1 && idx <= WORDS.length) {
    searchInput.value = '';
    showFlaggedOnly = false;
    document.getElementById('filterFlagBtn').classList.remove('active');
    filteredWords = WORDS.map((w, i) => ({ ...w, idx: i }));
    highlightedIdx = idx - 1;
    renderWords();
    cardIdx = idx - 1;
    cardFlipped = false;
    renderMobile();
    setTimeout(() => {
      const el = document.querySelector('.word-item.highlighted');
      if (el) el.scrollIntoView({ block: 'center' });
    }, 50);
  }
}

function toggleSelect(idx) {
  if (selectedSet.has(idx)) selectedSet.delete(idx); else selectedSet.add(idx);
  renderWords();
  renderMobile();
}
function selectAll() { WORDS.forEach((_, i) => selectedSet.add(i)); renderWords(); renderMobile(); }
function selectNone() { selectedSet.clear(); renderWords(); renderMobile(); }
function selectVisible() { filteredWords.forEach(w => selectedSet.add(w.idx)); renderWords(); renderMobile(); }
function clearSelection() { selectedSet.clear(); renderWords(); renderMobile(); }

function toggleFlag(idx) {
  if (flaggedIdx === idx) {
    flaggedIdx = -1;
  } else {
    flaggedIdx = idx;
  }
  saveFlag();
  renderWords();
  renderMobile();
}
function toggleFlagFilter() {
  showFlaggedOnly = !showFlaggedOnly;
  document.getElementById('filterFlagBtn').classList.toggle('active', showFlaggedOnly);
  filterWords();
}

function exportFlags() {
  if (flaggedIdx < 0) { alert('No word flagged'); return; }
  const w = WORDS[flaggedIdx];
  const data = JSON.stringify({ version: 1, flag: w.w, index: flaggedIdx }, null, 2);
  downloadFile('gre_flag.flag', data);
}
function importFlags(event) {
  const file = event.target.files[0];
  if (!file) return;
  const reader = new FileReader();
  reader.onload = (e) => {
    try {
      const data = JSON.parse(e.target.result);
      if (data.index !== undefined && data.index >= 0 && data.index < WORDS.length) {
        flaggedIdx = data.index;
      } else if (data.flag) {
        const idx = WORDS.findIndex(x => x.w === data.flag);
        if (idx >= 0) flaggedIdx = idx;
      }
      saveFlag();
      renderWords();
      renderMobile();
      alert('Imported flagged word: ' + WORDS[flaggedIdx].w);
    } catch(err) { alert('Invalid flag file'); }
  };
  reader.readAsText(file);
  event.target.value = '';
}

function exportSelected() {
  if (selectedSet.size === 0) { alert('No words selected'); return; }
  const sorted = Array.from(selectedSet).sort((a,b) => a - b);
  const lines = sorted.map(i => {
    const w = WORDS[i];
    return `${i+1}. ${w.w}\\n   UK: ${w.uk}  US: ${w.us}\\n   ${w.pos}\\n   ${w.en}`;
  });
  downloadFile('gre_selected.txt', lines.join('\\n\\n'));
}

function downloadFile(name, content) {
  const blob = new Blob([content], { type: 'text/plain;charset=utf-8' });
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = name;
  a.click();
  URL.revokeObjectURL(a.href);
}

searchInput.addEventListener('input', () => filterWords(false));
jumpInput.addEventListener('keydown', e => { if (e.key === 'Enter') jumpToIndex(); });

document.addEventListener('keydown', e => {
  if (e.key === '/' && document.activeElement !== searchInput && document.activeElement !== jumpInput) {
    e.preventDefault(); searchInput.focus();
  }
  if (e.key === 'Escape') {
    searchInput.value = ''; jumpInput.value = '';
    document.querySelectorAll('.alpha-nav button').forEach(b => b.classList.remove('active'));
    showFlaggedOnly = false;
    document.getElementById('filterFlagBtn').classList.remove('active');
    filterWords();
    searchInput.blur();
  }
  if (document.activeElement === searchInput || document.activeElement === jumpInput) return;
  if (e.key === 'ArrowDown') {
    e.preventDefault();
    highlightedIdx = Math.min(highlightedIdx + 1, filteredWords.length - 1);
    renderWords();
    const el = document.querySelector('.word-item.highlighted');
    if (el) el.scrollIntoView({ block: 'nearest' });
  }
  if (e.key === 'ArrowUp') {
    e.preventDefault();
    highlightedIdx = Math.max(highlightedIdx - 1, 0);
    renderWords();
    const el = document.querySelector('.word-item.highlighted');
    if (el) el.scrollIntoView({ block: 'nearest' });
  }
  if (e.key === 'PageDown') {
    e.preventDefault();
    highlightedIdx = Math.min(highlightedIdx + 20, filteredWords.length - 1);
    renderWords();
    const el = document.querySelector('.word-item.highlighted');
    if (el) el.scrollIntoView({ block: 'nearest' });
  }
  if (e.key === 'PageUp') {
    e.preventDefault();
    highlightedIdx = Math.max(highlightedIdx - 20, 0);
    renderWords();
    const el = document.querySelector('.word-item.highlighted');
    if (el) el.scrollIntoView({ block: 'nearest' });
  }
  if (e.key === ' ' && filteredWords.length > 0) {
    e.preventDefault();
    const target = highlightedIdx >= 0 ? highlightedIdx : 0;
    toggleSelect(filteredWords[target].idx);
  }
  if (e.key === 'f' || e.key === 'F') {
    if (filteredWords.length > 0) {
      const target = highlightedIdx >= 0 ? highlightedIdx : 0;
      toggleFlag(filteredWords[target].idx);
    }
  }
});

function switchMobileTab(tab) {
  document.querySelectorAll('.mobile-tabs button').forEach(b => b.classList.remove('active'));
  event.target.classList.add('active');
  document.getElementById('flashcardContainer').classList.toggle('hidden', tab !== 'flashcard');
  document.getElementById('quicklistContainer').classList.toggle('hidden', tab !== 'quicklist');
  if (tab === 'flashcard') renderCard();
  if (tab === 'quicklist') renderQuicklist();
}

function renderCard() {
  if (filteredWords.length === 0) return;
  if (cardIdx >= filteredWords.length) cardIdx = filteredWords.length - 1;
  if (cardIdx < 0) cardIdx = 0;
  const w = filteredWords[cardIdx];
  const isFlag = flaggedIdx === w.idx;
  document.getElementById('fcIndex').textContent = '#' + (w.idx + 1);
  document.getElementById('fcWord').textContent = w.w;
  document.getElementById('fcPhonetic').innerHTML = 'UK ' + w.uk + '<br>US ' + w.us;
  document.getElementById('fcPos').textContent = w.pos;
  document.getElementById('fcEn').textContent = w.en;
  document.getElementById('fcCn').textContent = w.cn;
  document.getElementById('fcFlag').className = 'flag-btn fc-flag' + (isFlag ? ' flagged' : '');
  document.getElementById('fcCounter').textContent = (cardIdx + 1) + ' / ' + filteredWords.length;
  document.getElementById('flashcard').classList.toggle('flipped', cardFlipped);
}

function flipCard() { cardFlipped = !cardFlipped; document.getElementById('flashcard').classList.toggle('flipped', cardFlipped); }
function cardPrev() { cardFlipped = false; cardIdx = Math.max(0, cardIdx - 1); renderCard(); }
function cardNext() { cardFlipped = false; cardIdx = Math.min(filteredWords.length - 1, cardIdx + 1); renderCard(); }
function toggleFlagCard() {
  if (filteredWords.length === 0) return;
  toggleFlag(filteredWords[cardIdx].idx);
  renderCard();
}

function renderQuicklist() {
  const el = document.getElementById('quicklist');
  const fragment = document.createDocumentFragment();
  filteredWords.forEach((w, i) => {
    const div = document.createElement('div');
    div.className = 'quicklist-item';
    const isFlag = flaggedIdx === w.idx;
    div.innerHTML = `
      <span class="ql-flag ${isFlag ? 'flagged' : ''}" onclick="event.stopPropagation(); toggleFlag(${w.idx}); renderQuicklist();">&#9873;</span>
      <span class="ql-word">${w.w}</span>
      <span class="ql-pos">${w.pos}</span>
    `;
    div.onclick = () => { cardIdx = i; cardFlipped = false; switchMobileTabDirect('flashcard'); renderCard(); };
    fragment.appendChild(div);
  });
  el.innerHTML = '';
  el.appendChild(fragment);
}

function switchMobileTabDirect(tab) {
  document.querySelectorAll('.mobile-tabs button').forEach(b => b.classList.remove('active'));
  const tabs = document.querySelectorAll('.mobile-tabs button');
  if (tab === 'flashcard' && tabs[0]) tabs[0].classList.add('active');
  if (tab === 'quicklist' && tabs[1]) tabs[1].classList.add('active');
  document.getElementById('flashcardContainer').classList.toggle('hidden', tab !== 'flashcard');
  document.getElementById('quicklistContainer').classList.toggle('hidden', tab !== 'quicklist');
}

function renderMobile() {
  renderCard();
  if (!document.getElementById('quicklistContainer').classList.contains('hidden')) renderQuicklist();
}

renderWords();
renderMobile();
</script>
</body>
</html>'''

html = html_template.replace('WORD_DATA_PLACEHOLDER', js_data)
html = html.replace('__WORD_COUNT__', str(len(words)))

with open('gre_words.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f'Generated gre_words.html with {len(words)} words')
