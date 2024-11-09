import sqlite3
import pandas as pd

'''
This file adds new spells into Gestalt.db and handles
the appropriate junction table insertions.
'''


#TODO: convert to pandas implementation
def add_spell(
	connection: sqlite3.Connection,
	spell,
	character_classes: list[int] = None
):
	'''
	Add the standard spell into the Spell table and associate
	the spell with every character class unless provided a list
	to specify otherwise.
	
	Provided spell format should match the variables specified for the Spell
	table specified in Gestalt_ERD.png

	spell_name: str, in title case.
	level: int.
	casting_time: str, being "Action", "Bonus Action", "Reaction", or an amount
				  of time being abbreviated (Min./Hr.).
	duration: str, with the time being abbreviated (Min./Hr.).
	school: str, capitalized.
	range: str, with the distance being abbreviated (Ft./Mi.).
	components: str, in format "V, S, M (<material components>)".
	description: str.
	upcast_effect: str or None. Description for higher level effects, None type otherwise.
	concentration: bool.
	ritual: bool.

	Parameters
	----------
	connection: sqlite3.Connection
		Database connection to Gestalt.db.
	spell:
		New spell in the format specified above and in the Spell table
		within Gestalt_ERD.png.
	character_classes: list[int]
		character_class_id's of the classes the spell is available to. 
		Associated with all spellcasting classes if no list given.

	Returns
	-------
	new_spell_id: int
	'''
	gestalt_cursor = connection.cursor()
	gestalt_cursor.execute("PRAGMA foreign_keys = ON")
	
	gestalt_cursor.execute(
		"""
		INSERT INTO Spell(spell_name, level, casting_time, duration, school, range, components, description, upcast_effect, concentration, ritual) 
		VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
		""",
		spell
	)
	
	new_spell_id = gestalt_cursor.lastrowid

	spell_class_ids = associate_classes(new_spell_id, character_classes, gestalt_cursor)

	gestalt_cursor.executemany("INSERT INTO Spell_Class VALUES (?, ?)", spell_class_ids)

	return new_spell_id

	return


def add_XYZ(connection: sqlite3.Connection, xyz, character_classes: list[int] = None):
	'''
	Add the XYZ spell into the XYZ table and associate the XYZ
	spell with every character class unless provided a list to
	specify otherwise.

	Provided XYZ format should match the variables specified for the XYZ
	table specified in Gestalt_ERD.png

	xyz_name: str, in title case.
	rank: int representing XYZ rank (1-9 typically).
	casting_time: str representing the action economy to cast (typically "Action and Bonus Action").
	duration: str, with the time being abbreviated (Min./Hr.). Typically last 1 Hr.
	range: str, with the distance being abbreviated (Ft./Mi.). Can also be "Line of sight".
	components: str, typically "V, S, M (2 level <rank> spell slots and <rank> sorcery points)".
				Can also specify "May also use a pre-existing <XYZ or spell_name> and n 
				sorcery points" if you can overlay from an existing spell into this XYZ.
				Example: "V, S, M (2 level 4 spell slots and 4 sorcery points. May also
						  also use a pre-existing 'Sparks' XYZ spell and 2 sorcery points)".
	description: str, typically in format of continuous effect, then the effect that occurs
				 when you detach a material.

	Parameters
	----------
	connection: sqlite.Connection
		Database connection to Gestalt.db.
	XYZ:
		New XYZ spell in the format specified above and in the XYZ table
		within Gestalt_ERD.png.
	character_classes: list[int]
		character_class_id's of the classes the XYZ is available to. 
		Associated with all full casters if no list given.

	Returns
	-------
	new_XYZ_id: int
	'''
	gestalt_cursor = connection.cursor()
	gestalt_cursor.execute("PRAGMA foreign_keys = ON")

	# XYZ have no spell school, do not use concentration, can't be rituals, and have no upcast effects
	gestalt_cursor.execute(
		"""
		INSERT INTO XYZ(xyz_name, rank, casting_time, duration, range, components, description) 
		VALUES (?, ?, ?, ?, ?, ?, ?)
		""",
		xyz
	)
	
	new_xyz_id = gestalt_cursor.lastrowid

	# if no specifying class list given, use default character_class_id's for
	# XYZ spells (any full caster class that can obtain 9th lvl spells)
	if not character_classes:
		character_classes = list(*range(5)) # id's: [Wizard, Cleric, Sorc, Bard, Druid]

	xyz_class_ids = associate_classes(new_xyz_id, character_classes, gestalt_cursor)

	gestalt_cursor.executemany("INSERT INTO XYZ_Class VALUES (?, ?)", xyz_class_ids)

	return new_xyz_id


def add_Link(connection: sqlite3.Connection, link, character_classes: list[int] = None):
	'''
	Add the Link spell into the Spell table and associate the Link
	spell with every character class unless provided a list to specify.

	Provided Link format should match the variables specified for the Link
	table specified in Gestalt_ERD.png.

	link_name: str, in title case.
	rating: int representing the amount of materials required to cast the Link spell.
	casting_time: str, typically "Action"
	duration: str, with the time being abbreviated (Min./Hr.). Typically last 1 Min. * Link rating.
	range: str, with the distance being abbreviated (Ft./Mi.). Can also be "Line of Sight".
	components: str, typically "V, S, M (<Link materials>)".
				Example: "V, S, M (1 Synchro spell and 1 spell)"
	description: str, typically in format "As an Action, link <Link materials>", then specify
				 the Link effect.

	Parameters
	----------
	connection: sqlite3.Connection
		Database connection to Gestalt.db.
	Link:
		New Link spell in the format specified above and in the Link table
		within Gestalt_ERD.png.
	character_classes: list[int]
		character_class_id's of the classes the Link is available to. 
		Associated with all classes if no list given. Links are typically
		associated with ALL spellcasting classes and only have an
		Intelligence attribute requirement.

	Returns
	-------
	new_Link_id: int
	'''
	gestalt_cursor = connection.cursor()
	gestalt_cursor.execute("PRAGMA foreign_keys = ON")

	# XYZ have no spell school, do not use concentration, can't be rituals, and have no upcast effects
	gestalt_cursor.execute(
		"""
		INSERT INTO Link(link_name, rating, casting_time, duration, range, components, description) 
		VALUES (?, ?, ?, ?, ?, ?, ?)
		""",
		link
	)

	new_link_id = gestalt_cursor.lastrowid

	link_class_ids = associate_classes(new_link_id, character_classes, gestalt_cursor)

	gestalt_cursor.executemany("INSERT INTO Link_Class VALUES (?, ?)", link_class_ids)

	return new_link_id


def add_Fusion(connection: sqlite3.Connection, fusion, constituent_spells: list[int]):
	'''
	Add the Fusion into the Fusion table and associate the Fusion with all of
	its constituent spells in the Spell_Fusion table.
	
	Provided Fusion format should match the variables specified for the Fusion
	table specified in Gestalt_ERD.png

	fusion_name: str, in title case
	duration: str, with the time being abbreviated (Min./Hr.).
	range: str, with the distance being abbreviation (Ft./Mi.).
	description: str.
	concentration: bool.

	Parameters
	----------
	connection: sqlite3.Connection
		Database connection to Gestalt.db.
	fusion:
		New Fusion spell in the format specified above and in the Fusion table
		within Gestalt_ERD.png.
	constituent_spells: list[int]
		spell_id's of spells used to create the fusion.

	Returns
	-------
	new_fusion_id: int
	'''
	gestalt_cursor = connection.cursor()
	gestalt_cursor.execute("PRAGMA foreign_keys = ON")

	gestalt_cursor.execute(
		"""
		INSERT INTO 
		Fusion(fusion_name, duration, range, description, concentration)
		VALUES (?, ?, ?, ?, ?)
		""",
		fusion
	)

	gestalt_cursor.executemany(
	"INSERT INTO Spell_Fusion VALUES (?, ?)",
	[(spell_id, new_Fusion_id) for spell_id in constituent_spells]
	)

	new_Fusion_id = gestalt_cursor.lastrowid

	return new_Fusion_id


def associate_classes(cursor: sqlite3.Cursor, spell_id: int, character_classes: list[int]):
	'''
	Generate a result of [spell_id, character_class_id] lists
	to associate a spell with character classes. Associates
	a spell with every class if character_classes = None.
	'''
	if not character_classes: # passed an empty list, associate with all classes
		cursor.execute("SELECT character_class_id FROM Class")
	# unpack the result to match the character_classes param
	character_classes = [character_class[0] for character_class in cursor.fetchall()]

	# return our list of [spell_id, character_class_id] lists
	return [[spell_id, character_class_id] for character_class_id in character_classes]

	
def main():

	return 0



if __name__ == "__main__":
	main()
