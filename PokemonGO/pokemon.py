import collections

TYPE_NONE = ''
TYPE_BUG = 'BUG'
TYPE_DARK = 'DARK'
TYPE_DRAGON = 'DRAGON'
TYPE_ELECTRIC = 'ELECTRIC'
TYPE_FAIRY = 'FAIRY'
TYPE_FIGHTING = 'FIGHTING'
TYPE_FIRE = 'FIRE'
TYPE_FLYING = 'FLYING'
TYPE_GHOST = 'GHOST'
TYPE_GRASS = 'GRASS'
TYPE_GROUND = 'GROUND'
TYPE_ICE = 'ICE'
TYPE_NORMAL = 'NORMAL'
TYPE_POISON = 'POISON'
TYPE_PSYCHIC = 'PSYCHIC'
TYPE_ROCK = 'ROCK'
TYPE_STEEL = 'STEEL'
TYPE_WATER = 'WATER'

types = [
    TYPE_NONE,
    TYPE_BUG,
    TYPE_DARK,
    TYPE_DRAGON,
    TYPE_ELECTRIC,
    TYPE_FAIRY,
    TYPE_FIGHTING,
    TYPE_FIRE,
    TYPE_FLYING,
    TYPE_GHOST,
    TYPE_GRASS,
    TYPE_GROUND,
    TYPE_ICE,
    TYPE_NORMAL,
    TYPE_POISON,
    TYPE_PSYCHIC,
    TYPE_ROCK,
    TYPE_STEEL,
    TYPE_WATER]

weaknesses = {
    TYPE_NONE:[],
    TYPE_BUG:[TYPE_FIRE, TYPE_FLYING, TYPE_ROCK],
    TYPE_DARK:[TYPE_BUG, TYPE_FAIRY, TYPE_FIGHTING],
    TYPE_DRAGON:[TYPE_DRAGON, TYPE_FAIRY, TYPE_ICE],
    TYPE_ELECTRIC:[TYPE_GROUND],
    TYPE_FAIRY:[TYPE_POISON, TYPE_STEEL],
    TYPE_FIGHTING:[TYPE_FAIRY, TYPE_FLYING, TYPE_PSYCHIC],
    TYPE_FIRE:[TYPE_GROUND, TYPE_ROCK, TYPE_WATER],
    TYPE_FLYING:[TYPE_ELECTRIC, TYPE_ICE, TYPE_ROCK],
    TYPE_GHOST:[TYPE_DARK, TYPE_GHOST],
    TYPE_GRASS:[TYPE_BUG, TYPE_FIRE, TYPE_FLYING, TYPE_ICE, TYPE_POISON],
    TYPE_GROUND:[TYPE_GRASS, TYPE_ICE, TYPE_WATER],
    TYPE_ICE:[TYPE_FIGHTING, TYPE_FIRE, TYPE_ROCK, TYPE_STEEL],
    TYPE_NORMAL:[TYPE_FIGHTING],
    TYPE_POISON:[TYPE_GROUND, TYPE_PSYCHIC],
    TYPE_PSYCHIC:[TYPE_BUG, TYPE_DARK, TYPE_GHOST],
    TYPE_ROCK:[TYPE_FIGHTING, TYPE_GRASS, TYPE_GROUND, TYPE_STEEL, TYPE_WATER],
    TYPE_STEEL:[TYPE_FIGHTING, TYPE_FIRE, TYPE_GROUND],
    TYPE_WATER:[TYPE_ELECTRIC, TYPE_GRASS]}

resistances = {
    TYPE_NONE:[],
    TYPE_BUG:[TYPE_FIGHTING, TYPE_GRASS, TYPE_GROUND],
    TYPE_DARK:[TYPE_DARK, TYPE_GHOST, TYPE_PSYCHIC],
    TYPE_DRAGON:[TYPE_ELECTRIC, TYPE_FIRE, TYPE_GRASS, TYPE_WATER],
    TYPE_ELECTRIC:[TYPE_ELECTRIC, TYPE_FLYING, TYPE_STEEL],
    TYPE_FAIRY:[TYPE_BUG, TYPE_DARK, TYPE_DRAGON, TYPE_FIGHTING],
    TYPE_FIGHTING:[TYPE_BUG, TYPE_DARK, TYPE_ROCK],
    TYPE_FIRE:[TYPE_BUG, TYPE_FAIRY, TYPE_FIRE, TYPE_GRASS, TYPE_ICE, TYPE_STEEL],
    TYPE_FLYING:[TYPE_BUG, TYPE_FIGHTING, TYPE_GRASS, TYPE_GROUND],
    TYPE_GHOST:[TYPE_BUG, TYPE_FIGHTING, TYPE_NORMAL, TYPE_NORMAL],
    TYPE_GRASS:[TYPE_ELECTRIC, TYPE_GRASS, TYPE_GROUND, TYPE_WATER],
    TYPE_GROUND:[TYPE_ELECTRIC, TYPE_POISON, TYPE_ROCK],
    TYPE_ICE:[TYPE_ICE],
    TYPE_NORMAL:[TYPE_GHOST],
    TYPE_POISON:[TYPE_BUG, TYPE_FAIRY, TYPE_FIGHTING, TYPE_GRASS, TYPE_POISON],
    TYPE_PSYCHIC:[TYPE_FIGHTING, TYPE_PSYCHIC],
    TYPE_ROCK:[TYPE_FIRE, TYPE_FLYING, TYPE_NORMAL, TYPE_POISON],
    TYPE_STEEL:[TYPE_BUG, TYPE_DRAGON, TYPE_FAIRY, TYPE_FLYING, TYPE_GRASS, TYPE_ICE, TYPE_NORMAL, TYPE_POISON, TYPE_PSYCHIC, TYPE_ROCK, TYPE_STEEL],
    TYPE_WATER:[TYPE_FIRE, TYPE_ICE, TYPE_STEEL, TYPE_WATER]}


def get_resistances(type):
    return resistances[type]


def get_weaknesses(type):
    return weaknesses[type]


def get_defender_resistances(typeA, typeB = TYPE_NONE):
    r = get_resistances(typeA) + get_resistances(typeB)
    w = get_weaknesses(typeA) + get_weaknesses(typeB)
    return list(set(r) - set(w))


def get_defender_weaknesses(typeA, typeB = TYPE_NONE):
    r = get_resistances(typeA) + get_resistances(typeB)
    w = get_weaknesses(typeA) + get_weaknesses(typeB)
    return list(set(w) - set(r))


def get_defender_rating(typeA, typeB = TYPE_NONE):
    w = get_defender_weaknesses(typeA, typeB)
    r = get_defender_resistances(typeA, typeB)
    effective_type_count = len(types) - 1
    wr = len(w) / effective_type_count
    rr = len(r) / effective_type_count
    return rr - wr


def get_resistance_rankings(includes = []):
    rankings = {}
    for i in range(0, len(types)):
        for j in range(i + 1, len(types)):
            if (not len(includes) is 0) and (not types[i] in includes and not types[j] in includes):
                continue 

            resistance_count = len(get_defender_resistances(types[i], types[j]))
            
            current_type = [types[i], types[j]]
            if not resistance_count in rankings.keys():
                rankings[resistance_count] = [current_type]
            else:
                rankings[resistance_count].append(current_type)
    
    return collections.OrderedDict(sorted(rankings.items()))


def get_resistance_ratings(includes = []):
    ratings = {}
    for i in range(0, len(types)):
        for j in range(i + 1, len(types)):
            if (not len(includes) is 0) and (not types[i] in includes and not types[j] in includes):
                continue

            rating = get_defender_rating(types[i], types[j])
            
            current_type = [types[i], types[j]]
            if not rating in ratings.keys():
                ratings[rating] = [current_type]
            else:
                ratings[rating].append(current_type)
    
    return collections.OrderedDict(sorted(ratings.items()))


def get_attack_effectiveness(atk_type, typeA, typeB):
    if atk_type in get_defender_resistances(typeA, typeB):
        # Not effective
        return -1
    
    if atk_type in get_defender_weaknesses(typeA, typeB):
        # Effective
        return 1
    
    # Neutral
    return 0


def get_attack_targets(atk_type, includes = []):
    targets = []
    for i in range(0, len(types)):
        for j in range(i + 1, len(types)):
            if (not len(includes) is 0) and (not types[i] in includes and not types[j] in includes):
                continue

            if get_attack_effectiveness(atk_type, types[i], types[j]) > 0:
                targets.append([types[i], types[j]])
    
    return targets

def get_attack_resistors(atk_type, includes = []):
    resistors = []
    for i in range(0, len(types)):
        for j in range(i + 1, len(types)):
            if (not len(includes) is 0) and (not types[i] in includes and not types[j] in includes):
                continue

            if get_attack_effectiveness(atk_type, types[i], types[j]) < 0:
                resistors.append([types[i], types[j]])
    
    return resistors


def get_effectiveness_ratings(includes = []):
    ratings = {}
    for ti in types:
        targets = get_attack_targets(ti, includes)
        resistors = get_attack_resistors(ti, includes)
        target_count = len(targets) - len(resistors)
        if not target_count in ratings.keys():
            ratings[target_count] = [ti]
        else:
            ratings[target_count].append(ti)

    return collections.OrderedDict(sorted(ratings.items()))


def get_defender_teams():
    teams = {}
    return teams


def print_effectiveness_ratings(includes = []):
    print()
    r = get_effectiveness_ratings(includes)
    for k, v in r.items():
        print(str(k) + " : " + str(v))


print()

restrictions = [TYPE_ELECTRIC, TYPE_FLYING, TYPE_GHOST, TYPE_GRASS, TYPE_ICE, TYPE_NORMAL]

atk_ratings = get_resistance_ratings(restrictions)
for k, v in atk_ratings.items():
    print(str(k) + ":" + str(v))

t = [
    [TYPE_NORMAL, TYPE_WATER],
    [TYPE_NORMAL, TYPE_ELECTRIC],
    [TYPE_NORMAL, TYPE_FAIRY],
    [TYPE_NORMAL, TYPE_FLYING],
    [TYPE_NORMAL, TYPE_NONE],
    [TYPE_NORMAL, TYPE_DARK],
    [TYPE_FLYING, TYPE_DRAGON],
    [TYPE_FLYING, TYPE_DARK],
    [TYPE_ELECTRIC, TYPE_NONE],
    [TYPE_ELECTRIC, TYPE_GROUND],
    [TYPE_GRASS, TYPE_FAIRY],
    [TYPE_GRASS, TYPE_NONE],
    [TYPE_GRASS, TYPE_ICE],
    [TYPE_ICE, TYPE_DRAGON],
    [TYPE_ICE, TYPE_NONE],
    [TYPE_ICE, TYPE_STEEL],
    [TYPE_FLYING, TYPE_BUG],
    [TYPE_GHOST, TYPE_GROUND],
    [TYPE_GHOST, TYPE_BUG],
    [TYPE_GHOST, TYPE_NONE],
]

tr = {}
for ti in t:
    r = get_defender_rating(ti[0], ti[1])
    if r in tr.keys():
        tr[r].append(ti)
    else:
        tr[r] = [ti]

print()
trs = collections.OrderedDict(sorted(tr.items()))
for key, val in trs.items():
    print(str(key) + " : " + str(val))

print_effectiveness_ratings(restrictions)

'''
sample = [TYPE_ICE, TYPE_PSYCHIC]
print(sample)
print(get_defender_weaknesses(sample[0], sample[1]))
print(get_defender_resistances(sample[0], sample[1]))
print(get_attack_effectiveness(TYPE_DARK, sample[0], sample[1]))
print(get_attack_effectiveness(TYPE_ICE, sample[0], sample[1]))
print(get_attack_effectiveness(TYPE_NORMAL, sample[0], sample[1]))
'''