import sqlite3



# TODO: decide if I want to add error handling to the Accel Synchro getters to
#		check if the input spell has a duration greater than Instantaneous.
# TODO: change the getters to handle a list of int spell_id's instead of a single input.
def get_counterspelled_Accel_Synchro(spell_id: int):
	'''
	Given the spell_id of a spell with a duration longer than "Instantaneous", 
	determine the eligible Reaction spells to Accel Synchro into.

	Parameters
	----------
	spell_id: int

	Returns
	-------
	target_spells: list[tuple]
		List of tuples of counterspelled Accel Synchro target spells.

	Raises
	------
	ValueError
		Provided spell_id not found in Spell table
	'''
	with sqlite3.connect("../Gestalt.db") as connection:
		gestalt_cursor = connection.cursor()

		gestalt_cursor.execute("SELECT * FROM Spell WHERE spell_id == ?", spell_id)
		source_spell = gestalt_cursor.fetchall()

		if not source_spell:
			raise ValueError(f"spell_id {spell_id} not found.")
		
		source_spell = gestalt_cursor.fetchall()
		source_spell = source_spell[0] # .fetchall() result is in format [(spell)]

		gestalt_cursor.execute(
			"""
			SELECT 
				* FROM Spell 
			WHERE 
				(casting_time == "Action" OR casting_time == "Bonus Action")
				AND level > ?
				AND school == ?
			""",
			[source_spell[2], source_spell[5]] # [level, school]
		)

		return gestalt_cursor.fetchall()


def get_reaction_Accel_Synchro(spell_id: int):
	'''
	Given a spell with a duration greater than Instantaneous, determine the
	eligible Reaction spells to Accel Synchro into.

	Parameters
	----------
	source_spell: int
		spell_id of the source spell.
	
	Returns
	-------
	target_spells: list[tuple]
		List of tuples of Reaction Accel Synchro target spells.

	Raises
	------
	ValueError
		Provided spell_id not found in Spell table
	'''
	with sqlite3.connect("../Gestalt.db") as connection:
		gestalt_cursor = connection.cursor()

		gestalt_cursor.execute("SELECT * FROM Spell WHERE spell_id == ?", spell_id)
		source_spell = gestalt_cursor.fetchall()

		if not source_spell:
			raise ValueError(f"spell_id {spell_id} not found.")
		
		source_spell = gestalt_cursor.fetchall()
		source_spell = source_spell[0] # .fetchall() result is in format [(spell)]

		gestalt_cursor.execute(
			"""
			SELECT 
				* FROM Spell 
			WHERE 
				casting_time == "Reaction"
				AND level > ?
				AND school == ?
			""",
			[source_spell[2], source_spell[5]] # [level, school]
		)

		return gestalt_cursor.fetchall()


def get_main_action_Accel_Synchro(spell_id: int):
	'''
	Given the spell_id of a spell with a duration greater than Instantaneous,
	determine the eligible spells to Accel Synchro into.

	Parameters
	----------
	spell_id: int
	
	Returns
	-------
	target_spells: list[tuple]
		List of tuples of Reaction Accel Synchro target spells.

	Raises
	------
	ValueError
		Provided spell_id not found in Spell table
	'''
	with sqlite3.connect("../Gestalt.db") as connection:
		gestalt_cursor = connection.cursor()

		gestalt_cursor.execute("SELECT * FROM Spell WHERE spell_id == ?", spell_id)
		source_spell = gestalt_cursor.fetchall()

		if not source_spell:
			raise ValueError(f"spell_id {spell_id} not found.")

		source_spell = source_spell[0] # .fetchall() result is in format [(spell)]

		gestalt_cursor.execute(
			"""
			SELECT 
				* FROM Spell 
			WHERE 
				level > ?
				AND school == ?
			""",
			[source_spell[2], source_spell[5]] # [level, school]
		)

		return gestalt_cursor.fetchall()


def get_Fusion_targets(spell_id: int):
	'''
	Given a spell_id, return any available Fusion spell targets and their
	spell components, EXCEPT for the input spell.

	Parameters
	----------
	spell_id: int

	Returns
	-------
	target_fusions: list[tuple]
		List of query results with tuples in format (Fusion.*, Spell.*)
	'''
	with sqlite3.connect("../Gestalt.db") as connection:
		gestalt_cursor = connection.cursor()

		gestalt_cursor.execute(
			"""
			SELECT * FROM Fusion
			JOIN Spell_Fusion ON Fusion.fusion_id = Spell_Fusion.fusion_id
			JOIN Spell ON Spell_Fusion.spell_id = Spell.spell_id
			WHERE Fusion.fusion_id IN (
   				SELECT fusion_id
   				FROM Spell_Fusion
   				WHERE spell_id == ?
   			)
			AND Spell.spell_id != ?
			""",
			[spell_id, spell_id]
		)

		# tuples containing fusions using input spell_id as components
		# and the OTHER spells required as their components
		target_fusions = gestalt_cursor.fetchall()

		if not target_fusions:
			raise ValueError(f"spell_id {spell_id} not found as a Fusion component.")

		return target_fusions

	return


def main():

	fireball_Fusions = get_Fusion_targets(181)

	print(fireball_Fusions)

	return 0


if __name__ == "__main__":
	main()