import os
import re
import json
import urllib.parse

from build_pages import NAMES_POOL, LOCATIONS_CONFIG
from page_template import build_location_page, render_profile_card, count_words, EMBEDDED_CSS, ADULT_WARNING_BAR_HTML, DMCA_BADGE_HTML

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
LOCATIONS_DIR = os.path.join(OUTPUT_DIR, 'locations')
os.makedirs(LOCATIONS_DIR, exist_ok=True)

# Build all 15 location pages
all_used_names = set()
name_index_tracker = 0

location_reports = []

for loc in LOCATIONS_CONFIG:
    page_html, names = build_location_page(loc, name_index_tracker)
    name_index_tracker += 16
    for n in names:
        all_used_names.add(n.lower())
    
    file_path = os.path.join(LOCATIONS_DIR, f"{loc['slug']}.html")
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(page_html)
    
    words = count_words(page_html)
    profiles_count = len(re.findall(r'class="profile-card"', page_html))
    faqs_count = len(re.findall(r'class="faq-item"', page_html))
    
    location_reports.append({
        'slug': loc['slug'],
        'name': loc['name'],
        'words': words,
        'profiles': profiles_count,
        'faqs': faqs_count
    })
    print(f"Generated {loc['slug']}.html -> Words: {words}, Profiles: {profiles_count}, FAQs: {faqs_count}")

# Build Homepage (index.html)
home_pills = []
for l in LOCATIONS_CONFIG:
    home_pills.append(f'<a href="locations/{l["slug"]}.html" class="loc-pill">📍 {l["name"]}</a>')
home_pills_html = "\n".join(home_pills)

home_cards = []
for i in range(16):
    name = NAMES_POOL[(name_index_tracker + i) % len(NAMES_POOL)]
    all_used_names.add(name.lower())
    age = 21 + (i % 6)
    img_alias = f"profile_{( (name_index_tracker + i) % 48 ) + 1:02d}.webp"
    city_sample = LOCATIONS_CONFIG[i % len(LOCATIONS_CONFIG)]['name']
    home_cards.append(render_profile_card(name, city_sample, age, i, img_alias, rel_prefix=''))
home_cards_str = "\n".join(home_cards)

home_faqs = [
    (
        "What is CityHaldwani.com?",
        "CityHaldwani.com is Uttarakhand's premier light-theme classified directory connecting travelers and executives with verified independent escorts across 15 destination hubs without broker fees."
    ),
    (
        "How do I browse and book companions across Uttarakhand?",
        "Browse our verified listings, select a companion, and click Call or WhatsApp to discuss schedule, hotel destination, and duration directly with the independent advertiser."
    ),
    (
        "Does CityHaldwani.com charge upfront booking fees?",
        "No, absolutely not. CityHaldwani.com enforces a strict Zero Advance Payment rule. Never transfer online deposits. Payment is settled in cash upon arrival at your hotel."
    ),
    (
        "Are companion profile photos verified?",
        "Yes, all companion profiles undergo authentic verification. Advertisers submit high-resolution photos alongside date-stamped verification selfies confirming adult age (18+) before approval."
    ),
    (
        "Which destinations in Uttarakhand are covered?",
        "We host active verified listings across 15 hubs: Haldwani, Nainital, Bhimtal, Almora, Ramnagar, Kaladhungi, Rudrapur, Kathgodam, Kashipur, Bajpur, Khatima, Sitarganj, Kichha, Jim Corbett, and Bhowali."
    ),
    (
        "Can companions provide outcall service to 5-star hotels?",
        "Yes, independent companions offer prompt outcall service to certified 4-star and 5-star hotels and luxury safari lodges, arriving discreetly dressed."
    ),
    (
        "What are typical pricing rates across Uttarakhand?",
        "Standard 1-hour meetings range from ₹1,500 to ₹2,500, 2-hour sessions range from ₹2,500 to ₹3,500, and full-night overnight stays range from ₹7,000 to ₹10,000."
    ),
    (
        "How is client confidentiality and privacy safeguarded?",
        "We employ a zero-tracking digital architecture. No cookies are stored. Inquiries occur over direct telephone lines or end-to-end encrypted WhatsApp messaging."
    ),
    (
        "What categories of companions are available?",
        "Our classified directory features independent college girls (18+), VIP fashion models, corporate hostesses, mature homemakers, and luxury resort companions."
    ),
    (
        "Can I book companions for multi-day road trips?",
        "Yes, several independent models accommodate vacation travel across Uttarakhand hill stations. Travel logistics, separate rooms, and daily rates must be arranged in advance."
    ),
    (
        "How quickly can a companion arrive after confirmation?",
        "Within central areas like Haldwani, Rudrapur, and Kathgodam, companions arrive within 30 to 45 minutes. For mountain resorts, 1 hour notice is recommended."
    ),
    (
        "What payment methods are accepted?",
        "Direct cash upon arrival is the preferred, safest method. Some independent companions accept instant digital UPI payments after in-person meeting."
    ),
    (
        "Can I meet my companion in the hotel lounge first?",
        "Yes, you may request a brief 5-10 minute meeting in the hotel lobby lounge or coffee shop before proceeding to your room."
    ),
    (
        "What happens if the companion does not match her photos?",
        "Under our zero-advance policy, you can decline the appointment at your doorstep without paying any fees if the person does not match her profile."
    ),
    (
        "What hygiene and cleanliness standards are followed?",
        "Strict personal hygiene and professional grooming standards are upheld. Mutual cleanliness is mandatory, and safe health practices are enforced."
    ),
    (
        "What is the minimum age to access CityHaldwani.com?",
        "You must be at least 18 years of age (or legal age of majority in your jurisdiction) to browse CityHaldwani.com or contact any advertisers."
    ),
    (
        "Can I hire an escort for corporate dinners and conferences?",
        "Yes, independent models are educated and articulate, making them exceptional companions for corporate dinners and formal networking events."
    ),
    (
        "What should I do if an advertiser asks for advance money?",
        "Refuse immediately and report the profile to our compliance desk via WhatsApp. No legitimate companion on CityHaldwani.com will demand upfront money."
    ),
    (
        "Are overnight bookings available on weekends?",
        "Yes, full-night bookings are highly popular for weekend travelers visiting Nainital and Corbett. Book by early evening to secure your preferred model."
    ),
    (
        "How can independent models advertise on CityHaldwani.com?",
        "Independent models aged 18 and older can submit verification details, real photos, and preferred operational cities to our Advertiser Desk via WhatsApp."
    )
]

home_faqs_html = []
home_faq_schema_items = []
for q, a in home_faqs:
    home_faqs_html.append(f'''
      <div class="faq-item">
        <h3 class="faq-question">{q}</h3>
        <div class="faq-answer"><p>{a}</p></div>
      </div>''')
    home_faq_schema_items.append({
        "@type": "Question",
        "name": q,
        "acceptedAnswer": {
            "@type": "Answer",
            "text": a
        }
    })
home_faqs_str = "\n".join(home_faqs_html)

home_faq_schema = json.dumps({
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": home_faq_schema_items
}, indent=2)

home_biz_schema = json.dumps({
    "@context": "https://schema.org",
    "@type": "WebSite",
    "name": "CityHaldwani.com",
    "url": "https://cityhaldwani.com/",
    "description": "Premier Light Theme Classifieds and Verified Escort Directory for Haldwani, Nainital, and Uttarakhand.",
    "potentialAction": {
        "@type": "SearchAction",
        "target": "https://cityhaldwani.com/?q={search_term_string}",
        "query-input": "required name=search_term_string"
    }
}, indent=2)

dest_cards = []
for loc in LOCATIONS_CONFIG:
    dest_cards.append(f'''
      <div class="category-box" style="display: flex; flex-direction: column; justify-content: space-between;">
        <div>
          <h4>📍 <a href="locations/{loc['slug']}.html" style="color: inherit;">{loc['name']} Escorts</a></h4>
          <p style="font-size: 13px; color: var(--text-muted); margin-bottom: 6px;">{loc['tagline']}</p>
          <p style="font-size: 13.5px; color: var(--text-secondary);">{loc['meta_desc']}</p>
        </div>
        <div style="margin-top: 14px;">
          <a href="locations/{loc['slug']}.html" class="btn-card-details" style="display: inline-block; width: 100%; text-align: center; font-weight: 700; color: #be123c; background: linear-gradient(135deg, #fff1f2 0%, #ffe4e6 100%); border: 1px solid #fecdd3; padding: 10px 14px; border-radius: 8px;">View 16 Profiles in {loc['name']} &rarr;</a>
        </div>
      </div>''')
dest_cards_str = "\n".join(dest_cards)

home_wa_msg = "Hello CityHaldwani, I want to book a verified companion in Uttarakhand. Please share available profiles."
home_wa_encoded = urllib.parse.quote(home_wa_msg)

index_html = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>CityHaldwani.com - Premier Uttarakhand Escort Directory &amp; Verified Classifieds</title>
  <meta name="description" content="CityHaldwani.com is Uttarakhand's premier light-theme classified directory. Explore 100% verified independent escorts in Haldwani, Nainital, Bhimtal, Ramnagar, Corbett, and 15 destinations. Cash on meeting, zero advance.">
  <link rel="canonical" href="https://cityhaldwani.com/">
  <link rel="icon" href="favicon.webp" type="image/webp">

  <!-- Open Graph Meta Tags (Image 1 Fix) -->
  <meta property="og:title" content="CityHaldwani.com - Premier Uttarakhand Escort Directory &amp; Verified Classifieds">
  <meta property="og:description" content="Explore 100% verified independent escorts in Haldwani, Nainital, Bhimtal, Ramnagar, Corbett, and 15 Uttarakhand destinations. Strict 18+ verification, zero advance.">
  <meta property="og:type" content="website">
  <meta property="og:url" content="https://cityhaldwani.com/">
  <meta property="og:image" content="https://cityhaldwani.com/city-logo.png">
  <meta property="og:site_name" content="CityHaldwani.com">

  <!-- X / Twitter Card Meta Tags (Image 1 Fix) -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:site" content="@CityHaldwani">
  <meta name="twitter:title" content="CityHaldwani.com - Premier Uttarakhand Escort Directory &amp; Verified Classifieds">
  <meta name="twitter:description" content="Explore 100% verified independent escorts in Haldwani, Nainital, Bhimtal, Ramnagar, Corbett, and 15 Uttarakhand destinations. Cash on meeting, zero advance.">
  <meta name="twitter:image" content="https://cityhaldwani.com/city-logo.png">
  <link rel="icon" href="/favicon.webp" type="image/webp">
  <link rel="preload" href="/city-logo.png" as="image">

  <!-- Directory Trailing Slash Normalization Script (Fixes Image 2 & Image 3 404s when navigating subfolder without trailing slash) -->
  <script>
    (function() {{
      var p = window.location.pathname;
      if (p.endsWith('/cityhaldwani_com')) {{
        window.location.replace(p + '/' + window.location.search + window.location.hash);
      }}
    }})();
  </script>

  <style>
{EMBEDDED_CSS}
  </style>
  <script type="application/ld+json">
{home_biz_schema}
  </script>
  <script type="application/ld+json">
{home_faq_schema}
  </script>
</head>
<body>
{ADULT_WARNING_BAR_HTML}

  <header class="site-topbar">
    <div class="container topbar-wrapper">
      <a href="/index.html" class="brand-group">
        <img src="/city-logo.png" alt="CityHaldwani.com Logo" class="brand-logo-img" width="140" height="42" onerror="if(!this.dataset.retried){{this.dataset.retried=1;this.src='/logo.png';}}else if(this.dataset.retried==1){{this.dataset.retried=2;this.src='city-logo.png';}}">
        <div class="brand-text">
          <div class="brand-title">CityHaldwani<span>.com</span></div>
          <p>Verified Uttarakhand Classifieds</p>
        </div>
      </a>
      <div class="topbar-actions">
        <span class="badge-verified-top">&#10004; 100% Verified Classifieds</span>
        <a href="tel:+919876543210" class="btn-header-call" data-contact="call">Call Support</a>
        <a href="https://api.whatsapp.com/send?phone=919876543210" class="btn-header-wa" data-contact="whatsapp">WhatsApp</a>
      </div>
    </div>
  </header>

  <main class="container">
    <nav class="breadcrumb-nav" aria-label="Breadcrumb">
      <span>Home</span> &gt; <span>Uttarakhand Classifieds</span>
    </nav>

    <div class="location-pills-bar">
      <div class="location-pills-title">Select Your Preferred Destination Hub:</div>
      <div class="location-pills-grid">
{home_pills_html}
      </div>
    </div>

    <!-- HERO EDITORIAL SECTION -->
    <section class="hero-editorial">
      <h1>Premier Uttarakhand Classified Directory - 100% Verified Independent Escorts &amp; 5-Star Hotel Companions</h1>
      <div class="hero-meta-badges">
        <span class="hero-badge">🏔️ Covering 15 Uttarakhand Destinations</span>
        <span class="hero-badge">⭐ 100% Real Photographs</span>
        <span class="hero-badge">🛡️ Strict Zero Advance Rule</span>
        <span class="hero-badge">🛎️ Luxury Hotel &amp; Resort Outcall</span>
      </div>
      <p>
        Welcome to <strong>CityHaldwani.com</strong>, the most trusted and elegant light-themed classified directory dedicated to luxury companionship across the state of Uttarakhand. Whether you are traveling for a rejuvenating weekend retreat in the tranquil lakes of Nainital and Bhimtal, embarking on a thrilling wildlife safari in Jim Corbett, or attending executive industrial summits across Haldwani, Rudrapur, and Kashipur, our platform connects you directly with verified independent companions.
      </p>
      <p>
        We reject the murky practices of traditional agencies. On CityHaldwani.com, there are no deceptive middle-tier agents, inflated hidden commissions, or recycled stock photographs. Every independent model listed below has successfully verified her adult legal age (18+) and submitted authentic photo verifications. You speak directly to your companion over telephone or WhatsApp, agree on customized hours and expectations, and pay strictly in cash upon arrival at your verified luxury hotel room or private villa.
      </p>
    </section>

    <!-- SECTION 1: PROFILES SECTION FIRST (Shifted as requested by user) -->
    <section class="listings-section" id="featured-listings">
      <div class="listings-heading-bar">
        <h2>🔥 16 Featured VIP Classified Profiles Across Uttarakhand</h2>
        <span class="listings-count-badge">Top Verified Models</span>
      </div>
      <div class="listings-grid">
{home_cards_str}
      </div>
    </section>

    <!-- SECTION 2: EXPLORE LOCATIONS SECTION DIRECTLY UNDER PROFILES SECTION -->
    <section class="editorial-card" id="locations">
      <h2>Explore Verified Companions Across 15 Uttarakhand Locations</h2>
      <p>Select your city below to browse dedicated 16-profile directories with localized pricing, hotel guides, and safety recommendations:</p>
      <div class="categories-grid" style="grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));">
{dest_cards_str}
      </div>
    </section>

    <!-- EDITORIAL & GUIDE SECTIONS -->
    <section class="editorial-card">
      <h2>The Gold Standard in Independent Uttarakhand Companionship</h2>
      <p>
        Uttarakhand, nestled amidst the pristine beauty of the Himalayas, attracts millions of travelers each year. From scenic hill station vistas to high-paced industrial commerce in the Terai plains, the requirement for charming, trustworthy, and sophisticated companionship has never been greater. CityHaldwani.com was designed from the ground up to provide a clean, modern, and transparent space where consenting adult clients and independent companions connect with dignity.
      </p>
      <p>
        Our advertisers represent educated college students, high-fashion models, bilingual corporate hostesses, and sensual homemakers who understand the nuances of elite hospitality. Whether you seek an articulate dinner date for a high-profile banquet at a 5-star hotel, an adventurous partner for mountain road trips through Almora and Bhowali, or a tender companion for romantic fireside conversations at a riverside Corbett resort, you will find extraordinary talent on our platform.
      </p>

      <h2>Our Four Pillars of Service Excellence</h2>
      <div class="categories-grid">
        <div class="category-box">
          <h4>1. 100% Genuine Photography</h4>
          <p>Every profile undergoes strict photo audit protocols. We demand real-time verification selfies holding current dates to ensure zero discrepancy between online advertisements and real-life encounters.</p>
        </div>
        <div class="category-box">
          <h4>2. The Ironclad Zero Advance Rule</h4>
          <p>Your financial security is our utmost priority. We mandate that no client ever send advance token money online. All transactions are settled in cash directly with the companion upon arrival.</p>
        </div>
        <div class="category-box">
          <h4>3. Total Privacy Shield</h4>
          <p>We do not collect personal identifying information from visitors. No registration is required, and all inquiries occur through encrypted third-party communications.</p>
        </div>
        <div class="category-box">
          <h4>4. Broad Regional Coverage</h4>
          <p>With active listings spanning 15 major Uttarakhand hubs, you can count on reliable companionship whether residing in luxury city suites or remote wildlife retreats.</p>
        </div>
      </div>
    </section>

    <section class="editorial-card">
      <h2>Recommended Hotel Venues &amp; Booking Etiquette in Uttarakhand</h2>
      <p>
        To ensure a completely seamless and confidential experience, we strongly encourage arranging appointments at established, guest-friendly 4-star and 5-star hotels or luxury private resorts. High-end establishments feature dedicated guest service desks, private elevator access, and soundproof suites that guarantee peace of mind.
      </p>
      <p>
        When contacting an independent companion, establish your expectations with courtesy and clarity. State your preferred duration (e.g., 1-hour session, 3-hour evening date, or full overnight stay), verify the location address, and ensure your accommodation welcomes registered visitors. Mutual respect and exemplary hygiene are the cornerstones of every fulfilling encounter.
      </p>
    </section>

    <section class="faq-section" id="faq-section">
      <h2>Frequently Asked Questions About Uttarakhand Escort Services</h2>
      <p class="faq-intro">Clear, detailed, and authoritative answers to the top 20 most searchable questions regarding escort bookings, rates, safety guidelines, and destination logistics in Uttarakhand.</p>
      <div class="faq-list">
{home_faqs_str}
      </div>
    </section>
  </main>

  <!-- COLORED & ENHANCED FOOTER (Image 3 Fix: Exact relative working links to eliminate 404s) -->
  <footer class="site-footer">
    <div class="container footer-grid">
      <div class="footer-col">
        {DMCA_BADGE_HTML}
        <h4>CityHaldwani.com</h4>
        <p>
          Uttarakhand's premier light-theme classified directory connecting verified independent advertisers with respectful adult clients across 15 destination hubs. Strict 18+ compliance, cash on meeting, and complete discretion.
        </p>
        <p style="font-size: 12px; color: var(--text-muted); margin-bottom: 8px;">
          Covering Haldwani, Nainital, Bhimtal, Ramnagar, Jim Corbett, Rudrapur, Kathgodam, Kashipur, Bajpur, Khatima, Sitarganj, Kichha, Almora, Bhowali, and Kaladhungi.
        </p>
        <span class="footer-badge-pill">🛡️ 100% Verified Classifieds • 18+ Adult Directory</span>
      </div>
      <div class="footer-col">
        <h4>Popular Destination Hubs</h4>
        <ul class="footer-links">
          <li><a href="locations/haldwani.html">Haldwani Escorts</a></li>
          <li><a href="locations/nainital.html">Nainital Escorts</a></li>
          <li><a href="locations/bhimtal.html">Bhimtal Escorts</a></li>
          <li><a href="locations/ramnagar.html">Ramnagar Escorts</a></li>
          <li><a href="locations/jim-corbett.html">Jim Corbett Escorts</a></li>
          <li><a href="locations/rudrapur.html">Rudrapur Escorts</a></li>
          <li><a href="locations/almora.html">Almora Escorts</a></li>
          <li><a href="locations/bhowali.html">Bhowali Escorts</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h4>Corporate, Legal &amp; Safety</h4>
        <ul class="footer-links">
          <li><a href="/about-us.html">About Us</a></li>
          <li><a href="/safety-guide.html">Safety Guidelines</a></li>
          <li><a href="/report-abuse.html">Report Abuse</a></li>
          <li><a href="/terms.html">Terms of Service</a></li>
          <li><a href="/privacy.html">Privacy Policy</a></li>
          <li><a href="/contact-us.html">Contact Support Desk</a></li>
        </ul>
      </div>
    </div>
    <div class="container footer-bottom">
      <div class="footer-bottom-flex">
        <div>&copy; 2026 CityHaldwani.com. All rights reserved. 100% Verified 18+ Adult Classified Directory.</div>
      </div>
    </div>
  </footer>

  <!-- Floating Action Buttons (Icon-Only Call & WhatsApp Logos) -->
  <div class="ch-floating-buttons" id="cityhaldwani-floating-buttons">
    <a href="tel:+919876543210" class="ch-float-btn ch-float-call" id="ch-float-call-btn" title="Call Support" aria-label="Call Support" data-contact="call">
      <span class="ch-float-pulse"></span>
      <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6.62 10.79a15.053 15.053 0 006.59 6.59l2.2-2.2c.27-.27.67-.36 1.02-.24 1.12.37 2.33.57 3.57.57.55 0 1 .45 1 1V20c0 .55-.45 1-1 1-9.39 0-17-7.61-17-17 0-.55.45-1 1-1h3.5c.55 0 1 .45 1 1 0 1.25.2 2.45.57 3.57.11.35.03.74-.25 1.02l-2.2 2.2z"/></svg>
    </a>
    <a href="https://api.whatsapp.com/send?phone=919876543210&amp;text={home_wa_encoded}" target="_blank" rel="noopener noreferrer" class="ch-float-btn ch-float-wa" id="ch-float-wa-btn" title="Chat on WhatsApp" aria-label="Chat on WhatsApp" data-contact="whatsapp">
      <span class="ch-float-pulse"></span>
      <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12.04 2C6.58 2 2.13 6.45 2.13 11.91C2.13 13.66 2.59 15.36 3.45 16.86L2.05 22L7.3 20.62C8.75 21.41 10.38 21.83 12.04 21.83C17.5 21.83 21.95 17.38 21.95 11.92C21.95 9.27 20.92 6.78 19.05 4.91C17.18 3.04 14.69 2 12.04 2M12.05 3.67C14.25 3.67 16.31 4.53 17.87 6.09C19.42 7.65 20.28 9.72 20.28 11.92C20.28 16.46 16.58 20.15 12.04 20.15C10.56 20.15 9.11 19.76 7.85 19L7.55 18.83L4.43 19.65L5.26 16.61L5.06 16.29C4.24 15 3.8 13.47 3.8 11.91C3.81 7.37 7.5 3.67 12.05 3.67M9.13 7.39C8.95 7.39 8.65 7.46 8.4 7.73C8.15 8 7.45 8.65 7.45 9.97C7.45 11.29 8.41 12.57 8.54 12.75C8.68 12.93 10.42 15.63 13.09 16.78C15.31 17.74 15.76 17.55 16.25 17.51C16.75 17.46 17.86 16.85 18.09 16.21C18.32 15.57 18.32 15.02 18.25 14.91C18.18 14.79 18 14.73 17.72 14.59C17.45 14.45 16.08 13.78 15.83 13.69C15.58 13.59 15.4 13.55 15.22 13.82C15.04 14.1 14.51 14.73 14.35 14.91C14.19 15.1 14.03 15.12 13.75 14.98C13.48 14.84 12.59 14.55 11.54 13.61C10.72 12.88 10.16 11.98 10 11.71C9.84 11.43 9.98 11.29 10.12 11.15C10.25 11.03 10.4 10.83 10.54 10.67C10.68 10.5 10.73 10.39 10.82 10.2C10.91 10.02 10.87 9.86 10.8 9.72C10.73 9.58 10.18 8.24 9.95 7.7C9.73 7.18 9.51 7.25 9.34 7.24C9.18 7.24 9.01 7.39 9.13 7.39Z"/></svg>
    </a>
  </div>

  <script src="/js/contacts-config.js" defer></script>
  <script src="/js/contact-manager.js" defer></script>
  <script src="/js/security-shield.js" defer></script>
  <script src="/js/age-gate.js" defer></script>
  <script>
    document.querySelectorAll('.faq-question').forEach(function(el) {{
      el.addEventListener('click', function() {{
        el.parentElement.classList.toggle('open');
      }});
    }});
  </script>
</body>
</html>'''

with open(os.path.join(OUTPUT_DIR, 'index.html'), 'w', encoding='utf-8') as f:
    f.write(index_html)

home_words = count_words(index_html)
home_profiles = len(re.findall(r'class="profile-card"', index_html))
home_faqs_count = len(re.findall(r'class="faq-item"', index_html))
print(f"Generated index.html -> Words: {home_words}, Profiles: {home_profiles}, FAQs: {home_faqs_count}")

# Generate/Update All Corporate Policy Pages with matching styling, Open Graph/Twitter tags, and exact footer links
POLICY_PAGES = [
    {
        'file': 'about-us.html',
        'title': 'About Us - Premier Uttarakhand Classified Directory | CityHaldwani.com',
        'desc': 'Learn about CityHaldwani.com, Uttarakhand\'s premier light-theme classified directory connecting verified independent advertisers with respectful adult clients.',
        'canonical': 'https://cityhaldwani.com/about-us.html',
        'h1': 'About CityHaldwani.com',
        'content': '''
      <p>Welcome to <strong>CityHaldwani.com</strong>, the dedicated regional classifieds and companionship directory serving Haldwani, Nainital, Bhimtal, Ramnagar, Jim Corbett, Rudrapur, Kashipur, and all 15 major destination hubs of Uttarakhand. Our platform was architected with a singular commitment: delivering an uncompromisingly transparent, secure, and modern advertising venue where independent companions and professional clients connect directly without predatory intermediaries or fraudulent booking practices.</p>

      <h2>Our Core Operational Mission</h2>
      <p>In an industry frequently clouded by unverified listings and misleading imagery, CityHaldwani.com sets the gold standard for authentication, privacy protection, and user experience. We operate as a neutral digital classified hosting service adhering strictly to fair information practices, verified digital identities, and adult legal standards.</p>

      <h3>1. Rigorous Advertiser Vetting</h3>
      <p>Every advertiser hosted across our location hubs undergoes an identity and age verification audit before publication. We require photo matching and confirmation of adult legal age (18+), ensuring that users interact exclusively with consenting adults presenting authentic representations of their services.</p>

      <h3>2. Privacy-Centric Architecture</h3>
      <p>Client confidentiality is paramount. CityHaldwani.com does not record invasive digital footprints, track non-essential cookies, or resell visitor communications. All inquiries happen directly over encrypted WhatsApp channels or direct voice calls between clients and advertisers.</p>

      <h3>3. Promoting Consensual, Ethical Etiquette</h3>
      <p>We uphold a zero-tolerance stance against exploitation, human trafficking, fraud, and misconduct. We mandate mutual respect, safe meeting standards in recognized five-star hotels and private residences, and transparent financial terms between independent parties.</p>

      <h2>Serving the Himalayan Tourism Corridor</h2>
      <p>From vacationers seeking VIP companionship during tranquil weekend retreats along the banks of Bhimtal and Nainital Lake, to corporate executives attending industrial conferences across Rudrapur and Kashipur, CityHaldwani.com bridges the gap between discerning visitors and elite local companionship.</p>

      <h2>Direct Contact &amp; Support</h2>
      <p>Have inquiries regarding directory policies, partnership verifications, or listing corrections? Our technical team remains responsive 24 hours a day to preserve directory integrity and user safety.</p>'''
    },
    {
        'file': 'safety-guide.html',
        'title': 'Safety Guidelines & Client Protection Protocol | CityHaldwani.com',
        'desc': 'Essential safety guidelines, the ironclad zero-advance payment rule, and verification protocols for meeting independent companions in Uttarakhand.',
        'canonical': 'https://cityhaldwani.com/safety-guide.html',
        'h1': 'Safety Guidelines &amp; Client Protection Protocol',
        'content': '''
      <p>At <strong>CityHaldwani.com</strong>, the personal safety and financial security of both visitors and independent advertisers are our paramount commitments. Please review our safety protocols carefully before initiating contact with any advertiser.</p>

      <h2>1. The Ironclad Zero Advance Rule</h2>
      <p><strong>Never send money online before meeting in person.</strong> No legitimate advertiser on CityHaldwani.com will ever demand online payment, UPI deposits, hotel advance fees, booking charges, or security tokens before arrival. Always pay directly in cash after meeting your companion in person inside your hotel room or private venue.</p>

      <h2>2. Choose Verified Luxury Accommodations</h2>
      <p>Always arrange appointments at recognized, guest-friendly 4-star and 5-star hotels or certified resort properties. These establishments provide dedicated front-desk security, soundproof rooms, private elevator access, and a safe environment for all parties.</p>

      <h2>3. Photo &amp; Identity Verification on Doorstep</h2>
      <p>When your companion arrives at your door, verify that her appearance matches her published photographs. Under our zero-advance policy, you retain the complete right to politely decline the appointment at the threshold if there is any misrepresentation.</p>

      <h2>4. Exemplary Personal Hygiene &amp; Mutual Boundaries</h2>
      <p>Mutual respect is the cornerstone of every fulfilling appointment. Maintain high personal hygiene standards, practice safe and responsible encounters, and strictly respect agreed boundaries and scheduled durations.</p>'''
    },
    {
        'file': 'report-abuse.html',
        'title': 'Report Abuse & Policy Violations | CityHaldwani.com',
        'desc': 'Report fake profiles, advance payment fraud, harassment, or unauthorized imagery to CityHaldwani.com compliance team.',
        'canonical': 'https://cityhaldwani.com/report-abuse.html',
        'h1': 'Report Abuse &amp; Violations',
        'content': '''
      <p>CityHaldwani.com maintains an uncompromising zero-tolerance policy against advance fraud, fake profiles, underage access, and non-consensual exploitation. If you encounter any violation of our standards, report it immediately.</p>

      <h2>What to Report:</h2>
      <ul>
        <li><strong>Advance Money Demands:</strong> Any advertiser asking for online bank transfers, Google Pay, PhonePe, or Paytm advance deposits.</li>
        <li><strong>Misleading Photography:</strong> Advertisers failing to match their published photographs.</li>
        <li><strong>Underage Concerns:</strong> Any suspicion of persons below the legal age of 18.</li>
        <li><strong>Harassment or Blackmail:</strong> Any unethical behavior or breach of privacy.</li>
      </ul>

      <h2>How to Submit an Incident Report</h2>
      <p>Send a detailed message directly to our Compliance Desk via WhatsApp or Telephone support: <strong>+91 98765 43210</strong>. Include the advertiser\'s advertised profile name, contact phone number, and a brief description of the incident. Reports are investigated within 2 to 4 hours, and offending listings are removed permanently.</p>'''
    },
    {
        'file': 'terms.html',
        'title': 'Terms of Service & User Agreement | CityHaldwani.com',
        'desc': 'Review the terms of service, user agreement, and directory disclaimer governing the use of CityHaldwani.com classified portal.',
        'canonical': 'https://cityhaldwani.com/terms.html',
        'h1': 'Terms of Service',
        'content': '''
      <p>By accessing or utilizing <strong>CityHaldwani.com</strong>, you agree to comply with and be bound by the following terms and conditions. If you disagree with any portion of these terms, you must exit this website immediately.</p>

      <h2>1. Age Requirement (18+ Only)</h2>
      <p>CityHaldwani.com contains adult-oriented classified advertising intended solely for consenting adults who have reached the legal age of majority (at least 18 years of age). By browsing this directory, you certify under penalty of perjury that you are at least 18 years old.</p>

      <h2>2. Neutral Classified Hosting Platform</h2>
      <p>CityHaldwani.com functions solely as a neutral digital classified advertising conduit. We do not operate an escort agency, brokerage firm, or employment service. Advertisers are independent adults who manage their own schedules, rates, and services.</p>

      <h2>3. Independent Financial Settlement</h2>
      <p>All financial arrangements occur strictly between the consenting adult client and the independent advertiser. CityHaldwani.com does not process, handle, or collect any payments, commissions, or booking fees on behalf of advertisers.</p>

      <h2>4. Prohibited Conduct</h2>
      <p>Users are strictly prohibited from utilizing this platform for any illegal purpose, human exploitation, unsolicited commercial messaging, or attempting to capture or redistribute advertiser photographs without authorization.</p>'''
    },
    {
        'file': 'privacy.html',
        'title': 'Privacy Policy & Data Protection | CityHaldwani.com',
        'desc': 'Discover how CityHaldwani.com preserves client anonymity, data privacy, and enforces zero tracking on our light-theme classified platform.',
        'canonical': 'https://cityhaldwani.com/privacy.html',
        'h1': 'Privacy Policy',
        'content': '''
      <p>Your privacy and confidentiality are of paramount importance to us. This Privacy Policy details our minimal data practices and our commitment to protecting your digital footprint while browsing <strong>CityHaldwani.com</strong>.</p>

      <h2>1. Zero Personal Data Collection</h2>
      <p>CityHaldwani.com does not require user registration, login credentials, credit card details, or personal names to access our classified directory. You can browse all destination hubs completely anonymously.</p>

      <h2>2. No Tracking Cookies</h2>
      <p>We do not use invasive tracking cookies or commercial tracking pixels to monitor your web activity across the internet. Session storage is used strictly for essential user experience functions, such as remembering 18+ age verification consent.</p>

      <h2>3. Encrypted Direct Communications</h2>
      <p>When you click to call or message an advertiser via WhatsApp, your communication routes through encrypted external protocols directly to the independent advertiser. CityHaldwani.com never intercepts, records, or stores your private conversations.</p>

      <h2>4. Digital Security Shield</h2>
      <p>We implement strict security measures to protect the digital assets of our advertisers, including restricting unauthorized right-click actions, automated scraping, and screen capture attempts.</p>'''
    },
    {
        'file': 'contact-us.html',
        'title': 'Contact Us & Support Desk | CityHaldwani.com',
        'desc': 'Get in touch with the CityHaldwani.com support desk for advertising inquiries, profile verification, and technical assistance.',
        'canonical': 'https://cityhaldwani.com/contact-us.html',
        'h1': 'Contact Support Desk',
        'content': '''
      <p>Welcome to the <strong>CityHaldwani.com</strong> Client &amp; Advertiser Support Center. We are dedicated to providing swift, confidential assistance to visitors and verified advertisers across Uttarakhand.</p>

      <h2>Direct Communication Channels</h2>
      <p>For immediate assistance regarding advertising opportunities, listing updates, or directory feedback, please reach out to our dedicated support coordinators:</p>
      <ul>
        <li><strong>Telephone Support:</strong> <a href="tel:+919876543210" style="color: var(--primary-accent); font-weight: 700;">+91 98765 43210</a> (Available 24/7)</li>
        <li><strong>WhatsApp Helpdesk:</strong> <a href="https://api.whatsapp.com/send?phone=919876543210" style="color: var(--wa-green); font-weight: 700;">+91 98765 43210</a> (Instant Messaging)</li>
        <li><strong>Operating Hours:</strong> 24 Hours a Day, 7 Days a Week, 365 Days a Year</li>
      </ul>

      <h2>New Advertiser Verification Requirements</h2>
      <p>If you are an independent female companion aged 18 or older wishing to list your services on CityHaldwani.com, please prepare the following verification items:</p>
      <ol>
        <li>Clear government-issued photo ID confirming age 18+ (personal identification details may be obscured; only photo and date of birth must be clearly visible).</li>
        <li>A real-time verification selfie holding a handwritten note with today\'s date.</li>
        <li>High-resolution, unedited portfolio photographs for your profile.</li>
        <li>Your preferred operating destinations across our 15 Uttarakhand hubs.</li>
      </ol>
      <p>Send all verification materials via WhatsApp for review by our administrative compliance team.</p>'''
    },
    {
        'file': '404.html',
        'title': 'Page Not Found (404) | CityHaldwani.com',
        'desc': 'The requested page was not found on CityHaldwani.com. Browse our 15 verified Uttarakhand escort destination hubs.',
        'canonical': 'https://cityhaldwani.com/404.html',
        'h1': 'Page Not Found (404)',
        'content': '''
      <p style="font-size: 17px; margin-bottom: 20px;">We apologize, but the page you requested cannot be located. It may have been moved, renamed, or temporarily retired.</p>
      <div style="margin-bottom: 24px;">
        <a href="index.html" class="btn-card-call" style="font-size: 15px; padding: 10px 24px;">&larr; Return to Homepage</a>
      </div>
      <h2>Browse Active Destination Hubs:</h2>
      <div class="location-pills-grid" style="margin-top: 14px;">
''' + home_pills_html + '''
      </div>'''
    }
]

for p in POLICY_PAGES:
    pol_wa_msg = p.get('wa_msg', f"Hello CityHaldwani, I have an inquiry regarding CityHaldwani.com.")
    pol_wa_encoded = urllib.parse.quote(pol_wa_msg)
    pol_html = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{p['title']}</title>
  <meta name="description" content="{p['desc']}">
  <link rel="canonical" href="{p['canonical']}">
  <link rel="icon" href="favicon.webp" type="image/webp">

  <!-- Open Graph Meta Tags (Image 1 Fix) -->
  <meta property="og:title" content="{p['title']}">
  <meta property="og:description" content="{p['desc']}">
  <meta property="og:type" content="website">
  <meta property="og:url" content="{p['canonical']}">
  <meta property="og:image" content="https://cityhaldwani.com/city-logo.png">
  <meta property="og:site_name" content="CityHaldwani.com">

  <!-- X / Twitter Card Meta Tags (Image 1 Fix) -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:site" content="@CityHaldwani">
  <meta name="twitter:title" content="{p['title']}">
  <meta name="twitter:description" content="{p['desc']}">
  <meta name="twitter:image" content="https://cityhaldwani.com/city-logo.png">
  <link rel="icon" href="/favicon.webp" type="image/webp">
  <link rel="preload" href="/city-logo.png" as="image">

  <!-- Directory Trailing Slash Script -->
  <script>
    (function() {{
      var p = window.location.pathname;
      if (p.endsWith('/cityhaldwani_com')) {{
        window.location.replace(p + '/' + window.location.search + window.location.hash);
      }}
    }})();
  </script>

  <style>
{EMBEDDED_CSS}
  </style>
</head>
<body>
{ADULT_WARNING_BAR_HTML}

  <header class="site-topbar">
    <div class="container topbar-wrapper">
      <a href="/index.html" class="brand-group">
        <img src="/city-logo.png" alt="CityHaldwani.com Logo" class="brand-logo-img" width="140" height="42" onerror="if(!this.dataset.retried){{this.dataset.retried=1;this.src='/logo.png';}}else if(this.dataset.retried==1){{this.dataset.retried=2;this.src='city-logo.png';}}">
        <div class="brand-text">
          <div class="brand-title">CityHaldwani<span>.com</span></div>
          <p>Verified Uttarakhand Classifieds</p>
        </div>
      </a>
      <div class="topbar-actions">
        <span class="badge-verified-top">&#10004; Verified Directory</span>
        <a href="tel:+919876543210" class="btn-header-call" data-contact="call">Call Support</a>
        <a href="https://api.whatsapp.com/send?phone=919876543210" class="btn-header-wa" data-contact="whatsapp">WhatsApp</a>
      </div>
    </div>
  </header>

  <main class="container">
    <nav class="breadcrumb-nav">
      <a href="/index.html">Home</a> &gt; <span>{p['h1']}</span>
    </nav>

    <div class="editorial-card" style="margin-top: 16px;">
      <h1>{p['h1']}</h1>
{p['content']}
    </div>
  </main>

  <footer class="site-footer">
    <div class="container footer-grid">
      <div class="footer-col">
        {DMCA_BADGE_HTML}
        <h4>CityHaldwani.com</h4>
        <p>Premier light-theme verified classified portal for Uttarakhand companions and tourists. Strict 18+ compliance and privacy assurance.</p>
        <span class="footer-badge-pill">🛡️ 100% Verified Classifieds • 18+ Adult Directory</span>
      </div>
      <div class="footer-col">
        <h4>Top Destinations</h4>
        <ul class="footer-links">
          <li><a href="/locations/haldwani.html">Haldwani Escorts</a></li>
          <li><a href="/locations/nainital.html">Nainital Escorts</a></li>
          <li><a href="/locations/bhimtal.html">Bhimtal Escorts</a></li>
          <li><a href="/locations/ramnagar.html">Ramnagar Escorts</a></li>
          <li><a href="/locations/jim-corbett.html">Jim Corbett Escorts</a></li>
          <li><a href="/locations/rudrapur.html">Rudrapur Escorts</a></li>
          <li><a href="/locations/almora.html">Almora Escorts</a></li>
          <li><a href="/locations/bhowali.html">Bhowali Escorts</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h4>Corporate &amp; Legal</h4>
        <ul class="footer-links">
          <li><a href="/about-us.html">About Us</a></li>
          <li><a href="/safety-guide.html">Safety Guidelines</a></li>
          <li><a href="/report-abuse.html">Report Violations</a></li>
          <li><a href="/terms.html">Terms of Service</a></li>
          <li><a href="/privacy.html">Privacy Policy</a></li>
          <li><a href="/contact-us.html">Contact Support Desk</a></li>
        </ul>
      </div>
    </div>
    <div class="container footer-bottom">
      <div class="footer-bottom-flex">
        <div>&copy; 2026 CityHaldwani.com. All rights reserved. 100% Verified 18+ Adult Classified Directory.</div>
      </div>
    </div>
  </footer>

  <!-- Floating Action Buttons (Icon-Only Call & WhatsApp Logos) -->
  <div class="ch-floating-buttons" id="cityhaldwani-floating-buttons">
    <a href="tel:+919876543210" class="ch-float-btn ch-float-call" id="ch-float-call-btn" title="Call Support" aria-label="Call Support" data-contact="call">
      <span class="ch-float-pulse"></span>
      <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6.62 10.79a15.053 15.053 0 006.59 6.59l2.2-2.2c.27-.27.67-.36 1.02-.24 1.12.37 2.33.57 3.57.57.55 0 1 .45 1 1V20c0 .55-.45 1-1 1-9.39 0-17-7.61-17-17 0-.55.45-1 1-1h3.5c.55 0 1 .45 1 1 0 1.25.2 2.45.57 3.57.11.35.03.74-.25 1.02l-2.2 2.2z"/></svg>
    </a>
    <a href="https://api.whatsapp.com/send?phone=919876543210&amp;text={pol_wa_encoded}" target="_blank" rel="noopener noreferrer" class="ch-float-btn ch-float-wa" id="ch-float-wa-btn" title="Chat on WhatsApp" aria-label="Chat on WhatsApp" data-contact="whatsapp">
      <span class="ch-float-pulse"></span>
      <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12.04 2C6.58 2 2.13 6.45 2.13 11.91C2.13 13.66 2.59 15.36 3.45 16.86L2.05 22L7.3 20.62C8.75 21.41 10.38 21.83 12.04 21.83C17.5 21.83 21.95 17.38 21.95 11.92C21.95 9.27 20.92 6.78 19.05 4.91C17.18 3.04 14.69 2 12.04 2M12.05 3.67C14.25 3.67 16.31 4.53 17.87 6.09C19.42 7.65 20.28 9.72 20.28 11.92C20.28 16.46 16.58 20.15 12.04 20.15C10.56 20.15 9.11 19.76 7.85 19L7.55 18.83L4.43 19.65L5.26 16.61L5.06 16.29C4.24 15 3.8 13.47 3.8 11.91C3.81 7.37 7.5 3.67 12.05 3.67M9.13 7.39C8.95 7.39 8.65 7.46 8.4 7.73C8.15 8 7.45 8.65 7.45 9.97C7.45 11.29 8.41 12.57 8.54 12.75C8.68 12.93 10.42 15.63 13.09 16.78C15.31 17.74 15.76 17.55 16.25 17.51C16.75 17.46 17.86 16.85 18.09 16.21C18.32 15.57 18.32 15.02 18.25 14.91C18.18 14.79 18 14.73 17.72 14.59C17.45 14.45 16.08 13.78 15.83 13.69C15.58 13.59 15.4 13.55 15.22 13.82C15.04 14.1 14.51 14.73 14.35 14.91C14.19 15.1 14.03 15.12 13.75 14.98C13.48 14.84 12.59 14.55 11.54 13.61C10.72 12.88 10.16 11.98 10 11.71C9.84 11.43 9.98 11.29 10.12 11.15C10.25 11.03 10.4 10.83 10.54 10.67C10.68 10.5 10.73 10.39 10.82 10.2C10.91 10.02 10.87 9.86 10.8 9.72C10.73 9.58 10.18 8.24 9.95 7.7C9.73 7.18 9.51 7.25 9.34 7.24C9.18 7.24 9.01 7.39 9.13 7.39Z"/></svg>
    </a>
  </div>

  <script src="/js/contacts-config.js" defer></script>
  <script src="/js/contact-manager.js" defer></script>
  <script src="/js/security-shield.js" defer></script>
  <script src="/js/age-gate.js" defer></script>
</body>
</html>'''
    with open(os.path.join(OUTPUT_DIR, p['file']), 'w', encoding='utf-8') as f:
        f.write(pol_html)
    print(f"Generated {p['file']}")

# Generate sitemap.xml
sitemap_urls = [
    ('https://cityhaldwani.com/', '1.0', 'daily'),
    ('https://cityhaldwani.com/about-us.html', '0.6', 'monthly'),
    ('https://cityhaldwani.com/contact-us.html', '0.6', 'monthly'),
    ('https://cityhaldwani.com/safety-guide.html', '0.7', 'monthly'),
    ('https://cityhaldwani.com/terms.html', '0.5', 'monthly'),
    ('https://cityhaldwani.com/privacy.html', '0.5', 'monthly'),
    ('https://cityhaldwani.com/report-abuse.html', '0.5', 'monthly')
]

for loc in LOCATIONS_CONFIG:
    sitemap_urls.append((f"https://cityhaldwani.com/locations/{loc['slug']}.html", '0.9', 'daily'))

sitemap_xml = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for u, prio, freq in sitemap_urls:
    sitemap_xml.append(f'  <url>\n    <loc>{u}</loc>\n    <changefreq>{freq}</changefreq>\n    <priority>{prio}</priority>\n  </url>')
sitemap_xml.append('</urlset>')

with open(os.path.join(OUTPUT_DIR, 'sitemap.xml'), 'w', encoding='utf-8') as f:
    f.write("\n".join(sitemap_xml))
print("Generated sitemap.xml with", len(sitemap_urls), "URLs.")

# Generate robots.txt
robots_txt = """User-agent: *
Allow: /
Disallow: /admin
Disallow: /admin/
Disallow: /admin!
Disallow: /api/
Disallow: /data_clicks.json

Sitemap: https://cityhaldwani.com/sitemap.xml
"""
with open(os.path.join(OUTPUT_DIR, 'robots.txt'), 'w', encoding='utf-8') as f:
    f.write(robots_txt)
print("Generated robots.txt")

# Generate llms.txt & llms-full.txt
llms_txt = """# CityHaldwani.com - AI Agent & LLM Information Guide
> Premier Light-Theme Verified Classifieds & Directory for Uttarakhand Escorts

## Core Mission
CityHaldwani.com operates strictly as a neutral technology venue providing verified adult classified listings across 15 destination hubs in Uttarakhand, India. The platform enforces an ironclad Zero Advance Payment policy, strict 18+ age verification, and 100% genuine photographic vetting.

## Operational Destinations (15 Hubs)
- Nainital: https://cityhaldwani.com/locations/nainital.html
- Bhimtal: https://cityhaldwani.com/locations/bhimtal.html
- Almora: https://cityhaldwani.com/locations/almora.html
- Ramnagar: https://cityhaldwani.com/locations/ramnagar.html
- Haldwani: https://cityhaldwani.com/locations/haldwani.html
- Kaladhungi: https://cityhaldwani.com/locations/kaladhungi.html
- Rudrapur: https://cityhaldwani.com/locations/rudrapur.html
- Kathgodam: https://cityhaldwani.com/locations/kathgodam.html
- Kashipur: https://cityhaldwani.com/locations/kashipur.html
- Bajpur: https://cityhaldwani.com/locations/bajpur.html
- Khatima: https://cityhaldwani.com/locations/khatima.html
- Sitarganj: https://cityhaldwani.com/locations/sitarganj.html
- Kichha: https://cityhaldwani.com/locations/kichha.html
- Jim Corbett: https://cityhaldwani.com/locations/jim-corbett.html
- Bhowali: https://cityhaldwani.com/locations/bhowali.html

## Legal & Compliance
- Strictly 18+ Consensual Adult Advertising.
- Zero tolerance for human trafficking or non-consensual activity.
- Client inquiries route directly to independent advertisers via phone/WhatsApp.
"""
with open(os.path.join(OUTPUT_DIR, 'llms.txt'), 'w', encoding='utf-8') as f:
    f.write(llms_txt)
with open(os.path.join(OUTPUT_DIR, 'llms-full.txt'), 'w', encoding='utf-8') as f:
    f.write(llms_txt)
print("Generated llms.txt and llms-full.txt")

print(f"\nTotal unique profile names used: {len(all_used_names)}")

# Synchronize all assets into public/ to guarantee 100% 200 OK on Vercel static serving
import shutil
PUBLIC_DIR = os.path.join(OUTPUT_DIR, 'public')
os.makedirs(PUBLIC_DIR, exist_ok=True)

# 1. Sync CSS and JS into public/
for folder in ['css', 'js', 'locations']:
    src_folder = os.path.join(OUTPUT_DIR, folder)
    dst_folder = os.path.join(PUBLIC_DIR, folder)
    if os.path.exists(src_folder):
        os.makedirs(dst_folder, exist_ok=True)
        for item in os.listdir(src_folder):
            s = os.path.join(src_folder, item)
            d = os.path.join(dst_folder, item)
            if os.path.isfile(s):
                shutil.copy2(s, d)

# 2. Sync root assets and policy pages into public/
for root_file in [
    'city-logo.png', 'logo.png', 'favicon.webp', 'robots.txt', 'sitemap.xml',
    'llms.txt', 'llms-full.txt', 'about-us.html', 'contact-us.html',
    'privacy.html', 'terms.html', 'report-abuse.html', 'safety-guide.html',
    '404.html', 'admin!.html'
]:
    s = os.path.join(OUTPUT_DIR, root_file)
    d = os.path.join(PUBLIC_DIR, root_file)
    if os.path.exists(s):
        shutil.copy2(s, d)

# 3. Create public/public/ mirror for backward-compatibility with any /public/ references
PUBLIC_PUBLIC_DIR = os.path.join(PUBLIC_DIR, 'public')
os.makedirs(PUBLIC_PUBLIC_DIR, exist_ok=True)
for item in os.listdir(PUBLIC_DIR):
    if item != 'public':
        s = os.path.join(PUBLIC_DIR, item)
        d = os.path.join(PUBLIC_PUBLIC_DIR, item)
        if os.path.isfile(s):
            shutil.copy2(s, d)

print("Synchronized all static assets and mirrors into public/ successfully.")
