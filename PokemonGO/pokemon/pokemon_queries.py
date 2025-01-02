import collections
import operator
from pokemon import pokemon_types as pt

def team_hash(pairA, pairB, pairC):
    hashA = pt.type_pair_hash(pairA)
    hashB = pt.type_pair_hash(pairB)
    hashC = pt.type_pair_hash(pairC)
    return "[" + hashA + hashB + hashC + "]"


"""
Returns a set of types to which 'type' is resistant.
"""
def get_resistances(type):
    return set(pt.RESISTANCES[type])

"""
Returns a set of types to which 'type' is vulnerable.
"""
def get_weaknesses(type):
    return set(pt.WEAKNESSES[type])

"""
Returns a set of types to which the type pair is net resistaant.
"""
def get_defender_resistances(typeA, typeB = pt.NONE):
    r = get_resistances(typeA) | get_resistances(typeB)
    w = get_weaknesses(typeA) | get_weaknesses(typeB)
    return set(r - w)

"""
Returns a set of types to which the type pair is net vulnerable.
"""
def get_defender_weaknesses(typeA, typeB = pt.NONE):
    r = get_resistances(typeA) | get_resistances(typeB)
    w = get_weaknesses(typeA) | get_weaknesses(typeB)
    return set(w - r)

"""
Returns a defender rating value between -1 and 1 where -1 indicates
the type pair has a net vulnerability to every other type and 1
indicates the type pair has a net resistance to every other pair.

Negative values indicate the type pair has more vulnerabilities
than resistances.

Positive values indicate the type pair has more resistances
than vulnerabilities.
"""
def get_defender_rating(typeA, typeB = pt.NONE):
    w = get_defender_weaknesses(typeA, typeB)
    r = get_defender_resistances(typeA, typeB)
    effective_count = len(pt.TYPES) - 1
    wr = len(w) / effective_count
    rr = len(r) / effective_count
    return rr - wr


"""
Returns a dictionary of all type combinations ordered by their
net number of resistances from least to most.
"""
def get_resistance_rankings(includes = []):
    rankings = {}
    for p in pt.REAL_TYPE_PAIRS.values():
        if (len(includes) != 0) and (not p[0] in includes and not p[1] in includes):
            continue 

        resistance_count = len(get_defender_resistances(p[0], p[1]))
        
        if not resistance_count in rankings.keys():
            rankings[resistance_count] = [p]
        else:
            rankings[resistance_count].append(p)
    
    return collections.OrderedDict(sorted(rankings.items()))


"""
Returns a dictionary of all type combinations ordered by their
resistance ratings from smallest to largest.
"""
def get_resistance_ratings(includes = []):
    ratings = {}
    for t in pt.REAL_TYPE_PAIRS.values():
        if (len(includes) != 0) and (not t[0] in includes and not t[1] in includes):
            continue

        rating = get_defender_rating(t[0], t[1])
        
        if not rating in ratings.keys():
            ratings[rating] = [t]
        else:
            ratings[rating].append(t)
    
    return collections.OrderedDict(sorted(ratings.items()))


"""
Returns a number indicating whether an attack type is effective (1),
neutral (0), or ineffective (-1) againts a Pokemon of the specified
type combination.
"""
def get_attack_effectiveness(atk_type, typeA, typeB):
    if atk_type in get_defender_resistances(typeA, typeB):
        # Not effective
        return -1
    
    if atk_type in get_defender_weaknesses(typeA, typeB):
        # Effective
        return 1
    
    # Neutral
    return 0


"""
Returns an array of type combinations against which the specified attack
type is effective.
"""
def get_attack_targets(atk_type, includes = []):
    targets = []
    for t in pt.REAL_TYPE_PAIRS.values():
        if (len(includes) != 0) and (not t[0] in includes and not t[1] in includes):
            continue

        if get_attack_effectiveness(atk_type, t[0], t[1]) > 0:
            targets.append([t[0], t[1]])
    
    return targets


"""
Returns an array of type combinations against which the specified attack
type is ineffective.
"""
def get_attack_resistors(atk_type, includes = []):
    resistors = []
    for t in pt.REAL_TYPE_PAIRS.values():
        if (len(includes) != 0) and (not t[0] in includes and not t[1] in includes):
            continue

        if get_attack_effectiveness(atk_type, t[0], t[1]) < 0:
            resistors.append([t[0], t[1]])
    
    return resistors


"""
Returns a dictionary of attack types ordered by their number of
effective target types from least to most.
"""
def get_effectiveness_ratings(includes = []):
    ratings = {}
    for ti in pt.TYPES:
        targets = get_attack_targets(ti, includes)
        resistors = get_attack_resistors(ti, includes)

        atk_score = len(targets)
        for target in targets:
            atk_score *= (1.0 + get_type_likelihood(target))
        
        def_score = len(resistors)
        for defender in resistors:
            def_score *= (1.0 + get_type_likelihood(defender))

        score = atk_score - def_score
        ratings[ti] = score

    return dict(sorted(ratings.items(), key=lambda kv:kv[1]))


"""
"""
def get_defender_teams():
    teams = {}
    return teams


def get_type_likelihood(pair):
    hash = pt.type_pair_hash(pair)
    return pt.TYPE_HISTOGRAM[hash] / len(pt.POKEMON_DB.items())


"""
Returns a defense rating for a given team of 3 Pokemon with the
specified type combinations. A value between -1 and 1 where -1
indicates the team is vulnerable to every type of attack, 1 indicates
the team is not vulnerable to any type. Negative values indicate
the team has more vulnerabilities than resistances and positive values
indicate the team has more resistances than vulnerabilities.
"""
def get_team_defense_rating(typesA, typesB, typesC):
    team_weaknesses = set()
    team_resistances = set()

    weaknesses = get_defender_weaknesses(typesA[0], typesA[1])
    resistances = get_defender_resistances(typesA[0], typesA[1])

    team_weaknesses = (team_weaknesses | weaknesses) - resistances
    team_resistances = (team_resistances | resistances) - weaknesses

    weaknesses = get_defender_weaknesses(typesB[0], typesB[1])
    resistances = get_defender_resistances(typesB[0], typesB[1])

    team_weaknesses = (team_weaknesses | weaknesses) - resistances
    team_resistances = (team_resistances | resistances) - weaknesses

    weaknesses = get_defender_weaknesses(typesC[0], typesC[1])
    resistances = get_defender_resistances(typesC[0], typesC[1])

    team_weaknesses = (team_weaknesses | weaknesses) - resistances
    team_resistances = (team_resistances | resistances) - weaknesses

    effective_count = len(pt.TYPES) - 1
    wr = len(team_weaknesses) / effective_count
    rr = len(team_resistances) / effective_count
    rating = rr - wr

    ratingA = get_defender_rating(typesA[0], typesA[1])
    ratingB = get_defender_rating(typesB[0], typesB[1])
    ratingC = get_defender_rating(typesC[0], typesC[1])

    return rating + ((ratingA + ratingB + ratingC) / 3.0)


def get_team_defense_ratings(threshold = -1, includes = []):
    ratings = {}

    types = list(pt.REAL_TYPE_PAIRS.values())
    for i in range(0, len(types)):
        foundA = False

        a = types[i]
        if len(includes) == 0 or (a[0] in includes or a[1] in includes):
            foundA = True

        for j in range(i, len(types)):
            foundB = False

            b = types[j]
            if len(includes) == 0 or (b[0] in includes or b[1] in includes):
                foundB = True

            for k in range(j, len(types)):
                foundC = False

                c = types[k]
                if len(includes) == 0 or (c[0] in includes or c[1] in includes):
                    foundC = True

                if not foundA and not foundB and not foundC:
                    continue

                rating = get_team_defense_rating(a, b, c)
                if rating < threshold:
                    continue

                hash = team_hash(a, b, c)
                ratings[hash] = rating

    return dict(sorted(ratings.items(), key=lambda kv:kv[1]))


def get_pokemon_by_type(includes):
    result = {}
    for k, v in pt.POKEMON_DB.items():
        if v[0] in includes or v[1] in includes:
            result[k] = v
        
    return result


def get_pokemon_by_type_pair(pair):
    result = []
    for k, v in pt.POKEMON_DB.items():
        if pt.compare_type_pairs(pair, v):
            result.append(k)
        
    return result
