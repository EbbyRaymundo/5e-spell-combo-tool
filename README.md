# 5e spell Combo Tool
This tool is a database with an API for querying and adding custom 5e spells. The spells intended to be added to the database are standard, XYZ, Fusion, and Link spells. Rather than adding Synchro spells (it wouldn't make sense since it's just fancy upcasting), you can use querying to find Synchro compatible spells and Accel Synchro targets.

## Extra Deck Spellcasting Methods

### Synchro Spellcasting

To Synchro Cast on their turn, the user consumes 1 leveled spell slot of level X in addition to casting a spell of a level of Y, then increases that spell’s level by Y. For example, a 5th level mage casts the spell Fireball at 3rd level and consumes a 2nd-level spell slot to increase Fireball’s cast level to 5, which would normally be unobtainable at that mage’s level. The conditions for a Synchro cast are below:
1. The user must have the ability to cast spells innately.
2. The user must have both hands-free meaning that they cannot carry a shield. At most, they can hold an arcane focus, wand, or staff.
3. The user must have a number of sorcery points equal to the level of the spell they wish to cast.
4. The user also consumes their bonus action.
If one performs a Synchro Cast, they cannot use any other sorcery points that turn (besides for use of Empowered Spell).

To perform any type of Synchro Cast, a mage redirects the energy of their spell slots by moving their hands in a circle while consuming the lower-leveled spell, creating an emerald ring of light, then pushing the energy of the higher-leveled spell outward.

In addition to the benefits of casting a spell that one would otherwise be unable to cast, the spell’s power tends to be enhanced.
#### Accelerated Synchro Spellcasting (A.K.A. Accel Synchro)
In addition to the conditions needed for a normal Synchro Spellcast, the user must also follow these conditions:
1. The spells cast must be in the same school.
2. If one performs an Accel Cast, they cannot use any other sorcery points that turn (besides for use of Empowered Spell).

The sequence of an Accel Casting is simple in concept but extremely difficult to execute. There are 3 main routes: either their spell was just counterspelled, they attempted it as a reaction, or they’re using it as the main action.

1. **Counterspell route**: If their spell was successfully counterspelled by an opponent, they can Synchro Cast as a bonus action. This allows the caster to reabsorb the spell's energy, then as part of the same spellcasting move, they consume another leveled spell slot to cast a spell of a higher level. For example, if a level 5 Sorcerer casts Magic Missile, a 1st level Evocation spell, that is counterspelled, they can reabsorb that energy and consume a level 3 spell slot and 4 Sorcery points to cast the 4th Level Evocation spell Ice Storm.
2. **Reaction route**: If the user is attempting to cast a spell as a reaction, they can perform an Accel Cast as normal with extra conditions in addition to the ones listed above:
   - The user cannot cast 2 spells in order to Accel Cast; instead, they must use a spell that either has a duration that they are currently maintaining or it must be a Concentration spell. In either case, the spell’s effects are then ended in favor of the Accel Casting.
   - The spell they are Accel Casting must have a casting time of a reaction.
For example, if a mage has the 1st-level spell Mage Armor active, they can consume a 2nd-level spell slot and 3 sorcery points to cast Counterspell. This type of Accel Casting is fairly limited as many higher-level spells do not have a casting time of a reaction. Its main purpose is to provide a means of Counterspelling as a last resort by consuming a spell they have active in favor of preventing a bigger threat created by an enemy’s spellcasting.
3. **Main Action Route**: This version is very similar to the reaction route, in which they use a spell that either has a duration they have already cast or a Concentration spell. However, the main differentiation is that there is no limitation on the casting time.

### Fusion Spellcasting

1. When fusing two or more spells, the duration will typically be that of the shortest spell.
2. For instantaneous spells, you can use your main action to cast the first spell for no effect, then use polymerization with a bonus action to retroactively fuse it.
3. Cantrips count as a 1st level spell for the purposes of sorcery point cost.

#### What Fusion spells can I use?

1. **Polymerization** (1st lvl, Transmutation, 1 bonus action, Self, V, S, M (at least 2 spells), Instantaneous): You attempt to fuse 2 or more spells in order to create a more powerful version that combines their aspects in some way. If you consume a number of sorcery points equal to the total level of both spells, you can use Polymerization without having to actually cast the spells. Both spell slots are consumed as if you had cast them.
2. **Super Polymerization** (4th lvl, Transmutation, 1 action or reaction, Self, V, S, M (at least 2 spells), Instantaneous): You fuse 2 or more spells in order to create a more powerful version that combines their aspects in some way. Both spell slots are consumed as if you had cast them. You may also use spells that your opponent is currently casting or has already cast whose effects remain. No one may attempt to interrupt the casting of this spell.
