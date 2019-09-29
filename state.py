#!/usr/bin/env python3


class State:
    def __init__(self, values, parent, g, h):
        self.values = values
        self.parent = parent
        self.g = g
        self.h = h
        self.f = g + h

    def __lt__(self, other):
        return self.f < other.f

    def moves(self):
        def swap(l, a, b):
            l[a], l[b] = l[b], l[a]

        z = self.values.index(0)
        moves_dict = {0: [1, 3],
                      1: [0, 2, 4],
                      2: [1, 5],
                      3: [0, 4, 6],
                      4: [1, 3, 5, 7],
                      5: [2, 4, 8],
                      6: [3, 7],
                      7: [4, 6, 8],
                      8: [5, 7]}
        moves = []
        for move in moves_dict[z]:
            new_state = self.values[:]
            swap(new_state, z, move)
            moves.append(new_state)

        return moves

    def __repr__(self):
        return '\n'.join(' '.join(str(x) if x != 0 else '_' for x in self.values[n:n+3]) for n in range(0, 9, 3))

    def output_board(self, fname):
        with open(fname, 'a') as f:
            f.write(self.__repr__() + '\n\n')
