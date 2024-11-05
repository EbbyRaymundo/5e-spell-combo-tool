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

	return

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

	master_table = (
		pl.scan_csv(
			source = csv_name,
			has_header = True,
			null_values = "",
			new_columns = [
					"spell_name",
					"level",
					"casting_time",
					"duration",
					"school",
					"range",
					"components",
					"character_classes",
					"optional_classes",
					"description",
					"upcast_effect"
				]
		)
	)

	spell_table = (master_table.select(
			
		pl.col("spell_name").str.strip_chars(),

		pl.col("level").str.strip_chars().str.replace_many({
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
		)
		.cast(pl.UInt32),

		pl.col("casting_time").str.strip_chars().str.replace_all(
			pattern = "Bonus", 
			value = "Bonus Action",
			literal = True 
		),

		pl.col("duration").str.strip_chars().str.strip_prefix("Concentration, ")
		.str.replace_all(
			pattern = "minute(s)?",
			value = "Min."
		)
		.str.replace_all(
			pattern = "hour(s)?",
			value = "Hr."
		)
		.map_elements(lambda duration: duration.capitalize(), return_dtype = pl.String),

		pl.col("school").str.strip_chars().str.strip_suffix(" (ritual)"),

		pl.col("range").str.strip_chars().str.replace_all(
			pattern = "feet|foot",
			value = "Ft."
		)
		.str.replace_all(
			pattern = "mile(s)?",
			value = "Mi."
		),

		pl.col("components").str.strip_chars(),

		pl.col("description").str.strip_chars(),

		pl.col("upcast_effect").str.strip_chars().str.strip_prefix("At Higher Levels. "),

		pl.col("duration").str.contains("Concentration").alias("concentration"),

		pl.col("school").str.contains("ritual").alias("ritual")
		)
		.with_row_index("spell_id")
	)
	
	# create table for character_class and corresponding character_class_id
	dnd_classes = (
		pl.LazyFrame(
			data = {
				"character_class": [
					"Wizard", "Cleric", "Sorcerer", 
					"Bard", "Druid", "Artificer", 
					"Paladin", "Warlock", "Ranger"
				]
			},
			schema = {"character_class": pl.String}
		)
		.with_row_index("character_class_id")
	)
	
	# concat spell_id with listified character_classes,
	# then do the same with spell_id and listified optional_classes,
	# then merge these two dataframes together
	class_availability = (
		pl.concat([
				spell_table.select(pl.col("spell_id")),
				master_table.select(
					pl.col("character_classes")
					.str.strip_chars()
					.str.split(by = ", "))
			],
			how = "horizontal"
		)
		.explode("character_classes")
		.drop_nulls()
		# the spell_id sorting is preserved from the demolition process so this
		# will produce defined behavior
		.merge_sorted(
			# repeating same process as above
			pl.concat([
					spell_table.select(pl.col("spell_id")),
					master_table.select(
						pl.col("optional_classes")
						.str.strip_chars()
						.str.split(by = ", ")
						.alias("character_classes"))
	 			],
				how = "horizontal"
			)
			.explode("character_classes")
			.drop_nulls(),
			key = "spell_id"
		)
		.unique() # drop dupes from merged result
		.select(
			pl.col("spell_id"),
			pl.col("character_classes").str.replace_many({
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
			)
			.cast(pl.UInt32)
			.alias("character_class_id")
		)
	)


	return spell_table.collect(), dnd_classes.collect(), class_availability.collect()


def import_default_xyz(csv_name: str):
	'''
	Read a csv containing the default homebrew XYZ spells
	'''

	""" xyz_table = pd.read_csv(
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
	class_availability = class_availability.melt(id_vars = "xyz_id", value_name = "character_class_id").drop("variable", axis = "columns") # pivot longer """

	return #xyz_table, class_availability


def import_default_links(csv_name: str):
	'''
	Read a csv containing the default homebrew Link spells
	'''
	"""link_table = pd.read_csv(
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
 	"""
	return #link_table, class_availability


def import_default_fusions(csv_name: str):
	# TODO: read in the default Fusions csv, construct a table out of it
	#		then search for the referenced spells in main spell table,
	#		and create a junction table.

	"""fusion_table = pd.DataFrame()
	spell_fusion_table = pd.DataFrame()"""

	return #fusion_table, spell_fusion_table


def main():
	
	#spell_table, dnd_classes, all_availability = format_spell_csv("../spell_data/all_5e_spells.csv")
	#import_default_xyz("../spell_data/kites_xyz_spells.csv")
	#import_default_links("../spell_data/aleisters_link_spells.csv")
	polar_spells, polars_classes, polars_availability = format_spell_csv("../spell_data/all_5e_spells.csv")
	#print(polar_spells.head(10))
	#sprint(polars_classes.height)
	#print(polars_classes)

	return 0


if __name__ == "__main__":
	main()