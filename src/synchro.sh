#! /bin/bash

sqlite3 -csv ../Gestalt.db 'SELECT * FROM Spell WHERE (casting_time == "Action" OR casting_time == "Bonus Action") AND level > 5 AND school == "Evocation"' > synchro_results.csv