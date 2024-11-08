import Import_Spells

'''
This file is for populating the generated tables of the 
'''

def populate_main_tables(
	connection,
	spell_DataFrame,
	class_DataFrame,
	fusion_DataFrame,
	xyz_DataFrame,
	link_DataFrame,
):
	'''
	Parameters
	----------
	connection
	spell_DataFrame:
		Data frame of Spell table specified in Gestalt_ERD.png.
		Data frame of Class table specified in Gestalt_ERD.png.
		Data frame of Fusion table specified in Gestalt_ERD.png.
		Data frame of XYZ table specified in Gestalt_ERD.png.
		Data frame of Link table specified in Gestalt_ERD.png.

	Returns
	-------
	0: int
		Function completed successfully.
	'''

	return 0

def populate_junction_tables(
	connection,
	spell_class_DataFrame,
	spell_fusion_DataFrame,
	xyz_class_DataFrame,
	link_class_DataFrame
):
	'''
	Parameters
	----------
	connection
	spell_DataFrame:
		Data frame of Spell_Class table specified in Gestalt_ERD.png.
		Data frame of Spell_Fusion table specified in Gestalt_ERD.png.
		Data frame of XYZ_Class table specified in Gestalt_ERD.png.
		Data frame of Link_Class table specified in Gestalt_ERD.png.

	Returns
	-------
	0: int
		Function completed successfully.
	'''
	
	return 0



def main():

	return 0



if __name__ == "__main__":
	main()