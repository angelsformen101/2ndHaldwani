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
        'title': 'Nainital Escorts - Verified Call Girls & Luxury Hotel Companions',
        'meta_desc': 'Discover verified independent Nainital escorts and Mall Road hotel companions. 100% genuine photos, zero advance payment, and 24/7 private booking.',
        'tagline': 'Queen of Lakes & High-Altitude Leisure Retreats',
        'landmarks': 'Mall Road, Naini Lake, Snow View Point, Tallital, Sukhatal, Pangot',
        'hotels': 'The Manu Maharani, Shervani Hilltop, Vikram Vintage Inn, The Naini Retreat, Swiss Hotel',
        'vibe': 'scenic lakeside promenades, luxury pine view villas, romantic boating dates, and mountain hideaways'
    },
    {
        'slug': 'bhimtal',
        'name': 'Bhimtal',
        'title': 'Bhimtal Escorts - Elite Lake Resort Call Girls & Private Companions',
        'meta_desc': 'Book elite independent Bhimtal escorts and private lake resort call girls. 100% authentic models, discreet in-room companionship, and transparent cash payment.',
        'tagline': 'Tranquil Island Lake & Secluded Nature Escapes',
        'landmarks': 'Bhimtal Island Lake, Victoria Dam, Hidimba Parvat, Nal Damyanti Tal, Sattal Junction',
        'hotels': 'The Fern Hillside Resort, Country Inn Bhimtal, Aamod Resorts, Fishermens Lodge, V Resort',
        'vibe': 'peaceful waterside serenity, secluded pine forest cottages, private bonfire evenings, and relaxing weekend vacations'
    },
    {
        'slug': 'almora',
        'name': 'Almora',
        'title': 'Almora Escorts - Charming Independent Companions & Hillside Call Girls',
        'meta_desc': 'Explore verified Almora escorts and independent hill station call girls. Genuine high-class college companions, heritage resort visits, and zero advance fee.',
        'tagline': 'Cultural Heartland of Kumaon with Majestic Himalayan Vistas',
        'landmarks': 'Bright End Corner, Kasar Devi, Lal Bazaar, Deer Park, Binsar Wildlife Sanctuary',
        'hotels': 'Kalmatia Sangam, Grand Oak Manor, Deodar Sanctuary, Imperial Heights Binsar, Kasaar Jungle Resort',
        'vibe': 'soothing ridge-line sunsets, deep pine fragrance, artistic conversations, and unhurried intellectual companionship'
    },
    {
        'slug': 'ramnagar',
        'name': 'Ramnagar',
        'title': 'Ramnagar Escorts - Jungle Safari Lodge Call Girls & VIP Companions',
        'meta_desc': 'Verified Ramnagar escorts and luxury jungle lodge call girls near Corbett Gateway. 100% discreet models, outcall service to luxury safari resorts, and cash on arrival.',
        'tagline': 'Corbett Gateway & Wilderness Luxury Destination',
        'landmarks': 'Kosi River Barrage, Dhangarhi Gate, Garjiya Devi Temple, Ringora, Ramnagar Main Town',
        'hotels': 'Namah Resort, The Den Corbett, Tarangi Resort & Spa, Lemon Tree Premier Corbett, Corbett River Creek',
        'vibe': 'exhilarating jungle lodge getaways, riverside evening drinks, luxury safari retreats, and warm passionate encounters'
    },
    {
        'slug': 'haldwani',
        'name': 'Haldwani',
        'title': 'Haldwani Escorts - Verified City Call Girls & VIP In-Hotel Companions',
        'meta_desc': 'Top-rated Haldwani escorts and verified college call girls available 24/7. 100% real photos, zero advance money, and safe five-star hotel outcall service.',
        'tagline': 'Commercial Metropolis & Foothill Transit Capital of Kumaon',
        'landmarks': 'Nainital Road, Tikonia, Kaladhungi Road, Kusumkhera, Mukhani, Canal Road, Kathgodam Bypass',
        'hotels': 'Hotel Saurabh Candy by Peppermint, Fortune Walkway Mall, Hotel Maple Wood, Hotel Crossroad, The Central Hotel',
        'vibe': 'vibrant urban nightlife, upscale business dining, modern hotel hospitality, and convenient central connectivity'
    },
    {
        'slug': 'kaladhungi',
        'name': 'Kaladhungi',
        'title': 'Kaladhungi Escorts - Rustic Nature Retreat Call Girls & Companions',
        'meta_desc': 'Connect with genuine Kaladhungi escorts and private forest resort call girls. Discretion assured, zero upfront charges, and authentic verified profiles.',
        'tagline': 'Jim Corbett Heritage Country & Lush Forest Foothills',
        'landmarks': 'Jim Corbett Heritage Museum, Corbett Falls, Boar River Valley, Choti Haldwani, Forest Belt',
        'hotels': 'Camp Corbett, Corbett Panorama, Forest Haven Eco Resort, Hidden Valley Camp, The Banyan Retreat',
        'vibe': 'quiet countryside privacy, fresh mountain streams, rustic bonfire retreats, and deeply personal relaxed moments'
    },
    {
        'slug': 'rudrapur',
        'name': 'Rudrapur',
        'title': 'Rudrapur Escorts - Corporate Executive Companions & VIP Call Girls',
        'meta_desc': 'High-profile Rudrapur escorts and executive hotel call girls for business travelers. Verified SIDCUL companions, discreet 4-star hotel visits, cash on meeting.',
        'tagline': 'Industrial Engine of Terai & High-Speed Corporate Hub',
        'landmarks': 'SIDCUL Industrial Sector, Metropolis Mall, Kashipur Bypass, Awas Vikas, Gaba Chowk, Nainital Highway',
        'hotels': 'Radisson Blu Hotel Rudrapur, Hotel Ark, Rosewood Apartment Hotel, Uday Residency, Ginger Rudrapur',
        'vibe': 'sophisticated business dinner dates, post-conference executive relaxation, modern luxury suites, and discrete professionalism'
    },
    {
        'slug': 'kathgodam',
        'name': 'Kathgodam',
        'title': 'Kathgodam Escorts - Railway Junction & Hill Gateway Call Girls',
        'meta_desc': 'Reliable Kathgodam escorts and transit hotel call girls near railway terminus. 100% verified independent girls, instant outcall service, zero advance fee.',
        'tagline': 'Historic Railhead & Gateway into the Misty Hills',
        'landmarks': 'Kathgodam Railway Station, Gaula Barrage, Shivalik Foothills, Ranibagh Bridge, Nainital Road Junction',
        'hotels': 'Hotel Fiesta, Relax Inn Kathgodam, Pineview Hotel, Gaula River View Resort, The Grand Kailash',
        'vibe': 'convenient transit rendezvous, scenic river terrace evenings, refreshing welcome companionship, and smooth hill departures'
    },
    {
        'slug': 'kashipur',
        'name': 'Kashipur',
        'title': 'Kashipur Escorts - High Profile College Models & Elite Call Girls',
        'meta_desc': 'Book authentic Kashipur escorts and independent VIP call girls. Serving industrial parks and luxury hotels with full confidentiality and zero advance payments.',
        'tagline': 'Ancient Heritage & Thriving Industrial Commercial Centre',
        'landmarks': 'Bazpur Road, Ramnagar Road, IIM Kashipur Campus, Drona Sagar, Industrial Area Sector 1',
        'hotels': 'The Manor Kashipur, Anand Castle, Hotel Kumaon Plaza, Gautam Residency, Hotel Ashiyana',
        'vibe': 'private boutique hotel leisure, lively youthful energy, educated conversationalists, and total discretion'
    },
    {
        'slug': 'bajpur',
        'name': 'Bajpur',
        'title': 'Bajpur Escorts - Independent Sugar Belt Call Girls & Farmhouse Companions',
        'meta_desc': 'Verified Bajpur escorts and discreet farmhouse call girls. 100% authentic local models, outcall service across luxury private farms, and zero advance deposit.',
        'tagline': 'Lush Agricultural Plains & Scenic Terai Countryside',
        'landmarks': 'Bajpur Sugar Mill Area, Kashipur-Haldwani Road, Terai Orchards, Kosi Canal Crossing',
        'hotels': 'Green Park Hotel, Terai Royal Residency, The Orchard Retreat, Hotel Shivalik View Bajpur',
        'vibe': 'private farmhouse rendezvous, spacious country estates, peaceful rural sunsets, and genuine warm hospitality'
    },
    {
        'slug': 'khatima',
        'name': 'Khatima',
        'title': 'Khatima Escorts - Border Town Verified Call Girls & Hotel Escort Service',
        'meta_desc': 'Premium Khatima escorts and genuine college call girls available for hotel and outstation companionship. 100% real photos, transparent pricing, cash on arrival.',
        'tagline': 'Indo-Nepal Border Corridor & Verdant Terai Woodlands',
        'landmarks': 'Tanakpur Road, Sharda River Canal, Khatima Main Market, Lohiahead Power House, Nanakmatta Junction',
        'hotels': 'Hotel Royal Park Khatima, City Heart Inn, Sharda Heritage Hotel, The Green Valley Inn',
        'vibe': 'frontier town charm, serene riverbank strolls, genuine affectionate companionship, and private suite encounters'
    },
    {
        'slug': 'sitarganj',
        'name': 'Sitarganj',
        'title': 'Sitarganj Escorts - SIDCUL Industrial Zone Call Girls & Private Models',
        'meta_desc': 'Verified Sitarganj escorts and corporate call girls serving ELDECO SIDCUL industrial complex. Safe hotel outcall, 100% discreet models, zero upfront payment.',
        'tagline': 'Manufacturing Growth Corridor & Waterside Reservoir Environs',
        'landmarks': 'ELDECO SIDCUL Industrial Park, Baigul Dam, Nanakmatta Sahib Bypass, Khatima Highway',
        'hotels': 'Hotel Sitarganj Grand, The Industrial Inn, Green View Palace, Lakeview Comfort Stay Sitarganj',
        'vibe': 'quiet industrial executive unwinding, peaceful dam viewpoints, unhurried evening companionship, and total privacy'
    },
    {
        'slug': 'kichha',
        'name': 'Kichha',
        'title': 'Kichha Escorts - High Class Local Call Girls & Highway Suite Companions',
        'meta_desc': 'Authentic Kichha escorts and independent female call girls. Reliable outcall service to certified hotels and private suites with zero advance financial deposit.',
        'tagline': 'Crossroads of Terai Trade & Rice Granary of the Foothills',
        'landmarks': 'Bareilly Highway, Rudrapur Bypass, Kichha Railway Station, Grain Market Complex, Terai Canal',
        'hotels': 'Hotel Celebration Kichha, The Highway Heritage, City Pride Inn, Amar Palace Kichha',
        'vibe': 'relaxed highway transit stopovers, friendly open-hearted companionship, stress-relieving massages, and cozy comfort'
    },
    {
        'slug': 'jim-corbett',
        'name': 'Jim Corbett',
        'title': 'Jim Corbett Escorts - Luxury 5-Star Safari Resort Call Girls & VIP Escorts',
        'meta_desc': 'Experience ultra-luxury Jim Corbett escorts and forest retreat call girls. Five-star safari lodge companions, private pool villa visits, zero advance deposit.',
        'tagline': 'India’s Legendary Tiger Reserve & World-Class Eco-Luxury Lodges',
        'landmarks': 'Bijrani Gate, Dhikala Zone, Jhirna Gate, Sitabani Forest, Kosi River Valley, Marchula',
        'hotels': 'Taj Corbett Resort & Spa, The Solluna Resort, Paatlidun Safari Lodge, Namah Resort, Aahana The Corbett Wilderness',
        'vibe': 'exclusive private pool villas, wilderness jungle sounds, candlelit riverside dinners, and unforgettable passionate intimacy'
    },
    {
        'slug': 'bhowali',
        'name': 'Bhowali',
        'title': 'Bhowali Escorts - Mist-Covered Pine Forest Call Girls & Hill Villa Companions',
        'meta_desc': 'Book charming Bhowali escorts and independent pine cottage call girls. 100% verified photos, Kainchi Dham junction access, and zero advance payment.',
        'tagline': 'The Fruit Bowl of Kumaon & Refreshing Pine Valley Ridge',
        'landmarks': 'Bhowali Sanatorium Ridge, Kainchi Dham Junction, Ramgarh Road, Golu Devta Temple Road, Pine Crest',
        'hotels': 'The White Peaks Bhowali, Aqua De Vida Resort, Pine Crest Hotel, Soulitude in the Himalayas, Cedar Cottage',
        'vibe': 'cool pine-scented breezes, misty hillside mornings, cozy warm fireside cuddles, and unhurried romantic escapes'
    }
]

print(f"Loaded {len(NAMES_POOL)} unique names and {len(LOCATIONS_CONFIG)} location configurations.")
