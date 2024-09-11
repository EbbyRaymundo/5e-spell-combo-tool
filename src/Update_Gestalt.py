import sqlite3
import pandas as pd

'''
TODO: potentially use Pandas to get values into dataframes
before inserting them into tables.
'''

def add_XYZ(XYZ: tuple[str, int, str, str, str, str], character_classes: list[int] = None):
	"""
	Add the XYZ spell into the Spell table and associate each XYZ
	spell with every character class unless provided a list to specify.
	Tuple representing XYZ should be in format:

	(<XYZ_name>, <XYZ_rank>, <duration>, <range>, <components>, <description>)

	XYZ_name: str, in title case.
	XYZ_rank: int representing XYZ rank (1-9 typically)
	duration: str, with the time being abbreviated (Min./Hr.). Typically last 1 Hr.
	range: str, with the distance being abbreviated (Ft./Mi.). Can also be "Line of Sight".
	components: str, typically "V, S, M (2 level <rank> spell slots and <rank> sorcery points)".
				Can also specify "May also use a pre-existing <XYZ or spell_name> and n 
				sorcery points" if you can overlay from an existing spell into this XYZ.
				Example: "V, S, M (2 level 4 spell slots and 4 sorcery points. May also
						  also use a pre-existing 'Sparks' XYZ spell and 2 sorcery points)"
	description: str, typically in format of continuous effect, then the effect that occurs
				 when you detach a material.

	Parameters
	----------
	XYZ: tuple[str, int, str, str, str, str]
		XYZ data to be inserted into the database.
	character_classes: list[int]
		character_class_id's of the classes the XYZ is available to. 
		Associated with all classes if no list given.

	Returns
	-------
	new_XYZ_id: int
		spell_id of the newly added XYZ spell
	"""
	with sqlite3.connect("../Gestalt.db") as connection:
		gestalt_cursor = connection.cursor()
		gestalt_cursor.execute("PRAGMA foreign_keys = ON")
		# XYZ have no spell school, do not use concentration, can't be rituals, and have no upcast effects
		gestalt_cursor.execute(
			"""
			INSERT INTO Spell(spell_name, level, casting_time, duration, range, components, description, concentration, ritual, spell_type) 
			VALUES (?, ?, 'Action and Bonus Action', ?, ?, ?, ?, 0, 0, 'XYZ')
			""",
			XYZ
			)

		new_XYZ_id = gestalt_cursor.lastrowid
		spell_class_ids = associate_classes(new_XYZ_id, character_classes, gestalt_cursor)

		gestalt_cursor.executemany("INSERT INTO Spell_Class VALUES (?, ?)", spell_class_ids)

		return new_XYZ_id


def add_Link(Link: list, character_classes: list = None):
	"""
	Add a list of Link spells into the Spell table and associate each Link
	spell with every character class unless provided a list to specify.
	"""

	# TODO: join newly inserted spells with the character classes, then insert those into the Spell_Class table


	return


def add_Fusion(Fusion: list):
	"""
	Add a list of Fusion effects to the Fusion table and their associated
	spells to the Spell_Fusion table.
	"""

	return

def associate_classes(spell_id: int, character_classes: list[int], gestalt_cursor: sqlite3.Cursor):
	"""
	Generate a list of [spell_id, character_class_id] lists
	to associate a spell with character classes. Associates
	a spell with every class if character_classes = None.
	"""
	if not character_classes: # passed an empty list, associate with all classes
		gestalt_cursor.execute("SELECT character_class_id FROM Class")

		# unpack the result to match the character_classes param
		character_classes = [character_class[0] for character_class in gestalt_cursor.fetchall()]

	# return our list of [spell_id, character_class_id] lists
	return [[spell_id, character_class_id] for character_class_id in character_classes]

	
def main():

	# (<XYZ_name>, <XYZ_rank>, <duration>, <range>, <components>, <description>)
	starlight_blessing = (
		"Starlight Blessing",
		1,
		"1 Hr.",
		"Self",
		"V, S, M (2 level 1 spell slots and 1 sorcery point)",
		"A hole in space opens above the caster’s head, revealing a "
		+ "beautiful, starry nebula. While this spell still has overlay "
		+ "materials, you may reroll one attack roll per turn. You may "
		+ "not know the result of the first attack roll and must take "
		+ "the second roll. As a reaction, you may detach one overlay "
		+ "material to make an opponent reroll an attack roll before the "
		+ "result is declared."
		)
	add_XYZ(starlight_blessing, [0, 1, 2, 3, 4])

	return 0



if __name__ == "__main__":
	main()