import pokemon.pokemon_moves as pm
import pokemon.pokemon_queries as pq
import pokemon.pokemon_types as pt
import pokemon.pokemon_tests as tests

INCLUDES = set()
INCLUDE_PAIRS = set()

EXCLUDES = set()
EXCLUDE_PAIRS = set()

def ask_type(msg = ""):
    t = input(msg).upper()
    while not t in pt.TYPES:
        t = input(msg).upper()
    
    return t


def ask_rating(msg = ""):
    r = input(msg)
    while True:
        try:
            rv = float(r)
            return rv
        except:
            print("Must enter a valid float value.")
            r = input(msg)


def print_atk_ratings(includes = []):
    print()
    r = pq.get_effectiveness_ratings(includes)
    for k, v in r.items():
        print(str(k) + " : " + str(v))


def print_def_ratings(includes = []):
    print()
    resistance_ratings = pq.get_resistance_ratings()
    for k, v in resistance_ratings.items():
        print(str(k) + ":" + str(v))


def print_filters():
    print("Type includes: " + str(INCLUDES))
    print("Type pair includes: " + str(INCLUDE_PAIRS))
    print()
    print("Type excludes: " + str(EXCLUDES))
    print("Type pair excludes: " + str(EXCLUDE_PAIRS))


def print_histogram():
    print()
    histogram = pt.TYPE_HISTOGRAM
    for k, v in histogram.items():
        print(str(k) + ":" + str(v))


def print_team_ratings(t = -1):
    print()
    ratings = pq.get_team_defense_ratings(t, INCLUDES, INCLUDE_PAIRS, EXCLUDES, EXCLUDE_PAIRS)
    for k, v in ratings.items():
        print(str(k) + " : " + str(v))


tests.run_tests()

CMD_ADD_EXCLUDE = 'add exclude'
CMD_ADD_EXCLUDE_PAIR = 'add exclude pair'
CMD_ADD_INCLUDE = 'add include'
CMD_ADD_INCLUDE_PAIR = 'add include pair'
CMD_CLEAR_EXCLUDES = 'clear excludes'
CMD_CLEAR_INCLUDES = 'clear includes'
CMD_LIST_ATTACKS = 'list atk'
CMD_LIST_DEFENDERS = 'list def'
CMD_LIST_EXCLUDES = 'list excludes'
CMD_LIST_INCLUDES = 'list includes'
CMD_LIST_POKEMON = 'list pokemon'
CMD_LIST_POKEMON_BROAD = 'list pokemon broad'
CMD_LIST_POKEMON_NARROW = 'list pokemon narrow'
CMD_LIST_TEAM_TYPES = 'list team types'
CMD_LIST_TEAMS = 'list teams'
CMD_LIST_TYPES = 'list types'
CMD_TEAM_RATING = 'team rating'
CMD_TEAM_TRAITS = 'team traits'
CMD_TYPE_SHARE = 'type share'

cmd = input("Query: ").lower()
while cmd != 'done':

    if cmd == CMD_ADD_EXCLUDE:
        types = []
        type = ask_type("Add type: ")
        while type != None and type != '':
            EXCLUDES.add(type)
            type = ask_type("Add type: ")

        print_filters()
    
    
    if cmd == CMD_ADD_EXCLUDE_PAIR:
        t1 = ask_type("Type 1: ")
        while t1 != None and t1 != '':
            t2 = ask_type("Type 2: ")
            EXCLUDE_PAIRS.add(pt.type_pair_hash([t1, t2]))
            t1 = ask_type("Type 1: ")
        
        print_filters()

    
    if cmd == CMD_ADD_INCLUDE:
        types = []
        type = ask_type("Add type: ")
        while type != None and type != '':
            INCLUDES.add(type)
            type = ask_type("Add type: ")

        print_filters()


    if cmd == CMD_ADD_INCLUDE_PAIR:
        t1 = ask_type("Type 1: ")
        while t1 != None and t1 != '':
            t2 = ask_type("Type 2: ")
            INCLUDE_PAIRS.add(pt.type_pair_hash([t1, t2]))
            t1 = ask_type("Type 1: ")

        print_filters()
        
    
    if cmd == CMD_CLEAR_EXCLUDES:
        EXCLUDE_PAIRS = set()


    if cmd == CMD_CLEAR_INCLUDES:
        INCLUDE_PAIRS = set()


    if cmd == CMD_LIST_ATTACKS:
        print_atk_ratings()


    if cmd == CMD_LIST_DEFENDERS:
        print_def_ratings()
    

    if cmd == CMD_LIST_EXCLUDES:
        print(EXCLUDE_PAIRS)


    if cmd == CMD_LIST_INCLUDES:
        print(INCLUDE_PAIRS)

    
    if cmd == CMD_LIST_POKEMON:
        pokemon = pq.get_pokemon(INCLUDES, INCLUDE_PAIRS, EXCLUDES, EXCLUDE_PAIRS)
        for k, v in pokemon.items():
            print(str(k) + " : " + str(v))


    if cmd == CMD_LIST_POKEMON_BROAD:
        types = []
        type = ask_type("Add type restriction: ")
        while type != None and type != '':
            types.append(type)
            type = ask_type("Add type restriction: ")

        poke = pq.get_pokemon_by_type(types)
        for k, v in poke.items():
            print(str(k) + " : " + str(v))
    

    if cmd == CMD_LIST_POKEMON_NARROW:
        t1 = ask_type("Type 1: ")
        t2 = ask_type("Type 2: ")
        print(str(pq.get_pokemon_by_type_pair([t1, t2])))
    

    if cmd == CMD_LIST_TEAM_TYPES:
        threshold = ask_rating("Min rating: ")
        print_team_ratings(threshold)


    if cmd == CMD_LIST_TEAMS:
        tA = [
            ask_type("Slot 1 - Type 1: "),
            ask_type("Slot 1 - Type 2: ")
        ]
        
        tB = [
            ask_type("Slot 2 - Type 1: "),
            ask_type("Slot 2 - Type 2: ")
        ]
        
        tC = [
            ask_type("Slot 3 - Type 1: "),
            ask_type("Slot 3 - Type 2: ")
        ]
        
        teams = pq.get_possible_teams(
            tA,
            tB,
            tC
        )

        print('\n== Slot 1 ==')
        for t in teams[0]:
            print(str(t))

        print('\n== Slot 2 ==')
        for t in teams[1]:
            print(str(t))

        print('\n== Slot 3 ==')
        for t in teams[2]:
            print(str(t))

        print('\nRating')
        print(pq.get_team_defense_rating(
            tA, tB, tC
        ))

    
    if cmd == CMD_LIST_TYPES:
        print_histogram()
    

    if cmd == CMD_TEAM_RATING:
        a1 = ask_type("A Type 1: ")
        a2 = ask_type("A Type 2: ")

        b1 = ask_type("B Type 1: ")
        b2 = ask_type("B Type 2: ")

        c1 = ask_type("C Type 1: ")
        c2 = ask_type("C Type 2: ")

        r = pq.get_team_defense_rating(
            [a1, a2],
            [b1, b2],
            [c1, c2]
        )

        print(str(r))


    if cmd == CMD_TEAM_TRAITS:
        a1 = ask_type("A Type 1: ")
        a2 = ask_type("A Type 2: ")

        b1 = ask_type("B Type 1: ")
        b2 = ask_type("B Type 2: ")

        c1 = ask_type("C Type 1: ")
        c2 = ask_type("C Type 2: ")

        traits = pq.get_team_defense_traits(
            [a1, a2],
            [b1, b2],
            [c1, c2]
        )

        print("\nVulnerable to:")
        print(str(traits[0]))

        print("\nResistant to:")
        print(str(traits[1]))

        print()


    if cmd == CMD_TYPE_SHARE:
        typeA = ask_type("Type 1: ")
        typeB = ask_type("Type 2: ")
        r = pq.get_type_likelihood(typeA, typeB)
        print(str(r))


    cmd = input("Query: ").lower()
