import os
import re
import json
import urllib.parse

from build_pages import NAMES_POOL, LOCATIONS_CONFIG
from location_local_data import LOCATION_LOCAL_DATA
from location_bespoke_content import BESPOKE_LOCATION_DATA

# Load CSS content to embed directly in all generated pages
CSS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'css', 'style.css')
with open(CSS_FILE, 'r', encoding='utf-8') as f:
    EMBEDDED_CSS = f.read()

STATIC_ADULT_WARNING_HTML = '''      <div class="static-adult-warning" role="alert" aria-label="18+ Adult Content Warning">
        <div class="warning-line">
          <span class="warning-badge-18">🔞 18+ STRICT ADULT WARNING:</span>
          <span>This portal contains age-restricted 18+ adult classifieds intended solely for consenting adults (18+).</span>
        </div>
        <div class="warning-line">
          <span class="warning-badge-alert">⚠️ AGE VERIFICATION REQUIRED:</span>
          <span>Under penalty of law you confirm you are 18+ &bull; Strict Zero Advance Policy &bull; Cash On Direct Meeting Only.</span>
        </div>
      </div>'''

DMCA_BADGE_HTML = '''<div class="dmca-badge-wrap">
          <a href="//www.dmca.com/Protection/Status.aspx?ID=ba77071e-739a-4ae4-a1e0-e8e954c427e2" title="DMCA.com Protection Status" class="dmca-badge"><img src="https://images.dmca.com/Badges/dmca_protected_sml_120m.png?ID=ba77071e-739a-4ae4-a1e0-e8e954c427e2" alt="DMCA.com Protection Status" /></a>
          <script src="https://images.dmca.com/Badges/DMCABadgeHelper.min.js"></script>
        </div>'''

def build_mobile_drawer_html(rel_prefix='../', dest_prefix=''):
    return f'''  <!-- Mobile Navigation Drawer Overlay & Panel -->
  <div class="mobile-nav-overlay" id="mobileNavOverlay" aria-hidden="true"></div>
  <aside class="mobile-nav-drawer" id="mobileNavDrawer" aria-label="Mobile Navigation" aria-hidden="true" inert>
    <div class="drawer-header">
      <div class="drawer-brand">
        <div class="drawer-title">CityHaldwani<span>.com</span></div>
        <div class="drawer-subtitle">18+ Uttarakhand Directory</div>
      </div>
      <button class="drawer-close-btn" id="drawerCloseBtn" aria-label="Close Navigation Menu">&times;</button>
    </div>

    <div class="drawer-body">
      <!-- Quick Contact Actions -->
      <div class="drawer-cta-group">
        <a href="{rel_prefix}post-ad.html" class="drawer-btn-ad">📢 Post Your Free Ad</a>
        <div class="drawer-cta-row">
          <a href="tel:+919876543210" class="drawer-btn-call" data-contact="call">📞 Call Support</a>
          <a href="https://api.whatsapp.com/send?phone=919876543210" class="drawer-btn-wa" data-contact="whatsapp">💬 WhatsApp</a>
        </div>
      </div>

      <!-- Main Navigation -->
      <nav class="drawer-nav-section">
        <div class="drawer-section-title">Navigation</div>
        <ul class="drawer-nav-list">
          <li><a href="{rel_prefix}index.html">🏠 Home Portal</a></li>
          <li><a href="{rel_prefix}post-ad.html">📢 Post Advertisement</a></li>
          <li><a href="{rel_prefix}safety-guide.html">🛡️ Safety &amp; Anti-Scam Guide</a></li>
          <li><a href="{rel_prefix}about-us.html">ℹ️ About CityHaldwani.com</a></li>
          <li><a href="{rel_prefix}contact-us.html">✉️ Contact Support Desk</a></li>
        </ul>
      </nav>

      <!-- 15 Uttarakhand Destinations -->
      <div class="drawer-nav-section">
        <div class="drawer-section-title">📍 Explore 15 Destination Hubs</div>
        <div class="drawer-dest-grid">
          <a href="{dest_prefix}nainital.html">📍 Nainital</a>
          <a href="{dest_prefix}bhimtal.html">📍 Bhimtal</a>
          <a href="{dest_prefix}almora.html">📍 Almora</a>
          <a href="{dest_prefix}ramnagar.html">📍 Ramnagar</a>
          <a href="{dest_prefix}haldwani.html">📍 Haldwani</a>
          <a href="{dest_prefix}kaladhungi.html">📍 Kaladhungi</a>
          <a href="{dest_prefix}rudrapur.html">📍 Rudrapur</a>
          <a href="{dest_prefix}kathgodam.html">📍 Kathgodam</a>
          <a href="{dest_prefix}kashipur.html">📍 Kashipur</a>
          <a href="{dest_prefix}bajpur.html">📍 Bajpur</a>
          <a href="{dest_prefix}khatima.html">📍 Khatima</a>
          <a href="{dest_prefix}sitarganj.html">📍 Sitarganj</a>
          <a href="{dest_prefix}kichha.html">📍 Kichha</a>
          <a href="{dest_prefix}jim-corbett.html">📍 Jim Corbett</a>
          <a href="{dest_prefix}bhowali.html">📍 Bhowali</a>
        </div>
      </div>

      <!-- Legal & Discretion -->
      <nav class="drawer-nav-section">
        <div class="drawer-section-title">Legal, Safety &amp; Discretion</div>
        <ul class="drawer-nav-list small">
          <li><a href="{rel_prefix}terms.html">⚖️ Terms of Service</a></li>
          <li><a href="{rel_prefix}privacy.html">🔒 Privacy Policy</a></li>
          <li><a href="{rel_prefix}report-abuse.html">🚨 Report Abuse &amp; Misconduct</a></li>
        </ul>
      </nav>

      <!-- 18+ Warning Notice -->
      <div class="drawer-adult-notice">
        🔞 <strong>Strict 18+ Adult Portal:</strong> Strictly consenting adults (18+). Zero Advance Payment Policy &bull; Cash On Direct Meeting Only.
      </div>
    </div>
  </aside>'''

MOBILE_DRAWER_SCRIPT = '''  <!-- Mobile Navigation Drawer Toggle Script -->
  <script>
    (function() {
      var toggleBtn = document.getElementById('mobileMenuToggle');
      var drawer = document.getElementById('mobileNavDrawer');
      var overlay = document.getElementById('mobileNavOverlay');
      var closeBtn = document.getElementById('drawerCloseBtn');

      if (!toggleBtn || !drawer || !overlay) return;

      function openDrawer() {
        drawer.removeAttribute('inert');
        drawer.classList.add('active');
        overlay.classList.add('active');
        toggleBtn.setAttribute('aria-expanded', 'true');
        drawer.setAttribute('aria-hidden', 'false');
        overlay.setAttribute('aria-hidden', 'false');
        document.body.style.overflow = 'hidden';
        if (closeBtn) {
          closeBtn.focus();
        }
      }

      function closeDrawer() {
        if (drawer.contains(document.activeElement)) {
          document.activeElement.blur();
        }
        if (toggleBtn) {
          toggleBtn.focus();
        }
        drawer.classList.remove('active');
        overlay.classList.remove('active');
        toggleBtn.setAttribute('aria-expanded', 'false');
        drawer.setAttribute('aria-hidden', 'true');
        overlay.setAttribute('aria-hidden', 'true');
        drawer.setAttribute('inert', '');
        document.body.style.overflow = '';
      }

      toggleBtn.addEventListener('click', function(e) {
        e.stopPropagation();
        if (drawer.classList.contains('active')) {
          closeDrawer();
        } else {
          openDrawer();
        }
      });

      if (closeBtn) {
        closeBtn.addEventListener('click', function(e) {
          e.stopPropagation();
          closeDrawer();
        });
      }

      overlay.addEventListener('click', closeDrawer);

      document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && drawer.classList.contains('active')) {
          closeDrawer();
        }
      });
    })();
  </script>'''

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
        'sectors_detail': 'Whether your hotel is situated overlooking the tranquil waters of Naini Lake in Mallital, nestled among heritage deodars along the tranquil slopes of Ayarpatta, or perched near the scenic viewpoints of Snow View and Pangot, our independent escorts in Nainital offer prompt outcall coverage across all hill station zones. Dedicated outcall service is also extended to residential estates such as Raj Bhavan area escorts zones and secluded retreats near Sherwani area escorts. Most companions reach Mall Road and Tallital hotels within 30 to 40 minutes, while secluded villas in Pangot or Kilbury typically require approximately 50 minutes of advance coordination.',
        'hospitality': 'Nainital hosts some of Kumaon’s most prestigious heritage and boutique 5-star properties, including Manu Maharani hotel call girls retreats, Shervani Hilltop escorts destinations, Vikram Vintage Inn, The Naini Retreat, and Swiss Hotel. When reserving outcall companionship at these premier establishments, luxury suites and lake-facing private balconies provide an ideal atmosphere of comfort and discretion. Independent models arrive dressed in tasteful smart-casual attire, blending naturally with other upscale vacationers and hotel guests.',
        'itineraries': 'During warm summer months, romantic late-afternoon excursions to lookouts like Tiffin Top call girls viewpoints followed by a cozy candlelit dinner at a boutique lakeside cafe creates an unforgettable experience. In the brisk winter season, when snow dusts the surrounding peaks, sharing warm fireside cocktails in the comfort of your private heated suite with an affectionate companion offers the ultimate mountain retreat.'
    },
    'bhimtal': {
        'sectors': 'Bhimtal Island Lake Promenade, Victoria Dam Road, Hidimba Parvat Foothills, Nal Damyanti Tal Lane, Mehragaon Valley, Sattal Junction Corridor, and Bhowali-Bhimtal Highway',
        'sectors_detail': 'Bhimtal is celebrated for its uncrowded, serene waters and private nature resorts. Our verified independent companions provide discreet outcall across all key sectors, from waterside luxury cottages bordering Victoria Dam to secluded hillside retreats near Mehragaon and the lush pine trails of Sattal road. Travel time to central Bhimtal resorts averages 25 to 35 minutes, ensuring prompt arrivals for dinner dates or overnight stays.',
        'hospitality': 'Prominent luxury destinations such as The Fern Hillside Resort, Country Inn Bhimtal, Aamod Resorts, Fishermens Lodge, and V Resort cater to privacy-conscious holidaymakers. These properties feature expansive private lawns and lake-view verandas that ensure complete anonymity. Independent models uphold strict professional standards, arriving with zero pretense and honoring your private boundaries under our strict zero-advance cash payment guarantee.',
        'itineraries': 'Bhimtal is an idyllic setting for unhurried conversations and scenic nature strolls. Spend quiet mornings admiring migratory birds over the island lake, take a leisurely drive through the pine woods of Sattal, and return to your resort for a private candlelit evening under star-filled Himalayan skies.'
    },
    'almora': {
        'sectors': 'Kasar Devi Magnetic Ridge, Bright End Corner, Historic Lal Bazaar, Dharanaula Junction, Binsar Wildlife Sanctuary Approach Road, Ranikhet Highway Corridor, and Matena Valley',
        'sectors_detail': 'Almora represents the cultural heartland of Kumaon, perched atop a scenic horse-saddle ridge. Independent companions provide dependable outcall across Kasar Devi’s bohemian ridge, Bright End Corner’s sunset viewpoints, and along the scenic Ranikhet road call girls corridor. As part of our comprehensive Kumaon escort service, in-town visits to central Almora take between 30 and 40 minutes, while wilderness resorts along the Binsar forest corridor may require up to 55 minutes for safe mountain transit.',
        'hospitality': 'Prestigious heritage properties including Kalmatia Sangam, Grand Oak Manor, Deodar Sanctuary, Imperial Heights Binsar, and Kasaar Jungle Resort provide an unmatched backdrop of pine-wood elegance. Guests enjoy stone-carved fireplaces, panoramic Himalayan vistas of Nanda Devi, and attentive concierge service that ensures confidential guest visits without awkward scrutiny.',
        'itineraries': 'Almora is renowned for its inspiring sunsets and peaceful quietude. Pair your stay with an educated companion who appreciates culture, mountain tranquility, and engaging conversations. Sip fresh rhododendron tea during a brisk autumn afternoon, and spend unhurried evenings relaxing before a crackling deodar log fire.'
    },
    'ramnagar': {
        'sectors': 'Kosi River Barrage Corridor, Dhangarhi Tourist Gate, Ringora Wilderness Belt, Garjiya Devi Highway, Ramnagar Main Town, and Corbett National Park Periphery',
        'sectors_detail': 'As the primary entry gateway to the legendary Jim Corbett tiger reserve, Ramnagar buzzes with wildlife enthusiasts and luxury holidaymakers. Verified independent call girls in Ramnagar cater to private safari resorts along the Kosi River, secluded forest estates near Ringora, and comfortable business transit suites in Ramnagar town. Outcall transit to resorts along the Ramnagar-Ranikhet highway is exceptionally smooth, typically requiring 25 to 35 minutes.',
        'hospitality': 'Leading jungle venues like Namah Resort, The Den Corbett escorts retreats, Aahana resort call girls destinations, Riverview retreat escorts venues, and Lemon Tree Premier Corbett offer 5-star wilderness hospitality. These sprawling resorts feature private riverside decks, individual cottage compounds, and secure gated entry. Independent models arrive discreetly in smart travel attire, respecting guest privacy at all times.',
        'itineraries': 'After an exhilarating morning jeep safari tracking royal Bengal tigers, guests frequently arrange verified Corbett safari call girls to share relaxing riverside cocktails and in-room relaxation. Savor fresh river fish delicacies at a private barbecue dinner accompanied by a charming, articulate companion who enhances every moment of your wilderness vacation.'
    },
    'haldwani': {
        'sectors': 'Nainital Road, Tikonia Commercial Hub, Kaladhungi Road, Kusumkhera, Mukhani Crossing, Canal Road, Kathgodam Bypass, Bareilly Road, Rampur Road, Heera Nagar, and Subhash Nagar',
        'sectors_detail': 'As the largest commercial metropolis and economic engine of Kumaon, Haldwani features a fast-paced urban lifestyle with modern amenities. Active outcall coverage extends across all central residential and commercial neighborhoods including Subhash Nagar call girls zones, Awas Vikas Haldwani escorts colonies, Bhotia Parao call girls hubs, and accommodations near MBPG College area escorts. Companions typically arrive at your hotel suite within 20 to 30 minutes, offering the fastest outcall response times in the region.',
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
        'hospitality': 'Ultra-luxury resort properties including Taj Corbett Resort & Spa, The Solluna Resort, Paatlidun Safari Lodge, Namah Resort, and premier Corbett hotel call girls venues offer world-class hospitality. For travelers staying at wilderness lodges, our safari resort escort service provides poise, sophistication, and complete privacy.',
        'itineraries': 'Pair an exhilarating daytime wildlife safari with a magical candlelit dinner beside the Kosi River. Savor vintage wine under the stars, listen to the nocturnal sounds of the jungle, and enjoy passionate, uninhibited companionship in the secluded luxury of your private pool villa.'
    },
    'bhowali': {
        'sectors': 'Bhowali Sanatorium Ridge, Kainchi Dham Junction Highway, Ramgarh Fruit Orchard Road, Golu Devta Temple Corridor, Pine Crest Valley, and Shyamkhet Tea Gardens',
        'sectors_detail': 'Perched at a refreshing altitude of 1,700 meters, Bhowali is famous for its crisp pine-scented air, lush fruit orchards, and proximity to the sacred Kainchi Dham ashram. Independent companions cater to heritage cottages near the Sanatorium ridge, boutique hillside resorts along Ramgarh road, and private mountain homestays near the Shyamkhet tea estate. Outcall transit averages 30 to 40 minutes from central Bhowali junctions.',
        'hospitality': 'Charming mountain properties including The White Peaks Bhowali, Aqua De Vida Resort, Pine Crest Hotel, Soulitude in the Himalayas, and Cedar Cottage provide cozy fireplaces, panoramic valley views, and exceptional privacy. Independent companions arrive discreetly, ensuring your mountain holiday remains peaceful and confidential.',
        'itineraries': 'Bhowali is the ultimate romantic hideaway. Spend peaceful mornings driving through misty pine forests and visiting local tea plantations. As evening temperatures drop, share a warm bottle of wine beside a crackling stone fireplace, wrapped in warm blankets with a sweet, affectionate companion.'
    }
}

PROFILE_SENTENCE_PATTERNS = [
    ("Book Verified {kw} for Luxury Hotel Outcall",
     "Book verified {kw} for luxury hotel outcall with verified independent model {name} (age {age}) for quiet relaxation and dinner dates. Fluent in English and Hindi, she is admired for her punctuality, warm conversational charm, and attentive demeanor. Operates under our strict zero-advance policy with direct cash payment upon arrival at your room."),
    
    ("Experience Elite {kw} with Complete In-Room Privacy",
     "Experience elite {kw} with complete in-room privacy by meeting {name} (age {age}), an articulate and educated companion in the city. Whether you are staying at a secluded hillside retreat or a central boutique resort, she delivers relaxed, unhurried companionship tailored to your schedule. Enjoys meaningful conversations and quiet dining with 100% genuine verified photos."),
    
    ("Connect with Independent {kw} for Evening Dinner Dates",
     "Connect with independent {kw} for evening dinner dates by choosing high-profile companion {name} (age {age}) for private meetings. Elegant, stylish, and discreet, she is an ideal partner for corporate dinners, prestigious social banquets, or intimate suite encounters. Zero advance payment required; settle safely upon arrival at your room with complete peace of mind."),
    
    ("Reserve Top-Rated {kw} with Cash on Arrival Guarantee",
     "Reserve top-rated {kw} with cash on arrival guarantee when accompanied by charming independent model {name} (age {age}) in local resorts. She offers relaxed private meetings, polite conversation, and memorable holiday companionship across local destination resorts. Committed to strict client confidentiality, mutual respect, and transparent in-person booking with zero advance deposits."),
    
    ("Enjoy Discreet {kw} Tailored for Touring Executives",
     "Enjoy discreet {kw} tailored for touring executives and vacationers with verified model {name} (age {age}) during your stay. Known for her pleasant etiquette, sophisticated style, and punctual arrivals, she provides delightful companionship during your stay. Settle your booking securely with cash directly in your hotel room without upfront tokens or deposits."),
    
    ("Meet Charming {kw} for Unhurried Mountain Holiday Stays",
     "Meet charming {kw} for unhurried mountain holiday stays and scenic drives by booking sophisticated companion {name} (age {age}) today. She excels at relaxed conversation, romantic dinners, and stress-relieving companionship. Backed by verified authentication photos and our strict zero advance payment guarantee for complete peace of mind during your visit."),
    
    ("Find Trusted {kw} Available for Prompt In-Room Visits",
     "Find trusted {kw} available for prompt in-room visits across local luxury hotels with articulate model {name} (age {age}) anytime. She brings warmth, elegance, and cheerful conversation to any meeting, ensuring a memorable and confidential experience. Pay in direct cash upon arrival with zero hidden agency commissions or brokerage fees."),
    
    ("Schedule Private {kw} with 100% Photo Verified Profiles",
     "Schedule private {kw} with 100% photo verified profiles through polite and attractive companion {name} (age {age}) for total relaxation. Whether you require a companion for a business dinner or a quiet evening in your suite, she ensures total discretion and mutual respect. Enjoy verified authenticity with safe cash payment upon direct meeting.")
]

# Helper to clean duplicate words when keyword starts with the adjective in the sentence template
def clean_sentence_formatting(template_str, kw):
    res = template_str
    words = kw.strip().split()
    if words:
        first_word = words[0]
        pattern = rf'\b({re.escape(first_word)})\s+\{{kw\}}'
        res = re.sub(pattern, '{kw}', template_str, flags=re.IGNORECASE)
    return res

# Build a single profile card calibrated with full sentence title + keyword + expanded ~54-word description
def render_profile_card(name, city_name, age, index, img_alias, rel_prefix='../', profile_title=None, dedicated_tag=None):
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
    
    kw = (dedicated_tag if dedicated_tag else (profile_title if profile_title else f"{city_name} Call Girls")).title()
    title_pattern, desc_pattern = PROFILE_SENTENCE_PATTERNS[index % len(PROFILE_SENTENCE_PATTERNS)]
    
    fmt_title = clean_sentence_formatting(title_pattern, kw)
    fmt_desc = clean_sentence_formatting(desc_pattern, kw)
    
    full_sentence_title = fmt_title.format(kw=kw)
    desc = fmt_desc.format(name=name, age=age, kw=kw)
    photo_count = 3 + (index % 3)
    
    card_html = f'''
        <article class="profile-card" id="profile-{name.lower()}">
          <div class="card-media">
            <span class="vip-ribbon">VIP</span>
            <img src="{rel_prefix}public/{img_alias}" alt="{name} - {full_sentence_title} in {city_name}" loading="lazy" decoding="async" width="185" height="245" onerror="if(!this.dataset.retried){{this.dataset.retried=1;this.src='{rel_prefix}{img_alias}';}}">
            <span class="photo-count-pill">📷 {photo_count} Photos</span>
          </div>
          <div class="card-content">
            <div class="card-header-line">
              <span class="badge-vip-pill">VERIFIED VIP</span>
              <h3 class="profile-name-title">{full_sentence_title}</h3>
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

# Generate 20 concise, searchable FAQs calibrated to ~20-25 words each with natural keyword inclusion
def generate_20_faqs(city_name, hotels, landmarks, pop_tags=None):
    if not pop_tags:
        pop_tags = []
        
    def get_all_tags(kw):
        return [t for t in pop_tags if kw in t.lower()]
        
    near_me_tags = get_all_tags('near me')
    h24_tags = get_all_tags('24 hour')
    full_night_tags = get_all_tags('full night')
    short_time_tags = get_all_tags('short time')
    cash_tags = get_all_tags('cash on')
    verified_tags = [t for t in pop_tags if any(k in t.lower() for k in ['verified', 'genuine', 'safe escort'])]
    hotel_svc_tags = [t for t in pop_tags if any(k in t.lower() for k in ['hotel service', 'hotel outcall'])]

    # Intent Q&A customization
    if verified_tags:
        v_main = verified_tags[0]
        v_sub = verified_tags[1] if len(verified_tags) > 1 else v_main
        q_ver = f"How does CityHaldwani.com guarantee {v_main}?"
        a_ver = f"All independent advertisers for {v_sub} submit date-stamped verification photos confirming identity and legal adult age (18+) before approval. Misleading stock photos are strictly banned."
    else:
        q_ver = f"Are companion profile photos in {city_name} genuine?"
        a_ver = f"Yes, all independent advertisers in {city_name} submit date-verified authentication selfies before publication. We strictly forbid misleading stock photos."

    if cash_tags:
        c_tag = cash_tags[0]
        q_cash = f"Is {c_tag} strictly guaranteed?"
        a_cash = f"Yes, {c_tag} is our ironclad policy. CityHaldwani.com enforces a strict Zero Advance Payment rule. Never send online deposits; settle directly in cash upon in-person meeting."
    else:
        q_cash = f"Do escorts in {city_name} require advance payment?"
        a_cash = f"No! CityHaldwani.com enforces a strict Zero Advance Payment rule. Never send online deposits. You pay in direct cash upon meeting in person."

    if hotel_svc_tags:
        h_tag = hotel_svc_tags[0]
        q_hotel = f"Can companions provide {h_tag}?"
        a_hotel = f"Yes, independent companions provide prompt {h_tag} to certified 4-star and 5-star hotels, including {hotels}, with complete in-room discretion."
    else:
        q_hotel = f"Can companions visit my hotel room in {city_name}?"
        a_hotel = f"Yes, companions provide prompt outcall service to verified 4-star and 5-star hotels, including {hotels}, with complete in-room discretion."

    if near_me_tags:
        nm_q = near_me_tags[0]
        nm_a = near_me_tags[1] if len(near_me_tags) > 1 else nm_q
        q_nm = f"How quickly can {nm_q} arrive at my hotel?"
        a_nm = f"When requesting an {nm_a}, companions typically arrive within 30 to 45 minutes across central areas near {landmarks}. Hillside resorts may require 1 hour advance notice."
    else:
        q_nm = f"How quickly does a companion arrive in {city_name}?"
        a_nm = f"Companions typically arrive within 30 to 45 minutes across central areas near {landmarks}. Hillside resorts may require 1 hour advance notice."

    if h24_tags:
        h24_tag = h24_tags[0]
        q_24 = f"Is {h24_tag} available daily?"
        a_24 = f"Yes, {h24_tag} operates 24 hours a day, 7 days a week for daytime meetings, dinner dates, and late-night hotel visits."
    else:
        q_24 = f"Is 24-hour escort service available in {city_name}?"
        a_24 = f"Yes, verified companions are available round the clock for daytime dates, evening dinner accompaniment, and late-night hotel visits."

    if full_night_tags:
        fn_tag = full_night_tags[0]
        q_fn = f"Can I book {fn_tag} for overnight stays?"
        a_fn = f"Yes, {fn_tag} is available from 9 PM to 7 AM for unhurried dinners, evening relaxation, and morning companionship."
    else:
        q_fn = f"Can I book full-night escort service in {city_name}?"
        a_fn = f"Yes, full-night bookings (typically 9 PM to 7 AM) are available for unhurried dinners, evening relaxation, and morning companionship."

    if short_time_tags:
        st_tag = short_time_tags[0]
        q_st = f"Are {st_tag} available for flexible visits?"
        a_st = f"Yes, {st_tag} can be reserved for 1-hour or 2-hour sessions with clear, transparent cash rates upon meeting."
    else:
        q_st = f"Can I book an escort for full-day sightseeing in {city_name}?"
        a_st = f"Yes, companions can accompany clients for full-day leisure tours, scenic mountain drives, lake visits, and cafe outings across the region."

    faqs = [
        (
            f"How can I book verified escorts in {city_name}?",
            f"Browse our listings, select a preferred companion, and click Call or WhatsApp. Confirm duration, meeting time, and hotel location directly with the advertiser."
        ),
        (q_ver, a_ver),
        (q_cash, a_cash),
        (q_hotel, a_hotel),
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
        (q_nm, a_nm),
        (q_st, a_st),
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
        (q_fn, a_fn),
        (q_24, a_24),
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
            f"How do I cancel a booking in {city_name}?",
            f"If your travel plans change, notify the companion via WhatsApp at least 1 hour in advance so she can adjust her schedule."
        )
    ]
    return faqs

# Build location HTML page with target word count: ~3,800 - 4,200 words
def build_location_page(loc, start_name_idx):
    slug = loc['slug']
    city_name = loc['name']
    landmarks = loc['landmarks']
    hotels = loc['hotels']
    
    bespoke = BESPOKE_LOCATION_DATA.get(slug, {})
    title = bespoke.get('title', loc['title'])
    meta_desc = bespoke.get('meta_desc', loc['meta_desc'])
    tagline = bespoke.get('tagline', loc['tagline'])
    h1_title = bespoke.get('h1', loc.get('h1', f"{city_name} Call Girls - Verified {city_name} Escort Service"))
    hero_intro = bespoke.get('hero_intro', [
        f"Welcome to CityHaldwani.com, your verified destination for {city_name} call girls.",
        f"Every companion listed below has verified adult legal age and authentic photos."
    ])
    listings_title = bespoke.get('listings_title', f"🔥 16 Active Verified Call Girls & Escort Service in {city_name}")
    custom_sections = bespoke.get('sections', [])
    
    # 16 profiles with ../ relative prefix and unique local search keywords
    loc_local = LOCATION_LOCAL_DATA.get(slug, {})
    pop_tags = loc_local.get('popular_tags', [
        f"{city_name} call girls", f"{city_name} escort service", f"Call girls in {city_name}", f"Escorts in {city_name}",
        f"hotel service call girls {city_name}", f"independent escorts {city_name}", f"cash on arrival {city_name}",
        f"24 hour call girl service {city_name}", f"VIP escorts {city_name}", f"call girls near me {city_name}"
    ])
    prof_keywords = loc_local.get('profile_keywords', [])
    
    cards_html = []
    names_used = []
    for i in range(16):
        name = NAMES_POOL[(start_name_idx + i) % len(NAMES_POOL)]
        names_used.append(name)
        age = 20 + ((start_name_idx + i * 3) % 7)
        img_alias = f"profile_{( (start_name_idx + i) % 48 ) + 1:02d}.webp"
        if i < len(pop_tags):
            card_tag = pop_tags[i]
            prof_kw = card_tag.title()
        elif i < len(prof_keywords):
            card_tag = prof_keywords[i]
            prof_kw = card_tag.title()
        else:
            card_tag = f"{city_name} call girls"
            prof_kw = f"{city_name} Call Girls"
        cards_html.append(render_profile_card(name, city_name, age, i, img_alias, rel_prefix='../', profile_title=prof_kw, dedicated_tag=card_tag))
    
    all_cards_str = "\n".join(cards_html)
    
    # Render bespoke editorial sections
    sections_html = []
    for sec in custom_sections:
        sections_html.append(f'''
    <section class="editorial-card">
      <h2>{sec['title']}</h2>
      {sec['html']}
    </section>''')
    all_sections_str = "\n".join(sections_html)
    
    # 20 FAQs
    faqs = generate_20_faqs(city_name, hotels, landmarks, pop_tags=pop_tags)
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
    tag_accents = ['accent-blue', 'accent-pink', 'accent-green', 'accent-purple', '']
    pop_tags_html_list = []
    for idx, tag in enumerate(pop_tags):
        acc = tag_accents[idx % len(tag_accents)]
        cls = f"popular-tag {acc}".strip()
        pop_tags_html_list.append(f'<a href="#verified-listings" class="{cls}">{tag}</a>')
    popular_tags_html = "\n".join(pop_tags_html_list)

    cat_extra = ""
    if slug == 'nainital':
        cat_extra = '<p style="margin-top: 14px; font-size: 14px; color: var(--text-secondary); line-height: 1.6;">Our verified portal also features elite <strong>Nainital luxury call girls</strong>, sophisticated <strong>Russian escorts in Nainital</strong>, and trusted <strong>Independent escorts Nainital</strong> for executive banquets, private suite encounters, and hillside resort stays.</p>'
    elif slug == 'ramnagar':
        cat_extra = '<p style="margin-top: 14px; font-size: 14px; color: var(--text-secondary); line-height: 1.6;">Discerning executives visiting Ramnagar can also select verified <strong>Luxury call girls Ramnagar</strong> for prestigious social dinners and private pool villa retreats.</p>'
    elif slug == 'almora':
        cat_extra = '<p style="margin-top: 14px; font-size: 14px; color: var(--text-secondary); line-height: 1.6;">Our classifieds include charming independent <strong>Almora college call girls</strong> (18+) for scenic cafe dates and daytime sightseeing excursions.</p>'

    loc_wa_msg = f"Hello CityHaldwani, I want to book a verified companion in {city_name}. Please share available profiles."
    loc_wa_encoded = urllib.parse.quote(loc_wa_msg)
    drawer_html = build_mobile_drawer_html(rel_prefix='../', dest_prefix='')

    html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <meta name="description" content="{meta_desc}">
  <link rel="canonical" href="https://cityhaldwani.com/locations/{slug}.html">
  <link rel="icon" href="../favicon.webp" type="image/webp">
  <link rel="preload" href="../city-logo.png" as="image">

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

  <header class="site-topbar">
    <div class="container topbar-wrapper">
      <a href="../index.html" class="brand-group">
        <img src="../city-logo.png" alt="CityHaldwani.com Logo" class="brand-logo-img" width="140" height="42" onerror="if(!this.dataset.retried){{this.dataset.retried=1;this.src='../logo.png';}}else if(this.dataset.retried==1){{this.dataset.retried=2;this.src='city-logo.png';}}">
        <div class="brand-text">
          <div class="brand-title">CityHaldwani<span>.com</span></div>
          <p>Verified Uttarakhand Classifieds</p>
        </div>
      </a>
      <div class="topbar-actions">
        <span class="badge-verified-top">&#10004; 100% Genuine Profiles</span>
        <a href="../post-ad.html" class="btn-header-ad">📢 Post Ad</a>
        <a href="tel:+919876543210" class="btn-header-call" data-contact="call">Call Support</a>
        <a href="https://api.whatsapp.com/send?phone=919876543210" class="btn-header-wa" data-contact="whatsapp">WhatsApp</a>
        <button class="mobile-menu-toggle" id="mobileMenuToggle" aria-label="Open Navigation Menu" aria-expanded="false" aria-controls="mobileNavDrawer">
          <span class="hamburger-line"></span>
          <span class="hamburger-line"></span>
          <span class="hamburger-line"></span>
        </button>
      </div>
    </div>
  </header>

{drawer_html}

  <main class="container">
    <div class="top-nav-warning-bar">
      <nav class="breadcrumb-nav" aria-label="Breadcrumb">
        <a href="../index.html">Home</a> &gt; <a href="../index.html#locations">Uttarakhand</a> &gt; <span>{city_name} Escorts</span>
      </nav>
{STATIC_ADULT_WARNING_HTML}
    </div>

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
        {hero_intro[0]}
      </p>
      <p>
        {hero_intro[1]}
      </p>
    </section>

    <section class="listings-section" id="verified-listings">
      <div class="listings-heading-bar">
        <h2>{listings_title}</h2>
        <span class="listings-count-badge">16 Profiles Active Now</span>
      </div>
      <div class="listings-grid">
{all_cards_str}
      </div>
    </section>

{all_sections_str}

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
          <li><a href="../about-us.html">About Us</a></li>
          <li><a href="../safety-guide.html">Safety Guidelines</a></li>
          <li><a href="../report-abuse.html">Report Violations</a></li>
          <li><a href="../terms.html">Terms of Service</a></li>
          <li><a href="../privacy.html">Privacy Policy</a></li>
          <li><a href="../contact-us.html">Contact Support Desk</a></li>
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

  <script src="../js/contacts-config.js" defer></script>
  <script src="../js/contact-manager.js" defer></script>
  <script src="../js/security-shield.js" defer></script>
  <script src="../js/age-gate.js" defer></script>
{MOBILE_DRAWER_SCRIPT}
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
