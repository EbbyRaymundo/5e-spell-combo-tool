import pandas as pd
import polars as pl



'''
This file is for creating the dataframes that will populate the
database tables. It can read either a JSON that is provided in
the spell_data folder. It can also read a CSV from 5etools with
any set of spells.
'''
def format_spell_JSON(JSON_name: str):
	'''
	Read the JSON file containing initial batch of spells into
	a dataframe. Use dataframe operations to add the missing data
	members for each spell. Clean entries to remove unnecessary
	text from strings.

	TODO: rework function to accept JSON from 5etools instead
	of where they were originally sourced from :^)


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
	'''

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
	'''
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
	'''

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
			}
		)
	
	spell_table = spell_table.replace(
		{"level": {
			"Cantrip": '0',
			"1st": '1',
			"2nd": '2',
			"3rd": '3',
			"4th": '4',
			"5th": '5',
			"6th": '6',
			"7th": '7',
			"8th": '8',
			"9th": '9'
			}
   		}
	).astype({"level": "int64"}, copy = False)

	spell_table.rename_axis("spell_id", inplace = True)

	# useless text; "At Higher Levels" in an upcast column is just redundant
	spell_table["upcast_effect"] = spell_table["upcast_effect"].str.removeprefix("At Higher Levels. ").str.strip()

	# make boolean concentration column and clean up afterwards
	spell_table["concentration"] = spell_table["duration"].str.contains("Concentration")
	spell_table["duration"] = spell_table["duration"].str.removeprefix("Concentration, ").str.capitalize().str.strip()

	# TODO: review this line
	# Replacing "Bonus" with "Bonus Action" for casting_time
	spell_table.replace({"casting_time": "Bonus"}, "Bonus Action", inplace = True)

	# "casting_time" is already abbreviated, so we'll be consistent with abbreviations
	spell_table["duration"] = spell_table["duration"].str.replace(pat = "minute(s)?", repl = "Min.", regex = True)
	spell_table["duration"] = spell_table["duration"].str.replace(pat = "hour(s)?", repl = "Hr.", regex = True)

	# chose to use abbreviations in the "duration" column so I should be consistent
	spell_table["range"] = spell_table["range"].str.replace(pat = "feet|foot", repl = "Ft.", regex = True)
	spell_table["range"] = spell_table["range"].str.replace(pat = "mile(s)?", repl = "Mi.", regex = True)

	# make the boolean ritual column and clean up afterwards
	spell_table["ritual"] = spell_table["school"].str.contains("ritual")
	spell_table["school"] = spell_table["school"].str.removesuffix(" (ritual)").str.strip()


	# construct DataFrame for the Class table
	dnd_classes = pd.DataFrame(data = ["Wizard", "Cleric", "Sorcerer", "Bard", "Druid", "Artificer", "Paladin", "Warlock", "Ranger"], columns = ["character_class"])
	dnd_classes.rename_axis("character_class_id", inplace = True)

	# listify, expand, and merge the class_availability with its corresponding spell_id

	# listify and expand the classes column
	class_availability = spell_table["character_class"].str.split(", ", expand = True)
	class_availability = pd.concat([spell_table.index.to_series(), class_availability], axis = "columns")
	class_availability = class_availability.melt(id_vars = "spell_id", value_name = "character_class").drop("variable", axis = "columns") # pivot longer
	class_availability.dropna(inplace = True)

	# repeat for the optional_availability column
	optional_availability = spell_table["optional_classes"].str.split(", ", expand = True) # listify and expand
	optional_availability = pd.concat([spell_table.index.to_series(), optional_availability], axis = "columns")
	optional_availability = optional_availability.melt(id_vars = "spell_id", value_name = "character_class").drop("variable", axis = "columns") # pivot longer
	optional_availability.dropna(inplace = True)

	all_availability = pd.merge(class_availability, optional_availability, how = "outer")

	all_availability.replace(to_replace = "", value = pd.NA, inplace = True)
	all_availability.dropna(inplace = True)

	# this replaces with the corresponding character_class_id in
	# the dnd_classes dataframe
	all_availability = all_availability.replace(
		{"character_class": {
			"Wizard": '0',
			"Cleric": '1',
			"Sorcerer": '2',
			"Bard": '3',
			"Druid": '4',
			"Artificer": '5',
			"Paladin": '6',
			"Warlock": '7',
			"Ranger": '8'
			}
   		}
	).astype({"character_class": "int64"}, copy = False)

	all_availability.reset_index(drop = True, inplace = True) # index is spotty from the dropna()
	# need to appropriately rename the column after remapping
	all_availability.rename(columns = {"character_class": "character_class_id"}, inplace = True)
	
	spell_table.drop(columns = ["character_class", "optional_classes"], inplace = True) # new tables made, no longer needed
	# empty upcast values were never filled with NAs by pandas in read_csv for some reason
	spell_table.replace(to_replace = "", value = pd.NA, inplace = True)


	return spell_table, dnd_classes, all_availability

def format_spell_csv_pl(csv_name: str):

	'''
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
	'''

	spell_table = (
		pl.scan_csv(
			source = csv_name,
			has_header = True,
			new_columns = 
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
				]
		)
		.with_columns(
			pl.col("duration").str.contains("Concentration").alias("concentration"),
			pl.col("school").str.contains("ritual").alias("ritual"),
			pl.col("spell_name").str.strip_chars(),
			pl.col("level").str.strip_chars().str.replace_many(
				{
					"Cantrip": '0',
					"1st": '1',
					"2nd": '2',
					"3rd": '3',
					"4th": '4',
					"5th": '5',
					"6th": '6',
					"7th": '7',
					"8th": '8',
					"9th": '9'
				}
			),
			pl.col("casting_time").str.strip_chars().str.replace_all(
				pattern = "Bonus", 
				value = "Bonus Action",
				literal = True 
			),
			pl.col("duration").str.strip_chars().str.strip_prefix("Concentration, ").str.replace_all(
				pattern = "minute(s)?",
				value = "Min."
			).str.replace_all(
				pattern = "hour(s)?",
				value = "Hr."
			)
		)
	)
	
	'''
	spell_table.rename_axis("spell_id", inplace = True)

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


	# construct DataFrame for the Class table
	dnd_classes = pd.DataFrame(data = ["Wizard", "Cleric", "Sorcerer", "Bard", "Druid", "Artificer", "Paladin", "Warlock", "Ranger"], columns = ["character_class"])
	dnd_classes.rename_axis("character_class_id", inplace = True)

	# listify, expand, and merge the class_availability with its corresponding spell_id

	# listify and expand the classes column
	class_availability = spell_table["character_class"].str.split(", ", expand = True)
	class_availability = pd.concat([spell_table.index.to_series(), class_availability], axis = "columns")
	class_availability = class_availability.melt(id_vars = "spell_id", value_name = "character_class").drop("variable", axis = "columns") # pivot longer
	class_availability.dropna(inplace = True)

	# repeat for the optional_availability column
	optional_availability = spell_table["optional_classes"].str.split(", ", expand = True) # listify and expand
	optional_availability = pd.concat([spell_table.index.to_series(), optional_availability], axis = "columns")
	optional_availability = optional_availability.melt(id_vars = "spell_id", value_name = "character_class").drop("variable", axis = "columns") # pivot longer
	optional_availability.dropna(inplace = True)

	all_availability = pd.merge(class_availability, optional_availability, how = "outer")

	all_availability.replace(to_replace = "", value = pd.NA, inplace = True)
	all_availability.dropna(inplace = True)

	# this replaces with the corresponding character_class_id in
	# the dnd_classes dataframe
	all_availability = all_availability.replace(
		{"character_class": {
			"Wizard": '0',
			"Cleric": '1',
			"Sorcerer": '2',
			"Bard": '3',
			"Druid": '4',
			"Artificer": '5',
			"Paladin": '6',
			"Warlock": '7',
			"Ranger": '8'
			}
   		}
	).astype({"character_class": "int64"}, copy = False)

	all_availability.reset_index(drop = True, inplace = True) # index is spotty from the dropna()
	# need to appropriately rename the column after remapping
	all_availability.rename(columns = {"character_class": "character_class_id"}, inplace = True)
	
	spell_table.drop(columns = ["character_class", "optional_classes"], inplace = True) # new tables made, no longer needed
	# empty upcast values were never filled with NAs by pandas in read_csv for some reason
	spell_table.replace(to_replace = "", value = pd.NA, inplace = True)

	'''

	return spell_table.collect()


def import_default_xyz(csv_name: str):
	'''
	Read a csv containing the default homebrew XYZ spells
	'''
	xyz_table = pd.read_csv(
	csv_name,
	header = 0,
	converters = # removes any whitespace issues immediately
		{
			"xyz_name": str.strip,
			"casting_time": str.strip,
			"duration": str.strip,
			"range": str.strip,
			"components": str.strip,
			"description": str.strip
		}
	)
	xyz_table.rename_axis("xyz_id", inplace = True, axis = "index")

	# dtype = {"rank": "int64"} not working in the read_csv()
	xyz_table = xyz_table.astype({"rank": "int64"})

	# 0:4 correspond to Wizard, Cleric, Sorcerer, Bard, Druid class_id's
	class_availability = pd.DataFrame(data = list(range(5)), columns = ["character_class_id"]).transpose()
	# bind a repeating number of rows equal to the row count of the xyz_table
	class_availability = pd.concat([class_availability] * xyz_table.shape[0]).reset_index(drop = True)

	# listify and expand the classes column
	class_availability = pd.concat([xyz_table.index.to_series(), class_availability], axis = "columns")
	class_availability = class_availability.melt(id_vars = "xyz_id", value_name = "character_class_id").drop("variable", axis = "columns") # pivot longer

	return xyz_table, class_availability


def import_default_links(csv_name: str):
	'''
	Read a csv containing the default homebrew Link spells
	'''
	link_table = pd.read_csv(
	csv_name,
	header = 0,
	converters = # removes any whitespace issues immediately
		{
			"link_name": str.strip,
			"casting_time": str.strip,
			"duration": str.strip,
			"range": str.strip,
			"components": str.strip,
			"description": str.strip
		}
	)
	link_table.rename_axis("link_id", inplace = True, axis = "index")

	# dtype = {"rating": "int64"} not working in the read_csv()
	link_table = link_table.astype({"rating": "int64"})

	# 0:8 correspond to all spellcasting class_id's
	class_availability = pd.DataFrame(data = list(range(9)), columns = ["character_class_id"]).transpose()
	# bind a repeating number of rows equal to the row count of the link_table
	class_availability = pd.concat([class_availability] * link_table.shape[0]).reset_index(drop = True)

	# listify and expand the classes column
	class_availability = pd.concat([link_table.index.to_series(), class_availability], axis = "columns")
	class_availability = class_availability.melt(id_vars = "link_id", value_name = "character_class_id").drop("variable", axis = "columns") # pivot longer

	return link_table, class_availability



def main():
	
	#format_spell_csv("../spell_data/all_5e_spells.csv")
	#import_default_xyz("../spell_data/kites_xyz_spells.csv")
	#import_default_links("../spell_data/aleisters_link_spells.csv")
	polar_spells = format_spell_csv_pl("../spell_data/all_5e_spells.csv")
	print(polar_spells.head(10))

	return 0


if __name__ == "__main__":
	main()