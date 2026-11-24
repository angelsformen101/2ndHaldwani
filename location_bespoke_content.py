"""
Bespoke Location Editorial Content and Unique SEO Identity for CityHaldwani.com
Merges Part 1, Part 2, and Part 3 into unified BESPOKE_LOCATION_DATA dictionary.
Eliminates all template-like duplication, provides unique H1s, titles, metas, intros, and section structures.
"""

from bespoke_data_part1 import PART1_DATA
from bespoke_data_part2 import PART2_DATA
from bespoke_data_part3 import PART3_DATA

BESPOKE_LOCATION_DATA = {}
BESPOKE_LOCATION_DATA.update(PART1_DATA)
BESPOKE_LOCATION_DATA.update(PART2_DATA)
BESPOKE_LOCATION_DATA.update(PART3_DATA)

print(f"Loaded BESPOKE_LOCATION_DATA with all {len(BESPOKE_LOCATION_DATA)} locations successfully!")
