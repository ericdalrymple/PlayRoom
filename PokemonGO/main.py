import collections
import pokemon.pokemon_queries as pq
import pokemon.pokemon_types as pt

print()

restrictions = [pt.ELECTRIC, pt.FLYING, pt.GHOST, pt.GRASS, pt.ICE, pt.NORMAL]

atk_ratings = pq.get_resistance_ratings(restrictions)
for k, v in atk_ratings.items():
    print(str(k) + ":" + str(v))

t = [
    [pt.NORMAL, pt.WATER],
    [pt.NORMAL, pt.ELECTRIC],
    [pt.NORMAL, pt.FAIRY],
    [pt.NORMAL, pt.FLYING],
    [pt.NORMAL, pt.NONE],
    [pt.NORMAL, pt.DARK],
    [pt.FLYING, pt.DRAGON],
    [pt.FLYING, pt.DARK],
    [pt.ELECTRIC, pt.NONE],
    [pt.ELECTRIC, pt.GROUND],
    [pt.GRASS, pt.FAIRY],
    [pt.GRASS, pt.NONE],
    [pt.GRASS, pt.ICE],
    [pt.ICE, pt.DRAGON],
    [pt.ICE, pt.NONE],
    [pt.ICE, pt.STEEL],
    [pt.FLYING, pt.BUG],
    [pt.GHOST, pt.GROUND],
    [pt.GHOST, pt.BUG],
    [pt.GHOST, pt.NONE],
]

tr = {}
for ti in t:
    r = pq.get_defender_rating(ti[0], ti[1])
    if r in tr.keys():
        tr[r].append(ti)
    else:
        tr[r] = [ti]

print()
trs = collections.OrderedDict(sorted(tr.items()))
for key, val in trs.items():
    print(str(key) + " : " + str(val))

pq.print_effectiveness_ratings(restrictions)

'''
sample = [ICE, PSYCHIC]
print(sample)
print(get_defender_weaknesses(sample[0], sample[1]))
print(get_defender_resistances(sample[0], sample[1]))
print(get_attack_effectiveness(DARK, sample[0], sample[1]))
print(get_attack_effectiveness(ICE, sample[0], sample[1]))
print(get_attack_effectiveness(NORMAL, sample[0], sample[1]))
'''