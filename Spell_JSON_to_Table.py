import sqlite3
import pandas as pd

"""
JSON is in format:

{
	"spell_1" {
		"casting_time": "action_type",
		"components": "spell_components",
		"description: "spell_description",
		"duration": "spell_duration",
		"level": spell_level (int),
		"range": "spell_range",
		"school": "spell_school"
	}
	"spell_2" {
		...
	}
	...
}

To format for the database:
- Remove concentration from description and add as
has_concentration boolean.
- Add has_upcast_effect as boolean.
- Add spell_type (they're all "standard")
"""
	

def pandas_format_JSON(JSON_name: str):
	"""
	Read the JSON file into a dataframe directly. Use dataframe
	operations to add the missing data members for each spell.
	"""

	spell_table = pd.read_json(JSON_name).transpose()

	# pull the spell names out of the row indices, give them their own 
	# named column, and change row indices into auto-incrementing integers
	spell_table.reset_index(inplace = True, names = "spell")
	spell_table["has_upcast_effect"] = spell_table["description"].apply(lambda spell_description: "At Higher Levels" in spell_description)
	spell_table["concentration"] = spell_table["duration"].apply(lambda spell_duration: "Concentration" in spell_duration)

	# "Concentration, " can be cut out of the duration since it doesn't entail any further description, unlike "has_upcast_effect"
	spell_table["duration"] = spell_table["duration"].apply(lambda duration: duration.replace("Concentration, ", "").capitalize())
	spell_table["spell_type"] = "standard" # every spell is standard since we'll add XYZ, Fusion, Links later

	return spell_table.infer_objects(copy = False) # may have to force the "Object" types into strings later.

def main():
	
	main_spell_table = pandas_format_JSON("PHB_spell_data/spells.json")
	#python_format_JSON()


if __name__ == "__main__":
	main()