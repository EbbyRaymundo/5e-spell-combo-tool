import adbc_driver_sqlite.dbapi as adbc
import polars as pl
'''
This file adds new spells into Gestalt.db and handles
the appropriate junction table insertions.
'''



def add_spell(connection: adbc.Connection, spell: pl.DataFrame, character_classes: list[int] = None):
	'''
	Add the standard spell into the Spell table and associate
	the spell with every character class unless provided a list
	to specify otherwise.
	
	Provided spell format should match the variables specified for the Spell
	table specified in Gestalt_ERD.png

	spell_name: str, in title case.
	level: int.
	casting_time: str, being "Action", "Bonus Action", "Reaction", or an amount
				  of time being abbreviated (Min./Hr.).
	duration: str, with the time being abbreviated (Min./Hr.).
	school: str, capitalized.
	range: str, with the distance being abbreviated (Ft./Mi.).
	components: str, in format "V, S, M (<material components>)".
	description: str.
	upcast_effect: str or None. Description for higher level effects, None type otherwise.
	concentration: bool.
	ritual: bool.

	Parameters
	----------
	connection:
		Database connection to Gestalt.db.
	spell:
		New spell in the format specified above and in the Spell table
		within Gestalt_ERD.png.
	character_classes: list[int]
		character_class_id's of the classes the spell is available to. 
		Associated with all spellcasting classes if no list given.
	'''

	return


def add_XYZ(connection, xyz, character_classes: list[int] = None):
	'''
	Add the XYZ spell into the XYZ table and associate the XYZ
	spell with every character class unless provided a list to
	specify otherwise.

	Provided XYZ format should match the variables specified for the XYZ
	table specified in Gestalt_ERD.png

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
	connection:
		Database connection to Gestalt.db.
	XYZ:
		New XYZ spell in the format specified above and in the XYZ table
		within Gestalt_ERD.png.
	character_classes: list[int]
		character_class_id's of the classes the XYZ is available to. 
		Associated with all full casters if no list given.

	Returns
	-------
	new_XYZ_id: int
	'''

	return


def add_Link(connection, link, character_classes: list[int] = None):
	'''
	Add the Link spell into the Spell table and associate the Link
	spell with every character class unless provided a list to specify.

	Provided Link format should match the variables specified for the Link
	table specified in Gestalt_ERD.png.

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
	Link:
		New Link spell in the format specified above and in the Link table
		within Gestalt_ERD.png.
	character_classes: list[int]
		character_class_id's of the classes the Link is available to. 
		Associated with all classes if no list given. Links are typically
		associated with ALL spellcasting classes and only have an
		Intelligence attribute requirement.

	Returns
	-------
	new_Link_id: int
	'''

	return


def add_Fusion(connection, fusion, constituent_spells: list[int]):
	'''
	Add the Fusion into the Fusion table and associate the Fusion with all of
	its constituent spells in the Spell_Fusion table.
	
	Provided Fusion format should match the variables specified for the Fusion
	table specified in Gestalt_ERD.png

	fusion_name: str, in title case
	duration: str, with the time being abbreviated (Min./Hr.).
	range: str, with the distance being abbreviation (Ft./Mi.).
	description: str.
	concentration: bool.

	Parameters
	----------
	connection:
		database connection to Gestalt.db.
	fusion:
		New Fusion spell in the format specified above and in the Fusion table
		within Gestalt_ERD.png.
	constituent_spells: list[int]
		spell_id's of spells used to create the fusion.

	Returns
	-------
	new_fusion_id: int
	'''

	return


def associate_classes(connection, spell_id: int, character_classes: list[int]):
	'''
	Generate a result of [spell_id, character_class_id] lists
	to associate a spell with character classes. Associates
	a spell with every class if character_classes = None.
	'''

	return

	
def main():

	with adbc.connect("../Gestalt.db") as connection:
	
		with connection.cursor() as cursor:

			cursor.execute("PRAGMA foreign_keys = ON")

		connection.commit()

		# use update functions here since the pl write_database( )
		# functions can only take a Connection object

	return 0



if __name__ == "__main__":
	main()
