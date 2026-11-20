import os
import re
import json

from build_pages import NAMES_POOL, LOCATIONS_CONFIG
from page_template import build_location_page, render_profile_card, count_words, EMBEDDED_CSS

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
          <p style="font-size: 13px;">{loc['meta_desc']}</p>
        </div>
        <div style="margin-top: 10px;">
          <a href="locations/{loc['slug']}.html" class="btn-card-details" style="display: inline-block; width: 100%; text-align: center;">View 16 Profiles in {loc['name']} &rarr;</a>
        </div>
      </div>''')
dest_cards_str = "\n".join(dest_cards)

index_html = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>CityHaldwani.com - Premier Uttarakhand Escort Directory &amp; Verified Classifieds</title>
  <meta name="description" content="CityHaldwani.com is Uttarakhand's premier light-theme classified directory. Explore 100% verified independent escorts in Haldwani, Nainital, Bhimtal, Ramnagar, Corbett, and 15 destinations. Cash on meeting, zero advance.">
  <link rel="canonical" href="https://cityhaldwani.com/">
  <link rel="icon" href="favicon.webp" type="image/webp">
  <link rel="stylesheet" href="css/style.css">
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
  <header class="site-topbar">
    <div class="container topbar-wrapper">
      <a href="index.html" class="brand-group">
        <img src="logo.png" alt="CityHaldwani.com Logo" class="brand-logo-img" onerror="if(!this.dataset.retried){{this.dataset.retried=1;this.src='city-logo.png';}}">
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

    <section class="editorial-card" id="locations">
      <h2>Explore Verified Companions Across 15 Uttarakhand Locations</h2>
      <p>Select your city below to browse dedicated 16-profile directories with localized pricing, hotel guides, and safety recommendations:</p>
      <div class="categories-grid" style="grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));">
{dest_cards_str}
      </div>
    </section>

    <section class="listings-section" id="featured-listings">
      <div class="listings-heading-bar">
        <h2>🔥 16 Featured VIP Classified Profiles Across Uttarakhand</h2>
        <span class="listings-count-badge">Top Verified Models</span>
      </div>
      <div class="listings-grid">
{home_cards_str}
      </div>
    </section>

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

  <footer class="site-footer">
    <div class="container footer-grid">
      <div class="footer-col">
        <h4>CityHaldwani.com</h4>
        <p>
          Uttarakhand's premier light-theme classified directory connecting verified independent advertisers with respectful adult clients across 15 destination hubs. Strict 18+ compliance, cash on meeting, and complete discretion.
        </p>
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
          <li><a href="about-us.html">About Us</a></li>
          <li><a href="safety-guide.html">Safety Guidelines</a></li>
          <li><a href="report-abuse.html">Report Abuse</a></li>
          <li><a href="terms.html">Terms of Service</a></li>
          <li><a href="privacy.html">Privacy Policy</a></li>
          <li><a href="contact-us.html">Contact Support Desk</a></li>
        </ul>
      </div>
    </div>
    <div class="container footer-bottom">
      &copy; 2026 CityHaldwani.com. All rights reserved. 18+ Classified Directory.
    </div>
  </footer>

  <script src="js/contacts-config.js"></script>
  <script src="js/contact-manager.js"></script>
  <script src="js/security-shield.js"></script>
  <script src="js/age-gate.js"></script>
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

# Generate sitemap.xml
sitemap_urls = [
    ('https://cityhaldwani.com/', '1.0', 'daily'),
    ('https://cityhaldwani.com/about-us', '0.6', 'monthly'),
    ('https://cityhaldwani.com/contact-us', '0.6', 'monthly'),
    ('https://cityhaldwani.com/safety-guide', '0.7', 'monthly'),
    ('https://cityhaldwani.com/terms', '0.5', 'monthly'),
    ('https://cityhaldwani.com/privacy', '0.5', 'monthly'),
    ('https://cityhaldwani.com/report-abuse', '0.5', 'monthly')
]

for loc in LOCATIONS_CONFIG:
    sitemap_urls.append((f"https://cityhaldwani.com/locations/{loc['slug']}", '0.9', 'daily'))

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
- Nainital: https://cityhaldwani.com/locations/nainital
- Bhimtal: https://cityhaldwani.com/locations/bhimtal
- Almora: https://cityhaldwani.com/locations/almora
- Ramnagar: https://cityhaldwani.com/locations/ramnagar
- Haldwani: https://cityhaldwani.com/locations/haldwani
- Kaladhungi: https://cityhaldwani.com/locations/kaladhungi
- Rudrapur: https://cityhaldwani.com/locations/rudrapur
- Kathgodam: https://cityhaldwani.com/locations/kathgodam
- Kashipur: https://cityhaldwani.com/locations/kashipur
- Bajpur: https://cityhaldwani.com/locations/bajpur
- Khatima: https://cityhaldwani.com/locations/khatima
- Sitarganj: https://cityhaldwani.com/locations/sitarganj
- Kichha: https://cityhaldwani.com/locations/kichha
- Jim Corbett: https://cityhaldwani.com/locations/jim-corbett
- Bhowali: https://cityhaldwani.com/locations/bhowali

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
