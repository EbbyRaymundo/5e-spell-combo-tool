"""
Notes to self:
- .timer on to time db operations
- .expert on for index suggestions
- Prefix query with EXPLAIN QUERY PLAN to check if any queries
  have to scan across a table.
"""



# TODO: decide if I want to add error handling to the Accel Synchro getters to
#		check if the input spell has a duration greater than Instantaneous.
# TODO: change the getters to handle a list of int spell_id's instead of a single input.
def get_counterspelled_Accel_Synchro(connection, spell_id: int):
	'''
	Given the spell_id of a spell with a duration longer than "Instantaneous", 
	determine the eligible Reaction spells to Accel Synchro into.

	Parameters
	----------
	connection:
		Database connection to Gestalt.db.
	spell_id: int

	Returns
	-------
	target_spells
		Counterspelled Accel Synchro target spells.

	Raises
	------
	ValueError
		Provided spell_id not found in Spell table
	'''

	return


def get_reaction_Accel_Synchro(connection, spell_id: int):
	'''
	Given a spell with a duration greater than Instantaneous, determine the
	eligible Reaction spells to Accel Synchro into.

	Parameters
	----------
	connection:
		Database connection to Gestalt.db.
	source_spell: int
		spell_id of the source spell.
	
	Returns
	-------
	target_spells
		Reaction Accel Synchro target spells.

	Raises
	------
	ValueError
		Provided spell_id not found in Spell table
	'''

	return


def get_main_action_Accel_Synchro(connection, spell_id: int):
	'''
	Given the spell_id of a spell with a duration greater than Instantaneous,
	determine the eligible spells to Accel Synchro into.

	Parameters
	----------
	connection:
		Database connection to Gestalt.db.
	spell_id: int
	
	Returns
	-------
	target_spells
		Reaction Accel Synchro target spells.

	Raises
	------
	ValueError
		Provided spell_id not found in Spell table
	'''

	return


def get_Fusion_targets(connection, spell_id: int):
	'''
	Given a spell_id, return any available Fusion spell targets and their
	spell components, EXCEPT for the input spell.

	Parameters
	----------
	connection:
		Database connection to Gestalt.db.
	spell_id: int

	Returns
	-------
	target_fusions:
		Eligible Fusion spells that use the provided spell and their constituent
		spells. Result in format [consituent_spell, target_fusion].
	'''

	return


def main():

	return 0



if __name__ == "__main__":
	main()