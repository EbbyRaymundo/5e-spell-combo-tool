import sqlite3

'''
TODO: potentially use Pandas to get values into dataframes
before inserting them into tables.
'''

def add_XYZ(XYZ: list):
	'''
	Add a list of XYZ spells into the Spell table and associate each XYZ
	spell with every character class.

	TODO: Add a method to specify which classes have access to ED spells if
	it isn't all character classes.
	'''

	with sqlite3.connect("Gestalt.db") as connection:
		gestalt_cursor = connection.cursor()
		# XYZ have no spell school, do not use concentration, can't be rituals, and have no upcast effects
		gestalt_cursor.executemany("INSERT INTO Spell VALUES (?, ?, ?, ?, ?, ?, ?, NULL, 0, 0, 'XYZ', NULL)", list)

	return


def add_Link(Link: list):

	with sqlite3.connect("Gestalt.db") as connection:
		gestalt_cursor = connection.cursor()
		# Links have no spell school, do not use concentration, can't be rituals, and have no upcast effects
		gestalt_cursor.executemany("INSERT INTO Spell VALUES (?, ?, ?, ?, ?, ?, ?, ?, NULL, 0, 'Link', NULL)", list)

	return


def add_Fusion(Fusion: list):

	return

def associate_classes(classes: list = None): # the argument should be an optional list
	'''
	This class takes a list of classes that have access to an extra deck spell.
	If every class has access to it, then no arguments should be given.
	'''

	return

def main():

	return 0