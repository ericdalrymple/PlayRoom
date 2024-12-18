import collections
from pokemon import pokemon_types as pt


def get_resistances(type):
    return pt.RESISTANCES[type]


def get_weaknesses(type):
    return pt.WEAKNESSES[type]


def get_defender_resistances(typeA, typeB = pt.NONE):
    r = get_resistances(typeA) + get_resistances(typeB)
    w = get_weaknesses(typeA) + get_weaknesses(typeB)
    return list(set(r) - set(w))


def get_defender_weaknesses(typeA, typeB = pt.NONE):
    r = get_resistances(typeA) + get_resistances(typeB)
    w = get_weaknesses(typeA) + get_weaknesses(typeB)
    return list(set(w) - set(r))


def get_defender_rating(typeA, typeB = pt.NONE):
    w = get_defender_weaknesses(typeA, typeB)
    r = get_defender_resistances(typeA, typeB)
    effective_count = len(pt.TYPES) - 1
    wr = len(w) / effective_count
    rr = len(r) / effective_count
    return rr - wr


def get_resistance_rankings(includes = []):
    rankings = {}
    for i in range(0, len(pt.TYPES)):
        for j in range(i + 1, len(pt.TYPES)):
            if (len(includes) != 0) and (not pt.TYPES[i] in includes and not pt.TYPES[j] in includes):
                continue 

            resistance_count = len(get_defender_resistances(pt.TYPES[i], pt.TYPES[j]))
            
            current_type = [pt.TYPES[i], pt.TYPES[j]]
            if not resistance_count in rankings.keys():
                rankings[resistance_count] = [current_type]
            else:
                rankings[resistance_count].append(current_type)
    
    return collections.OrderedDict(sorted(rankings.items()))


def get_resistance_ratings(includes = []):
    ratings = {}
    for i in range(0, len(pt.TYPES)):
        for j in range(i + 1, len(pt.TYPES)):
            if (len(includes) != 0) and (not pt.TYPES[i] in includes and not pt.TYPES[j] in includes):
                continue

            rating = get_defender_rating(pt.TYPES[i], pt.TYPES[j])
            
            current_type = [pt.TYPES[i], pt.TYPES[j]]
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
    for i in range(0, len(pt.TYPES)):
        for j in range(i + 1, len(pt.TYPES)):
            if (len(includes) != 0) and (not pt.TYPES[i] in includes and not pt.TYPES[j] in includes):
                continue

            if get_attack_effectiveness(atk_type, pt.TYPES[i], pt.TYPES[j]) > 0:
                targets.append([pt.TYPES[i], pt.TYPES[j]])
    
    return targets

def get_attack_resistors(atk_type, includes = []):
    resistors = []
    for i in range(0, len(pt.TYPES)):
        for j in range(i + 1, len(pt.TYPES)):
            if (len(includes) != 0) and (not pt.TYPES[i] in includes and not pt.TYPES[j] in includes):
                continue

            if get_attack_effectiveness(atk_type, pt.TYPES[i], pt.TYPES[j]) < 0:
                resistors.append([pt.TYPES[i], pt.TYPES[j]])
    
    return resistors


def get_effectiveness_ratings(includes = []):
    ratings = {}
    for ti in pt.TYPES:
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
