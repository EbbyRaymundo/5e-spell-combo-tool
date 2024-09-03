import sqlite3

'''
TODO: potentially use Pandas to get values into dataframes
before inserting them into tables.
'''

def add_XYZ(XYZ: list):
	'''
	Add a list of XYZ spells into the Spell table and associate each XYZ
	spell with every character class.

	TODO: Add a method to specify which classes have access to an XYZ if
	it isn't all character classes.
	'''

	with sqlite3.connect("Gestalt.db") as connection:
		gestalt_cursor = connection.cursor()
		gestalt_cursor.executemany("INSERT INTO Spell VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", list)

	return


def add_Link(Link: list):

	return


def add_Fusion(Fusion: list):

	return


def main():

	return 0