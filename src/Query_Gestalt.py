import sqlite3



def find_Accel_Synchro_target(source_spell: str, synchro_route: str):
	"""
	Given a spell and Accel Synchro route (counterspelled, reaction, main action),
	determine the available spell options.

	Raises
	------
	No spell found with the provided spell name.
		source_spell was not found in the database.
	Multiple spells found with the provided spell name.
		source_spell had multiple matches in the database.
	"""

	with sqlite3.connect("../Gestalt.db") as connection:
		gestalt_cursor = connection.cursor()
		gestalt_cursor.execute("SELECT * FROM Spell WHERE spell_name LIKE ?", [f"%{source_spell}%"])

		check_provided_spell = gestalt_cursor.fetchall()

		# 
		if not check_provided_spell:
			raise Exception("No spell found with the provided spell name.")
		
		elif len(check_provided_spell) > 1:
			raise Exception(f"Multiple spells found with the provided spell name: {[spell[1] for spell in check_provided_spell]}.")

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
	#find_Accel_Synchro_target("ploopy", "doyle")

	return 0



if __name__ == "__main__":
	main()