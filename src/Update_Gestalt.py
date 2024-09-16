import sqlite3
import pandas as pd



def add_spell(spell: tuple[str, int, str, str, str, str, str, str, str, bool, bool], character_classes: list[int] = None):
	'''
	Add the standard spell into the Spell table and associate
	the spell with every character class unless provided a list
	to specify otherwise.
	Tuple representing spell should be in format:

	(spell_name, level, casting_time, duration, school, range, components, description, upcast_effect, concentration, ritual)

	spell_name: str, in title case
	level: int
	casting_time: str, being "Action", "Bonus Action", "Reaction", or an amount of time being abbreviated (Min./Hr.)
	duration: str, with the time being abbreviated (Min./Hr.).
	school: str, capitalized.
	range: str, with the distance being abbreviation (Ft./Mi.).
	components: str, in format "V, S, M (<material components>).
	description: str.
	upcast_effect: str or None, description at higher levels, None type otherwise.
	concentration: bool.
	ritual: bool.

	Parameters
	----------
	spell: tuple[str, int, str, str, str, str, str, str, str, bool, bool]
	character_classes: list[int]
		character_class_id's of the classes the spell is available to. 
		Associated with all spellcasting classes if no list given.

	'''
	with sqlite3.connect("../Gestalt.db") as connection:
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



	return 0


def add_XYZ(xyz: tuple[str, int, str, str, str, str, str], character_classes: list[int] = None):
	'''
	Add the XYZ spell into the XYZ table and associate the XYZ
	spell with every character class unless provided a list to
	specify otherwise.
	Tuple representing XYZ should be in format:

	(XYZ_name, rank, casting_time, duration, range, components, description)

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
	XYZ: tuple[str, int, str, str, str, str, str]
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

		xyz_class_ids = associate_classes(new_xyz_id, character_classes, gestalt_cursor)

		gestalt_cursor.executemany("INSERT INTO XYZ_Class VALUES (?, ?)", xyz_class_ids)

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
		link_class_ids = associate_classes(new_link_id, character_classes, gestalt_cursor)

		gestalt_cursor.executemany("INSERT INTO Link_Class VALUES (?, ?)", link_class_ids)

		return new_link_id


def add_Fusion(fusion: tuple[str, str, str, str, bool], constituent_spells: list[int]):
	'''
	Add the Fusion into the Fusion table and associate the Fusion with all of
	its constituent spells in the Spell_Fusion table.
	Tuple representing fusion should be in format:

	(fusion_name, duration, range, description, concentration)

	spell_name: str, in title case
	duration: str, with the time being abbreviated (Min./Hr.).
	range: str, with the distance being abbreviation (Ft./Mi.).
	description: str.
	concentration: bool.

	Parameters
	----------
	fusion: list[str, str, str, str, bool]
	constituent_spells: list[int]
		spell_id's of spells used to create the fusion.

	Returns
	-------
	new_fusion_id: int
	'''
	with sqlite3.connect("../Gestalt.db") as connection:
		gestalt_cursor = connection.cursor()

		gestalt_cursor.execute("PRAGMA foreign_keys = ON")
		gestalt_cursor.execute("INSERT INTO Fusion(fusion_name, duration, range, description, concentration) VALUES (?, ?, ?, ?, ?)", fusion)

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

	add_Fusion(("Slip by Like Vapor", "Up to 10 Min.", "Touch", "Touch one creature; they become an invisible gas with the same restrictions as Gaseous Form.", True), [258, 197])
	add_Fusion(("Prescient Ignition", "Instantaneous", "120 Ft.", "Scorching Ray's 3 beams no longer require a ranged spell attack and each ray deals an additional 1d4 force damage.", False), [285, 377])
	add_Fusion(("Prescient Conflagration", "Instantaneous", "120 Ft.", "Target one creature to send a Fireball dart that detonates on impact instead of an area of effect. The dart deals 8d6 fire damage and 1d4 force damage.", False), [285, 181])
	add_Fusion(("Ethereal Step", "1 Min.", "Self", "Roll a d20 at the beginning of your turn. On an 11 or higher, you shift into the Ethereal Plane when moving during that turn, and reappear during actions that split up your movement. You Blink as normal at the end of your turn if you rolled an 11 or higher at the beginning of your turn.", False), [312, 45])
	add_Fusion(("Flash Step", "Instantaneous", "30 Ft.", "Target one creature to swap places with. Unwilling creatures make a Constitution saving throw.", False), [312, 477])
	add_Fusion(("Sonic Step", "Instantaneous", "90 Ft.", "Target one creature to swap places with. The targeted creature makes a Constitution saving throw and takes 3d10 thunder damage on a failure (radius of 10 Ft.) where you teleported from and swaps places with you. On a success, this spell uses the effect of Thunder Step and the creature isn't teleported.", False), [477, 456])
	add_Fusion(("Shadow Clones", "1 Min.", "Self", "Your illusory duplicates gain the benefits of Mage Armor.", False), [281, 310])
	add_Fusion(("Scholar's Whisperings", "1 Hr.", "Self", "In addition to the effects of Comprehend Languages and Tongues, you no longer need to be touching the surface the language is written on to read it.", False), [75, 464])
	add_Fusion(("Speed Reading", "Up to 1 Hr.", "Self", "Your reading speed is quadrupled and you gain the effects of Comprehend Languages.", True), [75, 224])
	add_Fusion(("Aegis of the Element", "1 round", "Self", "You have immunity to a damage type specified by Absorb Elements. This spell de-Fusions back to Protection from Energy when its duration ends.", True), [1, 353])
	add_Fusion(("Expulsion to the Elements", "Up to 1 Min.", "60 Ft.", "The effect of Banishment sends the creature to an adjacent elemental plane of your choice.", True), [31, 336])
	add_Fusion(("Perfect Disguise", "1 Hr.", "Self", "Appearance changes from Disguise self stand up to physical inspection", False), [124, 339])
	add_Fusion(("Perfect Crime", "Up to 1 Hr.", "30 Ft.", "All creatures changed by Seeming stand up to physical inspection.", True), [381, 293])
	add_Fusion(("Freedom of Chronology", "Instantaneous", "Touch", "Touch one creature; they can now act during the continuous duration of stopped time. The same restrictions apply as the Time Stop they currently reside in.", False), [224, 194, 461])
	add_Fusion(("Expulsion from the Chronology", "Instantaneous", "Touch", "Touch one creature that is currently acting within stopped time; they are ejected from stopped time.", False), [31, 461])
	add_Fusion(("Stellar Screech", "Instantaneous", "120 Ft.", "This spell requires 3 Fireballs for the Fireball material. You conjure 3 orange orbs. Each orb streaks an orange laser originating from the caster across a surface in a 40 Ft. line within 120 Ft. Any creature caught in the laser must make a Dexterity saving throw, taking 10d6 fire + 4d6 force damage on a failure, or half as much damage on a successful one. Each laser leaves a glowing trail on the surface that detonates after 1 round in a 5 Ft. radius for 10d6 fire + 10d6 force damage.", False), [377, 181, 125])


	return 0


if __name__ == "__main__":
	main()