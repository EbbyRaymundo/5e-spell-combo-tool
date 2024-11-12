SELECT spell_name, level, duration, range, concentration
FROM Spell
WHERE (casting_time == "Action" OR casting_time == "Bonus Action")
AND level > 5
AND school == "Evocation";