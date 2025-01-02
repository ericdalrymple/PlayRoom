from pokemon import pokemon_types as pt


def run_compare_tests():
    result = pt.compare_type_pairs([pt.BUG, pt.DARK], [pt.BUG, pt.DARK])
    assert result
    
    result = pt.compare_type_pairs([pt.BUG, pt.DARK], [pt.DARK, pt.BUG])
    assert result

    result = pt.compare_type_pairs([pt.BUG, pt.DARK], [pt.BUG, pt.DRAGON])
    assert not result

    result = pt.compare_type_pairs([pt.BUG, pt.DARK], [pt.DRAGON, pt.BUG])
    assert not result


def run_histogram_test():

    # Ensure all possible type combinations are represented in the histogram
    assert len(pt.TYPE_PAIRS.items()) == len(pt.TYPE_HISTOGRAM)

    # Ensure all pokemon are in the histogram
    count = 0
    for v in pt.TYPE_HISTOGRAM.values():
        count += v
    
    assert count == len(pt.POKEMON_DB.items())


def run_tests():
    run_compare_tests()
    run_histogram_test()