import sqlite3
import pandas as pd



def format_spell_JSON(JSON_name: str):
	"""
	Read the JSON file into a dataframe. Use dataframe
	operations to add the missing data members for each spell.
	Clean entries to remove unnecessary text from strings.

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

	"""
	Read the csv from 5etools containing all spells currently available on the website,
	clean entries to remove unnecessary information or create additional columns,
	create Class and Spell_Class junction table.

	To format the csv for the database:
	- Rename column names to those matching the Gestalt ERD
	- Remap all string names in "level" to their corresponding spell level as integers (cantrips == 0)
	- Abbreviate "hour(s)" and "minute(s)" in "duration" column
	- Remove "Concentration, " from "duration" and give it its own boolean column
	- Remove " (ritual)" from "school" and give it its own boolean column
	- Abbreviate "foot", "feet", "mile(s)" in "range" column
	- Listify "character_class" and "optional_classes" column, expand them, pivot longer, then full outer join
	- Remove "At Higher Levels. " from "upcast_effect"
	- Create a table with all spellcasting classes (except you Monks that only have one spell)
		- Subclasses are not considered since that data is irrelevant for to the purpose of the database
	- Create a junction table between the spells and classes
	"""

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
				"character_class",
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
				"character_class": str.strip,
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
	spell_table["upcast_effect"] = spell_table["upcast_effect"].str.removeprefix("At Higher Levels. ").str.strip()

	# make boolean concentration column and clean up afterwards
	spell_table["concentration"] = spell_table["duration"].str.contains("Concentration")
	spell_table["duration"] = spell_table["duration"].str.removeprefix("Concentration, ").str.capitalize().str.strip()

	# "casting_time" is already abbreviated, so we'll be consistent with abbreviations
	spell_table["duration"] = spell_table["duration"].str.replace(pat = "minute(s)?", repl = "Min.", regex = True)
	spell_table["duration"] = spell_table["duration"].str.replace(pat = "hour(s)?", repl = "Hr.", regex = True)

	# chose to use abbreviations in the "duration" column so I should be consistent
	spell_table["range"] = spell_table["range"].str.replace(pat = "feet|foot", repl = "Ft.", regex = True)
	spell_table["range"] = spell_table["range"].str.replace(pat = "mile(s)?", repl = "Mi.", regex = True)

	# make the boolean ritual column and clean up afterwards
	spell_table["ritual"] = spell_table["school"].str.contains("ritual")
	spell_table["school"] = spell_table["school"].str.removesuffix(" (ritual)").str.strip()

	# make the spell_type column; all imported spells are "standard" since we'll be adding
	# the Links and XYZ ourselves
	spell_table["spell_type"] = "standard"

	# listify, expand, merge, and clear empty rows with the "character_class" and "optional_classes" columns

	class_availability = spell_table["character_class"].str.split(", ", expand = True) # listify and expand the classes column
	class_availability = pd.concat([spell_table["spell_name"], class_availability], axis = 1) # join with corresponding spell name
	class_availability = class_availability.melt(id_vars = "spell_name", value_name = "character_class").drop("variable", axis = 1) # pivot longer
	# some rows have to stay as None for now since the spell would get dropped entirely otherwise.
	# a few of them are optional only (I think due to unearthed arcana shenanigans)
	class_availability.dropna(axis = 0, inplace = True)

	optional_availability = spell_table["optional_classes"].str.split(", ", expand = True) # listify and expand
	optional_availability = pd.concat([spell_table["spell_name"], optional_availability], axis = 1) # join with corresponding spell name
	optional_availability = optional_availability.melt(id_vars = "spell_name", value_name = "character_class").drop("variable", axis = 1) # pivot longer
	optional_availability.dropna(axis = 0, inplace = True)

	all_availability = pd.merge(class_availability, optional_availability, how = "outer")
	all_availability.dropna(inplace = True)
	all_availability = all_availability[all_availability.character_class != ""]

	dnd_classes = pd.DataFrame(data = ["Wizard", "Cleric", "Sorcerer", "Bard", "Druid", "Artificer", "Paladin", "Warlock", "Ranger"], columns = ["character_class"])
	
	spell_table.drop(columns = ["character_class", "optional_classes"], inplace = True)

	# outer join all_availability to dnd_classes, then outer join spell_table to result
	# reset indices so that we can have index columns for both
	spell_table.reset_index(names = "spell_id", inplace = True)
	dnd_classes.reset_index(names = "character_class_id", inplace = True)

	junction_table = pd.merge(dnd_classes, all_availability, how = "outer", on = "character_class")

	# only need the index and spell_name from our main table
	junction_table = pd.merge(junction_table, spell_table[["spell_id", "spell_name"]], how = "outer", on = "spell_name")
	junction_table["character_class_id"] = junction_table["character_class_id"].convert_dtypes(convert_integer = True)
	junction_table.drop(columns = ["character_class", "spell_name"], inplace = True)

	spell_table.to_html("images/Spell_table.html")
	dnd_classes.to_html("images/Class_table.html")
	junction_table.to_html("images/Spell_Class_table.html")

	return spell_table, dnd_classes, junction_table


def create_spell_table(spell_DataFrame: pd.core.frame.DataFrame):

	with sqlite3.connect("Gestalt.db") as connection:
		spell_DataFrame.to_sql(name = "Spell", con = connection, index = False)


def create_class_table(class_DataFrame: pd.core.frame.DataFrame):

	with sqlite3.connect("Gestalt.db") as connection:
		class_DataFrame.to_sql(name = "Class", con = connection, index = False)

def create_spell_class_table(spell_class_DataFrame):

	with sqlite3.connect("Gestalt.db") as connection:
		spell_class_DataFrame.to_sql(name = "Spell_Class", con = connection, index = False)

def main():
	
	#main_spell_table = format_spell_JSON("spell_data/spells.json")
	#create_spell_table(main_spell_table)
	main_spell_table, classes_table, spell_class_table = format_spell_csv("spell_data/all_5e_spells.csv")
	create_spell_table(main_spell_table)
	create_class_table(classes_table)
	create_spell_class_table(spell_class_table)

	return 0

if __name__ == "__main__":
	main()