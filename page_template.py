import os
import re
import json
import urllib.parse

from build_pages import NAMES_POOL, LOCATIONS_CONFIG
from location_local_data import LOCATION_LOCAL_DATA

# Load CSS content to embed directly in all generated pages
CSS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'css', 'style.css')
with open(CSS_FILE, 'r', encoding='utf-8') as f:
    EMBEDDED_CSS = f.read()

ADULT_WARNING_BAR_HTML = '''  <!-- 18+ Adult Content Moving Warning Bar -->
  <aside class="adult-warning-bar" role="alert" aria-label="18+ Adult Content Warning">
    <div class="warning-marquee-track">
      <div class="warning-marquee-content">
        <span class="warning-badge-18">🔞 18+ STRICT ADULT WARNING</span>
        <span>This website contains age-restricted 18+ adult classifieds and sensitive content intended solely for consenting adults aged 18 years and older.</span>
        <span class="warning-badge-alert">⚠️ AGE VERIFICATION REQUIRED</span>
        <span>By accessing this portal, you confirm under penalty of law that you are at least 18 years of age and agree to our Terms of Service &amp; Privacy Policy.</span>
        <span class="warning-divider">&#9670;</span>
        <span>Strict Zero Advance Payment Policy &bull; 100% Genuine Verified Profiles &bull; Cash On Direct Meeting Only &bull; Discreet In-Room &amp; Resort Outcall</span>
        <span class="warning-divider">&#9670;</span>
        <span>If you are under 18 years of age or find adult material objectionable, please exit this website immediately.</span>
      </div>
      <div class="warning-marquee-content" aria-hidden="true">
        <span class="warning-badge-18">🔞 18+ STRICT ADULT WARNING</span>
        <span>This website contains age-restricted 18+ adult classifieds and sensitive content intended solely for consenting adults aged 18 years and older.</span>
        <span class="warning-badge-alert">⚠️ AGE VERIFICATION REQUIRED</span>
        <span>By accessing this portal, you confirm under penalty of law that you are at least 18 years of age and agree to our Terms of Service &amp; Privacy Policy.</span>
        <span class="warning-divider">&#9670;</span>
        <span>Strict Zero Advance Payment Policy &bull; 100% Genuine Verified Profiles &bull; Cash On Direct Meeting Only &bull; Discreet In-Room &amp; Resort Outcall</span>
        <span class="warning-divider">&#9670;</span>
        <span>If you are under 18 years of age or find adult material objectionable, please exit this website immediately.</span>
      </div>
    </div>
  </aside>'''

DMCA_BADGE_HTML = '''<div class="dmca-badge-wrap">
          <a href="//www.dmca.com/Protection/Status.aspx?ID=ba77071e-739a-4ae4-a1e0-e8e954c427e2" title="DMCA.com Protection Status" class="dmca-badge"><img src="https://images.dmca.com/Badges/dmca_protected_sml_120m.png?ID=ba77071e-739a-4ae4-a1e0-e8e954c427e2" alt="DMCA.com Protection Status" /></a>
          <script src="https://images.dmca.com/Badges/DMCABadgeHelper.min.js"></script>
        </div>'''

# Helper to calculate clean visible body word count (excluding head, script, style)
def count_words(html_str):
    body_match = re.search(r'<body[\s\S]*?</body>', html_str, re.I)
    body_text = body_match.group(0) if body_match else html_str
    clean = re.sub(r'<script[\s\S]*?</script>', ' ', body_text, flags=re.I)
    clean = re.sub(r'<style[\s\S]*?</style>', ' ', clean, flags=re.I)
    words = re.sub(r'<[^>]+>', ' ', clean).split()
    return len(words)

# Localized SEO detailed knowledge for all 15 locations (~400+ words of genuine searchable local content)
LOCAL_SEO_GUIDES = {
    'nainital': {
        'sectors': 'Mallital, Tallital, Ayarpatta Hill, Sukhatal Valley, Snow View Ridge, Pangot Forest Road, Kilbury Bird Sanctuary Route, and Governor House (Raj Bhavan) Road',
        'sectors_detail': 'Whether your hotel is situated overlooking the tranquil waters of Naini Lake in Mallital, nestled among heritage deodars along the tranquil slopes of Ayarpatta, or perched near the scenic viewpoints of Snow View and Pangot, our independent escorts in Nainital offer prompt outcall coverage across all hill station zones. Most companions reach Mall Road and Tallital hotels within 30 to 40 minutes, while secluded villas in Pangot or Kilbury typically require approximately 50 minutes of advance coordination.',
        'hospitality': 'Nainital hosts some of Kumaon’s most prestigious heritage and boutique 5-star properties, such as The Manu Maharani, Shervani Hilltop, Vikram Vintage Inn, The Naini Retreat, and Swiss Hotel. When reserving outcall companionship at these premier establishments, luxury suites and lake-facing private balconies provide an ideal atmosphere of comfort and discretion. Independent models arrive dressed in tasteful smart-casual attire, blending naturally with other upscale vacationers and hotel guests.',
        'itineraries': 'During warm summer months, romantic late-afternoon yachting on Naini Lake followed by a cozy candlelit dinner at a boutique lakeside cafe creates an unforgettable experience. In the brisk winter season, when snow dusts the surrounding peaks, sharing warm fireside cocktails in the comfort of your private heated suite with an affectionate companion offers the ultimate mountain retreat.'
    },
    'bhimtal': {
        'sectors': 'Bhimtal Island Lake Promenade, Victoria Dam Road, Hidimba Parvat Foothills, Nal Damyanti Tal Lane, Mehragaon Valley, Sattal Junction Corridor, and Bhowali-Bhimtal Highway',
        'sectors_detail': 'Bhimtal is celebrated for its uncrowded, serene waters and private nature resorts. Our verified independent companions provide discreet outcall across all key sectors, from waterside luxury cottages bordering Victoria Dam to secluded hillside retreats near Mehragaon and the lush pine trails of Sattal road. Travel time to central Bhimtal resorts averages 25 to 35 minutes, ensuring prompt arrivals for dinner dates or overnight stays.',
        'hospitality': 'Prominent luxury destinations such as The Fern Hillside Resort, Country Inn Bhimtal, Aamod Resorts, Fishermens Lodge, and V Resort cater to privacy-conscious holidaymakers. These properties feature expansive private lawns and lake-view verandas that ensure complete anonymity. Independent models uphold strict professional standards, arriving with zero pretense and honoring your private boundaries under our strict zero-advance cash payment guarantee.',
        'itineraries': 'Bhimtal is an idyllic setting for unhurried conversations and scenic nature strolls. Spend quiet mornings admiring migratory birds over the island lake, take a leisurely drive through the pine woods of Sattal, and return to your resort for a private candlelit evening under star-filled Himalayan skies.'
    },
    'almora': {
        'sectors': 'Kasar Devi Magnetic Ridge, Bright End Corner, Historic Lal Bazaar, Dharanaula Junction, Binsar Wildlife Sanctuary Approach Road, Ranikhet Highway Corridor, and Matena Valley',
        'sectors_detail': 'Almora represents the cultural heartland of Kumaon, perched atop a scenic horse-saddle ridge. Independent companions provide dependable outcall across Kasar Devi’s bohemian ridge, Bright End Corner’s sunset viewpoints, and upscale forest lodges bordering the Binsar sanctuary. In-town visits to central Almora take between 30 and 40 minutes, while wilderness resorts along the Binsar forest corridor may require up to 55 minutes for safe mountain transit.',
        'hospitality': 'Prestigious heritage properties including Kalmatia Sangam, Grand Oak Manor, Deodar Sanctuary, Imperial Heights Binsar, and Kasaar Jungle Resort provide an unmatched backdrop of pine-wood elegance. Guests enjoy stone-carved fireplaces, panoramic Himalayan vistas of Nanda Devi, and attentive concierge service that ensures confidential guest visits without awkward scrutiny.',
        'itineraries': 'Almora is renowned for its inspiring sunsets and peaceful quietude. Pair your stay with an educated companion who appreciates culture, mountain tranquility, and engaging conversations. Sip fresh rhododendron tea during a brisk autumn afternoon, and spend unhurried evenings relaxing before a crackling deodar log fire.'
    },
    'ramnagar': {
        'sectors': 'Kosi River Barrage Corridor, Dhangarhi Tourist Gate, Ringora Wilderness Belt, Garjiya Devi Highway, Ramnagar Main Town, and Corbett National Park Periphery',
        'sectors_detail': 'As the primary entry gateway to the legendary Jim Corbett tiger reserve, Ramnagar buzzes with wildlife enthusiasts and luxury holidaymakers. Verified independent call girls in Ramnagar cater to private safari resorts along the Kosi River, secluded forest estates near Ringora, and comfortable business transit suites in Ramnagar town. Outcall transit to resorts along the Ramnagar-Ranikhet highway is exceptionally smooth, typically requiring 25 to 35 minutes.',
        'hospitality': 'Leading jungle venues like Namah Resort, The Den Corbett, Tarangi Resort & Spa, Lemon Tree Premier Corbett, and Corbett River Creek offer 5-star wilderness hospitality. These sprawling resorts feature private riverside decks, individual cottage compounds, and secure gated entry. Independent models arrive discreetly in smart travel attire, respecting guest privacy at all times.',
        'itineraries': 'After an exhilarating morning jeep safari tracking royal Bengal tigers, unwind with an in-room relaxation massage and a refreshing riverside cocktail. Savor fresh river fish delicacies at a private barbecue dinner accompanied by a charming, articulate companion who enhances every moment of your wilderness vacation.'
    },
    'haldwani': {
        'sectors': 'Nainital Road, Tikonia Commercial Hub, Kaladhungi Road, Kusumkhera, Mukhani Crossing, Canal Road, Kathgodam Bypass, Bareilly Road, Rampur Road, Heera Nagar, and Subhash Nagar',
        'sectors_detail': 'As the largest commercial metropolis and economic engine of Kumaon, Haldwani features a fast-paced urban lifestyle with modern amenities. Our verified escort classifieds cover every major sector in Haldwani, from high-end corporate suites near Tikonia and Nainital Road to peaceful residential avenues in Kusumkhera, Mukhani, and Heera Nagar. Companions typically arrive at your hotel suite within 20 to 30 minutes, offering the fastest outcall response times in the region.',
        'hospitality': 'Haldwani offers top-tier corporate hospitality at venues like Hotel Saurabh Candy by Peppermint, Fortune Walkway Mall, Hotel Maple Wood, Hotel Crossroad, and The Central Hotel. These establishments provide modern executive suites, private elevators, and discrete guest entry protocols. Our independent companions are well-versed in executive etiquette, making them ideal partners for business dinners and corporate suite meetings.',
        'itineraries': 'Begin your evening with gourmet dining and cocktails at upscale rooftop lounges along Nainital Road, followed by private suite entertainment. Whether visiting for commercial negotiations, industrial summits, or as a stopover before heading into the hills, Haldwani offers premier entertainment backed by transparent zero-advance cash payments.'
    },
    'kaladhungi': {
        'sectors': 'Jim Corbett Heritage Museum Precinct, Corbett Falls Forest Route, Boar River Valley, Choti Haldwani Village Corridor, Forest Checkpost Road, and Bazpur-Kaladhungi Highway',
        'sectors_detail': 'Kaladhungi is an enchanting nature enclave situated at the scenic junction where fertile Terai agricultural lands meet the towering Shivalik foothills. Independent companions provide dependable outcall service to eco-resorts nestled along the Boar River, private mango orchard farmhouses in Choti Haldwani, and forest hideaways near the Corbett Falls trail. Outcall arrivals to local lodges take between 30 and 45 minutes.',
        'hospitality': 'Boutique properties such as Camp Corbett, Corbett Panorama, Forest Haven Eco Resort, Hidden Valley Camp, and The Banyan Retreat cater to nature lovers seeking authentic privacy. These venues offer open-air bonfires, private cottage verandas, and rustic luxury. Independent models understand the expectations of countryside privacy, ensuring an intimate, relaxed experience free from urban distractions.',
        'itineraries': 'Explore the lush green trails of Choti Haldwani village and take a refreshing daytime dip at Corbett Falls. In the evening, relax beside a riverside bonfire under star-filled skies, enjoying deep conversation, laughter, and passionate companionship with a vetted independent partner.'
    },
    'rudrapur': {
        'sectors': 'SIDCUL Industrial Sector, Metropolis City Mall Corridor, Kashipur Bypass, Awas Vikas Colony, Gaba Chowk, National Highway 87, Kichha Bypass Junction, and Civil Lines',
        'sectors_detail': 'Rudrapur is the booming industrial heart of Uttarakhand, housing hundreds of multinational manufacturing enterprises in the SIDCUL industrial complex. We provide elite corporate companionship across all commercial zones, including business hotels along NH 87, executive apartments near Metropolis Mall, and private residences in Awas Vikas. Independent companions arrive punctually within 20 to 30 minutes for business travelers staying in central Rudrapur.',
        'hospitality': 'Premier executive business hotels such as Radisson Blu Hotel Rudrapur, Hotel Ark, Rosewood Apartment Hotel, Uday Residency, and Ginger Rudrapur provide 4-star and 5-star amenities. These hotels offer state-of-the-art conference facilities, luxury suites, and discrete private elevators. Independent models in Rudrapur are educated, articulate, and bilingual, perfectly suited for high-level business dinners and unwinding after intensive corporate meetings.',
        'itineraries': 'After a long day of factory inspections or corporate negotiations in SIDCUL, treat yourself to a lavish private suite dinner and a rejuvenating full-body relaxation massage. Our independent corporate hostesses provide sophisticated company, helping you recharge in complete comfort and privacy.'
    },
    'kathgodam': {
        'sectors': 'Kathgodam Railway Station Terminus, Gaula River Barrage, Ranibagh Historic Bridge, Shivalik Foothill Entrance, Nainital Road Junction, Damuadhunga, and Circuit House Area',
        'sectors_detail': 'Kathgodam serves as the historic railhead where the Indian Railway network reaches the base of the Kumaon Himalayas. Independent escorts provide swift outcall to transit hotels along the railway terminus, riverside resorts near Gaula Barrage, and heritage rest houses on Ranibagh Bridge. Because Kathgodam is closely linked to Haldwani, companions arrive within 20 to 30 minutes at any transit hotel or private guest house.',
        'hospitality': 'Popular hospitality venues including Hotel Fiesta, Relax Inn Kathgodam, Pineview Hotel, Gaula River View Resort, and The Grand Kailash provide clean, guest-friendly accommodations. These hotels are accustomed to welcoming travelers arriving on express trains like the Shatabdi and Ranikhet Express, offering flexible check-in hours and discreet elevator access.',
        'itineraries': 'Whether you have a 6-hour layover before your mountain taxi arrives or wish to spend a quiet evening enjoying the cool mountain air off the Gaula River, hiring a local companion makes your transit effortless and delightful. Enjoy private room service dining and soothing conversation before continuing your journey.'
    },
    'kashipur': {
        'sectors': 'Bazpur Road Industrial Sector, Ramnagar Road Highway Corridor, IIM Kashipur Campus Vicinity, Drona Sagar Lake Precinct, Industrial Area Phase 1 & 2, Kundeshwari Road, and Aliganj Road',
        'sectors_detail': 'Kashipur combines rich historical heritage with a thriving paper, textile, and chemical industrial hub. Independent companions cater to executives, engineers, and visiting professionals across the Bazpur Road commercial belt, Ramnagar Road hotel corridor, and private residential colonies near the premier IIM Kashipur campus. Average outcall arrival time to certified hotels is approximately 25 to 35 minutes.',
        'hospitality': 'Quality local properties including The Manor Kashipur, Anand Castle, Hotel Kumaon Plaza, Gautam Residency, and Hotel Ashiyana offer comfortable executive accommodations. These hotels feature secure private parking, multi-cuisine restaurants, and discreet suite service. Independent models arrive unassumingly, ensuring zero embarrassment or intrusion.',
        'itineraries': 'Spend your afternoon exploring the historic archaeological ruins of Drona Sagar, followed by an intimate evening of dining and relaxation at a premier local hotel. Our verified models bring youthful charm, intelligent conversation, and sensual warmth to your Kashipur stay.'
    },
    'bajpur': {
        'sectors': 'Bajpur Sugar Mill Complex, Kashipur-Haldwani State Highway, Terai Orchard Farm Belts, Kosi River Canal Crossing, Sultanpur Patti Road, and Main Bazaar Chowk',
        'sectors_detail': 'Bajpur is renowned throughout northern India for its sprawling agricultural estates, historic sugar mills, and tranquil countryside living. Verified escorts provide discreet outcall service to private farmhouses along the Kashipur-Haldwani highway, boutique rural homestays, and local hotel suites in Bajpur town. Companions typically reach local venues within 30 to 45 minutes.',
        'hospitality': 'Establishments like Green Park Hotel, Terai Royal Residency, The Orchard Retreat, and Hotel Shivalik View Bajpur offer clean, comfortable stays tailored to business travelers and agricultural entrepreneurs. For clients staying at private family farmhouses, independent models are happy to visit directly with complete discretion and cash-on-arrival terms.',
        'itineraries': 'Experience the peaceful beauty of the Terai countryside away from city noise. Enjoy expansive sunset views over sugarcane fields, organize a private outdoor barbecue, and share an unhurried, romantic overnight encounter with an affectionate companion.'
    },
    'khatima': {
        'sectors': 'Tanakpur Highway Corridor, Sharda River Canal Banks, Khatima Main Market, Lohiahead Power House Road, Nanakmatta Link Road, and Melghat Border Checkpoint Area',
        'sectors_detail': 'Khatima is an important commercial corridor and transit junction situated near the scenic Indo-Nepal international border and the holy pilgrimage shrine of Nanakmatta. Verified independent call girls offer prompt outcall to certified hotels on Tanakpur Road, private guest lodges near the Sharda Canal, and commercial suites in Khatima market. Companions arrive within 25 to 35 minutes across all local addresses.',
        'hospitality': 'Leading local properties including Hotel Royal Park Khatima, City Heart Inn, Sharda Heritage Hotel, and The Green Valley Inn feature air-conditioned executive rooms and respectful hotel staff. Independent companions arrive dressed in elegant, casual clothing, ensuring completely private meetings with zero unwanted attention.',
        'itineraries': 'Take a relaxing daytime drive along the crystal-clear Sharda River canal and visit the serene waters of Nanakmatta reservoir. Return to your hotel suite for a private evening of wine, delicious local Kumaoni cuisine, and passionate companionship with a genuine independent companion.'
    },
    'sitarganj': {
        'sectors': 'ELDECO SIDCUL Industrial Park, Baigul Dam Reservoir Road, Nanakmatta Sahib Bypass, Khatima Highway, Amariya Road, and Industrial Phase 1 & 2',
        'sectors_detail': 'Sitarganj is a major manufacturing growth center in the Terai, anchored by the sprawling ELDECO SIDCUL industrial complex and the picturesque waters of Baigul Dam. Independent models provide professional outcall to corporate hotels near the industrial zone, lakeside guest houses, and private residences along the Khatima highway. Companions arrive within 25 to 35 minutes for verified hotel bookings.',
        'hospitality': 'Hotels such as Hotel Sitarganj Grand, The Industrial Inn, Green View Palace, and Lakeview Comfort Stay Sitarganj provide reliable amenities for corporate executives, plant heads, and technical consultants. These establishments respect client privacy, making them ideal for confidential evening appointments.',
        'itineraries': 'After a strenuous day overseeing manufacturing operations or visiting industrial facilities, unwind with the attentive care of an independent companion. Savor a peaceful dinner overlooking the tranquil waters of Baigul Dam and enjoy a stress-relieving massage in your private hotel suite.'
    },
    'kichha': {
        'sectors': 'Bareilly-Nainital Highway, Rudrapur Bypass Crossing, Kichha Railway Station Area, Grain Market Mandi Road, Terai Canal Banks, and Pulbhatta Border Corridor',
        'sectors_detail': 'Kichha occupies a strategic geographic crossroads in southern Uttarakhand, serving as a key junction linking Bareilly, Rudrapur, and Haldwani. Verified independent escorts provide reliable outcall service to highway transit hotels, private suites near the railway station, and upscale residential farmhouses. Average arrival time is 20 to 30 minutes across all main highway corridors.',
        'hospitality': 'Properties like Hotel Celebration Kichha, The Highway Heritage, City Pride Inn, and Amar Palace Kichha provide spacious rooms, secure parking, and guest-friendly hospitality. Independent models arrive with zero hassle, allowing you to settle payment directly in cash upon their arrival with complete peace of mind.',
        'itineraries': 'Kichha is ideal for travelers seeking a comfortable transit stopover before traveling deeper into Kumaon. Rejuvenate with a warm shower, delicious hot room service dinner, and the affectionate company of a beautiful independent model who makes your transit restful and memorable.'
    },
    'jim-corbett': {
        'sectors': 'Dhikala Safari Zone Approach, Bijrani Gate Corridor, Jhirna Gate Tourism Zone, Sitabani Forest Reserve, Kosi River Valley, Marchula Valley, and Mohan Forest Belt',
        'sectors_detail': 'The Jim Corbett national park region is world-renowned for eco-luxury safari lodges and pristine wildlife wilderness. Verified VIP escorts in Jim Corbett provide exclusive outcall to 5-star forest resorts across Dhikala, Bijrani, and Jhirna zones, as well as secluded riverside cottages along the Kosi River in Marchula and Mohan. Because of the vast expanse of the forest reserve, companions typically coordinate travel within 35 to 50 minutes.',
        'hospitality': 'Ultra-luxury resort properties including Taj Corbett Resort & Spa, The Solluna Resort, Paatlidun Safari Lodge, Namah Resort, and Aahana The Corbett Wilderness offer world-class hospitality. These resorts boast private plunge pools, private villas surrounded by dense sal trees, and secluded verandas. Our VIP models are accustomed to elite luxury settings, arriving with impeccable poise and sophistication.',
        'itineraries': 'Pair an exhilarating daytime wildlife safari with a magical candlelit dinner beside the Kosi River. Savor vintage wine under the stars, listen to the nocturnal sounds of the jungle, and enjoy passionate, uninhibited companionship in the secluded luxury of your private pool villa.'
    },
    'bhowali': {
        'sectors': 'Bhowali Sanatorium Ridge, Kainchi Dham Junction Highway, Ramgarh Fruit Orchard Road, Golu Devta Temple Corridor, Pine Crest Valley, and Shyamkhet Tea Gardens',
        'sectors_detail': 'Perched at a refreshing altitude of 1,700 meters, Bhowali is famous for its crisp pine-scented air, lush fruit orchards, and proximity to the sacred Kainchi Dham ashram. Independent companions cater to heritage cottages near the Sanatorium ridge, boutique hillside resorts along Ramgarh road, and private mountain homestays near the Shyamkhet tea estate. Outcall transit averages 30 to 40 minutes from central Bhowali junctions.',
        'hospitality': 'Charming mountain properties including The White Peaks Bhowali, Aqua De Vida Resort, Pine Crest Hotel, Soulitude in the Himalayas, and Cedar Cottage provide cozy fireplaces, panoramic valley views, and exceptional privacy. Independent companions arrive discreetly, ensuring your mountain holiday remains peaceful and confidential.',
        'itineraries': 'Bhowali is the ultimate romantic hideaway. Spend peaceful mornings driving through misty pine forests and visiting local tea plantations. As evening temperatures drop, share a warm bottle of wine beside a crackling stone fireplace, wrapped in warm blankets with a sweet, affectionate companion.'
    }
}

# Build a single profile card calibrated with single local keyword title + expanded ~60-word description
def render_profile_card(name, city_name, age, index, img_alias, rel_prefix='../', profile_title=None):
    rates_options = [
        ("₹1,500", "₹2,500", "₹7,000"),
        ("₹2,000", "₹3,000", "₹8,000"),
        ("₹1,800", "₹2,800", "₹7,500"),
        ("₹2,500", "₹3,500", "₹10,000")
    ]
    rates = rates_options[index % len(rates_options)]
    
    categories = [
        "Independent College Model",
        "VIP 5-Star Resort Companion",
        "Sensual Corporate Hostess",
        "Charming Freelance Companion"
    ]
    category = categories[index % len(categories)]
    
    if not profile_title:
        profile_title = f"{city_name} Call Girls"
    
    descriptions = [
        f"Verified independent model {name} (age {age}) offers elite companionship in {city_name} and nearby luxury hotels. Fluent in English and Hindi, she specializes in sophisticated dinner dates, relaxed private suite meetings, and overnight companionship. Known for punctuality, pleasant communication, and strict confidentiality, {name} operates under our zero-advance guarantee with direct cash payment upon arrival at your room.",
        f"Meet {name}, a sweet and educated companion (age {age}) serving clients across {city_name}. Whether you are staying at a hillside resort or central hotel, she provides warm, attentive in-room companionship tailored to your schedule. Enjoys deep conversations, pleasant dining, and stress-relieving relaxation. Direct cash on meeting with 100% genuine verified photographs.",
        f"High-profile independent companion {name} (age {age}) provides VIP outcall service to certified 4-star and 5-star properties in {city_name}. Articulate, stylish, and discreet, she is an ideal partner for corporate dinners, social gatherings, or intimate suite encounters. Zero advance payment required; settle directly in cash upon her arrival at your room.",
        f"Charming and affectionate, {name} (age {age}) is an independent verified model available for prompt hotel visits in {city_name}. She offers relaxed private meetings, polite conversation, and memorable holiday companionship across local destinations. Committed to strict client confidentiality, mutual respect, and transparent cash-on-meeting booking."
    ]
    desc = descriptions[index % len(descriptions)]
    photo_count = 3 + (index % 3)
    
    card_html = f'''
        <article class="profile-card" id="profile-{name.lower()}">
          <div class="card-media">
            <span class="vip-ribbon">VIP</span>
            <img src="/{img_alias}" alt="{name} - {profile_title} in {city_name}" loading="lazy" decoding="async" width="175" height="220" onerror="if(!this.dataset.retried){{this.dataset.retried=1;this.src='/public/{img_alias}';}}else if(this.dataset.retried==1){{this.dataset.retried=2;this.src='{rel_prefix}public/{img_alias}';}}">
            <span class="photo-count-pill">📷 {photo_count} Photos</span>
          </div>
          <div class="card-content">
            <div class="card-header-line">
              <span class="badge-vip-pill">VERIFIED VIP</span>
              <h3 class="profile-name-title">{profile_title}</h3>
            </div>
            <div class="card-model-subtitle">
              <span class="model-name">👑 {name}</span> &bull; <span class="model-age">{age} Yrs</span> &bull; <span class="model-category">{category}</span> &bull; <span class="model-badge">&#10004; Photo Verified</span>
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

# Build location HTML page with target word count: ~2,800 - 3,200 words
def build_location_page(loc, start_name_idx):
    slug = loc['slug']
    city_name = loc['name']
    title = loc['title']
    meta_desc = loc['meta_desc']
    tagline = loc['tagline']
    landmarks = loc['landmarks']
    hotels = loc['hotels']
    vibe = loc['vibe']
    h1_title = loc.get('h1', f"{city_name} Call Girls - Verified {city_name} Escort Service in {loc.get('seo_landmark', landmarks.split(',')[0])}")
    seo_landmark = loc.get('seo_landmark', landmarks.split(',')[0].strip())
    seo_hotel = loc.get('seo_hotel', hotels.split(',')[0].strip())
    
    local_guide = LOCAL_SEO_GUIDES.get(slug, {
        'sectors': landmarks,
        'sectors_detail': f"Companions in {city_name} cover all major transit points and hotel clusters promptly.",
        'hospitality': f"Certified hotels in {city_name} including {hotels} provide safe outcall settings.",
        'itineraries': f"Enjoy scenic mountain drives and private dining in {city_name} with verified models."
    })
    
    # 16 profiles with ../ relative prefix and unique local search keywords
    loc_local = LOCATION_LOCAL_DATA.get(slug, {})
    prof_keywords = loc_local.get('profile_keywords', [])
    
    cards_html = []
    names_used = []
    for i in range(16):
        name = NAMES_POOL[(start_name_idx + i) % len(NAMES_POOL)]
        names_used.append(name)
        age = 20 + ((start_name_idx + i * 3) % 7)
        img_alias = f"profile_{( (start_name_idx + i) % 48 ) + 1:02d}.webp"
        prof_kw = prof_keywords[i % len(prof_keywords)] if prof_keywords else f"{city_name} Call Girls"
        cards_html.append(render_profile_card(name, city_name, age, i, img_alias, rel_prefix='../', profile_title=prof_kw))
    
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
        "image": "https://cityhaldwani.com/city-logo.png",
        "url": f"https://cityhaldwani.com/locations/{slug}.html",
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
    
    # In location pages, pills link to sister locations cleanly
    pills = []
    for l in LOCATIONS_CONFIG:
        active_cls = " active" if l['slug'] == slug else ""
        pills.append(f'<a href="{l["slug"]}.html" class="loc-pill{active_cls}">📍 {l["name"]}</a>')
    pills_html = "\n".join(pills)

    # Popular Searches Section for location
    pop_tags = loc_local.get('popular_tags', [
        f"{city_name} call girls", f"{city_name} escort service", f"Call girls in {city_name}", f"Escorts in {city_name}",
        f"hotel service call girls {city_name}", f"independent escorts {city_name}", f"cash on arrival {city_name}",
        f"24 hour call girl service {city_name}", f"VIP escorts {city_name}", f"call girls near me {city_name}"
    ])
    tag_accents = ['accent-blue', 'accent-pink', 'accent-green', 'accent-purple', '']
    pop_tags_html_list = []
    for idx, tag in enumerate(pop_tags):
        acc = tag_accents[idx % len(tag_accents)]
        cls = f"popular-tag {acc}".strip()
        pop_tags_html_list.append(f'<a href="#verified-listings" class="{cls}">{tag}</a>')
    popular_tags_html = "\n".join(pop_tags_html_list)

    loc_wa_msg = f"Hello CityHaldwani, I want to book a verified companion in {city_name}. Please share available profiles."
    loc_wa_encoded = urllib.parse.quote(loc_wa_msg)

    html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <meta name="description" content="{meta_desc}">
  <link rel="canonical" href="https://cityhaldwani.com/locations/{slug}.html">
  <link rel="icon" href="/favicon.webp" type="image/webp">
  <link rel="preload" href="/city-logo.png" as="image">

  <!-- Open Graph Meta Tags (Image 1 Fix) -->
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{meta_desc}">
  <meta property="og:type" content="website">
  <meta property="og:url" content="https://cityhaldwani.com/locations/{slug}.html">
  <meta property="og:image" content="https://cityhaldwani.com/city-logo.png">
  <meta property="og:site_name" content="CityHaldwani.com">

  <!-- X / Twitter Card Meta Tags (Image 1 Fix) -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:site" content="@CityHaldwani">
  <meta name="twitter:title" content="{title}">
  <meta name="twitter:description" content="{meta_desc}">
  <meta name="twitter:image" content="https://cityhaldwani.com/city-logo.png">

  <style>
{EMBEDDED_CSS}
  </style>
  <script type="application/ld+json">
{local_biz_schema}
  </script>
  <script type="application/ld+json">
{faq_schema_json}
  </script>
</head>
<body>
{ADULT_WARNING_BAR_HTML}

  <header class="site-topbar">
    <div class="container topbar-wrapper">
      <a href="/index.html" class="brand-group">
        <img src="/city-logo.png" alt="CityHaldwani.com Logo" class="brand-logo-img" width="140" height="42" onerror="if(!this.dataset.retried){{this.dataset.retried=1;this.src='/logo.png';}}else if(this.dataset.retried==1){{this.dataset.retried=2;this.src='../city-logo.png';}}">
        <div class="brand-text">
          <div class="brand-title">CityHaldwani<span>.com</span></div>
          <p>Verified Uttarakhand Classifieds</p>
        </div>
      </a>
      <div class="topbar-actions">
        <span class="badge-verified-top">&#10004; 100% Genuine Profiles</span>
        <a href="/post-ad.html" class="btn-header-ad">📢 Post Ad</a>
        <a href="tel:+919876543210" class="btn-header-call" data-contact="call">Call Support</a>
        <a href="https://api.whatsapp.com/send?phone=919876543210" class="btn-header-wa" data-contact="whatsapp">WhatsApp</a>
      </div>
    </div>
  </header>

  <main class="container">
    <nav class="breadcrumb-nav" aria-label="Breadcrumb">
      <a href="../index.html">Home</a> &gt; <a href="../index.html#locations">Uttarakhand</a> &gt; <span>{city_name} Escorts</span>
    </nav>

    <div class="location-pills-bar">
      <div class="location-pills-title">Browse Uttarakhand Destination Hubs:</div>
      <div class="location-pills-grid">
{pills_html}
      </div>
    </div>

    <section class="hero-editorial">
      <h1>{h1_title}</h1>
      <div class="hero-meta-badges">
        <span class="hero-badge">🏔️ {tagline}</span>
        <span class="hero-badge">⭐ 100% Real Photographs</span>
        <span class="hero-badge">🛡️ Strict Zero Advance Rule</span>
        <span class="hero-badge">🛎️ In-Room &amp; Resort Outcall</span>
      </div>
      <p>
        Welcome to <strong>CityHaldwani.com</strong>, your verified destination for <strong>{city_name} call girls</strong> and premier <strong>{city_name} escort service in {seo_landmark}</strong>. Renowned for its {vibe}, {city_name} attracts holidaymakers, executives, and regional visitors seeking unhurried, discreet luxury. Whether staying at a luxury resort along {landmarks} or relaxing in an executive suite near {seo_hotel}, our vetted independent companions deliver genuine warmth, high-class elegance, and confidential charm.
      </p>
      <p>
        At CityHaldwani.com, we prioritize transparency and safety above all else. Every companion listed below has completed strict photo authentication and age verification checks (18+). You connect directly with the independent advertiser over phone or WhatsApp, eliminating brokerage fees and predatory third-party intermediaries. Review authentic profile details, compare flexible packages, and enjoy confidential companionship backed by our ironclad zero upfront payment policy.
      </p>
    </section>

    <section class="listings-section" id="verified-listings">
      <div class="listings-heading-bar">
        <h2>🔥 16 Active Verified Call Girls &amp; Escort Service in {city_name}</h2>
        <span class="listings-count-badge">16 Profiles Active Now</span>
      </div>
      <div class="listings-grid">
{all_cards_str}
      </div>
    </section>

    <section class="editorial-card">
      <h2>Comprehensive Guide to Hiring Independent Companions in {city_name}</h2>
      <p>
        Planning a mountain holiday, business retreat, or weekend escape to {city_name} is made memorable with verified companionship. Independent models offer personalized companionship tailored to your schedule, from scenic daytime drives to private fireside hotel dinners with warmth and discretion.
      </p>

      <h2>Elite Companion Categories in {city_name}</h2>
      <div class="categories-grid">
        <div class="category-box">
          <h3>🎓 Independent College Girls</h3>
          <p>Fresh, educated students (18+) in {city_name}. Energetic, talkative, and perfect for casual outings, sightseeing, and lively cafe dates.</p>
        </div>
        <div class="category-box">
          <h3>👑 VIP Fashion Models</h3>
          <p>Glamorous, tall models suitable for high-profile business dinners, luxury suite stays, and prestigious social events across Uttarakhand.</p>
        </div>
        <div class="category-box">
          <h3>💖 Sensual Mature Companions</h3>
          <p>Attentive homemakers and independent women excelling at passionate, relaxing companionship with zero drama and complete understanding.</p>
        </div>
        <div class="category-box">
          <h3>🌿 Luxury Resort Escorts</h3>
          <p>Versatile companions accustomed to high-end hospitality, wilderness safaris, and overnight tours across {landmarks}.</p>
        </div>
      </div>
    </section>

    <!-- NEW SECTION: Detailed Local Neighborhood & Sector Coverage Guide (~150 words of rich local SEO content) -->
    <section class="editorial-card">
      <h2>📍 Local Neighborhood &amp; Call Girls Coverage in {city_name}</h2>
      <p>
        Our verified independent escort network spans every prominent commercial zone, residential colony, and transit artery in and around {city_name}. Specifically, active outcall coverage is provided across <strong>{local_guide['sectors']}</strong>.
      </p>
      <p>
        {local_guide['sectors_detail']}
      </p>
      <p>
        Whether you require a prompt appointment at your central hotel within 25 to 35 minutes or wish to schedule an evening date at a private farmhouse or mountain homestay, our independent advertisers guarantee timely arrival. We recommend contacting your chosen companion at least 45 minutes prior to your preferred meeting time so she can travel comfortably and arrive fresh, relaxed, and ready to provide an exceptional hospitality experience.
      </p>
    </section>

    <!-- NEW SECTION: 5-Star Hotel Hospitality & Concierge Etiquette (~150 words of local hotel guide) -->
    <section class="editorial-card">
      <h2>🛎️ Elite Hospitality, Hotel Concierge Etiquette &amp; 5-Star Outcall in {city_name}</h2>
      <p>
        For a completely stress-free and confidential appointment in {city_name}, we strongly recommend booking a certified 4-star or 5-star hotel or a verified luxury boutique resort. Recommended establishments include <strong>{hotels}</strong>, known throughout Kumaon for their spacious suites, soundproof rooms, private parking, and professional front-desk hospitality.
      </p>
      <p>
        {local_guide['hospitality']}
      </p>
      <p>
        When welcoming an independent companion to your hotel room, simple courtesy ensures a delightful time for both parties. Call the front desk to notify them of an incoming visitor or meet your companion in the hotel lobby lounge for a brief introductory greeting. Independent companions take pride in their hygiene, grooming, and discrete etiquette, arriving in fashionable attire suitable for any 5-star property.
      </p>

      <h2>Client Safety Protocol &amp; Zero Advance Rule</h2>
      <ul>
        <li><strong>Never Pay Advance Money:</strong> Independent companions in {city_name} never ask for UPI transfers or booking deposits in advance. Pay in direct cash after meeting in person at your hotel room.</li>
        <li><strong>Verify Identity on Arrival:</strong> Confirm your companion matches her photographs before commencing your private appointment. If photos differ, you are free to cancel at the door.</li>
        <li><strong>Maintain Mutual Respect:</strong> Treat companions with courtesy, maintain good personal hygiene, and honor agreed personal boundaries and scheduled hours.</li>
        <li><strong>Preserve Discretion:</strong> Refrain from taking unauthorized photos or recording private moments. Total mutual privacy is guaranteed on CityHaldwani.com.</li>
      </ul>
    </section>

    <!-- NEW SECTION: Seasonal Travel, Sightseeing Drives & Romantic Rendezvous (~120 words of local travel tips) -->
    <section class="editorial-card">
      <h2>🌄 Best Seasons, Scenic Mountain Drives &amp; Romantic Rendezvous in {city_name}</h2>
      <p>
        {city_name} offers distinct seasonal charms throughout the year, from refreshing summer escapes to crisp winter evenings beside crackling deodar fireplaces. {local_guide['itineraries']}
      </p>
      <p>
        Pairing your regional exploration with a charming local companion transforms an ordinary trip into an extraordinary holiday. Independent escorts know the finest viewpoint cafes, scenic valley routes along {landmarks}, and quiet dining spots where you can enjoy each other’s company without intrusion. Discuss your preferred itinerary directly when calling your companion to create a bespoke holiday experience.
      </p>
    </section>

    <!-- POPULAR SEARCHES TAG CLOUD SECTION (Requested for all location pages) -->
    <section class="popular-searches-section" id="popular-searches">
      <div class="popular-searches-container">
        <h2 class="popular-searches-title">🔍 Popular Searches for {city_name} Call Girls &amp; Escort Service</h2>
        <p class="popular-searches-subtitle">Most searched local keywords, verified escort directories, and 5-star hotel call girls in {city_name}:</p>
        <div class="popular-tags-grid">
{popular_tags_html}
        </div>
      </div>
    </section>

    <section class="faq-section" id="faq-section">
      <h2>Frequently Asked Questions About {city_name} Call Girls &amp; Escort Service</h2>
      <p class="faq-intro">Find clear, authoritative answers to the top 20 most searchable questions regarding escort bookings, rates, hotel visits, and safety in {city_name}.</p>
      <div class="faq-list">
{all_faqs_str}
      </div>
    </section>
  </main>

  <footer class="site-footer">
    <div class="container footer-grid">
      <div class="footer-col">
        {DMCA_BADGE_HTML}
        <h4>CityHaldwani.com</h4>
        <p>
          Premier light-theme verified classified portal for Uttarakhand companions and tourists. Strict 18+ compliance, zero advance fee guarantee, and total client privacy.
        </p>
        <p style="font-size: 12px; color: var(--text-muted); margin-bottom: 8px;">
          Serving {city_name}, Haldwani, Nainital, Bhimtal, Ramnagar, Jim Corbett, Rudrapur, and all 15 major Uttarakhand hubs.
        </p>
        <span class="footer-badge-pill">🛡️ 100% Verified Classifieds • 18+ Adult Directory</span>
      </div>
      <div class="footer-col">
        <h4>Top Uttarakhand Hubs</h4>
        <ul class="footer-links">
          <li><a href="haldwani.html">Haldwani Escorts</a></li>
          <li><a href="nainital.html">Nainital Escorts</a></li>
          <li><a href="bhimtal.html">Bhimtal Escorts</a></li>
          <li><a href="ramnagar.html">Ramnagar Escorts</a></li>
          <li><a href="jim-corbett.html">Jim Corbett Escorts</a></li>
          <li><a href="rudrapur.html">Rudrapur Escorts</a></li>
          <li><a href="almora.html">Almora Escorts</a></li>
          <li><a href="bhowali.html">Bhowali Escorts</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h4>Corporate &amp; Safety</h4>
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
    <a href="https://api.whatsapp.com/send?phone=919876543210&amp;text={loc_wa_encoded}" target="_blank" rel="noopener noreferrer" class="ch-float-btn ch-float-wa" id="ch-float-wa-btn" title="Chat on WhatsApp" aria-label="Chat on WhatsApp" data-contact="whatsapp">
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
    return html_content, names_used
