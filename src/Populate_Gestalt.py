import adbc_driver_sqlite.dbapi as adbc
import polars as pl
import Import_Spells

def populate_main_tables(
		spell_DataFrame: pl.DataFrame,
		class_DataFrame: pl.DataFrame,
		fusion_DataFrame: pl.DataFrame,
		xyz_DataFrame: pl.DataFrame,
		link_DataFrame: pl.DataFrame,
	):
	'''
	Write the main tables of Gestalt.db. "Append" to the tables
	created in Build_Gestalt.py.
	'''

	spell_DataFrame.write_database(name = "Spell", if_table_exists = "append")
	class_DataFrame.write_database(name = "Class", if_table_exists = "append")
	# TODO: implement fusion_DataFrame function
	fusion_DataFrame.write_database(name = "Fusion", if_table_exists = "append")
	xyz_DataFrame.write_database(name = "XYZ", if_table_exists = "append")
	link_DataFrame.write_database(name = "Link", if_table_exists = "append")	

	return 0

def populate_junction_tables(
		spell_class_DataFrame: pl.DataFrame,
		spell_fusion_DataFrame: pl.DataFrame,
		xyz_class_DataFrame: pl.DataFrame,
		link_class_DataFrame: pl.DataFrame
	):
	'''
	Write the main tables of Gestalt.db. "Append" to the tables
	created in Build_Gestalt.py.
	'''

	spell_class_DataFrame.write_database(name = "Spell_Class", if_table_exists = "append")
	# TODO: implement
	spell_fusion_DataFrame.write_database(name = "Spell_Fusion", if_table_exists = "append")
	xyz_class_DataFrame.write_database(name = "XYZ_Class", if_table_exists = "append")
	link_class_DataFrame.write_database(name = "Link_Class", if_table_exists = "append")

	return 0


def main():

	spell_table, class_table, spell_class_table = Import_Spells.format_spell_csv("../spell_data/all_5e_spells.csv")
	fusion_table, spell_fusion_table = Import_Spells.import_default_fusions("../spell_data/aleisters_fusion_spells.csv")
	xyz_table, xyz_class_table = Import_Spells.import_default_xyz("../spell_data/kites_xyz_spells.csv")
	link_table, link_class_table = Import_Spells.import_default_links("../spell_data/aleisters_link_spells.csv")

	populate_main_tables(
		spell_table,
		class_table,
		fusion_table,
		xyz_table,
		link_table,
		
	)

	populate_junction_tables(
		spell_class_table,
		spell_fusion_table,
		xyz_class_table,
		link_class_table
	)

	return 0



if __name__ == "__main__":
	main()