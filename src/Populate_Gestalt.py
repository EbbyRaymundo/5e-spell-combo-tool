import sqlite3
import pandas as pd
import Import_Spell_Data as import_spell
'''
This file is for creating tables for the Gestalt database,
adding constraints and populating with dataframes. This does
not need to be run again by the user.
'''

def create_spell_table(connection, spell_DataFrame: pd.core.frame.DataFrame):
	'''
	Initialize the Spell table with constraints using SQL, then insert the
	dataframe to populate.
	'''
	connection.execute(
		'''
		CREATE TABLE Spell(
			spell_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
			spell_name TEXT UNIQUE NOT NULL,
			level INTEGER NOT NULL,
			casting_time TEXT NOT NULL,
			duration TEXT NOT NULL,
			school TEXT,
			range TEXT NOT NULL,
			components TEXT NOT NULL,
			description TEXT NOT NULL,
			upcast_effect TEXT,
			concentration INTEGER CHECK (concentration IN (0, 1)) NOT NULL,
			ritual INTEGER CHECK (concentration IN (0, 1)) NOT NULL,
			spell_type TEXT NOT NULL
		)
		'''
		)
	
	spell_DataFrame.to_sql(name = "Spell", con = connection, if_exists = "append", index = False)


def create_class_table(connection, class_DataFrame: pd.core.frame.DataFrame):
	'''
	Initialize the Class table with the PK constraint, then insert the
	dataframe to populate.
	'''
	connection.execute(
		'''
		CREATE TABLE Class(
			character_class_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
			character_class TEXT UNIQUE NOT NULL
		)
		'''
	)

	class_DataFrame.to_sql(name = "Class", con = connection, if_exists = "append", index = False)


def create_spell_class_table(connection, spell_class_DataFrame: pd.core.frame.DataFrame):
	'''
	Initialize the Spell_Class junction table with FK constraints, then insert
	the dataframe to populate.
	'''
	connection.execute(
		'''
		CREATE TABLE Spell_Class(
			spell_id INTEGER NOT NULL,
			character_class_id INTEGER NOT NULL,
			FOREIGN KEY (spell_id) REFERENCES Spell(spell_id),
			FOREIGN KEY (character_class_id) REFERENCES Class(character_class_id)
		)
		'''
	)
	spell_class_DataFrame.to_sql(name = "Spell_Class", con = connection, if_exists = "append", index = False)

def create_fusion_table(connection):
	'''
	Initialize the Fusion table with the PK constraint. This table will be
	populated later.
	'''
	connection.execute(
		'''
		CREATE TABLE Fusion(
			fusion_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
			fusion_name TEXT UNIQUE NOT NULL,
			effect TEXT UNIQUE NOT NULL
		)
		'''
	)

def create_spell_fusion_table(connection):
	'''
	Initialize the Spell_Fusion junction table with FK constraints. This
	table will be populated later when the Fusion tables are added.
	'''
	connection.execute(
		'''
		CREATE TABLE Spell_Fusion(
			spell_id INTEGER NOT NULL,
			fusion_id INTEGER NOT NULL,
			FOREIGN KEY (spell_id) REFERENCES Spell(spell_id),
			FOREIGN KEY (fusion_id) REFERENCES Fusion(fusion_id)
		)
		'''
	)

def main():

	with sqlite3.connect("../Gestalt.db") as connection:
		spell_table, class_table, spell_class_table = import_spell.format_spell_csv("../spell_data/all_5e_spells.csv")

		#create_spell_table(connection, spell_table)
		#create_class_table(connection, class_table)
		#create_spell_class_table(connection, spell_class_table)
		#create_fusion_table(connection)
		#create_spell_fusion_table(connection)

	return 0

if __name__ == "__main__":
	main()