/**
 * CityHaldwani.com - Light Theme 18+ Legal Age Verification Modal
 * Modern, clean white modal with distinct text and compliant consent flow.
 */
(function() {
  const STORAGE_KEY = 'cityhaldwani_age_verified_v1';

  function initAgeGate() {
    // If already verified, do nothing
    if (localStorage.getItem(STORAGE_KEY) === 'true') {
      return;
    }

    // Do not show on admin panel
    if (window.location.pathname.includes('admin')) {
      return;
    }

    const modal = document.createElement('div');
    modal.id = 'ch-age-gate-modal';
    modal.innerHTML = `
      <style>
        #ch-age-gate-modal {
          position: fixed;
          top: 0;
          left: 0;
          width: 100%;
          height: 100%;
          background: rgba(15, 23, 42, 0.75);
          backdrop-filter: blur(8px);
          -webkit-backdrop-filter: blur(8px);
          z-index: 999999;
          display: flex;
          align-items: center;
          justify-content: center;
          padding: 16px;
          animation: chFadeIn 0.3s ease-out;
        }
        @keyframes chFadeIn {
          from { opacity: 0; }
          to { opacity: 1; }
        }
        .ch-age-card {
          background: #ffffff;
          border-radius: 16px;
          max-width: 480px;
          width: 100%;
          padding: 32px 28px;
          box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
          text-align: center;
          border: 1px solid #e2e8f0;
          position: relative;
        }
        .ch-age-badge {
          display: inline-flex;
          align-items: center;
          justify-content: center;
          width: 64px;
          height: 64px;
          border-radius: 50%;
          background: #fee2e2;
          color: #dc2626;
          font-size: 26px;
          font-weight: 800;
          margin-bottom: 20px;
          border: 3px solid #fecaca;
        }
        .ch-age-title {
          font-size: 22px;
          font-weight: 700;
          color: #0f172a;
          margin-bottom: 12px;
          line-height: 1.3;
        }
        .ch-age-desc {
          font-size: 14.5px;
          color: #475569;
          line-height: 1.6;
          margin-bottom: 20px;
        }
        .ch-age-terms {
          font-size: 13px;
          color: #64748b;
          margin-bottom: 26px;
          line-height: 1.5;
          padding: 10px;
          background: #f8fafc;
          border-radius: 8px;
          border: 1px solid #f1f5f9;
        }
        .ch-age-terms a {
          color: #2563eb;
          text-decoration: underline;
        }
        .ch-age-actions {
          display: flex;
          flex-direction: column;
          gap: 12px;
        }
        .ch-btn-enter {
          background: linear-gradient(135deg, #e11d48 0%, #be123c 100%);
          color: #ffffff;
          border: none;
          padding: 14px 24px;
          font-size: 16px;
          font-weight: 700;
          border-radius: 10px;
          cursor: pointer;
          transition: transform 0.15s, box-shadow 0.15s;
          box-shadow: 0 4px 14px rgba(225, 29, 72, 0.35);
        }
        .ch-btn-enter:hover {
          transform: translateY(-2px);
          box-shadow: 0 6px 20px rgba(225, 29, 72, 0.45);
        }
        .ch-btn-exit {
          background: #f1f5f9;
          color: #475569;
          border: 1px solid #cbd5e1;
          padding: 12px 24px;
          font-size: 14px;
          font-weight: 600;
          border-radius: 10px;
          cursor: pointer;
          text-decoration: none;
          transition: background 0.15s;
        }
        .ch-btn-exit:hover {
          background: #e2e8f0;
          color: #0f172a;
        }
      </style>
      <div class="ch-age-card">
        <div class="ch-age-badge">18+</div>
        <h2 class="ch-age-title">Legal Age Verification & Advisory</h2>
        <p class="ch-age-desc">
          Welcome to <strong>CityHaldwani.com</strong>. This directory hosts verified adult classified advertisements and escort service listings intended strictly for mature consenting adults.
        </p>
        <div class="ch-age-terms">
          By entering, you confirm you are <strong>18 years of age or older</strong> (or legal majority in your region), consent to viewing adult material, and agree to our 
          <a href="/terms" target="_blank">Terms of Service</a> &amp; <a href="/privacy" target="_blank">Privacy Policy</a>.
        </div>
        <div class="ch-age-actions">
          <button id="ch-enter-btn" class="ch-btn-enter">I AM 18+ — ENTER SITE</button>
          <a href="https://www.google.com" class="ch-btn-exit">I AM UNDER 18 — EXIT</a>
        </div>
      </div>
    `;

    document.body.appendChild(modal);
    document.body.style.overflow = 'hidden';

    document.getElementById('ch-enter-btn').addEventListener('click', function() {
      localStorage.setItem(STORAGE_KEY, 'true');
      modal.remove();
      document.body.style.overflow = '';
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initAgeGate);
  } else {
    initAgeGate();
  }
})();
