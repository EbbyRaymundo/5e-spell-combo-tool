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
	

def format_spell_JSON(JSON_name: str):
	"""
	Read the JSON file into a dataframe directly. Use dataframe
	operations to add the missing data members for each spell.
	"""

	spell_table = pd.read_json(JSON_name).transpose()

	# pull the spell names out of the row indices, give them their own 
	# named column, and change row indices into auto-incrementing integers
	spell_table.reset_index(inplace = True, names = "spell")

	# TODO: Do the entire upcast effect in the "upcast_effect" column
	# insead of just doing a boolean here. Will have to do a substring
	# and trim out the upcast portion. Remove "At Higher Levels" since
	# that's implicit if it has an upcast effect.
	spell_table["upcast_effect"] = spell_table["description"].apply(lambda spell_description: "At Higher Levels" in spell_description)
	spell_table["concentration"] = spell_table["duration"].apply(lambda spell_duration: "Concentration" in spell_duration)

	# TODO: replace this line with the Pandas .replace() function.
	# "Concentration, " can be cut out of the duration since it doesn't entail any further description, unlike "has_upcast_effect"
	spell_table["duration"] = spell_table["duration"].apply(lambda duration: duration.replace("Concentration, ", "").capitalize())
	spell_table["spell_type"] = "standard" # every spell is standard since we'll add XYZ, Fusion, Links later

	return spell_table.infer_objects(copy = False) # may have to force the "Object" types into strings later.


def format_spell_csv(csv_name: str):

	spell_table = pd.read_csv(
		csv_name,
		header = 0,
		names = 
			[
				"spell_name",
				"level",
				"casting_time",
				"duration",
				"school",
				"range",
				"components",
				"classes",
				"optional_classes",
				"description",
				"upcast_effect"
			],
		converters = # removes any whitespace issues immediately
			{
				"spell_name": str.strip,
				"level": str.strip,
				"casting_time": str.strip,
				"duration": str.strip,
				"school": str.strip,
				"range": str.strip,
				"components": str.strip,
				"classes": str.strip,
				"optional_classes": str.strip,
				"description": str.strip,
				"upcast_effect": str.strip
			},
		keep_default_na = False) # leave blank spots blank
	
	spell_table["level"].replace( # numeric data will be considerably easier to use
		{
			"Cantrip": 0,
			"1st": 1,
			"2nd": 2,
			"3rd": 3,
			"4th": 4,
			"5th": 5,
			"6th": 6,
			"7th": 7,
			"8th": 8,
			"9th": 9
   		},
		inplace = True
	)

	# useless text; "At Higher Levels" in an upcast column is just redundant
	spell_table["upcast_effect"] = spell_table["upcast_effect"].str.removeprefix("At Higher Levels. ")

	# make boolean concentration column and clean up afterwards
	spell_table["concentration"] = spell_table["duration"].str.contains("Concentration")
	spell_table["duration"] = spell_table["duration"].str.removeprefix("Concentration, ")
	spell_table["duration"] = spell_table["duration"].str.capitalize()
	spell_table["duration"].replace(
		{
			"minute": "Min.",
			"minutes": "Min.",
			"hours": "Hr.",
			"hour": "Hr."
		},
		inplace = True
	)

	# make the boolean ritual column and clean up afterwards
	spell_table["ritual"] = spell_table["school"].str.contains("ritual")
	spell_table["school"] = spell_table["school"].str.removesuffix(" (ritual)")

	return spell_table

def create_spell_table(spell_DataFrame: pd.core.frame.DataFrame):

	connection = sqlite3.connect("Gestalt.db")

	spell_DataFrame.to_sql(name = "Spell", con = connection, index_label = "spell_id")

	connection.close()

def main():
	
	#main_spell_table = format_spell_JSON("spell_data/spells.json")
	#create_spell_table(main_spell_table)
	main_spell_table = format_spell_csv("spell_data/all_5e_spells.csv")
	main_spell_table.to_html("main_spell_table.html")

	return 0


if __name__ == "__main__":
	main()