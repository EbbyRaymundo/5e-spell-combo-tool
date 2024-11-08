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

	Parameters
	----------
	csv_name: str

	Returns
	-------
	spell_table:
		Data frame containing variables specified in Spell within Gestalt_ERD.png.
	dnd_classes:
		Data frame containing variables specified in Class within Gestalt_ERD.png.
	all_availability:
		Data frame containing variables specified in Spell_Class within Gestalt_ERD.png.
	'''

	return


def import_default_xyz(csv_name: str):
	'''
	Read a csv containing the default homebrew XYZ spells

	Parameters
	----------
	csv_name: str

	Returns
	-------
	xyz_table:
		Data frame containing variables specified in XYZ within Gestalt_ERD.png.
	class_availability:
		Data frame containing variables specified in XYZ_Class within Gestalt_ERD.png.
	'''

	return


def import_default_links(csv_name: str):
	'''
	Read a csv containing the default homebrew Link spells

	Parameters
	----------
	csv_name: str

	Returns
	-------
	link_table:
		Data frame containing variables specified in Link within Gestalt_ERD.png.
	class_availability:
		Data frame containing variables specified in Link_Class within Gestalt_ERD.png.
	'''

	return


def import_default_fusions(csv_name: str, spell_table):
	'''
	Read a csv containing the default homebrew Link spells

	Parameters
	----------
	csv_name: str
	spell_table:
		Data frame of the Spell table specified within Gestalt_ERD.png.

	Returns
	-------
	fusion_table:
		Data frame containing variables specified in Link within Gestalt_ERD.png.
	spell_associations:
		Data frame containing variables specified in Spell_Fusion within Gestalt_ERD.png.
	'''

	return


def main():
	
	return 0



if __name__ == "__main__":
	main()