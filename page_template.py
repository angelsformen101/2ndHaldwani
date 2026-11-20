import os
import re
import json

from build_pages import NAMES_POOL, LOCATIONS_CONFIG

# Helper to calculate clean visible body word count (excluding head, script, style)
def count_words(html_str):
    html = re.sub(r'<head[\s\S]*?</head>', ' ', html_str, flags=re.I)
    html = re.sub(r'<script[\s\S]*?</script>', ' ', html, flags=re.I)
    html = re.sub(r'<style[\s\S]*?</style>', ' ', html, flags=re.I)
    text = re.sub(r'<[^>]+>', ' ', html)
    words = text.split()
    return len(words)

# Build a single profile card calibrated to ~48 words
def render_profile_card(name, city_name, age, index, img_alias):
    rates_options = [
        ("₹1,500", "₹2,500", "₹7,000"),
        ("₹2,000", "₹3,000", "₹8,000"),
        ("₹1,800", "₹2,800", "₹7,500"),
        ("₹2,500", "₹3,500", "₹10,000")
    ]
    rates = rates_options[index % len(rates_options)]
    
    titles = [
        f"{name} 👑 VIP 5-Star Resort Companion",
        f"{name} 💖 Sweet Independent College Girl",
        f"{name} 🌟 Sensual Model For Romantic Dates",
        f"{name} 💃 Charming Mountain Tourism Escort",
        f"{name} 🔥 Elite Corporate Executive Companion",
        f"{name} ✨ Warm Mature Companion For Cozy Chats",
        f"{name} 🌺 Premium Freelance Model Real Photos",
        f"{name} 💎 Five-Star Luxury Suite Companion"
    ]
    title = titles[index % len(titles)]
    
    desc_snippets = [
        f"Verified companion in {city_name}. Clean, polite, and discreet hotel outcall with zero advance payment.",
        f"Educated companion offering verified hotel outcall in {city_name}. Punctual, with cash on meeting.",
        f"VIP companion in {city_name}. Polite disposition, good conversation, and relaxing hotel suite encounters.",
        f"Verified independent model in {city_name}. Discretion, comfort, and hospitality with genuine photos."
    ]
    desc = desc_snippets[index % len(desc_snippets)]
    
    photo_count = 3 + (index % 3)
    
    card_html = f'''
        <article class="profile-card" id="profile-{name.lower()}">
          <div class="card-media">
            <span class="vip-ribbon">VIP</span>
            <img src="/public/{img_alias}" alt="{name} - Verified Escort in {city_name}" loading="lazy">
            <span class="photo-count-pill">📷 {photo_count} Photos</span>
          </div>
          <div class="card-content">
            <div class="card-header-line">
              <span class="badge-vip-pill">VERIFIED</span>
              <h3 class="profile-name-title">{title}</h3>
            </div>
            <div class="card-rates-pill-row">
              <span class="rate-chip highlight">1 Hr: {rates[0]}</span>
              <span class="rate-chip highlight">2 Hr: {rates[1]}</span>
              <span class="rate-chip">Night: {rates[2]}</span>
              <span class="rate-chip">⭐ Cash on Arrival</span>
            </div>
            <p class="profile-description">{desc}</p>
            <div class="card-meta-row">
              <span class="meta-item">🎂 {age} Yrs</span>
              <span class="meta-item">📍 {city_name}</span>
              <span class="meta-item">🗣️ Hindi, English</span>
              <span class="meta-item">⭐ 4.9/5 ({120 + index * 8})</span>
            </div>
            <div class="card-action-bar">
              <a href="tel:+919876543210" class="btn-card-call" data-contact="call" data-profile-name="{name} ({city_name})">
                📞 Call {name}
              </a>
              <a href="https://api.whatsapp.com/send?phone=919876543210" class="btn-card-wa" data-contact="whatsapp" data-profile-name="{name} ({city_name})">
                💬 WhatsApp Chat
              </a>
              <span class="btn-card-details">Available Now</span>
            </div>
          </div>
        </article>'''
    return card_html

# Generate 20 concise, searchable FAQs calibrated to ~20-22 words each
def generate_20_faqs(city_name, hotels, landmarks):
    faqs = [
        (
            f"How can I book verified escorts in {city_name}?",
            f"Browse our listings, select a preferred companion, and click Call or WhatsApp. Confirm duration, meeting time, and hotel location directly with the advertiser."
        ),
        (
            f"Are companion profile photos in {city_name} genuine?",
            f"Yes, all independent advertisers in {city_name} submit date-verified authentication selfies before publication. We strictly forbid misleading stock photos."
        ),
        (
            f"Do escorts in {city_name} require advance payment?",
            f"No! CityHaldwani.com enforces a strict Zero Advance Payment rule. Never send online deposits. You pay in direct cash upon meeting in person."
        ),
        (
            f"Can companions visit my hotel room in {city_name}?",
            f"Yes, companions provide prompt outcall service to verified 4-star and 5-star hotels, including {hotels}, with complete in-room discretion."
        ),
        (
            f"What are the standard escort rates in {city_name}?",
            f"Standard rates are ₹1,500 to ₹2,500 for 1 hour, ₹2,500 to ₹3,500 for 2 hours, and ₹7,000 to ₹10,000 for full-night stays."
        ),
        (
            f"Is discretion guaranteed for appointments in {city_name}?",
            f"Yes, complete confidentiality is maintained. Companions arrive dressed casually, blending seamlessly into hotel lobbies and resort lounges without drawing attention."
        ),
        (
            f"What categories of companions are available in {city_name}?",
            f"Categories include independent college girls (18+), VIP models, corporate dinner hostesses, sensual mature homemakers, and outstation resort companions."
        ),
        (
            f"How quickly does a companion arrive in {city_name}?",
            f"Companions typically arrive within 30 to 45 minutes across central areas near {landmarks}. Hillside resorts may require 1 hour advance notice."
        ),
        (
            f"Can I book an escort for full-day sightseeing in {city_name}?",
            f"Yes, companions can accompany clients for full-day leisure tours, scenic mountain drives, lake visits, and cafe outings across the region."
        ),
        (
            f"What languages do escorts in {city_name} speak?",
            f"Companions are fluent in Hindi and possess proficient working knowledge of English, ensuring pleasant conversation during social dates."
        ),
        (
            f"Are outstation trips from {city_name} supported?",
            f"Yes, several independent models accommodate outstation travel to nearby hill stations. Travel logistics and per-day compensation are agreed beforehand."
        ),
        (
            f"What payment methods are accepted in {city_name}?",
            f"Direct cash on meeting is the preferred and safest method. Some companions accept instant UPI transfers after in-person arrival."
        ),
        (
            f"Can I book full-night escort service in {city_name}?",
            f"Yes, full-night bookings (typically 9 PM to 7 AM) are available for unhurried dinners, evening relaxation, and morning companionship."
        ),
        (
            f"What hygiene standards are maintained by companions?",
            f"Strict personal hygiene and grooming standards are upheld. Mutual cleanliness is mandatory, and safe health practices are strictly enforced."
        ),
        (
            f"Is it safe for solo tourists to hire escorts in {city_name}?",
            f"Yes, booking through CityHaldwani.com is completely safe. Always meet at recognized hotels, avoid advance money, and treat companions with respect."
        ),
        (
            f"Can I meet the companion in the hotel lobby first?",
            f"Yes, you can request a brief 5-minute meeting in the hotel lounge or coffee shop before proceeding to your room."
        ),
        (
            f"What if the companion does not match her photos?",
            f"Under our zero-advance guarantee, you can decline the meeting at your door with zero financial obligation if photos do not match."
        ),
        (
            f"What is the minimum legal age required to book?",
            f"You must be at least 18 years of age (or legal majority in your region) to access this directory or hire independent companions."
        ),
        (
            f"Are dinner dates and social events supported?",
            f"Yes, models are well-dressed and articulate, making them excellent partners for business dinners, private cocktails, and festive celebrations."
        ),
        (
            f"How do I cancel a booking in {city_name}?",
            f"If your travel plans change, notify the companion via WhatsApp at least 1 hour in advance so she can adjust her schedule."
        )
    ]
    return faqs

# Build location HTML page with target word count: 1,750 - 1,980 words
def build_location_page(loc, start_name_idx):
    slug = loc['slug']
    city_name = loc['name']
    title = loc['title']
    meta_desc = loc['meta_desc']
    tagline = loc['tagline']
    landmarks = loc['landmarks']
    hotels = loc['hotels']
    vibe = loc['vibe']
    
    # 16 profiles
    cards_html = []
    names_used = []
    for i in range(16):
        name = NAMES_POOL[(start_name_idx + i) % len(NAMES_POOL)]
        names_used.append(name)
        age = 20 + ((start_name_idx + i * 3) % 7)
        img_alias = f"profile_{( (start_name_idx + i) % 48 ) + 1:02d}.webp"
        cards_html.append(render_profile_card(name, city_name, age, i, img_alias))
    
    all_cards_str = "\n".join(cards_html)
    
    # 20 FAQs
    faqs = generate_20_faqs(city_name, hotels, landmarks)
    faqs_html = []
    faq_schema_items = []
    for q, a in faqs:
        faqs_html.append(f'''
          <div class="faq-item">
            <h3 class="faq-question">{q}</h3>
            <div class="faq-answer"><p>{a}</p></div>
          </div>''')
        faq_schema_items.append({
            "@type": "Question",
            "name": q,
            "acceptedAnswer": {
                "@type": "Answer",
                "text": a
            }
        })
    all_faqs_str = "\n".join(faqs_html)
    
    faq_schema_json = json.dumps({
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": faq_schema_items
    }, indent=2)

    local_biz_schema = json.dumps({
        "@context": "https://schema.org",
        "@type": "LocalBusiness",
        "name": f"CityHaldwani.com - {city_name} Escort Service",
        "image": "https://cityhaldwani.com/logo.png",
        "url": f"https://cityhaldwani.com/locations/{slug}",
        "telephone": "+919876543210",
        "priceRange": "₹1500 - ₹10000",
        "address": {
            "@type": "PostalAddress",
            "addressLocality": city_name,
            "addressRegion": "Uttarakhand",
            "addressCountry": "IN"
        },
        "openingHoursSpecification": {
            "@type": "OpeningHoursSpecification",
            "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
            "opens": "00:00",
            "closes": "23:59"
        }
    }, indent=2)
    
    pills = []
    for l in LOCATIONS_CONFIG:
        active_cls = " active" if l['slug'] == slug else ""
        pills.append(f'<a href="/locations/{l["slug"]}" class="loc-pill{active_cls}">📍 {l["name"]}</a>')
    pills_html = "\n".join(pills)

    html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <meta name="description" content="{meta_desc}">
  <link rel="canonical" href="https://cityhaldwani.com/locations/{slug}">
  <link rel="icon" href="/favicon.webp" type="image/webp">
  <link rel="stylesheet" href="/css/style.css">
  <script type="application/ld+json">
{local_biz_schema}
  </script>
  <script type="application/ld+json">
{faq_schema_json}
  </script>
</head>
<body>
  <header class="site-topbar">
    <div class="container topbar-wrapper">
      <a href="/" class="brand-group">
        <img src="/logo.png" alt="CityHaldwani.com Logo" class="brand-logo-img">
        <div class="brand-text">
          <div class="brand-title">CityHaldwani<span>.com</span></div>
          <p>Verified Uttarakhand Classifieds</p>
        </div>
      </a>
      <div class="topbar-actions">
        <span class="badge-verified-top">&#10004; 100% Genuine Profiles</span>
        <a href="tel:+919876543210" class="btn-header-call" data-contact="call">Call Support</a>
        <a href="https://api.whatsapp.com/send?phone=919876543210" class="btn-header-wa" data-contact="whatsapp">WhatsApp</a>
      </div>
    </div>
  </header>

  <main class="container">
    <nav class="breadcrumb-nav" aria-label="Breadcrumb">
      <a href="/">Home</a> &gt; <a href="/#locations">Uttarakhand</a> &gt; <span>{city_name} Escorts</span>
    </nav>

    <div class="location-pills-bar">
      <div class="location-pills-title">Browse Uttarakhand Destination Hubs:</div>
      <div class="location-pills-grid">
{pills_html}
      </div>
    </div>

    <section class="hero-editorial">
      <h1>Verified Independent Escorts in {city_name} - 5-Star Hotel Companions &amp; Genuine Call Girls</h1>
      <div class="hero-meta-badges">
        <span class="hero-badge">🏔️ {tagline}</span>
        <span class="hero-badge">⭐ 100% Real Photographs</span>
        <span class="hero-badge">🛡️ Strict Zero Advance Rule</span>
        <span class="hero-badge">🛎️ In-Room &amp; Resort Outcall</span>
      </div>
      <p>
        Welcome to the authoritative classified directory of verified escorts in {city_name}, Uttarakhand. Renowned for its {vibe}, {city_name} attracts holidaymakers and executives seeking unhurried, discreet luxury. Whether staying at a luxury resort along {landmarks} or relaxing in a private hillside villa, our vetted companions deliver unparalleled warmth, elegance, and charm.
      </p>
      <p>
        At CityHaldwani.com, we prioritize transparency and safety above all else. Every companion listed below has completed strict photo authentication and age verification checks (18+). You connect directly with the independent advertiser over phone or WhatsApp, eliminating brokerage fees and predatory third-party intermediaries. Review authentic profile details, compare flexible packages, and enjoy confidential companionship backed by our ironclad zero upfront payment policy.
      </p>
    </section>

    <section class="listings-section" id="verified-listings">
      <div class="listings-heading-bar">
        <h2>🔥 16 Active Verified Companions Available in {city_name}</h2>
        <span class="listings-count-badge">16 Profiles Active Now</span>
      </div>
      <div class="listings-grid">
{all_cards_str}
      </div>
    </section>

    <section class="editorial-card">
      <h2>Guide to Hiring Independent Companions in {city_name}</h2>
      <p>
        Planning a mountain holiday, business retreat, or weekend escape to {city_name} is made memorable with verified companionship. Independent models offer personalized companionship tailored to your schedule, from scenic daytime drives to private fireside hotel dinners with warmth and discretion.
      </p>

      <h2>Elite Companion Categories in {city_name}</h2>
      <div class="categories-grid">
        <div class="category-box">
          <h4>🎓 Independent College Girls</h4>
          <p>Fresh, educated students (18+) in {city_name}. Energetic, talkative, and perfect for casual outings and cafe dates.</p>
        </div>
        <div class="category-box">
          <h4>👑 VIP Fashion Models</h4>
          <p>Glamorous, tall models suitable for high-profile business dinners, luxury suite stays, and prestigious social events.</p>
        </div>
        <div class="category-box">
          <h4>💖 Sensual Mature Companions</h4>
          <p>Attentive homemakers and independent women excelling at passionate, relaxing companionship with zero drama.</p>
        </div>
        <div class="category-box">
          <h4>🌿 Luxury Resort Escorts</h4>
          <p>Versatile companions accustomed to high-end hospitality, wilderness safaris, and overnight tours across {landmarks}.</p>
        </div>
      </div>
    </section>

    <section class="editorial-card">
      <h2>Recommended Hotels &amp; Safe Meeting Spots in {city_name}</h2>
      <p>
        For a discreet encounter in {city_name}, reserve rooms at guest-friendly 4-star and 5-star properties, including {hotels}, offering secure parking, professional service, and private elevator access.
      </p>

      <h2>Client Safety Protocol &amp; Zero Advance Rule</h2>
      <ul>
        <li><strong>Never Pay Advance Money:</strong> Independent companions in {city_name} never ask for UPI transfers or booking deposits in advance. Pay in direct cash after meeting in person.</li>
        <li><strong>Verify Identity on Arrival:</strong> Confirm your companion matches her photographs before commencing your private appointment.</li>
        <li><strong>Maintain Mutual Respect:</strong> Treat companions with courtesy, maintain good personal hygiene, and honor agreed personal boundaries.</li>
        <li><strong>Preserve Discretion:</strong> Refrain from taking unauthorized photos or recording private moments.</li>
      </ul>
    </section>

    <section class="faq-section" id="faq-section">
      <h2>Frequently Asked Questions About Escorts in {city_name}</h2>
      <p class="faq-intro">Find clear, authoritative answers to the top 20 most searchable questions regarding escort bookings, rates, hotel visits, and safety in {city_name}.</p>
      <div class="faq-list">
{all_faqs_str}
      </div>
    </section>
  </main>

  <footer class="site-footer">
    <div class="container footer-grid">
      <div class="footer-col">
        <h4>CityHaldwani.com</h4>
        <p>
          Premier light-theme verified classified portal for Uttarakhand companions and tourists. Strict 18+ compliance, zero advance fee guarantee, and total client privacy.
        </p>
        <p style="font-size: 12px; color: var(--text-muted);">
          Operational across {city_name}, Haldwani, Nainital, Corbett, and all major Kumaon hill stations.
        </p>
      </div>
      <div class="footer-col">
        <h4>Top Uttarakhand Hubs</h4>
        <ul class="footer-links">
          <li><a href="/locations/haldwani">Haldwani Escorts</a></li>
          <li><a href="/locations/nainital">Nainital Escorts</a></li>
          <li><a href="/locations/bhimtal">Bhimtal Escorts</a></li>
          <li><a href="/locations/ramnagar">Ramnagar Escorts</a></li>
          <li><a href="/locations/jim-corbett">Jim Corbett Escorts</a></li>
          <li><a href="/locations/rudrapur">Rudrapur Escorts</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h4>Corporate &amp; Safety</h4>
        <ul class="footer-links">
          <li><a href="/about-us">About Us</a></li>
          <li><a href="/safety-guide">Safety Guidelines</a></li>
          <li><a href="/report-abuse">Report Abuse</a></li>
          <li><a href="/terms">Terms of Service</a></li>
          <li><a href="/privacy">Privacy Policy</a></li>
          <li><a href="/contact-us">Contact Support Desk</a></li>
        </ul>
      </div>
    </div>
    <div class="container footer-bottom">
      &copy; 2026 CityHaldwani.com. All rights reserved. 18+ Adult Classified Directory.
    </div>
  </footer>

  <script src="/js/contacts-config.js"></script>
  <script src="/js/contact-manager.js"></script>
  <script src="/js/security-shield.js"></script>
  <script src="/js/age-gate.js"></script>
  <script>
    document.querySelectorAll('.faq-question').forEach(function(el) {{
      el.addEventListener('click', function() {{
        el.parentElement.classList.toggle('open');
      }});
    }});
  </script>
</body>
</html>'''
    return html_content, names_used
