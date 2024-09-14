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

	Parameters
	----------
	connection: Connection
	spell_DataFrame: DataFrame
		DataFrame of the Spell table.
	'''
	connection.execute(
		"""
		CREATE TABLE Spell (
			spell_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
			spell_name TEXT UNIQUE NOT NULL,
			level INTEGER NOT NULL,
			casting_time TEXT NOT NULL,
			duration TEXT NOT NULL,
			school TEXT,
			range TEXT NOT NULL,
			components TEXT NOT NULL,
			description TEXT UNIQUE NOT NULL,
			upcast_effect TEXT,
			concentration INTEGER CHECK (concentration IN (0, 1)) NOT NULL,
			ritual INTEGER CHECK (concentration IN (0, 1)) NOT NULL
		)
		"""
		)
	
	spell_DataFrame.to_sql(name = "Spell", con = connection, if_exists = "append", index = True)


def create_class_table(connection, class_DataFrame: pd.core.frame.DataFrame):
	'''
	Initialize the Class table with the PK constraint, then insert the
	DataFrame to populate.

	Parameters
	----------
	connection: Connection
	class_DataFrame: DataFrame
		DataFrame of the table.
	'''
	connection.execute(
		"""
		CREATE TABLE Class(
			character_class_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
			character_class TEXT UNIQUE NOT NULL
		)
		"""
	)

	class_DataFrame.to_sql(name = "Class", con = connection, if_exists = "append", index = True)


def create_fusion_table(connection):
	'''
	Initialize the Fusion table with the PK constraint. This table will be
	populated later.
	'''
	connection.execute(
		"""
		CREATE TABLE Fusion(
			fusion_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
			fusion_name TEXT UNIQUE NOT NULL,
			description TEXT UNIQUE NOT NULL
		)
		"""
	)


def create_xyz_table(connection, xyz_DataFrame: pd.core.frame.DataFrame):
	'''
	Initialize the XYZ table with constraints using SQL, then insert the
	DataFrame to populate.

	Parameters
	----------
	connection: Connection
	xyz_DataFrame: DataFrame
		DataFrame of the XYZ table.
	'''
	connection.execute(
		"""
		CREATE TABLE XYZ(
			xyz_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
			xyz_name TEXT UNIQUE NOT NULL,
			rank INTEGER NOT NULL,
			casting_time TEXT NOT NULL,
			duration TEXT NOT NULL,
			range TEXT NOT NULL,
			components TEXT NOT NULL,
			description TEXT UNIQUE NOT NULL
		)
		"""
		)
	
	xyz_DataFrame.to_sql(name = "XYZ", con = connection, if_exists = "append", index = True)


def create_link_table(connection, link_DataFrame: pd.core.frame.DataFrame):
	'''
	Initialize the Link table with constraints using SQL, then insert the
	DataFrame to populate.

	Parameters
	----------
	connection: Connection
	link_DataFrame: DataFrame
		DataFrame of the Link table.
	'''
	connection.execute(
		"""
		CREATE TABLE Link(
			link_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
			link_name TEXT UNIQUE NOT NULL,
			rating INTEGER NOT NULL,
			casting_time TEXT NOT NULL,
			duration TEXT NOT NULL,
			range TEXT NOT NULL,
			components TEXT NOT NULL,
			description TEXT UNIQUE NOT NULL
		)
		"""
		)
	
	link_DataFrame.to_sql(name = "Link", con = connection, if_exists = "append", index = True)


def create_spell_class_table(connection: sqlite3.Connection, spell_class_DataFrame: pd.core.frame.DataFrame):
	'''
	Initialize the Spell_Class junction table with FK constraints, then insert
	the DataFrame to populate.

	Parameters
	----------
	connection: Connection
	spell_class_DataFrame: DataFrame
		Junction table dataframe between the Spell and Class tables.
	'''
	connection.execute(
		"""
		CREATE TABLE Spell_Class(
			spell_id INTEGER NOT NULL,
			character_class_id INTEGER NOT NULL,
			FOREIGN KEY (spell_id) REFERENCES Spell(spell_id) ON DELETE CASCADE,
			FOREIGN KEY (character_class_id) REFERENCES Class(character_class_id) ON DELETE CASCADE,
			PRIMARY KEY (spell_id, character_class_id)
		)
		"""
	)
	spell_class_DataFrame.to_sql(name = "Spell_Class", con = connection, if_exists = "append", index = False)


def create_spell_fusion_table(connection):
	'''
	Initialize the Spell_Fusion junction table with FK constraints. This
	table will be populated later.
	'''
	connection.execute(
		"""
		CREATE TABLE Spell_Fusion(
			spell_id INTEGER NOT NULL,
			fusion_id INTEGER NOT NULL,
			FOREIGN KEY (spell_id) REFERENCES Spell(spell_id) ON DELETE CASCADE,
			FOREIGN KEY (fusion_id) REFERENCES Fusion(fusion_id) ON DELETE CASCADE,
			PRIMARY KEY (spell_id, fusion_id)
		)
		"""
	)


def create_xyz_class_table(connection: sqlite3.Connection, spell_class_DataFrame: pd.core.frame.DataFrame):
	'''
	Initialize the XYZ_Class junction table with FK constraints, then insert
	the DataFrame to populate.

	Parameters
	----------
	connection: Connection
	xyz_class_DataFrame: DataFrame
		Junction table DataFrame between the XYZ and Class tables.
	'''
	connection.execute(
		"""
		CREATE TABLE XYZ_Class(
			xyz_id INTEGER NOT NULL,
			character_class_id INTEGER NOT NULL,
			FOREIGN KEY (xyz_id) REFERENCES XYZ(xyz_id) ON DELETE CASCADE,
			FOREIGN KEY (character_class_id) REFERENCES Class(character_class_id) ON DELETE CASCADE,
			PRIMARY KEY (xyz_id, character_class_id)
		)
		"""
	)
	spell_class_DataFrame.to_sql(name = "XYZ_Class", con = connection, if_exists = "append", index = False)


def create_link_class_table(connection: sqlite3.Connection, spell_class_DataFrame: pd.core.frame.DataFrame):
	'''
	Initialize the Link_Class junction table with FK constraints, then insert
	the DataFrame to populate.

	Parameters
	----------
	connection: Connection
	link_class_DataFrame: DataFrame
		Junction table dataframe between the Link and Class tables.
	'''
	connection.execute(
		"""
		CREATE TABLE Link_Class(
			link_id INTEGER NOT NULL,
			character_class_id INTEGER NOT NULL,
			FOREIGN KEY (link_id) REFERENCES Link(link_id) ON DELETE CASCADE,
			FOREIGN KEY (character_class_id) REFERENCES Class(character_class_id) ON DELETE CASCADE,
			PRIMARY KEY (link_id, character_class_id)
		)
		"""
	)
	spell_class_DataFrame.to_sql(name = "Link_Class", con = connection, if_exists = "append", index = False)


def main():

	with sqlite3.connect("../Gestalt.db") as connection:
		connection.execute("PRAGMA foreign_keys = ON")
		spell_table, class_table, spell_class_table = import_spell.format_spell_csv("../spell_data/all_5e_spells.csv")
		xyz_table, xyz_class_table = import_spell.import_default_xyz("../spell_data/kites_xyz_spells.csv")
		link_table, link_class_table = import_spell.import_default_links("../spell_data/aleisters_link_spells.csv")

		# main tables
		create_spell_table(connection, spell_table)
		create_class_table(connection, class_table)
		create_fusion_table(connection) # use add_fusion() to add these later
		create_xyz_table(connection, xyz_table)
		create_link_table(connection, link_table)

		# junction tables
		create_spell_class_table(connection, spell_class_table)
		create_spell_fusion_table(connection)
		create_xyz_class_table(connection, xyz_class_table)
		create_link_class_table(connection, link_class_table)

	return 0


if __name__ == "__main__":
	main()