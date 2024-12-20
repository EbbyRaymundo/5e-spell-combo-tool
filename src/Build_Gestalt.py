'''
This file is for creating the tables for the Gestalt database
and adding constraints. This does not need to be run by the user
unless they want to delete their database and rebuild their
tables.
'''



def create_spell_table(cursor):
	'''
	Initialize the Spell table with constraints.

	Parameters
	----------
	cursor

	Returns
	-------
	0: int
		Function successful.
	'''
	cursor.execute(
		"""
		CREATE TABLE Spell (
			spell_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
			spell_name TEXT UNIQUE NOT NULL,
			level INTEGER NOT NULL,
			casting_time TEXT NOT NULL,
			duration TEXT NOT NULL,
			school TEXT NOT NULL,
			range TEXT NOT NULL,
			components TEXT NOT NULL,
			description TEXT UNIQUE NOT NULL,
			upcast_effect TEXT,
			concentration INTEGER CHECK (concentration IN (0, 1)) NOT NULL,
			ritual INTEGER CHECK (concentration IN (0, 1)) NOT NULL
		)
		"""
	)
	

	# this index will optimize the Accel Synchro queries in Query_Gestalt.py
	cursor.execute(
		"""
		CREATE INDEX Spell_school_casting_time_level_idx
		ON Spell(school, casting_time, level)
		"""
	)
	
	return 0


def create_class_table(cursor):
	'''
	Initialize the Class table with the PK constraint.

	Parameters
	----------
	cursor

	Returns
	-------
	0: int
		Function successful.
	'''
	cursor.execute(
		"""
		CREATE TABLE Class(
			character_class_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
			character_class TEXT UNIQUE NOT NULL
		)
		"""
	)

	return 0


def create_fusion_table(cursor):
	'''
	Initialize the Fusion table with the PK constraint.

	Paramters
	---------
	cursor

	Returns
	-------
	0: int
		Function successful.
	'''
	cursor.execute(
		"""
		CREATE TABLE Fusion(
			fusion_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
			fusion_name TEXT UNIQUE NOT NULL,
			duration TEXT NOT NULL,
			range TEXT NOT NULL,
			description TEXT UNIQUE NOT NULL,
			concentration INTEGER CHECK (concentration IN (0, 1)) NOT NULL
		)
		"""
	)

	return 0


def create_xyz_table(cursor):
	'''
	Initialize the XYZ table with constraints.

	Parameters
	----------
	cursor: sqlite3.cursor

	Returns
	-------
	0: int
		Function successful.
	'''
	cursor.execute(
		"""
		CREATE TABLE XYZ(
			xyz_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
			xyz_name TEXT UNIQUE NOT NULL,
			rank INTEGER NOT NULL,
			casting_time TEXT NOT NULL,
			duration TEXT NOT NULL,
			range TEXT NOT NULL,
			components TEXT NOT NULL,
			description TEXT UNIQUE NOT NULL
		)
		"""
		)
	
	return 0


def create_link_table(cursor):
	'''
	Initialize the Link table with constraints.

	Parameters
	----------
	cursor

	Returns
	-------
	0: int
		Function successful.
	'''
	cursor.execute(
		"""
		CREATE TABLE Link(
			link_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
			link_name TEXT UNIQUE NOT NULL,
			rating INTEGER NOT NULL,
			casting_time TEXT NOT NULL,
			duration TEXT NOT NULL,
			range TEXT NOT NULL,
			components TEXT NOT NULL,
			description TEXT UNIQUE NOT NULL
		)
		"""
		)
	
	return 0


def create_spell_class_table(cursor):
	'''
	Initialize the Spell_Class junction table with FK constraints.

	Parameters
	----------
	cursor

	Returns
	-------
	0: int
		Function successful.
	'''
	cursor.execute(
		"""
		CREATE TABLE Spell_Class(
			spell_id INTEGER NOT NULL,
			character_class_id INTEGER NOT NULL,
			FOREIGN KEY (spell_id) REFERENCES Spell(spell_id) ON DELETE CASCADE,
			FOREIGN KEY (character_class_id) REFERENCES Class(character_class_id) ON DELETE CASCADE,
			PRIMARY KEY (spell_id, character_class_id)
		)
		"""
	)

	return 0


def create_spell_fusion_table(cursor):
	'''
	Initialize the Spell_Fusion junction table with FK constraints.

	Parameters
	----------
	cursor

	Returns
	-------
	0: int
		Function successful.
	'''
	cursor.execute(
		"""
		CREATE TABLE Spell_Fusion(
			spell_id INTEGER NOT NULL,
			fusion_id INTEGER NOT NULL,
			FOREIGN KEY (spell_id) REFERENCES Spell(spell_id) ON DELETE CASCADE,
			FOREIGN KEY (fusion_id) REFERENCES Fusion(fusion_id) ON DELETE CASCADE,
			PRIMARY KEY (spell_id, fusion_id)
		)
		"""
	)

	# this index will optimize the get_Fusion_targets() function in Query_Gestalt.py
	cursor.execute(
		"""
		CREATE INDEX Spell_Fusion_fusion_id_idx 
		ON Spell_Fusion(fusion_id)
		"""
		)

	return 0


def create_spell_fusion_table(cursor):
	'''
	Initialize the Spell_Fusion junction table with FK constraints.

	Parameters
	----------
	cursor

	Returns
	-------
	0: int
		Function successful.
	'''
	cursor.execute(
		"""
		CREATE TABLE Spell_Fusion(
			spell_id INTEGER NOT NULL,
			fusion_id INTEGER NOT NULL,
			FOREIGN KEY (spell_id) REFERENCES Spell(spell_id) ON DELETE CASCADE,
			FOREIGN KEY (fusion_id) REFERENCES Fusion(fusion_id) ON DELETE CASCADE,
			PRIMARY KEY (spell_id, fusion_id)
		)
		"""
	)

	return 0


def create_xyz_class_table(cursor):
	'''
	Initialize the XYZ_Class junction table with FK constraints.

	Parameters
	----------
	cursor

	Returns
	-------
	0: int
		Function successful.
	'''
	cursor.execute(
		"""
		CREATE TABLE XYZ_Class(
			xyz_id INTEGER NOT NULL,
			character_class_id INTEGER NOT NULL,
			FOREIGN KEY (xyz_id) REFERENCES XYZ(xyz_id) ON DELETE CASCADE,
			FOREIGN KEY (character_class_id) REFERENCES Class(character_class_id) ON DELETE CASCADE,
			PRIMARY KEY (xyz_id, character_class_id)
		)
		"""
	)

	return 0


def create_link_class_table(cursor):
	'''
	Initialize the Link_Class junction table with FK constraints.

	Parameters
	----------
	cursor

	Returns
	-------
	0: int
		Function successful.
	'''
	cursor.execute(
		"""
		CREATE TABLE Link_Class(
			link_id INTEGER NOT NULL,
			character_class_id INTEGER NOT NULL,
			FOREIGN KEY (link_id) REFERENCES Link(link_id) ON DELETE CASCADE,
			FOREIGN KEY (character_class_id) REFERENCES Class(character_class_id) ON DELETE CASCADE,
			PRIMARY KEY (link_id, character_class_id)
		)
		"""
	)


def main():

	return 0



if __name__ == "__main__":
	main()