import sqlite3

'''
TODO: potentially use Pandas to get values into dataframes
before inserting them into tables.
'''

def add_XYZ(XYZ: list, classes: list = None):
	'''
	Add a list of XYZ spells into the Spell table and associate each XYZ
	spell with every character class unless provided a list to specify.
	'''

	with sqlite3.connect("Gestalt.db") as connection:
		gestalt_cursor = connection.cursor()
		# XYZ have no spell school, do not use concentration, can't be rituals, and have no upcast effects
		gestalt_cursor.executemany(
			"""
			INSERT INTO Spell(spell_name, level, casting_time, duration, range, components, description, concentration, ritual, spell_type) 
			VALUES (?, ?, ?, ?, ?, ?, ?, 0, 0, 'XYZ')
			""",
			list
			)

	return


def add_Link(Link: list):
	"""
	Add a list of XYZ spells into the Spell table and associate each XYZ
	spell with every character class unless provided a list to specify.
	"""
	with sqlite3.connect("Gestalt.db") as connection:
		gestalt_cursor = connection.cursor()
		# Links have no spell school, do not use concentration, can't be rituals, and have no upcast effects
		gestalt_cursor.executemany(
			"""
			INSERT INTO Spell(spell_name, level, casting_time, duration, range, components, description, concentration, ritual, spell_type) 
			VALUES (?, ?, ?, ?, ?, ?, ?, 0, 0, 'Link')
			""",
			list
			)

	return


def add_Fusion(Fusion: list):
	"""
	Add a list of Fusion effects to the Fusion table and their associated
	spells to the Spell_Fusion table.
	"""

	return

def associate_classes(classes: list = None): # the argument should be an optional list
	'''
	This class takes a list of classes that have access to an extra deck spell.
	If every class has access to it, then no arguments should be given.
	'''

	return

def main():

	return 0