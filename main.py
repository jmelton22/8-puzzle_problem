#!/usr/bin/env python3

import heapq
import math
from random import shuffle
from state import State


def informed_search(start, goal=tuple(range(9))):
    """
        Iterative A* search function for 8-puzzle problem. Exits when goal state has been reached or
        when queue of unexplored states is empty.

    :return: if goal state is reached, return a list of board states back to the starting state.
             if queue is empty without reaching goal state, return None.
    """
    visited, unexplored, moves = [], [], []
    heapq.heappush(unexplored, State(start, None, 0, heuristic(start, goal, 'manhattan')))

    while unexplored:
        state = heapq.heappop(unexplored)  # Search through next state in queue
        visited.append(state)

        if len(visited) == 10000:
            print('Max move reached:', max(visited, key=lambda x: x.g).g)
            break

        if state.h == 0:
            return moves_list(state, moves)
        else:
            # Add board states of valid possible moves to unexplored queue
            expand_state(state, goal, visited, unexplored)

    return None


def moves_list(state, moves):
    """
        Recursive function to determine the move-set from the goal state to starting state
        by traversing the parent states until reaching the start state.
    """
    moves.append(state)
    if state.parent is None:
        return moves
    else:
        return moves_list(state.parent, moves)


def heuristic(current, goal, method='manhattan'):
    """
        Calculates the heuristic cost of a given state to the goal state.
        Choose from 3 different methods:
            - Tiles out of place
            - Manhattan distance
            - Euclidean distance
    """
    if method == 'tiles_out_of_place':
        return sum([1 for i in range(9) if current.index(i) != goal.index(i)])

    # Dict to convert flat number list to 3x3 board indices for distance calculation
    coord_dict = {0: [0, 0], 1: [0, 1], 2: [0, 2],
                  3: [1, 0], 4: [1, 1], 5: [1, 2],
                  6: [2, 0], 7: [2, 1], 8: [2, 2]}
    total = 0
    for num in range(9):
        curr_board_index = coord_dict[current.index(num)]
        goal_board_index = coord_dict[goal.index(num)]

        if method == 'manhattan':
            total += sum([abs(d1 - d2) for d1, d2 in zip(curr_board_index, goal_board_index)])
        else:
            total += math.sqrt(sum([(d1 - d2) ** 2 for d1, d2 in zip(curr_board_index, goal_board_index)]))

    return total


def expand_state(state, goal, visited, unexplored):
    """
        Given a state, push the board states of its valid possible moves to unexplored queue.
        Possible moves = swapping the blank tile with one of its neighboring tiles.
        - Board states are added if they have not already been visited and are not already in the queue

        - Or they have the same board as a state in the queue but with a lower path cost
        - In which case, the board state with higher path cost is removed from queue and
        the new board state is pushed to the queue
    """
    def in_unexplored(current, q):
        return current in [x.values for x in q]

    def in_visited(current, l):
        return current in [x.values for x in l]

    for s in state.moves():
        # Path cost of new board state is the path cost to the parent state + 1
        temp_state = State(s, state, state.g + 1, heuristic(s, goal, 'manhattan'))

        if in_unexplored(s, unexplored):
            for duplicate in [x for x in unexplored if x.values == s]:
                if duplicate.f > temp_state.f:
                    unexplored.remove(duplicate)
                    heapq.heappush(unexplored, temp_state)
        elif not in_visited(s, visited):
            heapq.heappush(unexplored, temp_state)


def main():
    start = list(range(9))
    shuffle(start)

    # start = [2, 8, 3, 1, 6, 4, 7, 0, 5]
    # goal = (1, 2, 3, 8, 6, 4, 7, 5, 0)
    # fname = 'moves1.txt'

    # start2 = [7, 2, 4, 5, 0, 6, 8, 3, 1]
    # fname = 'moves2.txt'

    fname = 'moves.txt'
    with open(fname, 'w') as f:
        f.close()

    solution = informed_search(start)

    if solution is None:
        print('No path found.')
    else:
        for state in solution[::-1]:
            state.output_board(fname)
            print(state)
            print()

        with open(fname, 'a') as f:
            f.write('Number of moves: {}'.format(len(solution) - 1))

        print('Number of moves:', len(solution) - 1)


if __name__ == '__main__':
    main()
