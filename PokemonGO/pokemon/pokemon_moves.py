import csv

def print_fast_moves():
    with open('res/fast_moves.csv') as fast_moves:
        reader = csv.reader(fast_moves)
        for row in reader:
            print(str(row))
