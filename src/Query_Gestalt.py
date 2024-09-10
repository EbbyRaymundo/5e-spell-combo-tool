import sqlite3


# TODO: decide if I want to add error handling to the Accel Synchro getters to
#		check if the input spell has a duration greater than Instantaneous.
# TODO: change the getters to handle a list of str instead of a single input.
def get_counterspelled_Accel_Synchro(source_spell: str):
	"""
	Given a spell with a duration greater than instantaneous, determine the
	eligible Reaction spells to Accel Synchro into.

	Parameters
	----------
	source_spell: str
		Completely or partially matching unique spell name within the database.

	Returns
	-------
	target_spells: list[tuple]
		List of tuples of Reaction Accel Synchro target spells.

	Raises
	------
	ValueError
		source_spell was not found in the database.
	ValueError
		source_spell has multiple matches in the database.
	"""
	with sqlite3.connect("../Gestalt.db") as connection:
		gestalt_cursor = connection.cursor()
		gestalt_cursor.execute("SELECT * FROM Spell WHERE spell_name LIKE ?", [f"%{source_spell}%"])

		check_provided_spell = gestalt_cursor.fetchall()

		# important that our query finds 1 and only 1 result
		if not check_provided_spell:
			raise ValueError("source_spell not found.")
		
		elif len(check_provided_spell) > 1:
			raise ValueError(f"Multiple spells found with the provided spell name: {[spell[1] for spell in check_provided_spell]}.")

		source_spell = check_provided_spell[0] # load spell tuple from db

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


def get_reaction_Accel_Synchro(source_spell: str):
	"""
	Given a spell with a duration greater than instantaneous, determine the
	eligible Reaction spells to Accel Synchro into.

	Parameters
	----------
	source_spell: str
		Completely or partially matching unique spell name within the database.

	Returns
	-------
	target_spells: list[tuple]
		List of tuples of Reaction Accel Synchro target spells.

	Raises
	------
	ValueError
		source_spell was not found in the database.
	ValueError
		source_spell has multiple matches in the database.
	"""
	with sqlite3.connect("../Gestalt.db") as connection:
		gestalt_cursor = connection.cursor()
		gestalt_cursor.execute("SELECT * FROM Spell WHERE spell_name LIKE ?", [f"%{source_spell}%"])

		check_provided_spell = gestalt_cursor.fetchall()

		# important that our query finds 1 and only 1 result
		if not check_provided_spell:
			raise ValueError("source_spell not found.")
		
		elif len(check_provided_spell) > 1:
			raise ValueError(f"Multiple spells found with the provided spell name: {[spell[1] for spell in check_provided_spell]}.")

		source_spell = check_provided_spell[0] # load spell tuple from db

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


def get_main_action_Accel_Synchro():
	"""
	Given a spell with a duration greater than instantaneous, determine the
	eligible Reaction spells to Accel Synchro into.

	Parameters
	----------
	source_spell: str
		Completely or partially matching unique spell name within the database.

	Returns
	-------
	target_spells: list[tuple]
		List of tuples of Reaction Accel Synchro target spells.

	Raises
	------
	ValueError
		source_spell was not found in the database.
	ValueError
		source_spell has multiple matches in the database.
	"""
	with sqlite3.connect("../Gestalt.db") as connection:
		gestalt_cursor = connection.cursor()
		gestalt_cursor.execute("SELECT * FROM Spell WHERE spell_name LIKE ?", [f"%{source_spell}%"])

		check_provided_spell = gestalt_cursor.fetchall()

		# important that our query finds 1 and only 1 result
		if not check_provided_spell:
			raise ValueError("source_spell not found.")
		
		elif len(check_provided_spell) > 1:
			raise ValueError(f"Multiple spells found with the provided spell name: {[spell[1] for spell in check_provided_spell]}.")

		source_spell = check_provided_spell[0] # load spell tuple from db

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


def find_Fusion_target():
	"""
	Given a spell, return any available Fusion spell targets.
	"""

	return


def main():

	# test if error handling properly works for non-specific spell queries
	#find_Accel_Synchro_target("ray", "doyle")

	# test if error handling properly works for nonexistent query
	#for spell in find_Accel_Synchro_target("death ward", 2):
	#	print(spell)

	return 0



if __name__ == "__main__":
	main()