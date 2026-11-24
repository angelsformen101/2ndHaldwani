import json

LOCATION_LOCAL_DATA = {
    'nainital': {
        'profile_keywords': [
            'Mallital Call Girls',
            'Tallital Escort Service',
            'Mall Road Call Girls',
            'Naini Lake Escorts',
            'Snow View Call Girls',
            'Ayarpatta Escort Service',
            'Pangot Independent Escorts',
            'Sukhatal Call Girls',
            'The Manu Maharani Hotel Escorts',
            'Shervani Hilltop Call Girls',
            'Kilbury Road Escort Service',
            'The Naini Retreat Call Girls',
            'Bhowali Road Call Girls',
            'Tiffin Top Escorts',
            'Nainital Luxury Call Girls',
            'Russian Escorts Nainital'
        ],
        'popular_tags': [
            'Nainital call girls', 'Nainital escort service', 'Call girls in Nainital', 'Escorts in Nainital',
            'Mall Road Nainital call girls', 'Tallital call girls', 'Tallital escort service', 'Mallital call girls',
            'Mallital escort service', 'Naini Lake call girls', 'Ayarpatta VIP escorts', 'Snow View call girls',
            'Pangot escort service', 'Kilbury Road call girls', 'Bhowali Road Nainital escorts', 'Sukhatal call girls',
            'Raj Bhavan area escorts', 'Tiffin Top call girls', 'Sherwani area escorts', 'Manu Maharani hotel call girls',
            'Shervani Hilltop escorts', 'Nainital luxury call girls', 'Russian escorts in Nainital', 'Independent escorts Nainital',
            'call girls near me Nainital', 'escort near me Nainital', 'hotel service call girls Nainital', '24 hour call girl service Nainital'
        ]
    },
    'bhimtal': {
        'profile_keywords': [
            'Bhimtal Island Lake Call Girls',
            'Victoria Dam Escort Service',
            'Hidimba Parvat Call Girls',
            'Nal Damyanti Tal Escorts',
            'Sattal Junction Call Girls',
            'The Fern Hillside Resort Escorts',
            'Country Inn Bhimtal Call Girls',
            'Aamod Resorts Escort Service',
            'Fishermens Lodge Call Girls',
            'Bhimtal Lake View Escorts',
            'Bhowali Road Bhimtal Call Girls',
            'Bhimtal Independent Escorts',
            'Bhimtal VIP Call Girls',
            'Luxury Lake Resort Escorts',
            'Bhimtal College Call Girls',
            'Bhimtal 24 Hour Escort Service'
        ],
        'popular_tags': [
            'Bhimtal call girls', 'Bhimtal escort service', 'Call girls in Bhimtal', 'Escorts in Bhimtal',
            'Bhimtal Lake call girls', 'Island Lake Bhimtal escorts', 'Victoria Dam call girls', 'Sattal road escorts',
            'The Fern resort call girls', 'Country Inn Bhimtal escorts', 'Aamod resort call girls', 'Bhimtal luxury escorts',
            'Independent call girls Bhimtal', 'Bhimtal hotel call girls', 'Bhimtal VIP escorts', 'Bhimtal bhabhi call girls',
            'call girls near me Bhimtal', 'escort near me Bhimtal', 'genuine escort service Bhimtal', 'cash on delivery call girls Bhimtal',
            '24 hour escort service Bhimtal', 'full night call girls Bhimtal', 'short time call girls Bhimtal', 'verified call girls Bhimtal'
        ]
    },
    'almora': {
        'profile_keywords': [
            'Bright End Corner Call Girls',
            'Kasar Devi Escort Service',
            'Lal Bazaar Call Girls',
            'Deer Park Escorts',
            'Binsar Wildlife Road Call Girls',
            'Kalmatia Sangam Resort Escorts',
            'Imperial Heights Call Girls',
            'Kumaon Heritage Escort Service',
            'Chitai Temple Road Call Girls',
            'Almora Mall Road Escorts',
            'Ranikhet Road Call Girls',
            'Almora Independent Escorts',
            'Almora VIP Call Girls',
            'Himalayan View Escort Service',
            'Almora College Call Girls',
            'Almora 24 Hour Escorts'
        ],
        'popular_tags': [
            'Almora call girls', 'Almora escort service', 'Call girls in Almora', 'Escorts in Almora',
            'Kasar Devi call girls', 'Bright End Corner escorts', 'Lal Bazaar call girls', 'Binsar road escorts',
            'Kalmatia resort call girls', 'Imperial Heights escorts', 'Almora luxury call girls', 'Independent escorts Almora',
            'Almora hotel call girls', 'Almora VIP escorts', 'Almora genuine call girls', 'call girls near me Almora',
            'escort near me Almora', '24 hour call girl service Almora', 'full night call girls Almora', 'safe escort service Almora',
            'Almora college call girls', 'cash on arrival escorts Almora', 'Ranikhet road call girls', 'Kumaon escort service'
        ]
    },
    'ramnagar': {
        'profile_keywords': [
            'Jim Corbett Resort Call Girls',
            'Dhikala Zone Escorts',
            'Bijrani Gate Call Girls',
            'Kosi River Resort Escorts',
            'Mohaan Ramnagar Call Girls',
            'Marchula Luxury Escorts',
            'Ringora Corbett Call Girls',
            'Sitabani Forest Escorts',
            'Garjiya Temple Area Call Girls',
            'Ramnagar Railway Station Escorts',
            'Corbett National Park Call Girls',
            'Taj Corbett Resort Escorts',
            'Namah Resort Call Girls',
            'The Den Corbett Escorts',
            'Aahana Resort Call Girls',
            'Luxury Call Girls Ramnagar'
        ],
        'popular_tags': [
            'Ramnagar call girls', 'Ramnagar escort service', 'Call girls in Ramnagar', 'Escorts in Ramnagar',
            'Jim Corbett resort call girls', 'Dhikala zone escorts', 'Bijrani gate call girls', 'Kosi River resort escorts',
            'Mohaan Ramnagar call girls', 'Marchula luxury escorts', 'Ringora Corbett call girls', 'Sitabani forest escorts',
            'Garjiya temple area call girls', 'Ramnagar Station escorts', 'Taj Corbett resort escorts', 'Namah resort call girls',
            'The Den Corbett escorts', 'Aahana resort call girls', 'Riverview retreat escorts', 'Luxury call girls Ramnagar',
            'call girls near me Ramnagar', 'escort near me Corbett', 'Corbett safari call girls', '24 hour escort service Ramnagar'
        ]
    },
    'haldwani': {
        'profile_keywords': [
            'Kaladhungi Road Call Girls',
            'Nainital Road Haldwani Escorts',
            'Kathgodam Call Girls',
            'Kathgodam Escort Service',
            'Tikonia Chowk Call Girls',
            'Mukhani Haldwani Escorts',
            'Kusumkhera Call Girls',
            'Transport Nagar Call Girls',
            'Bareilly Road Call Girls',
            'Rampur Road Haldwani Escorts',
            'Panchwati Colony Call Girls',
            'Heera Nagar Escorts',
            'Subhash Nagar Call Girls',
            'Awas Vikas Haldwani Escorts',
            'Bhotia Parao Call Girls',
            'MBPG College Area Escorts'
        ],
        'popular_tags': [
            'Haldwani call girls', 'Haldwani escort service', 'Call girls in Haldwani', 'Escorts in Haldwani',
            'Kaladhungi Road call girls', 'Nainital Road Haldwani escorts', 'Kathgodam call girls', 'Kathgodam escort service',
            'Tikonia Chowk call girls', 'Mukhani Haldwani escorts', 'Kusumkhera call girls', 'Transport Nagar call girls',
            'Bareilly Road call girls', 'Rampur Road Haldwani escorts', 'Panchwati Colony call girls', 'Heera Nagar escorts',
            'Subhash Nagar call girls', 'Awas Vikas Haldwani escorts', 'Bhotia Parao call girls', 'MBPG College area escorts',
            'call girls near me Haldwani', 'escort near me Haldwani', 'hotel service call girls Haldwani', '24 hour call girl service Haldwani'
        ]
    },
    'kaladhungi': {
        'profile_keywords': [
            'Corbett Museum Area Call Girls',
            'Chhoti Haldwani Escorts',
            'Corbett Falls Call Girls',
            'Nainital Road Kaladhungi Escorts',
            'Camp Corbett Call Girls',
            'Barati Rau River Escorts',
            'Baur Reservoir Call Girls',
            'Kaladhungi Heritage Escorts',
            'Bazpur Road Kaladhungi Call Girls',
            'Forest Rest House Escorts',
            'Kaladhungi Independent Call Girls',
            'Kaladhungi VIP Escorts',
            'Nature Retreat Call Girls',
            'Kaladhungi College Escorts',
            'Kaladhungi Hotel Call Girls',
            'Kaladhungi 24 Hour Escort Service'
        ],
        'popular_tags': [
            'Kaladhungi call girls', 'Kaladhungi escort service', 'Call girls in Kaladhungi', 'Escorts in Kaladhungi',
            'Corbett Museum call girls', 'Chhoti Haldwani escorts', 'Corbett Falls call girls', 'Camp Corbett escorts',
            'Barati Rau river call girls', 'Baur Reservoir escorts', 'Kaladhungi luxury call girls', 'Independent escorts Kaladhungi',
            'Kaladhungi resort call girls', 'Kaladhungi VIP escorts', 'call girls near me Kaladhungi', 'escort near me Kaladhungi',
            'hotel outcall call girls Kaladhungi', 'cash on arrival Kaladhungi escorts', '24 hour call girl service Kaladhungi', 'verified call girls Kaladhungi'
        ]
    },
    'rudrapur': {
        'profile_keywords': [
            'SIDCUL Sector Call Girls',
            'Radisson Blu Hotel Escorts',
            'Kashipur Road Rudrapur Call Girls',
            'Delhi Highway Escort Service',
            'Metropolis City Call Girls',
            'Kalyani View Escorts',
            'Hotel Sobti Continental Call Girls',
            'Uday Residency Escort Service',
            'Awas Vikas Rudrapur Call Girls',
            'Gandhi Colony Escorts',
            'Rudrapur Corporate Call Girls',
            'Rudrapur VIP Escort Service',
            'Rudrapur Independent Call Girls',
            'Industrial Sector Call Girls',
            'Rudrapur College Escorts',
            'Rudrapur 24 Hour Escort Service'
        ],
        'popular_tags': [
            'Rudrapur call girls', 'Rudrapur escort service', 'Call girls in Rudrapur', 'Escorts in Rudrapur',
            'SIDCUL Rudrapur call girls', 'Radisson Blu Rudrapur escorts', 'Kashipur Road call girls', 'Delhi Highway escorts',
            'Metropolis Mall call girls', 'Hotel Sobti escorts', 'Uday Residency call girls', 'Rudrapur corporate escorts',
            'Independent call girls Rudrapur', 'Rudrapur VIP escorts', 'call girls near me Rudrapur', 'escort near me Rudrapur',
            'hotel service call girls Rudrapur', '24 hour call girl service Rudrapur', 'full night call girls Rudrapur', 'cash on meeting Rudrapur escorts'
        ]
    },
    'kathgodam': {
        'profile_keywords': [
            'Kathgodam Railway Station Call Girls',
            'Gaula River View Escorts',
            'Ranibagh Bridge Call Girls',
            'Nainital Highway Escorts',
            'Hotel Fiesta Kathgodam Call Girls',
            'Relax Inn Kathgodam Escorts',
            'Pineview Hotel Call Girls',
            'The Grand Kailash Escorts',
            'Sheetla Devi Temple Road Call Girls',
            'Haldwani Link Road Escorts',
            'Kathgodam Transit Call Girls',
            'Kathgodam VIP Escort Service',
            'Kathgodam Independent Models',
            'Hillside View Call Girls',
            'Kathgodam Express Escorts',
            'Kathgodam 24 Hour Call Girls'
        ],
        'popular_tags': [
            'Kathgodam call girls', 'Kathgodam escort service', 'Call girls in Kathgodam', 'Escorts in Kathgodam',
            'Kathgodam Railway Station call girls', 'Gaula River escorts', 'Ranibagh call girls', 'Nainital highway escorts',
            'Hotel Fiesta call girls', 'The Grand Kailash escorts', 'Kathgodam transit call girls', 'Kathgodam luxury escorts',
            'Independent escorts Kathgodam', 'Kathgodam hotel call girls', 'call girls near me Kathgodam', 'escort near me Kathgodam',
            '24 hour escort service Kathgodam', 'full night call girls Kathgodam', 'cash on arrival Kathgodam escorts', 'verified call girls Kathgodam'
        ]
    },
    'kashipur': {
        'profile_keywords': [
            'Bazpur Road Industrial Call Girls',
            'Ramnagar Road Corridor Escorts',
            'IIM Kashipur Campus Call Girls',
            'Drona Sagar Lake Escorts',
            'Industrial Area Phase 1 Call Girls',
            'Kundeshwari Road Escorts',
            'The Manor Kashipur Call Girls',
            'Anand Castle Escort Service',
            'Hotel Kumaon Plaza Call Girls',
            'Gautam Residency Escorts',
            'Aliganj Road Call Girls',
            'Kashipur Corporate Escort Service',
            'Kashipur Independent Call Girls',
            'Kashipur VIP Hotel Escorts',
            'Kashipur College Call Girls',
            'Kashipur 24 Hour Escorts'
        ],
        'popular_tags': [
            'Kashipur call girls', 'Kashipur escort service', 'Call girls in Kashipur', 'Escorts in Kashipur',
            'Bazpur Road call girls', 'Ramnagar Road escorts', 'IIM Kashipur call girls', 'Drona Sagar escorts',
            'The Manor Kashipur call girls', 'Anand Castle escorts', 'Kumaon Plaza call girls', 'Kashipur corporate escorts',
            'Independent call girls Kashipur', 'Kashipur VIP escorts', 'call girls near me Kashipur', 'escort near me Kashipur',
            'hotel service call girls Kashipur', '24 hour call girl service Kashipur', 'full night call girls Kashipur', 'cash on arrival Kashipur escorts'
        ]
    },
    'bajpur': {
        'profile_keywords': [
            'Bajpur Sugar Mill Call Girls',
            'Kashipur-Haldwani Highway Escorts',
            'Terai Orchard Farm Call Girls',
            'Kosi River Canal Escorts',
            'Sultanpur Patti Road Call Girls',
            'Main Bazaar Chowk Escorts',
            'Green Park Hotel Call Girls',
            'Terai Royal Residency Escorts',
            'The Orchard Retreat Call Girls',
            'Hotel Shivalik View Escorts',
            'Bajpur Farmhouse Call Girls',
            'Bajpur Independent Escort Service',
            'Bajpur VIP Call Girls',
            'Rural Retreat Escorts',
            'Bajpur Highway Call Girls',
            'Bajpur 24 Hour Escorts'
        ],
        'popular_tags': [
            'Bajpur call girls', 'Bajpur escort service', 'Call girls in Bajpur', 'Escorts in Bajpur',
            'Sugar Mill Bajpur call girls', 'Haldwani Highway escorts', 'Terai farmhouse call girls', 'Kosi River canal escorts',
            'Green Park Hotel call girls', 'The Orchard Retreat escorts', 'Bajpur luxury call girls', 'Independent escorts Bajpur',
            'call girls near me Bajpur', 'escort near me Bajpur', 'hotel outcall call girls Bajpur', 'farmhouse escort service Bajpur',
            '24 hour escort service Bajpur', 'full night call girls Bajpur', 'cash on arrival Bajpur escorts', 'verified call girls Bajpur'
        ]
    },
    'khatima': {
        'profile_keywords': [
            'Tanakpur Highway Call Girls',
            'Sharda River Canal Escorts',
            'Khatima Main Market Call Girls',
            'Lohiahead Power House Escorts',
            'Nanakmatta Link Road Call Girls',
            'Melghat Border Area Escorts',
            'Hotel Royal Park Call Girls',
            'City Heart Inn Escorts',
            'Sharda Heritage Hotel Call Girls',
            'The Green Valley Inn Escorts',
            'Khatima Commercial Call Girls',
            'Khatima Independent Escort Service',
            'Khatima VIP Call Girls',
            'Border Highway Escorts',
            'Khatima College Call Girls',
            'Khatima 24 Hour Escorts'
        ],
        'popular_tags': [
            'Khatima call girls', 'Khatima escort service', 'Call girls in Khatima', 'Escorts in Khatima',
            'Tanakpur Road call girls', 'Sharda River escorts', 'Nanakmatta link call girls', 'Lohiahead road escorts',
            'Hotel Royal Park call girls', 'City Heart Inn escorts', 'Khatima luxury call girls', 'Independent escorts Khatima',
            'call girls near me Khatima', 'escort near me Khatima', 'hotel service call girls Khatima', '24 hour call girl service Khatima',
            'full night call girls Khatima', 'cash on arrival Khatima escorts', 'verified call girls Khatima', 'safe escort service Khatima'
        ]
    },
    'sitarganj': {
        'profile_keywords': [
            'ELDECO SIDCUL Industrial Call Girls',
            'Khatima-Rudrapur Highway Escorts',
            'Nanakmatta Sahib Vicinity Call Girls',
            'Baigul Dam Reservoir Escorts',
            'Phase 1 Industrial Belt Call Girls',
            'Main Chowk Market Escorts',
            'Hotel Sitarganj Grand Call Girls',
            'The Royal Palace Escorts',
            'Green City Hotel Call Girls',
            'Nanak Lake View Escorts',
            'Sitarganj Corporate Call Girls',
            'Sitarganj Independent Escorts',
            'Sitarganj VIP Call Girls',
            'Industrial Park Escorts',
            'Sitarganj Highway Call Girls',
            'Sitarganj 24 Hour Escorts'
        ],
        'popular_tags': [
            'Sitarganj call girls', 'Sitarganj escort service', 'Call girls in Sitarganj', 'Escorts in Sitarganj',
            'ELDECO SIDCUL call girls', 'Khatima highway escorts', 'Baigul Dam call girls', 'Nanakmatta vicinity escorts',
            'Hotel Sitarganj Grand call girls', 'The Royal Palace escorts', 'Sitarganj corporate call girls', 'Sitarganj luxury escorts',
            'Independent escorts Sitarganj', 'call girls near me Sitarganj', 'escort near me Sitarganj', 'hotel service call girls Sitarganj',
            '24 hour escort service Sitarganj', 'full night call girls Sitarganj', 'cash on arrival Sitarganj escorts', 'verified call girls Sitarganj'
        ]
    },
    'kichha': {
        'profile_keywords': [
            'Bareilly Highway Call Girls',
            'Pantnagar Airport Vicinity Escorts',
            'Sitarganj Road Commercial Call Girls',
            'Gaula Canal Crossing Escorts',
            'Grain Mandi Complex Call Girls',
            'Railway Station Road Escorts',
            'Hotel Celebration Kichha Call Girls',
            'City Pride Hotel Escorts',
            'Green Valley Resort Call Girls',
            'Highway Inn Kichha Escorts',
            'Kichha Transit Call Girls',
            'Kichha Independent Escort Service',
            'Kichha VIP Call Girls',
            'Pantnagar Highway Escorts',
            'Kichha College Call Girls',
            'Kichha 24 Hour Escorts'
        ],
        'popular_tags': [
            'Kichha call girls', 'Kichha escort service', 'Call girls in Kichha', 'Escorts in Kichha',
            'Bareilly Highway call girls', 'Pantnagar Airport escorts', 'Sitarganj Road call girls', 'Gaula Canal escorts',
            'Hotel Celebration call girls', 'City Pride Hotel escorts', 'Kichha transit call girls', 'Kichha luxury escorts',
            'Independent escorts Kichha', 'call girls near me Kichha', 'escort near me Kichha', 'hotel service call girls Kichha',
            '24 hour call girl service Kichha', 'full night call girls Kichha', 'cash on arrival Kichha escorts', 'verified call girls Kichha'
        ]
    },
    'jim-corbett': {
        'profile_keywords': [
            'Bijrani Gate Call Girls',
            'Dhikala Safari Zone Escorts',
            'Jhirna Buffer Zone Call Girls',
            'Dhela Ecotourism Zone Escorts',
            'Kosi Riverfront Call Girls',
            'Mohaan Forest Ridge Escorts',
            'Marchula Valley Call Girls',
            'Sitabani Wildlife Sanctuary Escorts',
            'Taj Corbett Resort & Spa Escorts',
            'The Solluna Resort Call Girls',
            'Namah Resort Jim Corbett Escorts',
            'Aahana The Corbett Wilderness Call Girls',
            'The Den Corbett Luxury Escorts',
            'Corbett Riverside Resort Call Girls',
            'Jim Corbett VIP Escort Service',
            'Russian Escorts Jim Corbett'
        ],
        'popular_tags': [
            'Jim Corbett call girls', 'Jim Corbett escort service', 'Corbett call girls', 'Corbett escort service',
            'Bijrani gate call girls', 'Dhikala zone escorts', 'Kosi Riverfront call girls', 'Marchula valley escorts',
            'Taj Corbett resort call girls', 'The Solluna resort escorts', 'Namah resort call girls', 'Aahana wilderness escorts',
            'The Den Corbett call girls', 'Riverside resort escorts', 'Corbett luxury call girls', 'Russian escorts Jim Corbett',
            'call girls near me Jim Corbett', 'escort near me Corbett', 'Corbett hotel call girls', 'safari resort escort service',
            '24 hour escort service Corbett', 'full night call girls Corbett', 'cash on arrival Corbett escorts', 'verified call girls Jim Corbett'
        ]
    },
    'bhowali': {
        'profile_keywords': [
            'Bhowali Sanatorium Ridge Call Girls',
            'Kainchi Dham Highway Escorts',
            'Ghorakhal Tea Garden Call Girls',
            'Nainital-Almora Junction Escorts',
            'Shyamkhet Pine Forest Call Girls',
            'Ramgarh Road Fruit Valley Escorts',
            'The White Peaks Bhowali Escorts',
            'Aqua De Vida Resort Call Girls',
            'Naini Hills View Resort Escorts',
            'Swiss Chalet Bhowali Call Girls',
            'Bhowali Fruit Market Area Escorts',
            'Bhowali Hilltop Call Girls',
            'Bhowali Independent Escort Service',
            'Bhowali VIP Resort Call Girls',
            'Bhowali College Escorts',
            'Bhowali 24 Hour Call Girls'
        ],
        'popular_tags': [
            'Bhowali call girls', 'Bhowali escort service', 'Call girls in Bhowali', 'Escorts in Bhowali',
            'Kainchi Dham road call girls', 'Ghorakhal tea garden escorts', 'Shyamkhet pine call girls', 'Ramgarh road escorts',
            'The White Peaks call girls', 'Aqua De Vida escorts', 'Naini Hills View call girls', 'Bhowali luxury escorts',
            'Independent call girls Bhowali', 'Bhowali hotel call girls', 'Bhowali VIP escorts', 'call girls near me Bhowali',
            'escort near me Bhowali', '24 hour call girl service Bhowali', 'full night call girls Bhowali', 'cash on arrival Bhowali escorts'
        ]
    }
}

print("Loaded LOCATION_LOCAL_DATA with all 15 locations!")


LOCATION_SEO = {
    'nainital': {
        'title': 'Nainital Call Girls - Nainital Escort Service in Mall Road',
        'meta_desc': 'Book verified Nainital call girls & elite Nainital escort service in Mall Road. 100% genuine independent models, The Manu Maharani outcall & cash on meeting.',
        'h1': 'Nainital Call Girls - Verified Nainital Escort Service in Mall Road',
        'landmark': 'Mall Road',
        'hotel': 'The Manu Maharani'
    },
    'bhimtal': {
        'title': 'Bhimtal Call Girls - Bhimtal Escort Service in Island Lake',
        'meta_desc': 'Book verified Bhimtal call girls & elite Bhimtal escort service in Island Lake. 100% genuine independent models, The Fern resort outcall & cash on meeting.',
        'h1': 'Bhimtal Call Girls - Verified Bhimtal Escort Service in Island Lake',
        'landmark': 'Island Lake',
        'hotel': 'The Fern Resort'
    },
    'almora': {
        'title': 'Almora Call Girls - Almora Escort Service in Kasar Devi',
        'meta_desc': 'Book verified Almora call girls & elite Almora escort service in Kasar Devi. 100% genuine independent models, Kalmatia resort outcall & cash on meeting.',
        'h1': 'Almora Call Girls - Verified Almora Escort Service in Kasar Devi',
        'landmark': 'Kasar Devi',
        'hotel': 'Kalmatia Resort'
    },
    'ramnagar': {
        'title': 'Ramnagar Call Girls - Ramnagar Escort Service, Kosi River',
        'meta_desc': 'Book verified Ramnagar call girls & elite Ramnagar escort service near Kosi River. 100% genuine independent models, Namah resort outcall & cash on meeting.',
        'h1': 'Ramnagar Call Girls - Verified Ramnagar Escort Service near Kosi River',
        'landmark': 'Kosi River',
        'hotel': 'Namah Resort'
    },
    'haldwani': {
        'title': 'Haldwani Call Girls - Haldwani Escort Service, Nainital Rd',
        'meta_desc': 'Book verified Haldwani call girls & elite Haldwani escort service on Nainital Road. 100% genuine independent models, luxury hotel outcall & cash on meeting.',
        'h1': 'Haldwani Call Girls - Verified Haldwani Escort Service on Nainital Road',
        'landmark': 'Nainital Road',
        'hotel': 'Hotel Saurabh Candy'
    },
    'kaladhungi': {
        'title': 'Kaladhungi Call Girls - Kaladhungi Escort Service, Corbett',
        'meta_desc': 'Book verified Kaladhungi call girls & elite Kaladhungi escort service near Corbett Museum. 100% genuine models, Camp Corbett outcall & cash on direct meeting.',
        'h1': 'Kaladhungi Call Girls - Verified Kaladhungi Escort Service near Corbett Museum',
        'landmark': 'Corbett Museum',
        'hotel': 'Camp Corbett'
    },
    'rudrapur': {
        'title': 'Rudrapur Call Girls - Rudrapur Escort Service in SIDCUL',
        'meta_desc': 'Book verified Rudrapur call girls & elite Rudrapur escort service in SIDCUL. 100% genuine independent models, Radisson Blu outcall & cash on meeting.',
        'h1': 'Rudrapur Call Girls - Verified Rudrapur Escort Service in SIDCUL',
        'landmark': 'SIDCUL',
        'hotel': 'Radisson Blu'
    },
    'kathgodam': {
        'title': 'Kathgodam Call Girls - Kathgodam Escort Service, Station',
        'meta_desc': 'Book verified Kathgodam call girls & elite Kathgodam escort service near Railway Station. 100% genuine models, Hotel Fiesta outcall & cash on meeting.',
        'h1': 'Kathgodam Call Girls - Verified Kathgodam Escort Service near Railway Station',
        'landmark': 'Railway Station',
        'hotel': 'Hotel Fiesta'
    },
    'kashipur': {
        'title': 'Kashipur Call Girls - Kashipur Escort Service, Bazpur Rd',
        'meta_desc': 'Book verified Kashipur call girls & elite Kashipur escort service on Bazpur Road. 100% genuine independent models, The Manor outcall & cash on meeting.',
        'h1': 'Kashipur Call Girls - Verified Kashipur Escort Service on Bazpur Road',
        'landmark': 'Bazpur Road',
        'hotel': 'The Manor'
    },
    'bajpur': {
        'title': 'Bajpur Call Girls - Bajpur Escort Service, Sugar Mill Rd',
        'meta_desc': 'Book verified Bajpur call girls & elite Bajpur escort service near Sugar Mill. 100% genuine independent models, Green Park hotel outcall & cash on meeting.',
        'h1': 'Bajpur Call Girls - Verified Bajpur Escort Service near Sugar Mill',
        'landmark': 'Sugar Mill',
        'hotel': 'Green Park Hotel'
    },
    'khatima': {
        'title': 'Khatima Call Girls - Khatima Escort Service, Tanakpur Rd',
        'meta_desc': 'Book verified Khatima call girls & elite Khatima escort service on Tanakpur Road. 100% genuine models, Royal Park hotel outcall & cash on direct meeting.',
        'h1': 'Khatima Call Girls - Verified Khatima Escort Service on Tanakpur Road',
        'landmark': 'Tanakpur Road',
        'hotel': 'Royal Park Hotel'
    },
    'sitarganj': {
        'title': 'Sitarganj Call Girls - Sitarganj Escort Service, SIDCUL',
        'meta_desc': 'Book verified Sitarganj call girls & elite Sitarganj escort service in SIDCUL Park. 100% genuine models, Sitarganj Grand outcall & cash on meeting.',
        'h1': 'Sitarganj Call Girls - Verified Sitarganj Escort Service in SIDCUL Park',
        'landmark': 'SIDCUL Park',
        'hotel': 'Hotel Sitarganj Grand'
    },
    'kichha': {
        'title': 'Kichha Call Girls - Kichha Escort Service, Highway Hub',
        'meta_desc': 'Book verified Kichha call girls & elite Kichha escort service on Bareilly Highway. 100% genuine models, Hotel Celebration outcall & cash on meeting.',
        'h1': 'Kichha Call Girls - Verified Kichha Escort Service on Bareilly Highway',
        'landmark': 'Bareilly Highway',
        'hotel': 'Hotel Celebration'
    },
    'jim-corbett': {
        'title': 'Jim Corbett Call Girls - Corbett Escort Service, Bijrani',
        'meta_desc': 'Book verified Jim Corbett call girls & elite Corbett escort service near Bijrani Gate. 100% genuine models, Taj Corbett resort outcall & cash on meeting.',
        'h1': 'Jim Corbett Call Girls - Verified Jim Corbett Escort Service near Bijrani Gate',
        'landmark': 'Bijrani Gate',
        'hotel': 'Taj Corbett Resort'
    },
    'bhowali': {
        'title': 'Bhowali Call Girls - Bhowali Escort Service, Pine Ridge',
        'meta_desc': 'Book verified Bhowali call girls & elite Bhowali escort service on Pine Ridge. 100% genuine models, The White Peaks resort outcall & cash on meeting.',
        'h1': 'Bhowali Call Girls - Verified Bhowali Escort Service on Pine Ridge',
        'landmark': 'Pine Ridge',
        'hotel': 'The White Peaks'
    }
}


HOME_SEO = {
    'title': 'Haldwani Call Girls & Escort Service Across Uttarakhand',
    'meta_desc': 'Browse verified Haldwani call girls & independent escort service across 15 Uttarakhand destinations. Genuine photos, zero upfront fees & cash on arrival.',
    'h1': 'Verified Haldwani Call Girls & Premier Uttarakhand Escort Service Hub'
}

HOME_POPULAR_TAGS = [
    'Haldwani call girls', 'Haldwani escort service', 'Call girls in Haldwani', 'Escorts in Haldwani',
    'escort near me Haldwani', 'call girls near me Haldwani', 'Haldwani escort service open now',
    'Haldwani call girl WhatsApp number', 'call girls website Haldwani', 'Nainital call girls',
    'Nainital escort service', 'Kathgodam call girls', 'Kathgodam escort service', 'Russian escorts Haldwani',
    'Rudrapur call girls', 'Rudrapur escort service', 'Ramnagar call girls', 'Jim Corbett escort service',
    'Bhimtal call girls', 'Bhimtal escort service', 'Kashipur call girls', 'Kashipur escort service',
    'Almora call girls', 'Almora escort service', 'Kaladhungi call girls', 'Bhowali call girls',
    'Khatima call girls', 'Sitarganj call girls', 'Kichha call girls', 'Bajpur call girls',
    'independent escorts Haldwani', 'hotel service call girls Haldwani', '24 hour call girl service Haldwani',
    'cash on arrival Haldwani escorts', 'verified call girls Uttarakhand', 'VIP escorts Haldwani',
    'college call girls Haldwani', 'full night escort service Haldwani'
]
