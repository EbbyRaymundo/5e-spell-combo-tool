import sqlite3



def find_Accel_Synchro_target(source_spell: str, synchro_route: int):
	"""
	Given a spell and Accel Synchro route specifier (counterspelled: 0,
	reaction: 1, main action: 2), determine the available spell options.
	Refer to README for details on different Accel Synchro routes.

	Returns
	-------
	target_spells: list[tuple]
		List of tuples representing valid Accel Synchro target spells

	Raises
	------
	ValueError
		synchro_route not a valid Accel Synchro route (counterspelled, reaction, main action)
	ValueError
		source_spell was not found in the database.
	ValueError
		source_spell has multiple matches in the database.

	TODO: add 3 different queries to handle the different synchro routes
	"""
	if not synchro_route in range(3):
		raise ValueError(
			f"{synchro_route} not a valid Accel Synchro route (counterspelled: 0, reaction: 1, main action: 2)"
			)

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

		spell_level = source_spell[2]
		spell_school = source_spell[5]

		route_constraints = ""

		if synchro_route == 0: # Synchro spell has just been counterspelled
			route_constraints = """
				(casting_time == "Action" OR casting_time == "Bonus Action")
				AND level > ?
				AND school == ?
				"""
		# could potentially add a check here to see if the input spell is a valid
		# source spell (duration != "Instantaneous"). Spells are weird so we
		# might just have to trust the caller.
		elif synchro_route == 1: # ending active spell to cast a reaction spell
			route_constraints = """
				casting_time == "Reaction"
				AND level > ?
				AND school == ?
				"""
		elif synchro_route == 2: # using main action, no limit on casting time
			route_constraints = """
				level > ?
				AND school == ?
				"""

		gestalt_cursor.execute(f"SELECT * FROM Spell WHERE {route_constraints}", (spell_level, spell_school))

		return gestalt_cursor.fetchall()

	return

def find_Fusion_target():
	"""
	Given a spell, return any available Fusion spell targets.
	"""

	return


def main():

	# test if error handling properly works for non-specific spell queries
	#find_Accel_Synchro_target("ray", "doyle")

	# test if error handling properly works for nonexistent query
	for spell in find_Accel_Synchro_target("death ward", 2):
		print(spell)

	return 0



if __name__ == "__main__":
	main()