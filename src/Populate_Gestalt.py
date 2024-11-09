import Import_Spells
import sqlite3
import pandas as pd

'''
This file is used to insert all tables preprocessed in Import_Spells.py
into their respective tables in the existing, empty database using
an sqlite3 connection. This file does not need to be run by the user
unless they are rebuilding their database.
'''



def populate_main_tables(
	connection: sqlite3.Connection,
	spell_DataFrame: pd.DataFrame,
	class_DataFrame: pd.DataFrame,
	#fusion_DataFrame: pd.DataFrame,
	xyz_DataFrame: pd.DataFrame,
	link_DataFrame: pd.DataFrame
):
	'''
	Parameters
	----------
	connection: sqlite3.Connection
		Database connection to Gestalt.db.
	spell_DataFrame: pd.DataFrame
		DataFrame of Spell table specified in Gestalt_ERD.png.
	class_DataFrame: pd.DataFrame
		DataFrame of Class table specified in Gestalt_ERD.png.
	fusion_DataFrame: pd.DataFrame
		DataFrame of Fusion table specified in Gestalt_ERD.png.
	xyz_DataFrame: pd.DataFrame
		DataFrame of XYZ table specified in Gestalt_ERD.png.
	link_DataFrame: pd.DataFrame
		DataFrame of Link table specified in Gestalt_ERD.png.

	Returns
	-------
	0: int
		Function completed successfully.
	'''
	spell_DataFrame.to_sql(name = "Spell", con = connection, if_exists = "append", index = True)
	class_DataFrame.to_sql(name = "Class", con = connection, if_exists = "append", index = True)
	# TODO: implement
	#fusion_DataFrame.to_sql(name = "Fusion", con = connection, if_exists = "append", index = True)
	xyz_DataFrame.to_sql(name = "XYZ", con = connection, if_exists = "append", index = True)
	link_DataFrame.to_sql(name = "Link", con = connection, if_exists = "append", index = True)

	return 0

def populate_junction_tables(
	connection: sqlite3.Connection,
	spell_class_DataFrame: pd.DataFrame,
	#spell_fusion_DataFrame: pd.DataFrame,
	xyz_class_DataFrame: pd.DataFrame,
	link_class_DataFrame: pd.DataFrame
):
	'''
	Parameters
	----------
	connection: sqlite3.Connection
		Database connection to Gestalt.db.
	spell_class_DataFrame: pd.DataFrame
		DataFrame of Spell_Class table specified in Gestalt_ERD.png.
	spell_fusion_DataFrame: pd.DataFrame
		DataFrame of Spell_Fusion table specified in Gestalt_ERD.png.
	xyz_class_DataFrame: pd.DataFrame
		DataFrame of XYZ_Class table specified in Gestalt_ERD.png.
	link_class_DataFrame: pd.DataFrame
		DataFrame of Link_Class table specified in Gestalt_ERD.png.

	Returns
	-------
	0: int
		Function completed successfully.
	'''
	spell_class_DataFrame.to_sql(name = "Spell_Class", con = connection, if_exists = "append", index = True)
	# TODO: implement
	#spell_fusion_DataFrame.to_sql(name = "Spell_Fusion", con = connection, if_exists = "append", index = True)
	xyz_class_DataFrame.to_sql(name = "XYZ_Class", con = connection, if_exists = "append", index = True)
	link_class_DataFrame.to_sql(name = "Link_Class", con = connection, if_exists = "append", index = True)
	
	return 0



def main():

	spell_table, class_table, spell_class_table = Import_Spells.format_spell_csv("../spell_data/Spells.csv")
	#fusion_table, spell_fusion_table = Import_Spells.import_default_fusions("../spell_data/aleisters_fusion_spells.csv")
	xyz_table, xyz_class_table = Import_Spells.import_default_xyz("../spell_data/kites_xyz_spells.csv")
	link_table, link_class_table = Import_Spells.import_default_links("../spell_data/aleisters_link_spells.csv")	

	with sqlite3.connect("../Gestalt.db") as connection:

		connection.execute("PRAGMA foreign_keys = ON")

		populate_main_tables(
			connection,
			spell_table,
			class_table,
			#fusion_table,
			xyz_table,
			link_table,
		)

		populate_junction_tables(
			connection,
			spell_class_table,
			#spell_fusion_table,
			xyz_class_table,
			link_class_table
		)

	return 0


if __name__ == "__main__":
	main()