/**
 * CityHaldwani.com - Comprehensive Security & Content Protection Shield
 * Prevents inspect element, copying, text selection, and screenshot attempts on both desktop and mobile.
 */
(function() {
  'use strict';

  // 1. Disable Right Click Context Menu
  document.addEventListener('contextmenu', function(e) {
    e.preventDefault();
    return false;
  }, { capture: true });

  // 2. Disable Keyboard Shortcuts (Inspect, View Source, Save, Print, Screenshot)
  document.addEventListener('keydown', function(e) {
    // F12
    if (e.keyCode === 123 || e.key === 'F12') {
      e.preventDefault();
      e.stopPropagation();
      return false;
    }

    // Ctrl+Shift+I, Ctrl+Shift+J, Ctrl+Shift+C (DevTools)
    if (e.ctrlKey && e.shiftKey && (e.keyCode === 73 || e.keyCode === 74 || e.keyCode === 67 || e.key === 'I' || e.key === 'J' || e.key === 'C')) {
      e.preventDefault();
      e.stopPropagation();
      return false;
    }

    // Ctrl+U (View Source)
    if (e.ctrlKey && (e.keyCode === 85 || e.key === 'u' || e.key === 'U')) {
      e.preventDefault();
      e.stopPropagation();
      return false;
    }

    // Ctrl+S (Save Page)
    if (e.ctrlKey && (e.keyCode === 83 || e.key === 's' || e.key === 'S')) {
      e.preventDefault();
      e.stopPropagation();
      return false;
    }

    // Ctrl+P (Print Page)
    if (e.ctrlKey && (e.keyCode === 80 || e.key === 'p' || e.key === 'P')) {
      e.preventDefault();
      e.stopPropagation();
      return false;
    }

    // PrintScreen key
    if (e.key === 'PrintScreen' || e.keyCode === 44) {
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText('');
      }
      triggerSecurityBlur();
      e.preventDefault();
      return false;
    }
  }, { capture: true });

  // 3. Disable Text Selection & Dragging
  document.addEventListener('selectstart', function(e) {
    if (e.target && (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA')) return true;
    e.preventDefault();
    return false;
  });

  document.addEventListener('dragstart', function(e) {
    e.preventDefault();
    return false;
  });

  // 4. Disable Copy / Cut / Paste on non-inputs
  document.addEventListener('copy', function(e) {
    if (e.target && (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA')) return true;
    e.preventDefault();
    if (e.clipboardData) {
      e.clipboardData.setData('text/plain', '');
    }
    return false;
  });

  document.addEventListener('cut', function(e) {
    if (e.target && (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA')) return true;
    e.preventDefault();
    return false;
  });

  // 5. Anti-Screenshot & Screen Capture Protection on Mobile & Desktop
  function triggerSecurityBlur() {
    let overlay = document.getElementById('ch-security-shield-overlay');
    if (!overlay) {
      overlay = document.createElement('div');
      overlay.id = 'ch-security-shield-overlay';
      overlay.style.cssText = 'position:fixed;top:0;left:0;width:100vw;height:100vh;background:#0f172a;z-index:9999999;display:flex;align-items:center;justify-content:center;color:#fff;font-family:sans-serif;font-size:16px;text-align:center;padding:20px;';
      overlay.innerHTML = '<div><p style="font-size:24px;margin-bottom:10px;">&#128737;&#65039;</p><p>Screen recording and screenshots are restricted to protect advertiser privacy.</p></div>';
      document.body.appendChild(overlay);
    }
    overlay.style.display = 'flex';
    setTimeout(function() {
      if (overlay) overlay.style.display = 'none';
    }, 1200);
  }

  // When user switches tabs, minimizes or takes mobile screenshot
  window.addEventListener('blur', function() {
    document.body.classList.add('ch-screen-protected');
  });

  window.addEventListener('focus', function() {
    document.body.classList.remove('ch-screen-protected');
  });

  document.addEventListener('visibilitychange', function() {
    if (document.hidden) {
      document.body.classList.add('ch-screen-protected');
    } else {
      document.body.classList.remove('ch-screen-protected');
    }
  });

  // Inject anti-copy CSS rules
  const style = document.createElement('style');
  style.textContent = `
    * {
      -webkit-touch-callout: none !important;
      -webkit-user-select: none !important;
      -khtml-user-select: none !important;
      -moz-user-select: none !important;
      -ms-user-select: none !important;
      user-select: none !important;
    }
    input, textarea {
      -webkit-user-select: text !important;
      user-select: text !important;
    }
    img {
      pointer-events: none !important;
      -webkit-user-drag: none !important;
    }
    body.ch-screen-protected {
      filter: blur(16px) !important;
      transition: filter 0.1s ease;
    }
    @media print {
      body { display: none !important; }
    }
  `;
  document.head.appendChild(style);
})();
