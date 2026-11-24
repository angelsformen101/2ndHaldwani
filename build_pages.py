import os
import re
import json

# Pool of 289 verified unique names with 0 overlap with Angle_forMen and Haldwani
NAMES_POOL = [
    'Priyanshi', 'Kashish', 'Devika', 'Lavanya', 'Urvashi', 'Tanvi', 'Mahi', 'Ira',
    'Ishita', 'Riddhi', 'Sneha', 'Avani', 'Siya', 'Barkha', 'Pallavi', 'Garima',
    'Charu', 'Jhanvi', 'Kirti', 'Mitali', 'Niharika', 'Parul', 'Radhika', 'Saloni',
    'Tarini', 'Vaidehi', 'Yamini', 'Akanksha', 'Bipasha', 'Chetna', 'Damini', 'Ekta',
    'Falguni', 'Gauri', 'Harshita', 'Ishika', 'Jaya', 'Komal', 'Lipika', 'Meenal',
    'Namrata', 'Ojasvi', 'Prachi', 'Rachna', 'Simran', 'Trisha', 'Upasana', 'Vandana',
    'Yashika', 'Zeenat', 'Ananya', 'Bhavna', 'Chhavi', 'Divya', 'Eshita', 'Gayatri',
    'Hema', 'Indu', 'Juhi', 'Karishma', 'Leena', 'Mona', 'Nidhi', 'Payal',
    'Reena', 'Swati', 'Teena', 'Uma', 'Vidya', 'Alisha', 'Bani', 'Chandni',
    'Deepali', 'Geetika', 'Heena', 'Ipsita', 'Jasmine', 'Kanika', 'Lata', 'Madhavi',
    'Neelam', 'Oorja', 'Prerna', 'Rupal', 'Shikha', 'Tripti', 'Urja', 'Varsha',
    'Yukti', 'Zoya', 'Aditi', 'Bhumi', 'Chitrangada', 'Drishti', 'Esha', 'Geeta',
    'Hansika', 'Inaya', 'Jivika', 'Kusum', 'Lipi', 'Manasi', 'Nandini', 'Pratibha',
    'Rashi', 'Shruti', 'Tulsi', 'Urmi', 'Vandita', 'Zaara', 'Amrita', 'Bindu',
    'Chaitali', 'Dolly', 'Ela', 'Gargi', 'Hansa', 'Ishaani', 'Jaspreet', 'Kalyani',
    'Laxmi', 'Mrinal', 'Navya', 'Pari', 'Renu', 'Sanskriti', 'Tanya', 'Unnati',
    'Vasundhara', 'Zara', 'Archana', 'Bela', 'Chhanda', 'Daksha', 'Ekavali', 'Gopika',
    'Hemlata', 'Ishani', 'Janaki', 'Kamini', 'Lochan', 'Madhur', 'Nirupama', 'Pooja',
    'Raveena', 'Sarita', 'Tanushree', 'Urmila', 'Vedika', 'Zalak', 'Anuradha', 'Binita',
    'Champa', 'Deepa', 'Eeshanvi', 'Gitanjali', 'Harini', 'Indrani', 'Jayashree', 'Kalyanika',
    'Lalita', 'Malini', 'Nandita', 'Pournami', 'Ritika', 'Sharmila', 'Tejaswini', 'Urmil',
    'Veenapani', 'Ashwini', 'Bulbul', 'Chirag', 'Devashree', 'Elina', 'Gopali',
    'Harshada', 'Indrakshi', 'Jheel', 'Kavita', 'Lavali', 'Manju', 'Nivedita', 'Preeti',
    'Ragini', 'Shalini', 'Trilochana', 'Urvasi', 'Vatsala', 'Apsara', 'Bimla', 'Chakor',
    'Devina', 'Ekantika', 'Gunjan', 'Himani', 'Inu', 'Jugnu', 'Kripa', 'Laveena',
    'Mohini', 'Nupur', 'Poonam', 'Roshni', 'Sheetal', 'Tripta', 'Vijaya',
    'Aradhya', 'Bratati', 'Chitralekha', 'Devyani', 'Eesha', 'Gunjita', 'Hita', 'Ila',
    'Jyotsna', 'Kshama', 'Lavina', 'Monika', 'Nutan', 'Purnima', 'Ruby', 'Shobha',
    'Seema', 'Suman', 'Tara', 'Usha', 'Vimla', 'Wamiqa', 'Yashasvi', 'Zarine', 'Amba',
    'Bakul', 'Chandrika', 'Damayanti', 'Eila', 'Gargie', 'Haimi', 'Inika', 'Mandira',
    'Nayantara', 'Padma', 'Rajni', 'Sujata', 'Tanu', 'Ujjwala', 'Veda', 'Yamuna',
    'Arundhati', 'Bhavika', 'Charvi', 'Dayita', 'Eeshita', 'Fulki', 'Girija', 'Hridya',
    'Ishana', 'Jaimini', 'Lalima', 'Manjari', 'Netra', 'Pankhuri', 'Rohini', 'Samiksha',
    'Tanirika', 'Vaani', 'Yashila', 'Anupama', 'Bhadra', 'Chinmayi', 'Darshana', 'Enakshi',
    'Gaurangi', 'Harinakshi', 'Indulekha', 'Jayanti', 'Kamakshi', 'Suhani', 'Meghna'
]

LOCATIONS_CONFIG = [
    {
        'slug': 'nainital',
        'name': 'Nainital',
        'title': 'Call Girls Nainital - Verified Resort Escorts in Naini Lake',
        'meta_desc': 'Connect with independent call girls in Nainital for luxury resort outcall along Mall Road & Ayarpatta. Real photos, zero advance fee & cash on arrival.',
        'tagline': 'Queen of Lakes & High-Altitude Leisure Retreats',
        'landmarks': 'Mall Road, Naini Lake, Snow View Point, Tallital, Sukhatal, Pangot',
        'hotels': 'The Manu Maharani, Shervani Hilltop, Vikram Vintage Inn, The Naini Retreat, Swiss Hotel',
        'vibe': 'scenic lakeside promenades, luxury pine view villas, romantic boating dates, and mountain hideaways'
    },
    {
        'slug': 'bhimtal',
        'name': 'Bhimtal',
        'title': 'Bhimtal Escort Service - Lakefront Escorts & Private Outcall',
        'meta_desc': 'Discover verified Bhimtal escort service for peaceful lakefront visits and luxury villa outcall near Victoria Dam. 100% genuine independent companions.',
        'tagline': 'Serene Waterfront Living & Unhurried Countryside Privacy',
        'landmarks': 'Bhimtal Island Lake, Victoria Dam, Hidimba Parvat, Nal Damyanti Tal, Sattal Junction',
        'hotels': 'The Fern Hillside Resort, Country Inn Bhimtal, Aamod Resorts, Fishermens Lodge, V Resort',
        'vibe': 'peaceful waterside serenity, secluded pine forest cottages, private bonfire evenings, and relaxing weekend vacations'
    },
    {
        'slug': 'almora',
        'name': 'Almora',
        'title': 'Almora Call Girls - Verified Mountain Escorts in Kasar Devi',
        'meta_desc': 'Meet verified Almora call girls for quiet mountain holiday outcall along Kasar Devi ridge and Binsar forest retreats. Real photos, discreet cash booking.',
        'tagline': 'Himalayan Saddleback Ridge & Bohemian Mountain Quietude',
        'landmarks': 'Bright End Corner, Kasar Devi, Lal Bazaar, Deer Park, Binsar Wildlife Sanctuary',
        'hotels': 'Kalmatia Sangam, Grand Oak Manor, Deodar Sanctuary, Imperial Heights Binsar, Kasaar Jungle Resort',
        'vibe': 'soothing ridge-line sunsets, deep pine fragrance, artistic conversations, and unhurried intellectual companionship'
    },
    {
        'slug': 'ramnagar',
        'name': 'Ramnagar',
        'title': 'Escort Service Ramnagar - Jungle Resort Companions & Escorts',
        'meta_desc': 'Explore premier escort service Ramnagar for private luxury lodges and riverfront pool villa outcall near Jim Corbett. Verified profiles, cash on meeting.',
        'tagline': 'Corbett Gateway, Sal Woodlands & Riverside Resort Sanctuaries',
        'landmarks': 'Kosi River Barrage, Dhangarhi Gate, Garjiya Devi Temple, Ringora, Ramnagar Main Town',
        'hotels': 'Namah Resort, The Den Corbett, Tarangi Resort & Spa, Lemon Tree Premier Corbett, Corbett River Creek',
        'vibe': 'exhilarating jungle lodge getaways, riverside evening drinks, luxury safari retreats, and warm passionate encounters'
    },
    {
        'slug': 'haldwani',
        'name': 'Haldwani',
        'title': 'Premium Call Girls in Haldwani Executive Hotel Escorts',
        'meta_desc': 'Reserve premium call girls in Haldwani for executive hotel outcall along Nainital Road and Bareilly transit hubs. Direct contact, cash on arrival.',
        'tagline': 'Commercial Capital of Kumaon & Dynamic Regional Gateway',
        'landmarks': 'Nainital Road, Tikonia, Kaladhungi Road, Kusumkhera, Mukhani, Canal Road, Kathgodam Bypass',
        'hotels': 'Hotel Saurabh Candy by Peppermint, Fortune Walkway Mall, Hotel Maple Wood, Hotel Crossroad, The Central Hotel',
        'vibe': 'vibrant urban nightlife, upscale business dining, modern hotel hospitality, and convenient central connectivity'
    },
    {
        'slug': 'kaladhungi',
        'name': 'Kaladhungi',
        'title': 'Vip Call Girls Kaladhungi Foothill Countryside Hotel Escorts',
        'meta_desc': 'Connect with independent call girls Kaladhungi for peaceful countryside outcall near Corbett Falls and Boar River. Genuine photos with cash on arrival.',
        'tagline': 'Historic Jim Corbett Heritage, Boar River & Peaceful Countryside',
        'landmarks': 'Jim Corbett Heritage Museum, Corbett Falls, Boar River Valley, Choti Haldwani, Forest Belt',
        'hotels': 'Camp Corbett, Corbett Panorama, Forest Haven Eco Resort, Hidden Valley Camp, The Banyan Retreat',
        'vibe': 'quiet countryside privacy, fresh mountain streams, rustic bonfire retreats, and deeply personal relaxed moments'
    },
    {
        'slug': 'rudrapur',
        'name': 'Rudrapur',
        'title': 'Escort Service in Rudrapur - SIDCUL Hotel Outcall Escorts',
        'meta_desc': 'Book professional escort service in Rudrapur for corporate travelers at Radisson Blu and Metropolis suites. Zero advance deposit, cash on hotel visit.',
        'tagline': 'Industrial Epicenter of the Terai & Premier Corporate Hub',
        'landmarks': 'SIDCUL Industrial Sector, Metropolis Mall, Kashipur Bypass, Awas Vikas, Gaba Chowk, Nainital Highway',
        'hotels': 'Radisson Blu Hotel Rudrapur, Hotel Ark, Rosewood Apartment Hotel, Uday Residency, Ginger Rudrapur',
        'vibe': 'sophisticated business dinner dates, post-conference executive relaxation, modern luxury suites, and discrete professionalism'
    },
    {
        'slug': 'kathgodam',
        'name': 'Kathgodam',
        'title': 'Kathgodam Escort Service - Cash Payment Delivery Escorts',
        'meta_desc': 'Meet verified Kathgodam escort service models for relaxing transit visits and hill gateway hotel appointments. Direct companion contact, zero advance.',
        'tagline': 'Railway Terminus Gateway, Gaula River Valley & Hill Ascent Transit',
        'landmarks': 'Kathgodam Railway Station, Gaula Barrage, Shivalik Foothills, Ranibagh Bridge, Nainital Road Junction',
        'hotels': 'Hotel Fiesta, Relax Inn Kathgodam, Pineview Hotel, Gaula River View Resort, The Grand Kailash',
        'vibe': 'convenient transit rendezvous, scenic river terrace evenings, refreshing welcome companionship, and smooth hill departures'
    },
    {
        'slug': 'kashipur',
        'name': 'Kashipur',
        'title': 'Cheap Kashipur Escort Service low cost Quick Hotel Escorts',
        'meta_desc': 'Select verified Cheap Kashipur escort service for discreet hotel outcall along Bazpur Road and central suites. Independent models, zero advance, direct cash.',
        'tagline': 'Historic Industrial Gateway, Paper Mills & Academic Corridor',
        'landmarks': 'Bazpur Road, Ramnagar Road, IIM Kashipur Campus, Drona Sagar, Industrial Area Sector 1',
        'hotels': 'The Manor Kashipur, Anand Castle, Hotel Kumaon Plaza, Gautam Residency, Hotel Ashiyana',
        'vibe': 'private boutique hotel leisure, lively youthful energy, educated conversationalists, and total discretion'
    },
    {
        'slug': 'bajpur',
        'name': 'Bajpur',
        'title': 'Low Cost Bajpur Call Girls 100% Verified Highway Hotel Escorts',
        'meta_desc': 'Book verified Bajpur call girls for quiet farmhouse outcall and highway hotel appointments across the Terai belt. Safe direct meetings, cash on arrival.',
        'tagline': 'Fertile Agricultural Heartland, Historic Sugar Mills & Rural Farm Retreats',
        'landmarks': 'Bajpur Sugar Mill Area, Kashipur-Haldwani Road, Terai Orchards, Kosi Canal Crossing',
        'hotels': 'Green Park Hotel, Terai Royal Residency, The Orchard Retreat, Hotel Shivalik View Bajpur',
        'vibe': 'private farmhouse rendezvous, spacious country estates, peaceful rural sunsets, and genuine warm hospitality'
    },
    {
        'slug': 'khatima',
        'name': 'Khatima',
        'title': 'Vip Escort Service in Khatima ₹2,000 Low Cost Escorts Hotel',
        'meta_desc': 'Arrange trusted vip escort service in Khatima for quiet in-room hotel appointments along Tanakpur Road and Melghat. Verified models,₹2,000 cash upon meeting.',
        'tagline': 'Indo-Nepal Border Gateway, Sharda River & Terai Transit Crossroads',
        'landmarks': 'Tanakpur Road, Sharda River Canal, Khatima Main Market, Lohiahead Power House, Nanakmatta Junction',
        'hotels': 'Hotel Royal Park Khatima, City Heart Inn, Sharda Heritage Hotel, The Green Valley Inn',
        'vibe': 'frontier town charm, serene riverbank strolls, genuine affectionate companionship, and private suite encounters'
    },
    {
        'slug': 'sitarganj',
        'name': 'Sitarganj',
        'title': 'Call Girls Sitarganj - SIDCUL Industrial Hotel Escorts',
        'meta_desc': 'Reserve independent call girls Sitarganj for executive outcall near Eldeco SIDCUL park and town hotels. Photo-verified companions with cash on arrival.',
        'tagline': 'Modern Industrial Growth, Eldeco SIDCUL & Terai Commercial Crossroads',
        'landmarks': 'ELDECO SIDCUL Industrial Park, Baigul Dam, Nanakmatta Sahib Bypass, Khatima Highway',
        'hotels': 'Hotel Sitarganj Grand, The Industrial Inn, Green View Palace, Lakeview Comfort Stay Sitarganj',
        'vibe': 'quiet industrial executive unwinding, peaceful dam viewpoints, unhurried evening companionship, and total privacy'
    },
    {
        'slug': 'kichha',
        'name': 'Kichha',
        'title': 'Premium Escort Service Kichha - Gularbhoj Dam Hotel Escorts',
        'meta_desc': 'Find verified escort service Kichha for comfortable transit appointments and hotel visits along Bareilly Highway. Zero upfront deposit, cash on arrival.',
        'tagline': 'Agricultural Trade Hub, Bareilly Highway Artery & Logistics Gateway',
        'landmarks': 'Bareilly Highway, Rudrapur Bypass, Kichha Railway Station, Grain Market Complex, Terai Canal',
        'hotels': 'Hotel Celebration Kichha, The Highway Heritage, City Pride Inn, Amar Palace Kichha',
        'vibe': 'relaxed highway transit stopovers, friendly open-hearted companionship, stress-relieving massages, and cozy comfort'
    },
    {
        'slug': 'jim-corbett',
        'name': 'Jim Corbett',
        'title': 'Jim Corbett Call Girls - Luxury Safari Resort Escorts',
        'meta_desc': 'Arrange in-room visits with verified Jim Corbett call girls at premier eco-lodges near Bijrani and Dhikala gates. 100% authentic photos, cash payment.',
        'tagline': 'India’s Legendary Tiger Sanctuary & Luxury Wilderness Lodges',
        'landmarks': 'Bijrani Gate, Dhikala Zone, Jhirna Gate, Sitabani Forest, Kosi River Valley, Marchula',
        'hotels': 'Taj Corbett Resort & Spa, The Solluna Resort, Paatlidun Safari Lodge, Namah Resort, Aahana The Corbett Wilderness',
        'vibe': 'exclusive private pool villas, wilderness jungle sounds, candlelit riverside dinners, and unforgettable passionate intimacy'
    },
    {
        'slug': 'bhowali',
        'name': 'Bhowali',
        'title': 'Call Girls in Bhowali - Pine Ridge & Orchard Villa Escorts',
        'meta_desc': 'Meet discreet call girls in Bhowali for peaceful mountain villa outcall along Kainchi Dham road and pine ridges. Real photographs, safe cash on meeting.',
        'tagline': 'Himalayan Fruit Orchard Ridge, Sanatorium Pine Heights & Highway Junction',
        'landmarks': 'Bhowali Sanatorium Ridge, Kainchi Dham Junction, Ramgarh Road, Golu Devta Temple Road, Pine Crest',
        'hotels': 'The White Peaks Bhowali, Aqua De Vida Resort, Pine Crest Hotel, Soulitude in the Himalayas, Cedar Cottage',
        'vibe': 'cool pine-scented breezes, misty hillside mornings, cozy warm fireside cuddles, and unhurried romantic escapes'
    }
]

# Integrate calibrated Google-compliant SEO Titles, Meta Descriptions, and H1 tags
try:
    from location_local_data import LOCATION_SEO
    for loc in LOCATIONS_CONFIG:
        slug = loc['slug']
        if slug in LOCATION_SEO:
            loc['title'] = LOCATION_SEO[slug]['title']
            loc['meta_desc'] = LOCATION_SEO[slug]['meta_desc']
            loc['h1'] = LOCATION_SEO[slug]['h1']
            loc['seo_landmark'] = LOCATION_SEO[slug].get('landmark', '')
            loc['seo_hotel'] = LOCATION_SEO[slug].get('hotel', '')
except ImportError:
    pass

print(f"Loaded {len(NAMES_POOL)} unique names and {len(LOCATIONS_CONFIG)} location configurations.")
