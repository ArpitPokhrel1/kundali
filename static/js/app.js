// Kundali Tarjun front end. Keeps the original API and DOM contracts intact.
(function () {
  const $ = (selector, root = document) => root.querySelector(selector);
  const $$ = (selector, root = document) => Array.from(root.querySelectorAll(selector));
  const apiBase = document.documentElement.dataset.apiBase || '';

  const themeSelect = $('#theme-select');
  const localeSelect = $('#locale-select');
  const storedTheme = localStorage.getItem('astro-theme');

  if (storedTheme && themeSelect) {
    document.documentElement.dataset.theme = storedTheme;
    themeSelect.value = storedTheme;
  }

  function apiFetch(path, options = {}) {
    return fetch(`${apiBase}${path}`, {
      credentials: apiBase ? 'omit' : 'same-origin',
      ...options
    });
  }

  function setPref(key, value) {
    if (key === 'theme') {
      document.documentElement.dataset.theme = value;
      localStorage.setItem('astro-theme', value);
    }

    apiFetch('/api/set-pref', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ [key]: value })
    }).finally(() => {
      if (key === 'locale') window.location.reload();
    });
  }

  if (themeSelect) {
    themeSelect.addEventListener('change', event => setPref('theme', event.target.value));
  }

  if (localeSelect) {
    localeSelect.addEventListener('change', event => setPref('locale', event.target.value));
  }

  const revealItems = $$('[data-reveal]');
  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.14 });
    revealItems.forEach(item => observer.observe(item));
  } else {
    revealItems.forEach(item => item.classList.add('is-visible'));
  }

  const computeForm = $('#compute-form');
  if (!computeForm) return;

  const bsToggle = $('#use-bs');
  const adInput = $('#ad-date');
  const adLabel = $('#row-date-ad-label');
  const bsRow = $('#row-date-bs');
  const bsLabel = $('#row-date-bs-label');
  const adField = $('#row-date-ad-field');
  const bsField = $('#row-date-bs-field');

  function syncDateMode() {
    const useBs = Boolean(bsToggle && bsToggle.checked);
    if (adField) adField.style.display = useBs ? 'none' : '';
    if (bsField) bsField.style.display = useBs ? '' : 'none';
    if (!adField && adInput) adInput.style.display = useBs ? 'none' : '';
    if (!adField && adLabel) adLabel.style.display = useBs ? 'none' : '';
    if (!bsField && bsRow) bsRow.style.display = useBs ? '' : 'none';
    if (!bsField && bsLabel) bsLabel.style.display = useBs ? '' : 'none';
  }

  if (bsToggle) {
    bsToggle.addEventListener('change', syncDateMode);
    syncDateMode();
  }

  const searchBtn = $('#search-place');
  const placeInput = $('#place');
  const resultsList = $('#place-results');
  const latInput = $('#lat');
  const lonInput = $('#lon');
  const tzInput = $('#tz');

  function clearResults() {
    if (!resultsList) return;
    resultsList.innerHTML = '';
    resultsList.style.display = 'none';
  }

  function setBusy(button, busy, label = 'Working') {
    if (!button) return;
    button.disabled = busy;
    button.dataset.originalText = button.dataset.originalText || button.innerHTML;
    if (busy) button.innerHTML = `<span>${escapeHtml(label)}</span><span class="btn-icon" aria-hidden="true">...</span>`;
    if (!busy && button.dataset.originalText) button.innerHTML = button.dataset.originalText;
  }

  async function doSearch() {
    const query = placeInput ? placeInput.value.trim() : '';
    if (!query || !resultsList) return;

    resultsList.innerHTML = '<li class="muted">Searching place index...</li>';
    resultsList.style.display = 'grid';
    setBusy(searchBtn, true, 'Searching');

    try {
      const response = await apiFetch(`/api/search-place?q=${encodeURIComponent(query)}`);
      const data = await response.json();
      resultsList.innerHTML = '';

      if (!data.results || !data.results.length) {
        resultsList.innerHTML = '<li class="muted">No matches found.</li>';
        return;
      }

      data.results.forEach(result => {
        const item = document.createElement('li');
        item.innerHTML = `<div>${escapeHtml(result.display)}</div><div class="coords">${Number(result.lat).toFixed(4)}, ${Number(result.lon).toFixed(4)}</div>`;
        item.addEventListener('click', () => pickPlace(result));
        resultsList.appendChild(item);
      });
    } catch (error) {
      resultsList.innerHTML = `<li class="error">Search failed: ${escapeHtml(error.message)}</li>`;
    } finally {
      setBusy(searchBtn, false);
    }
  }

  async function pickPlace(result) {
    if (latInput) latInput.value = Number(result.lat).toFixed(6);
    if (lonInput) lonInput.value = Number(result.lon).toFixed(6);
    if (placeInput) placeInput.value = String(result.display || '').split(',')[0];
    clearResults();

    const date = adInput && adInput.value ? adInput.value : new Date().toISOString().slice(0, 10);
    try {
      const response = await apiFetch(`/api/timezone?lat=${result.lat}&lon=${result.lon}&date=${date}`);
      const data = await response.json();
      if (data.offset != null && tzInput) tzInput.value = Number(data.offset).toFixed(2);
    } catch (error) {
      // Timezone lookup is helpful but not required to continue.
    }
  }

  if (searchBtn) searchBtn.addEventListener('click', doSearch);
  if (placeInput) {
    placeInput.addEventListener('keydown', event => {
      if (event.key === 'Enter') {
        event.preventDefault();
        doSearch();
      }
    });
  }

  const tabsContainer = $('#result-tabs');
  const tabBtns = tabsContainer ? $$('.tab-btn', tabsContainer) : [];
  const tabPanels = tabsContainer ? $$('.tab-panel', tabsContainer) : [];
  const errorBox = $('#error-box');
  const resultArea = $('#result-area');
  const loading = $('#loading');
  const resultTitle = $('#result-title');
  const resultSubtitle = $('#result-subtitle');
  const computeButton = computeForm.querySelector('button[type="submit"]');

  function activateTab(tabName) {
    tabBtns.forEach(button => button.classList.toggle('active', button.dataset.tab === tabName));
    tabPanels.forEach(panel => panel.classList.toggle('active', panel.id === `tab-${tabName}`));
  }

  tabBtns.forEach(button => {
    button.addEventListener('click', () => activateTab(button.dataset.tab));
  });

  computeForm.addEventListener('submit', async event => {
    event.preventDefault();
    if (errorBox) errorBox.style.display = 'none';
    if (loading) loading.style.display = 'block';
    if (resultArea) resultArea.style.display = 'none';
    document.body.classList.add('is-computing');
    setBusy(computeButton, true, 'Computing');

    const useBs = Boolean($('#use-bs') && $('#use-bs').checked);
    const payload = {
      name: valueOf('#name').trim(),
      date_mode: useBs ? 'bs' : 'ad',
      ad_date: valueOf('#ad-date'),
      bs_year: valueOf('#bs-year'),
      bs_month: valueOf('#bs-month'),
      bs_day: valueOf('#bs-day'),
      time: valueOf('#time'),
      lat: parseFloat(valueOf('#lat')),
      lon: parseFloat(valueOf('#lon')),
      tz: parseFloat(valueOf('#tz')),
      place: valueOf('#place').trim(),
      locale: document.documentElement.lang || 'en',
      theme: document.documentElement.dataset.theme || 'light'
    };

    try {
      const response = await apiFetch('/api/compute', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      const data = await response.json();

      if (!response.ok || data.error) {
        showError(data.error || `Request failed with status ${response.status}`);
        return;
      }

      setHtml('#tab-summary', data.summary);
      setHtml('#tab-topics', data.topics || '');
      setHtml('#tab-drik', data.drik);
      setHtml('#tab-d9', data.d9 || '');
      setHtml('#tab-yogas', data.yogas || '');
      setHtml('#tab-dasha', data.dasha);
      setHtml('#tab-antardasha', data.antardasha || '');
      setHtml('#tab-ss', data.ss);
      setHtml('#tab-compare', data.compare);
      setHtml('#tab-explanation', data.explanation);
      updateResultMeta(payload);

      if (loading) loading.style.display = 'none';
      if (resultArea) {
        resultArea.style.display = 'block';
        resultArea.classList.add('is-visible');
        resultArea.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
      activateTab('summary');
    } catch (error) {
      showError(`Compute failed: ${error.message}`);
    } finally {
      document.body.classList.remove('is-computing');
      setBusy(computeButton, false);
    }
  });

  function showError(message) {
    if (errorBox) {
      errorBox.textContent = message;
      errorBox.style.display = 'block';
    }
    if (loading) loading.style.display = 'none';
  }

  function updateResultMeta(payload) {
    const name = payload.name || 'Janma Kundali';
    const place = payload.place || 'selected place';
    const date = payload.date_mode === 'bs'
      ? `${payload.bs_year}-${payload.bs_month}-${payload.bs_day} BS`
      : payload.ad_date;
    if (resultTitle) resultTitle.textContent = `${name} - Kundali Interpretation`;
    if (resultSubtitle) {
      resultSubtitle.textContent = `${place} - ${date} at ${payload.time || 'birth time'} - all chart, dasha, and interpretation tabs are ready.`;
    }
  }

  function setHtml(selector, html) {
    const element = $(selector);
    if (element) element.innerHTML = cleanResultHtml(html);
  }

  function cleanResultHtml(html) {
    return String(html || '')
      .replace(/<style[\s\S]*?<\/style>/gi, '')
      .replace(/\sfont-family:\s*[^;"']+;?/gi, '');
  }

  const btnExport = $('#btn-export-pdf');
  if (btnExport) {
    btnExport.addEventListener('click', exportPdf);
  }

  function exportPdf() {
    const order = [
      ['summary', 'Summary'],
      ['topics', 'Life Topics'],
      ['drik', 'Drik + Janma Kundali'],
      ['d9', 'D9 Navamsha'],
      ['yogas', 'Yogas'],
      ['dasha', 'Vimshottari Mahadasha'],
      ['antardasha', 'Antardasha'],
      ['ss', 'Surya Siddhanta'],
      ['compare', 'Drik vs Surya Siddhanta'],
      ['explanation', 'Explanation']
    ];

    const name = (valueOf('#name') || 'Kundali').trim();
    const printCss = `
      @page { size: A4; margin: 16mm 14mm; }
      body {
        font-family: "Anek Devanagari", "Mukta", "Noto Sans Devanagari", "Plus Jakarta Sans", ui-sans-serif, system-ui, sans-serif;
        color: #17130f;
        font-size: 12px;
        line-height: 1.55;
      }
      h1 { text-align: center; margin: 0 0 4px; font-size: 24px; }
      h2 { border-bottom: 2px solid #d7b46f; padding-bottom: 4px; margin-top: 16px; page-break-after: avoid; }
      h3, h4 { page-break-after: avoid; }
      section.page { page-break-after: always; }
      section.page:last-child { page-break-after: auto; }
      table { width: 100%; border-collapse: collapse; margin: 6px 0 12px; font-size: 11px; }
      th { background: #eef3ff; color: #152044; text-align: left; padding: 5px 8px; border: 1px solid #d7dded; }
      td { padding: 5px 8px; border: 1px solid #e6e0d5; vertical-align: top; }
      tr, .panel, .era, .edu, .planet-block { page-break-inside: avoid; }
      .panel, .era, .edu, .planet-block {
        background: #fbf7ed;
        border-left: 4px solid #b1782b;
        padding: 8px 12px;
        margin: 6px 0;
      }
      svg { max-width: 100%; height: auto; page-break-inside: avoid; }
      .footer { margin-top: 20px; padding-top: 8px; border-top: 1px solid #ddd; text-align: center; color: #666; font-size: 11px; }
    `;
    const date = new Date().toLocaleDateString();
    let body = `
      <h1>${escapeHtml(name)} - Janma Kundali</h1>
      <div style="text-align:center;color:#666;font-size:11px;margin-bottom:14px;">
        Generated ${escapeHtml(date)} - kundali.tarjun.com
      </div>
    `;

    order.forEach(([tabId, sectionTitle]) => {
      const element = document.getElementById(`tab-${tabId}`);
      if (!element || !element.innerHTML.trim()) return;
      body += `<section class="page"><h2>${escapeHtml(sectionTitle)}</h2>${element.innerHTML}</section>`;
    });

    body += '<div class="footer">Kundali Tarjun - kundali.tarjun.com</div>';

    const doc = `<!doctype html><html lang="${document.documentElement.lang || 'en'}"><head><meta charset="utf-8"><title>Kundali - ${escapeHtml(name)}</title><style>${printCss}</style></head><body>${body}</body></html>`;
    const printWindow = window.open('', '_blank');
    if (!printWindow) {
      alert('Pop-up blocked. Please allow pop-ups to export PDF.');
      return;
    }
    printWindow.document.open();
    printWindow.document.write(doc);
    printWindow.document.close();
    setTimeout(() => {
      try {
        printWindow.focus();
        printWindow.print();
      } catch (error) {
        // Browser print failures are handled by the browser UI.
      }
    }, 350);
  }

  function valueOf(selector) {
    const element = $(selector);
    return element && 'value' in element ? element.value : '';
  }

  function escapeHtml(value) {
    return String(value).replace(/[&<>"']/g, char => ({
      '&': '&amp;',
      '<': '&lt;',
      '>': '&gt;',
      '"': '&quot;',
      "'": '&#39;'
    })[char]);
  }
})();
