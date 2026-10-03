// Injects the iOS status bar, tab bar (data-tabs, data-tab) and home indicator into .phone.
(function () {
  const ph = document.querySelector('.phone');
  const sb = document.createElement('div');
  sb.className = 'sbar';
  sb.innerHTML = `<span>9:41</span><span class="ic">
    <svg viewBox="0 0 18 12"><rect x="0" y="8" width="3" height="4" rx="1" fill="currentColor"/><rect x="5" y="5.5" width="3" height="6.5" rx="1" fill="currentColor"/><rect x="10" y="3" width="3" height="9" rx="1" fill="currentColor"/><rect x="15" y="0" width="3" height="12" rx="1" fill="currentColor"/></svg>
    <svg viewBox="0 0 16 12"><path d="M8 2.2c2.3 0 4.4.9 6 2.4l1.2-1.3A10.4 10.4 0 0 0 8 .4 10.4 10.4 0 0 0 .8 3.3L2 4.6a8.6 8.6 0 0 1 6-2.4zm0 3.6c1.3 0 2.5.5 3.4 1.3l1.2-1.3A6.6 6.6 0 0 0 8 4a6.6 6.6 0 0 0-4.6 1.8l1.2 1.3A4.9 4.9 0 0 1 8 5.8zm0 3.5L6 11.4 8 13.5l2-2.1z" fill="currentColor"/></svg>
    <svg viewBox="0 0 27 12" style="height:13px"><rect x=".5" y=".5" width="23" height="11" rx="3.2" fill="none" stroke="currentColor" opacity=".4"/><rect x="2" y="2" width="17" height="8" rx="2" fill="currentColor"/><rect x="24.6" y="4" width="1.6" height="4" rx=".8" fill="currentColor" opacity=".4"/></svg>
  </span>`;
  ph.prepend(sb);
  const ICONS = {
    Home: '<path d="M3 10.5 12 4l9 6.5V20a1 1 0 0 1-1 1h-5v-6h-6v6H4a1 1 0 0 1-1-1z"/>',
    Payments: '<rect x="3" y="5" width="18" height="14"/><path d="M3 10h18M7 15h4"/>',
    Progress: '<path d="M5 21V8l7-4 7 4v13M9 21v-5h6v5"/>',
    Documents: '<path d="M7 3h7l5 5v13H7zM14 3v5h5M10 13h6M10 17h6"/>',
    Policy: '<path d="M7 3h7l5 5v13H7zM14 3v5h5M10 13h6M10 17h6"/>',
    Claims: '<path d="M12 3 4 6v6c0 4.5 3.4 8.3 8 9 4.6-.7 8-4.5 8-9V6z"/><path d="M9 12l2 2 4-4"/>',
    Help: '<circle cx="12" cy="12" r="9"/><path d="M9.5 9.5a2.5 2.5 0 1 1 3.5 2.3c-.6.3-1 .8-1 1.5V14M12 17.5h.01"/>',
    Fleet: '<rect x="3" y="4" width="18" height="12"/><path d="M8 20h8M12 16v4"/>',
    Alarms: '<path d="M6 16V11a6 6 0 1 1 12 0v5l2 2H4zM10 21h4"/>',
    Handover: '<path d="M4 7h12l-3-3M20 17H8l3 3"/>',
    Apply: '<path d="M7 3h7l5 5v13H7zM14 3v5h5M10 14l2 2 4-4"/>',
    Status: '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    Fees: '<rect x="3" y="5" width="18" height="14"/><path d="M3 10h18M7 15h4"/>',
  };
  const names = (ph.dataset.tabs || 'Home,Payments,Progress,Documents').split(',');
  if (ph.dataset.tabs !== 'none') {
    const on = +ph.dataset.tab;
    const tb = document.createElement('nav');
    tb.className = 'tabs';
    tb.innerHTML = names.map((n, i) => `<span class="${i === on ? 'on' : ''}"><svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="square" stroke-linejoin="miter">${ICONS[n] || ICONS.Home}</svg>${n}</span>`).join('');
    ph.appendChild(tb);
  }
  const hi = document.createElement('div'); hi.className = 'home-ind'; ph.appendChild(hi);
})();
