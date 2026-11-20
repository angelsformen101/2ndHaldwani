/**
 * CityHaldwani.com - Contact Manager & Analytics Tracker
 * Handles dynamic contact numbers, floating action buttons, and click tracking with page duration.
 * Robust against subfolders (e.g. /cityhaldwani_com/), file://, and production roots.
 */
(function () {
  const pageStartTime = Date.now();

  function getPageKey() {
    let path = window.location.pathname.replace(/^\/+/, '');
    // Strip common subfolder prefixes if hosted in a nested folder (e.g. VS Code Live Server)
    path = path.replace(/^cityhaldwani_com\//i, '');

    if (!path || path === '' || path === 'index.html') return 'index.html';

    // Normalize clean URLs to .html key
    if (!path.endsWith('.html') && !path.includes('.')) {
      if (path.startsWith('locations/')) {
        path = path + '.html';
      } else if (!path.includes('/')) {
        const locs = ['nainital', 'bhimtal', 'almora', 'ramnagar', 'haldwani', 'kaladhungi', 'rudrapur', 'kathgodam', 'kashipur', 'bajpur', 'khatima', 'sitarganj', 'kichha', 'jim-corbett', 'bhowali'];
        if (locs.includes(path)) path = 'locations/' + path + '.html';
        else path = path + '.html';
      }
    }
    return path;
  }

  function getActiveConfig() {
    // 1. Check LocalStorage first (updated by Admin panel)
    let config = null;
    try {
      const stored = localStorage.getItem('cityhaldwani_contacts_config');
      if (stored) config = JSON.parse(stored);
    } catch (e) { }

    // 2. Fallback to window.SITE_CONTACTS_CONFIG (from contacts-config.js)
    if (!config && window.SITE_CONTACTS_CONFIG) {
      config = window.SITE_CONTACTS_CONFIG;
    }

    if (!config) {
      config = { master: { call: '+919876543210', whatsapp: '919876543210' }, pages: {} };
    }
    return config;
  }

  function getResolvedContacts() {
    const config = getActiveConfig();
    const master = config.master || { call: '+919876543210', whatsapp: '919876543210' };
    const pageKey = getPageKey();
    const pageOverride = (config.pages && config.pages[pageKey]) || {};

    const callNumber = (pageOverride.call && pageOverride.call.trim() !== '') ? pageOverride.call.trim() : master.call;
    const waNumber = (pageOverride.whatsapp && pageOverride.whatsapp.trim() !== '') ? pageOverride.whatsapp.trim() : master.whatsapp;

    return { call: callNumber, whatsapp: waNumber, pageKey: pageKey };
  }

  function formatWaNumber(num) {
    return String(num).replace(/[^0-9]/g, '');
  }

  function formatTelNumber(num) {
    if (num.startsWith('+')) return '+' + num.replace(/[^0-9]/g, '');
    return num.replace(/[^0-9]/g, '');
  }

  function trackClick(type, label) {
    const durationSeconds = Math.round((Date.now() - pageStartTime) / 1000);
    const resolved = getResolvedContacts();
    const payload = {
      type: type,
      label: label || 'button',
      page: resolved.pageKey,
      url: window.location.href,
      duration: durationSeconds,
      timestamp: new Date().toISOString()
    };

    // Persist in local storage (guarantees tracking works on any static preview, Live Server, localhost, or production)
    try {
      const logs = JSON.parse(localStorage.getItem('cityhaldwani_click_logs') || '[]');
      logs.unshift(payload);
      if (logs.length > 500) logs.pop();
      localStorage.setItem('cityhaldwani_click_logs', JSON.stringify(logs));
    } catch (e) { }

    // Send to backend API only in production environment (avoid 404 in static Live Server preview)
    const isStaticDev = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1' || window.location.port === '5500';
    if (!isStaticDev && window.location.protocol.startsWith('http')) {
      try {
        if (navigator.sendBeacon) {
          navigator.sendBeacon('/api/track', JSON.stringify(payload));
        } else {
          fetch('/api/track', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload),
            keepalive: true
          }).catch(function () { });
        }
      } catch (e) { }
    }
  }

  function applyContacts() {
    const resolved = getResolvedContacts();
    const cleanTel = formatTelNumber(resolved.call);
    const cleanWa = formatWaNumber(resolved.whatsapp);

    // Update all Call buttons
    document.querySelectorAll('a[href^="tel:"], .btn-call, .action-call, [data-contact="call"]').forEach(function (el) {
      el.setAttribute('href', 'tel:' + cleanTel);
      el.addEventListener('click', function () {
        trackClick('call', el.getAttribute('data-profile-name') || 'Direct Call Button');
      }, { once: false });
    });

    // Update all WhatsApp buttons
    const waMsg = encodeURIComponent("Hello CityHaldwani, I am interested in verified companions and booking details. Please share available profiles.");
    const waUrl = 'https://api.whatsapp.com/send?phone=' + cleanWa + '&text=' + waMsg;

    document.querySelectorAll('a[href*="whatsapp.com"], a[href*="wa.me"], .btn-whatsapp, .action-wa, [data-contact="whatsapp"]').forEach(function (el) {
      el.setAttribute('href', waUrl);
      el.setAttribute('target', '_blank');
      el.setAttribute('rel', 'noopener noreferrer');
      el.addEventListener('click', function () {
        trackClick('whatsapp', el.getAttribute('data-profile-name') || 'Direct WhatsApp Button');
      }, { once: false });
    });
  }

  function injectFloatingButtons() {
    if (document.getElementById('cityhaldwani-floating-buttons')) return;

    const resolved = getResolvedContacts();
    const cleanTel = formatTelNumber(resolved.call);
    const cleanWa = formatWaNumber(resolved.whatsapp);
    const waMsg = encodeURIComponent("Hello CityHaldwani, I want to book verified companions. Please provide active models.");
    const waUrl = 'https://api.whatsapp.com/send?phone=' + cleanWa + '&text=' + waMsg;

    const container = document.createElement('div');
    container.id = 'cityhaldwani-floating-buttons';
    container.innerHTML = `
      <style>
        .ch-float-btn {
          position: fixed;
          bottom: 22px;
          z-index: 99998;
          display: flex;
          align-items: center;
          justify-content: center;
          width: 56px;
          height: 56px;
          border-radius: 50%;
          box-shadow: 0 4px 18px rgba(0,0,0,0.22);
          transition: transform 0.25s ease, box-shadow 0.25s ease;
          text-decoration: none;
        }
        .ch-float-btn:hover {
          transform: translateY(-4px) scale(1.05);
          box-shadow: 0 8px 24px rgba(0,0,0,0.3);
        }
        .ch-float-call {
          left: 20px;
          background: linear-gradient(135deg, #10b981 0%, #059669 100%);
          border: 2px solid #ffffff;
        }
        .ch-float-wa {
          right: 20px;
          background: linear-gradient(135deg, #25D366 0%, #128C7E 100%);
          border: 2px solid #ffffff;
        }
        .ch-float-btn svg {
          width: 26px;
          height: 26px;
          fill: #ffffff;
        }
        .ch-float-pulse {
          position: absolute;
          width: 100%;
          height: 100%;
          border-radius: 50%;
          background: inherit;
          opacity: 0.6;
          animation: ch-pulse 2s cubic-bezier(0, 0, 0.2, 1) infinite;
          z-index: -1;
        }
        @keyframes ch-pulse {
          0% { transform: scale(1); opacity: 0.7; }
          100% { transform: scale(1.55); opacity: 0; }
        }
        @media (max-width: 768px) {
          .ch-float-btn { width: 48px; height: 48px; bottom: 14px; box-shadow: 0 4px 14px rgba(0,0,0,0.22); }
          .ch-float-call { left: 12px; }
          .ch-float-wa { right: 12px; }
          .ch-float-btn svg { width: 23px; height: 23px; }
        }
        @media (max-width: 480px) {
          .ch-float-btn { width: 44px; height: 44px; bottom: 12px; }
          .ch-float-call { left: 10px; }
          .ch-float-wa { right: 10px; }
          .ch-float-btn svg { width: 20px; height: 20px; }
        }
      </style>
      <a href="tel:${cleanTel}" class="ch-float-btn ch-float-call" id="ch-float-call-btn" title="Call Now" aria-label="Call Now">
        <div class="ch-float-pulse"></div>
        <svg viewBox="0 0 24 24"><path d="M6.62 10.79a15.053 15.053 0 006.59 6.59l2.2-2.2c.27-.27.67-.36 1.02-.24 1.12.37 2.33.57 3.57.57.55 0 1 .45 1 1V20c0 .55-.45 1-1 1-9.39 0-17-7.61-17-17 0-.55.45-1 1-1h3.5c.55 0 1 .45 1 1 0 1.25.2 2.45.57 3.57.11.35.03.74-.25 1.02l-2.2 2.2z"/></svg>
      </a>
      <a href="${waUrl}" target="_blank" rel="noopener noreferrer" class="ch-float-btn ch-float-wa" id="ch-float-wa-btn" title="Chat on WhatsApp" aria-label="Chat on WhatsApp">
        <div class="ch-float-pulse"></div>
        <svg viewBox="0 0 24 24"><path d="M12.04 2c-5.46 0-9.91 4.45-9.91 9.91 0 1.75.46 3.45 1.32 4.95L2.05 22l5.25-1.38c1.45.79 3.08 1.21 4.74 1.21 5.46 0 9.91-4.45 9.91-9.91 0-2.65-1.03-5.14-2.9-7.01A9.816 9.816 0 0012.04 2zm5.79 14.07c-.24.67-1.39 1.28-1.93 1.34-.51.05-1.18.08-3.41-.85-2.85-1.18-4.69-4.08-4.83-4.27-.14-.19-1.16-1.54-1.16-2.94 0-1.4.73-2.09 1-2.37.24-.26.54-.33.72-.33.18 0 .36 0 .52.01.17.01.39-.06.61.47.23.54.78 1.9.85 2.04.07.15.11.32.02.51-.09.18-.14.29-.28.46-.14.16-.29.37-.42.49-.14.14-.29.29-.12.58.17.29.75 1.24 1.62 2 1.11.98 2.05 1.28 2.34 1.43.29.14.46.12.63-.07.18-.19.74-.86.94-1.16.2-.29.4-.24.67-.14.27.1 1.73.81 2.03.96.29.15.49.23.56.36.07.12.07.72-.17 1.39z"/></svg>
      </a>
    `;
    document.body.appendChild(container);

    document.getElementById('ch-float-call-btn').addEventListener('click', function () {
      trackClick('call', 'Floating Call Icon');
    });
    document.getElementById('ch-float-wa-btn').addEventListener('click', function () {
      trackClick('whatsapp', 'Floating WhatsApp Icon');
    });
  }

  // Auto fallback for broken image paths (handles subdirectories, Live Server ports, etc.)
  function setupImageFallbacks() {
    document.querySelectorAll('img').forEach(function (img) {
      img.addEventListener('error', function () {
        if (!this.dataset.retried) {
          this.dataset.retried = '1';
          var originalSrc = this.getAttribute('src') || '';
          var filename = originalSrc.split('/').pop();
          if (originalSrc.includes('logo')) {
            this.src = '../city-logo.png';
          } else if (filename) {
            this.src = '../public/' + filename;
          }
        }
      });
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () {
      setupImageFallbacks();
      applyContacts();
      injectFloatingButtons();
    });
  } else {
    setupImageFallbacks();
    applyContacts();
    injectFloatingButtons();
  }

  window.CityHaldwaniTracker = {
    track: trackClick,
    refresh: applyContacts
  };
})();
