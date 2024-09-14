import sqlite3
import pandas as pd



def add_XYZ(xyz: tuple[str, int, str, str, str, str, str], character_classes: list[int] = None):
	'''
	Add the XYZ spell into the Spell table and associate each XYZ
	spell with every character class unless provided a list to specify.
	Tuple representing XYZ should be in format:

	(<XYZ_name>, <XYZ_rank>, <casting_time>, <duration>, <range>, <components>, <description>)

	xyz_name: str, in title case.
	rank: int representing XYZ rank (1-9 typically)
	casting_time: str representing the action economy to cast (typically "Action and Bonus Action")
	duration: str, with the time being abbreviated (Min./Hr.). Typically last 1 Hr.
	range: str, with the distance being abbreviated (Ft./Mi.). Can also be "Line of sight".
	components: str, typically "V, S, M (2 level <rank> spell slots and <rank> sorcery points)".
				Can also specify "May also use a pre-existing <XYZ or spell_name> and n 
				sorcery points" if you can overlay from an existing spell into this XYZ.
				Example: "V, S, M (2 level 4 spell slots and 4 sorcery points. May also
						  also use a pre-existing 'Sparks' XYZ spell and 2 sorcery points)"
	description: str, typically in format of continuous effect, then the effect that occurs
				 when you detach a material.

	Parameters
	----------
	XYZ: tuple[str, int, str, str, str, str, str]
		XYZ data to be inserted into the database.
	character_classes: list[int]
		character_class_id's of the classes the XYZ is available to. 
		Associated with all full casters if no list given.

	Returns
	-------
	new_XYZ_id: int
	'''
	with sqlite3.connect("../Gestalt.db") as connection:
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

		spell_class_ids = associate_classes(new_xyz_id, character_classes, gestalt_cursor)

		gestalt_cursor.executemany("INSERT INTO XYZ_Class VALUES (?, ?)", spell_class_ids)

		return new_xyz_id


def add_Link(link: tuple[str, int, str, str, str, str, str], character_classes: list[int] = None):
	"""
	Add the Link spell into the Spell table and associate the Link
	spell with every character class unless provided a list to specify.
	Tuple representing the Link should be in format:

	(<link_name>, <rating>, <duration>, <range>, <components>, <description>)

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
	Link: tuple[str, int, str, str, str, str, str]
		Link data to be inserted into the database.
	character_classes: list[int]
		character_class_id's of the classes the Link is available to. 
		Associated with all classes if no list given. Links are typically
		associated with ALL spellcasting classes and only have an
		Intelligence attribute requirement.

	Returns
	-------
	new_Link_id: int
	"""
	with sqlite3.connect("../Gestalt.db") as connection:
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
		spell_class_ids = associate_classes(new_link_id, character_classes, gestalt_cursor)

		gestalt_cursor.executemany("INSERT INTO Link_Class VALUES (?, ?)", spell_class_ids)

		return new_link_id

def add_Fusion(fusion: list[str, str], constituent_spells: list[int]):
	"""
	Add the Fusion into the Fusion table and associate the Fusion with all of
	its constituent spells in the Spell_Fusion table.

	Parameters
	----------
	fusion: list[str, str]
		fusion_name, description.
	constituent_spells: list[int]
		spell_id's of spells used to create the fusion.

	Returns
	-------
	new_fusion_id: int
	"""
	with sqlite3.connect("../Gestalt.db") as connection:
		gestalt_cursor = connection.cursor()

		gestalt_cursor.execute("PRAGMA foreign_keys = ON")
		gestalt_cursor.execute("INSERT INTO Fusion(fusion_name, description) VALUES (?, ?)", fusion)

		new_Fusion_id = gestalt_cursor.lastrowid

		gestalt_cursor.executemany(
			"INSERT INTO Spell_Fusion VALUES (?, ?)",
			[(spell_id, new_Fusion_id) for spell_id in constituent_spells]
			)

		return new_Fusion_id

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

	return 0


if __name__ == "__main__":
	main()