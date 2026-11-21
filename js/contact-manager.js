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

  const PAGE_WA_MESSAGES = {
    'nainital': "Hello CityHaldwani, I want to book a verified companion in Nainital. Please share available profiles.",
    'bhimtal': "Hello CityHaldwani, I want to book a verified companion in Bhimtal. Please share available profiles.",
    'almora': "Hello CityHaldwani, I want to book a verified companion in Almora. Please share available profiles.",
    'ramnagar': "Hello CityHaldwani, I want to book a verified companion in Ramnagar. Please share available profiles.",
    'haldwani': "Hello CityHaldwani, I want to book a verified companion in Haldwani. Please share available profiles.",
    'kaladhungi': "Hello CityHaldwani, I want to book a verified companion in Kaladhungi. Please share available profiles.",
    'rudrapur': "Hello CityHaldwani, I want to book a verified companion in Rudrapur. Please share available profiles.",
    'kathgodam': "Hello CityHaldwani, I want to book a verified companion in Kathgodam. Please share available profiles.",
    'kashipur': "Hello CityHaldwani, I want to book a verified companion in Kashipur. Please share available profiles.",
    'bajpur': "Hello CityHaldwani, I want to book a verified companion in Bajpur. Please share available profiles.",
    'khatima': "Hello CityHaldwani, I want to book a verified companion in Khatima. Please share available profiles.",
    'sitarganj': "Hello CityHaldwani, I want to book a verified companion in Sitarganj. Please share available profiles.",
    'kichha': "Hello CityHaldwani, I want to book a verified companion in Kichha. Please share available profiles.",
    'jim-corbett': "Hello CityHaldwani, I want to book a verified companion in Jim Corbett. Please share available profiles.",
    'bhowali': "Hello CityHaldwani, I want to book a verified companion in Bhowali. Please share available profiles.",
    'index': "Hello CityHaldwani, I want to book a verified companion in Uttarakhand. Please share available profiles.",
    'about-us': "Hello CityHaldwani, I have an inquiry regarding CityHaldwani.com verified directory.",
    'contact-us': "Hello CityHaldwani, I want to contact customer support regarding CityHaldwani.com.",
    'safety-guide': "Hello CityHaldwani, I have a question regarding safety guidelines and zero advance policy.",
    'report-abuse': "Hello CityHaldwani, I want to report a directory issue or violation on CityHaldwani.com.",
    'terms': "Hello CityHaldwani, I have an inquiry regarding terms of service on CityHaldwani.com.",
    'privacy': "Hello CityHaldwani, I have an inquiry regarding privacy policy on CityHaldwani.com."
  };

  function getAutoWhatsAppMessage(pageKey) {
    if (!pageKey) return "Hello CityHaldwani, I want to book a verified companion. Please share available profiles.";
    const cleanKey = pageKey.replace(/^locations\//i, '').replace(/\.html$/i, '').toLowerCase();
    if (PAGE_WA_MESSAGES[cleanKey]) {
      return PAGE_WA_MESSAGES[cleanKey];
    }
    for (const [key, msg] of Object.entries(PAGE_WA_MESSAGES)) {
      if (cleanKey.includes(key)) return msg;
    }
    return "Hello CityHaldwani, I want to book a verified companion. Please share available profiles.";
  }

  function applyContacts() {
    const resolved = getResolvedContacts();
    const cleanTel = formatTelNumber(resolved.call);
    const cleanWa = formatWaNumber(resolved.whatsapp);
    const defaultPageMsg = getAutoWhatsAppMessage(resolved.pageKey);

    // Update all Call buttons
    document.querySelectorAll('a[href^="tel:"], .btn-call, .action-call, [data-contact="call"]').forEach(function (el) {
      el.setAttribute('href', 'tel:' + cleanTel);
      if (!el.dataset.boundTrack) {
        el.dataset.boundTrack = '1';
        el.addEventListener('click', function () {
          trackClick('call', el.getAttribute('data-profile-name') || 'Direct Call Button');
        });
      }
    });

    // Update all WhatsApp buttons
    document.querySelectorAll('a[href*="whatsapp.com"], a[href*="wa.me"], .btn-whatsapp, .action-wa, [data-contact="whatsapp"]').forEach(function (el) {
      const profileName = el.getAttribute('data-profile-name');
      const msg = profileName
        ? `Hello CityHaldwani, I want to book ${profileName}. Please share booking details.`
        : defaultPageMsg;
      const waUrl = 'https://api.whatsapp.com/send?phone=' + cleanWa + '&text=' + encodeURIComponent(msg);

      el.setAttribute('href', waUrl);
      el.setAttribute('target', '_blank');
      el.setAttribute('rel', 'noopener noreferrer');
      if (!el.dataset.boundTrack) {
        el.dataset.boundTrack = '1';
        el.addEventListener('click', function () {
          trackClick('whatsapp', profileName || 'Direct WhatsApp Button');
        });
      }
    });

    // Ensure floating buttons are updated as well
    updateFloatingButtons(cleanTel, cleanWa, defaultPageMsg);
  }

  function updateFloatingButtons(cleanTel, cleanWa, pageMsg) {
    const callBtn = document.getElementById('ch-float-call-btn');
    if (callBtn) {
      callBtn.setAttribute('href', 'tel:' + cleanTel);
    }
    const waBtn = document.getElementById('ch-float-wa-btn');
    if (waBtn) {
      const waUrl = 'https://api.whatsapp.com/send?phone=' + cleanWa + '&text=' + encodeURIComponent(pageMsg);
      waBtn.setAttribute('href', waUrl);
    }
  }

  function injectFloatingButtons() {
    const resolved = getResolvedContacts();
    const cleanTel = formatTelNumber(resolved.call);
    const cleanWa = formatWaNumber(resolved.whatsapp);
    const autoMsg = getAutoWhatsAppMessage(resolved.pageKey);
    const waUrl = 'https://api.whatsapp.com/send?phone=' + cleanWa + '&text=' + encodeURIComponent(autoMsg);

    let container = document.getElementById('cityhaldwani-floating-buttons');
    if (!container) {
      container = document.createElement('div');
      container.id = 'cityhaldwani-floating-buttons';
      container.className = 'ch-floating-buttons';
      container.innerHTML = `
        <a href="tel:${cleanTel}" class="ch-float-btn ch-float-call" id="ch-float-call-btn" title="Call Support" aria-label="Call Support">
          <span class="ch-float-pulse"></span>
          <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6.62 10.79a15.053 15.053 0 006.59 6.59l2.2-2.2c.27-.27.67-.36 1.02-.24 1.12.37 2.33.57 3.57.57.55 0 1 .45 1 1V20c0 .55-.45 1-1 1-9.39 0-17-7.61-17-17 0-.55.45-1 1-1h3.5c.55 0 1 .45 1 1 0 1.25.2 2.45.57 3.57.11.35.03.74-.25 1.02l-2.2 2.2z"/></svg>
        </a>
        <a href="${waUrl}" target="_blank" rel="noopener noreferrer" class="ch-float-btn ch-float-wa" id="ch-float-wa-btn" title="Chat on WhatsApp" aria-label="Chat on WhatsApp">
          <span class="ch-float-pulse"></span>
          <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12.04 2C6.58 2 2.13 6.45 2.13 11.91C2.13 13.66 2.59 15.36 3.45 16.86L2.05 22L7.3 20.62C8.75 21.41 10.38 21.83 12.04 21.83C17.5 21.83 21.95 17.38 21.95 11.92C21.95 9.27 20.92 6.78 19.05 4.91C17.18 3.04 14.69 2 12.04 2M12.05 3.67C14.25 3.67 16.31 4.53 17.87 6.09C19.42 7.65 20.28 9.72 20.28 11.92C20.28 16.46 16.58 20.15 12.04 20.15C10.56 20.15 9.11 19.76 7.85 19L7.55 18.83L4.43 19.65L5.26 16.61L5.06 16.29C4.24 15 3.8 13.47 3.8 11.91C3.81 7.37 7.5 3.67 12.05 3.67M9.13 7.39C8.95 7.39 8.65 7.46 8.4 7.73C8.15 8 7.45 8.65 7.45 9.97C7.45 11.29 8.41 12.57 8.54 12.75C8.68 12.93 10.42 15.63 13.09 16.78C15.31 17.74 15.76 17.55 16.25 17.51C16.75 17.46 17.86 16.85 18.09 16.21C18.32 15.57 18.32 15.02 18.25 14.91C18.18 14.79 18 14.73 17.72 14.59C17.45 14.45 16.08 13.78 15.83 13.69C15.58 13.59 15.4 13.55 15.22 13.82C15.04 14.1 14.51 14.73 14.35 14.91C14.19 15.1 14.03 15.12 13.75 14.98C13.48 14.84 12.59 14.55 11.54 13.61C10.72 12.88 10.16 11.98 10 11.71C9.84 11.43 9.98 11.29 10.12 11.15C10.25 11.03 10.4 10.83 10.54 10.67C10.68 10.5 10.73 10.39 10.82 10.2C10.91 10.02 10.87 9.86 10.8 9.72C10.73 9.58 10.18 8.24 9.95 7.7C9.73 7.18 9.51 7.25 9.34 7.24C9.18 7.24 9.01 7.39 9.13 7.39Z"/></svg>
        </a>
      `;
      document.body.appendChild(container);
    } else {
      updateFloatingButtons(cleanTel, cleanWa, autoMsg);
    }

    const callEl = document.getElementById('ch-float-call-btn');
    if (callEl && !callEl.dataset.boundTrack) {
      callEl.dataset.boundTrack = '1';
      callEl.addEventListener('click', function () {
        trackClick('call', 'Floating Call Icon');
      });
    }

    const waEl = document.getElementById('ch-float-wa-btn');
    if (waEl && !waEl.dataset.boundTrack) {
      waEl.dataset.boundTrack = '1';
      waEl.addEventListener('click', function () {
        trackClick('whatsapp', 'Floating WhatsApp Icon');
      });
    }
  }

  // Auto fallback for broken image paths (handles subdirectories, Live Server ports, etc.)
  function setupImageFallbacks() {
    document.querySelectorAll('img').forEach(function (img) {
      img.addEventListener('error', function () {
        if (!this.dataset.retried) {
          this.dataset.retried = '1';
          var originalSrc = this.getAttribute('src') || '';
          var filename = originalSrc.split('/').pop().split('?')[0];
          if (filename.includes('logo')) {
            this.src = '/city-logo.png';
          } else if (filename) {
            this.src = '/' + filename;
          }
        } else if (this.dataset.retried === '1') {
          this.dataset.retried = '2';
          var originalSrc = this.getAttribute('src') || '';
          var filename = originalSrc.split('/').pop().split('?')[0];
          if (filename.includes('logo')) {
            this.src = 'city-logo.png';
          } else if (filename) {
            this.src = 'public/' + filename;
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
