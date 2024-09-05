import sqlite3



def find_Accel_Synchro_target(source_spell: str, synchro_route: str):
	"""
	Given a spell and Accel Synchro route (counterspelled, reaction, main action),
	determine the available spell options.
	"""

	with sqlite3.connect("../Gestalt.db") as connection:
		gestalt_cursor = connection.cursor()
		gestalt_cursor.execute("SELECT * FROM Spell WHERE spell_name LIKE ?", [f"%{source_spell}%"])

		check_provided_spell = gestalt_cursor.fetchall()

		if not check_provided_spell: # no spells were found with given name
			raise Exception("No spell found with the provided spell name")
		
		elif len(check_provided_spell) > 1:
			raise Exception(f"Multiple spells found with the provided spell name: {[spell[1] for spell in check_provided_spell]}")

		return gestalt_cursor.fetchall()

	return

def find_Fusion_target():
	"""
	Given a spell, return any available Fusion spell targets.
	"""

	return


def main():

	for spell in find_Accel_Synchro_target("ray", "doyle"):
		print(spell)

	return 0



if __name__ == "__main__":
	main()