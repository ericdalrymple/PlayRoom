import pokemon.pokemon_queries as pq
import pokemon.pokemon_types as pt
import pokemon.pokemon_tests as tests


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


def print_histogram():
    print()
    histogram = pt.TYPE_HISTOGRAM
    for k, v in histogram.items():
        print(str(k) + ":" + str(v))


def print_team_ratings(t = -1, includes = []):
    print()
    ratings = pq.get_team_defense_ratings(threshold=t, includes=includes)
    for k, v in ratings.items():
        print(str(k) + " : " + str(v))


tests.run_tests()

cmd = input("Query: ").lower()
while cmd != 'done':

    if cmd == 'list atk':
        print_atk_ratings()


    if cmd == 'list def':
        print_def_ratings()
    

    if cmd == 'list pokemon broad':
        types = []
        type = ask_type("Add type restriction: ")
        while type != None and type != '':
            types.append(type)
            type = ask_type("Add type restriction: ")

        poke = pq.get_pokemon_by_type(types)
        for k, v in poke.items():
            print(str(k) + " : " + str(v))
    

    if cmd == 'list pokemon narrow':
        t1 = ask_type("Type 1: ")
        t2 = ask_type("Type 2: ")
        print(str(pq.get_pokemon_by_type_pair([t1, t2])))
    

    if cmd == 'list teams':
        threshold = ask_rating("Min rating: ")

        types = []
        type = ask_type("Add type restriction: ")
        while type != None and type != '':
            types.append(type)
            type = ask_type("Add type restriction: ")

        print_team_ratings(threshold, types)


    if cmd == 'list types':
        print_histogram()
    

    if cmd == 'team rating':
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


    if cmd == 'type share':
        typeA = ask_type("Type 1: ")
        typeB = ask_type("Type 2: ")
        r = pq.get_type_likelihood(typeA, typeB)
        print(str(r))


    
    
    cmd = input("Query: ").lower()
