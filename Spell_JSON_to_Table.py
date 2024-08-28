import json
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

	return spell_table.infer_objects(copy = False)


def python_format_JSON(JSON_name: str):
	"""
	Use the JSON library in Python to read in the JSON as a
	dictionary, then format the dictionary to easily convert
	into a table. Due to a revision that uses Pandas instead,
	this function is no longer necessary.
	"""
	with open(JSON_name, "r") as spells_file:
		spells = json.load(spells_file)

	for spell, values in spells.items():

		# True and False will be changed in a later step
		# with R since sqlite and R use TRUE and FALSE
		if "Concentration, " in values["casting_time"]:
			values["casting_time"] = values["casting_time"].replace("Concentration, ", "")
			spell["concentration": False]

		else:
			values["concentration": True]

		values["has_upcast_effect": True] if "At Higher Levels" in values["description"] else values["has_upcast_effect": False]

		# Every spell in this JSON is a standard spell. Special spells will be added later.
		values["spell_type": "standard"]

	return spells

def main():
	
	main_spell_table = pandas_format_JSON("PHB_spell_data/spells.json")
	#python_format_JSON()


if __name__ == "__main__":
	main()