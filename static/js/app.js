// Astro-Nepali web frontend logic.
(function () {
  const $ = (sel, root = document) => root.querySelector(sel);
  const $$ = (sel, root = document) => Array.from(root.querySelectorAll(sel));

  // ------- Theme + locale persistence -------
  const themeSelect = $('#theme-select');
  const localeSelect = $('#locale-select');

  function setPref(key, value) {
    document.documentElement.dataset[key === 'theme' ? 'theme' : 'locale'] = value;
    fetch('/api/set-pref', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ [key]: value }),
    }).then(() => {
      // Reload to pick up server-side template changes (locale changes labels)
      if (key === 'locale') window.location.reload();
    });
  }

  if (themeSelect) {
    themeSelect.addEventListener('change', e => setPref('theme', e.target.value));
  }
  if (localeSelect) {
    localeSelect.addEventListener('change', e => setPref('locale', e.target.value));
  }

  // ------- Compute form (only on home page) -------
  const computeForm = $('#compute-form');
  if (!computeForm) return;

  // BS toggle (hides both label and field of the unused row)
  const bsToggle = $('#use-bs');
  const adInput = $('#ad-date');
  const adLabel = $('#row-date-ad-label');
  const bsRow = $('#row-date-bs');
  const bsLabel = $('#row-date-bs-label');
  if (bsToggle) {
    bsToggle.addEventListener('change', () => {
      const useBs = bsToggle.checked;
      if (adInput) adInput.style.display = useBs ? 'none' : '';
      if (adLabel) adLabel.style.display = useBs ? 'none' : '';
      if (bsRow) bsRow.style.display = useBs ? '' : 'none';
      if (bsLabel) bsLabel.style.display = useBs ? '' : 'none';
    });
  }

  // Place search
  const searchBtn = $('#search-place');
  const placeInput = $('#place');
  const resultsList = $('#place-results');
  const latInput = $('#lat');
  const lonInput = $('#lon');
  const tzInput = $('#tz');

  function clearResults() {
    resultsList.innerHTML = '';
    resultsList.style.display = 'none';
  }

  async function doSearch() {
    const q = placeInput.value.trim();
    if (!q) return;
    resultsList.innerHTML = '<li class="muted">Searching…</li>';
    resultsList.style.display = 'block';
    try {
      const res = await fetch('/api/search-place?q=' + encodeURIComponent(q));
      const data = await res.json();
      if (!data.results || !data.results.length) {
        resultsList.innerHTML = '<li class="muted">No matches.</li>';
        return;
      }
      resultsList.innerHTML = '';
      data.results.forEach(r => {
        const li = document.createElement('li');
        li.innerHTML = `<div>${r.display}</div><div class="coords">${r.lat.toFixed(4)}, ${r.lon.toFixed(4)}</div>`;
        li.addEventListener('click', () => pickPlace(r));
        resultsList.appendChild(li);
      });
    } catch (e) {
      resultsList.innerHTML = '<li class="error">Search failed.</li>';
    }
  }

  async function pickPlace(r) {
    latInput.value = r.lat.toFixed(6);
    lonInput.value = r.lon.toFixed(6);
    placeInput.value = r.display.split(',')[0];
    clearResults();
    // Resolve timezone for the entered date
    const date = $('#ad-date').value || new Date().toISOString().slice(0, 10);
    try {
      const tzRes = await fetch(`/api/timezone?lat=${r.lat}&lon=${r.lon}&date=${date}`);
      const tzData = await tzRes.json();
      if (tzData.offset != null) tzInput.value = tzData.offset.toFixed(2);
    } catch (e) { /* ignore */ }
  }

  if (searchBtn) searchBtn.addEventListener('click', doSearch);
  if (placeInput) {
    placeInput.addEventListener('keydown', e => {
      if (e.key === 'Enter') { e.preventDefault(); doSearch(); }
    });
  }

  // ------- Submit -------
  const tabsContainer = $('#result-tabs');
  const tabBtns = $$('.tab-btn', tabsContainer);
  const tabPanels = $$('.tab-panel', tabsContainer);
  const errorBox = $('#error-box');
  const resultArea = $('#result-area');
  const loading = $('#loading');

  tabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      tabBtns.forEach(b => b.classList.remove('active'));
      tabPanels.forEach(p => p.classList.remove('active'));
      btn.classList.add('active');
      $('#tab-' + btn.dataset.tab).classList.add('active');
    });
  });

  computeForm.addEventListener('submit', async e => {
    e.preventDefault();
    errorBox.style.display = 'none';
    loading.style.display = 'block';
    resultArea.style.display = 'none';

    const useBs = $('#use-bs').checked;
    const payload = {
      name: $('#name').value.trim(),
      date_mode: useBs ? 'bs' : 'ad',
      ad_date: $('#ad-date').value,
      bs_year: $('#bs-year').value,
      bs_month: $('#bs-month').value,
      bs_day: $('#bs-day').value,
      time: $('#time').value,
      lat: parseFloat($('#lat').value),
      lon: parseFloat($('#lon').value),
      tz: parseFloat($('#tz').value),
      place: $('#place').value.trim(),
      locale: document.documentElement.lang || 'en',
      theme: document.documentElement.dataset.theme || 'light',
    };

    try {
      const res = await fetch('/api/compute', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });
      const data = await res.json();
      if (data.error) {
        errorBox.textContent = data.error;
        errorBox.style.display = 'block';
        loading.style.display = 'none';
        return;
      }
      $('#tab-summary').innerHTML = data.summary;
      $('#tab-topics').innerHTML = data.topics || '';
      $('#tab-drik').innerHTML = data.drik;
      $('#tab-d9').innerHTML = data.d9 || '';
      $('#tab-yogas').innerHTML = data.yogas || '';
      $('#tab-dasha').innerHTML = data.dasha;
      $('#tab-antardasha').innerHTML = data.antardasha || '';
      $('#tab-ss').innerHTML = data.ss;
      $('#tab-compare').innerHTML = data.compare;
      $('#tab-explanation').innerHTML = data.explanation;
      loading.style.display = 'none';
      resultArea.style.display = 'block';
      // Activate first tab
      tabBtns.forEach(b => b.classList.remove('active'));
      tabPanels.forEach(p => p.classList.remove('active'));
      tabBtns[0].classList.add('active');
      tabPanels[0].classList.add('active');
      // Scroll into view
      resultArea.scrollIntoView({ behavior: 'smooth', block: 'start' });
    } catch (err) {
      errorBox.textContent = 'Compute failed: ' + err.message;
      errorBox.style.display = 'block';
      loading.style.display = 'none';
    }
  });

  // ------- Export as PDF (client-side print) -------
  const btnExport = $('#btn-export-pdf');
  if (btnExport) {
    btnExport.addEventListener('click', () => {
      // Tabs in the order they should appear in the PDF
      const order = [
        ['summary',     'Summary'],
        ['topics',      'Life Topics'],
        ['drik',        'Drik + Janma Kundali'],
        ['d9',          'D9 Navamsha'],
        ['yogas',       'Yogas'],
        ['dasha',       'Vimshottari Mahadasha'],
        ['antardasha',  'Antardasha (Sub-periods)'],
        ['ss',          'Surya Siddhanta'],
        ['compare',     'Drik vs Surya Siddhanta'],
        ['explanation', 'Explanation'],
      ];
      const name = ($('#name').value || 'Kundali').trim();
      const printCss = `
        @page { size: A4; margin: 16mm 14mm; }
        body { font-family: 'Segoe UI', 'Mangal', 'Nirmala UI', Arial, sans-serif;
               color: #222; font-size: 12px; line-height: 1.5; }
        h1 { color: #4a148c; text-align: center; margin: 0 0 4px 0; }
        h2 { color: #4a148c; border-bottom: 2px solid #ce93d8; padding-bottom: 4px;
             page-break-after: avoid; margin-top: 14px; }
        h3 { color: #6a1b9a; page-break-after: avoid; }
        h4 { color: #7b1fa2; page-break-after: avoid; }
        section.page { page-break-after: always; }
        section.page:last-child { page-break-after: auto; }
        table { width: 100%; border-collapse: collapse; margin: 4px 0 10px 0; font-size: 11px; }
        th { background: #ede7f6; color: #4a148c; text-align: left;
             padding: 4px 8px; border: 1px solid #d1c4e9; }
        td { padding: 4px 8px; border: 1px solid #e1bee7; vertical-align: top; }
        tr { page-break-inside: avoid; }
        .panel, .era, .edu, .planet-block {
          background: #f3e5f5; border-left: 4px solid #8e24aa;
          padding: 8px 12px; margin: 6px 0; page-break-inside: avoid; }
        .edu { background: #fff8e1; border-left-color: #fbc02d; }
        img, svg { max-width: 100%; height: auto; page-break-inside: avoid; }
        .footer { margin-top: 20px; padding-top: 8px; border-top: 1px solid #ddd;
                  text-align: center; color: #888; font-size: 11px; }
        .footer a { color: #6a1b9a; text-decoration: none; }
        .small { font-size: 10px; color: #666; }
      `;
      const date = new Date().toLocaleDateString();
      const titleHtml = `
        <h1>${escapeHtml(name)} — Janma Kundali</h1>
        <div style="text-align:center;color:#666;font-size:11px;margin-bottom:14px;">
          Generated ${date} ·
          <a href="https://www.sandeepkafle.com.np">www.sandeepkafle.com.np</a>
        </div>
      `;
      let body = titleHtml;
      for (const [tabId, sectionTitle] of order) {
        const el = document.getElementById(`tab-${tabId}`);
        if (!el || !el.innerHTML.trim()) continue;
        body += `<section class="page">${el.innerHTML}</section>`;
      }
      body += `
        <div class="footer">
          © Astro-Nepali ·
          <a href="https://www.sandeepkafle.com.np">www.sandeepkafle.com.np</a>
        </div>
      `;
      const doc = `<!DOCTYPE html>
<html lang="${document.documentElement.lang || 'en'}">
<head>
  <meta charset="utf-8">
  <title>Kundali — ${escapeHtml(name)}</title>
  <style>${printCss}</style>
</head>
<body>${body}</body>
</html>`;
      const w = window.open('', '_blank');
      if (!w) {
        alert('Pop-up blocked. Please allow pop-ups to export PDF.');
        return;
      }
      w.document.open();
      w.document.write(doc);
      w.document.close();
      // Give the new window a moment to load images / fonts, then print
      setTimeout(() => { try { w.focus(); w.print(); } catch (e) {} }, 350);
    });
  }

  function escapeHtml(s) {
    return String(s).replace(/[&<>"']/g, c => ({
      '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
    })[c]);
  }
})();
