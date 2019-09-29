#!/usr/bin/env python3

import heapq
from random import shuffle
from state import State


def informed_search(start, goal=tuple(range(9))):
    visited, unexplored, moves = [], [], []
    heuristic = tiles_out_of_place
    heapq.heappush(unexplored, State(start, None, 0, heuristic(start, goal)))

    while unexplored:
        state = heapq.heappop(unexplored)
        visited.append(state)

        if len(visited) == 10000:
            print('Max move reached:', max(visited, key=lambda x: x.g).g)
            break

        if state.h == 0:
            return moves_list(state, moves)
        else:
            expand_state(state, goal, visited, unexplored, heuristic)

    return None


def moves_list(state, moves):
    moves.append(state)
    if state.parent is None:
        return moves
    else:
        return moves_list(state.parent, moves)


def tiles_out_of_place(current, goal):
    return sum([1 for i in range(9) if current.index(i) != goal.index(i)])


def manhattan_distance(current, goal):
    pass


def euclidean_distance(current, goal):
    pass


def expand_state(state, goal, visited, unexplored, heuristic):
    def in_unexplored(current, q):
        return current in [x.values for x in q]

    def in_visited(current, l):
        return current in [x.values for x in l]

    for s in state.moves():
        temp_state = State(s, state, state.g + 1, heuristic(s, goal))

        if in_unexplored(s, unexplored):
            for duplicate in [x for x in unexplored if x.values == s]:
                if duplicate.f > temp_state.f:
                    unexplored.remove(duplicate)
                    heapq.heappush(unexplored, temp_state)
        elif not in_visited(s, visited):
            heapq.heappush(unexplored, temp_state)


def main():
    # start = list(range(9))
    # shuffle(start)

    start = [2, 8, 3, 1, 6, 4, 7, 0, 5]
    goal = (1, 2, 3, 8, 6, 4, 7, 5, 0)

    # start2 = [7, 2, 4, 5, 0, 6, 8, 3, 1]

    fname = 'moves.txt'
    with open(fname, 'w') as f:
        f.close()

    solution = informed_search(start, goal)

    if solution is None:
        print('No path found.')
    else:

        for state in solution[::-1]:
            state.output_board('moves.txt')
            print(state)
            print()

        print('Number of moves:', len(solution) - 1)


if __name__ == '__main__':
    main()
