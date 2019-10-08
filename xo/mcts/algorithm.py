import time, operator
import random
import numpy as np
from collections import namedtuple
from .. import board_utils, win_state_utils
from .. import models
from ..utils import timeit, make_logger


logger = make_logger('mcts.algorithm.py')
np.random.seed(123)


SEC_LIMIT_PER_MOVE = 10
UCB_CONSTANT = np.sqrt(2)


class Node:
    def __init__(self, board_x, board_o, marker,
                 n_rows, n_cols, n_connects, next_action_indexes,
                 n_wins=0, n_selected=0, parent=None, action=None):
        self.board_x = board_x
        self.board_o = board_o
        self.marker = marker
        self.n_rows = n_rows
        self.n_cols = n_cols
        self.n_connects = n_connects
        self.n_wins = n_wins 
        self.n_selected = n_selected
        self.children = list()
        self.next_child_index = 0
        self.next_action_indexes = next_action_indexes
        self.parent = parent
        self.action = action

    def __repr__(self):
        repr_ = '{}("{}", {}, {}, {:.1f}/{})'
        n_cells = self.n_rows * self.n_cols
        board_str = board_utils.get_board_str(self.board_x, self.board_o, n_cells)
        repr_ = repr_.format(Node.__name__,
                             board_str,
                             self.marker,
                             self.action,
                             self.n_wins, self.n_selected)
        return repr_

    def is_max(self):
        return self.marker == board_utils.MARKER_X

    def has_next_child(self):
        return self.next_child_index < len(self.next_action_indexes)

    def add_next_child(self, append=True):
        child_index = self.next_action_indexes[self.next_child_index]
        self.next_child_index += 1
        next_marker = board_utils.get_opposite_marker(self.marker)
        child = mark_cell(self, next_marker, child_index, append)
        return child

    @classmethod
    def make_root(cls, game):
        # info_msg = 'Making root node for game {}'.format(game)
        # logger.info(info_msg)

        n_cells = game.n_rows * game.n_cols
        cur_player = board_utils.get_cur_player(game.board_x, game.board_o, n_cells)
        # info_msg = 'Current player: {}'.format(cur_player)
        # logger.info(info_msg)

        next_action_indexes = board_utils.get_empty_indexes(game.board_x, 
                                                            game.board_o, 
                                                            n_cells)
        # shuffle them
        np.random.shuffle(next_action_indexes)
        root = Node(game.board_x, game.board_o, 
                    cur_player, game.n_rows, game.n_cols, 
                    game.n_connects, next_action_indexes)

        next_marker = board_utils.get_opposite_marker(root.marker)

        while root.has_next_child():
            root.add_next_child()

        return root


def mark_cell(node, marker, index, append=True):
    is_x = marker == board_utils.MARKER_X
    is_o = marker == board_utils.MARKER_O
    if not (is_x or is_o):
        err_msg = 'Do not recognize marker {}'.format(marker)
        raise ValueError(err_msg)

    if is_x:
        board_x = add_cross(node.board_x, index)
        board_o = node.board_o
    else:
        board_x = node.board_x
        board_o = add_circle(node.board_o, index)

    n_cells = node.n_rows * node.n_cols
    next_action_indexes = board_utils.get_empty_indexes(board_x, board_o, n_cells)
    np.random.shuffle(next_action_indexes)

    new_node = Node(
        board_x=board_x,
        board_o=board_o,
        marker=marker,
        n_rows=node.n_rows,
        n_cols=node.n_cols,
        n_connects=node.n_connects,
        next_action_indexes=next_action_indexes,
        parent=node, action=index
    )

    if append:
        node.children.append(new_node)
    return new_node


def is_game_over(node):
    is_over = board_utils.is_game_over(
        node.board_x, 
        node.board_o,
        node.n_rows,
        node.n_cols,
        node.n_connects
    )
    return is_over


def get_Q(node):
    v = node.n_wins / node.n_selected
    return v


def get_uct(node, time_):
    ucb = np.inf
    if node.n_selected > 0:
        v = get_Q(node)
        u = UCB_CONSTANT * np.sqrt(np.log(time_) / node.n_selected)
        ucb = v + u

        # info_msg = 'value: {:.3f} + uncertainty: {:.3f} = {:.3f}'
        # info_msg = info_msg.format(v, u, ucb)
        # logger.info(info_msg)

    return ucb


def select_child_by_ucb(node, time_):
    # info_msg = 'Selecting child by uct of node {}'.format(node)
    # logger.info(info_msg)

    # unexplored child always has infinity ucb
    if node.has_next_child():
        max_child = node.add_next_child()
        return max_child

    max_child = node.children[0]
    max_uct = get_uct(max_child, time_)

    for child in node.children:
        uct = get_uct(child, time_)
        if uct > max_uct:
            max_child = child
            max_uct = uct

    return max_child


def select(node, time_):
    while not is_game_over(node) and len(node.children) > 0:
        node = select_child_by_ucb(node, time_)
    return node


def add_cross(board, index):
    flag = 1 << index
    return board | flag


def add_circle(board, index):
    flag = 1 << index
    return board | flag


def expand(node):
    if is_game_over(node) or not node.has_next_child():
        return node
    # add a new child to node
    child = node.add_next_child()
    return child

#======================================================================
# Simulation policy using heuristic
#======================================================================

def get_heuristic(node):
    win_board = win_state_utils.get_board_wins(node.n_rows, 
                                               node.n_cols, 
                                               node.n_connects)
    n_wins = len(win_board)

    # measure its closeness to winning to all the wins
    # basically infinity
    max_score = -(1 << 30)
    n_cells = node.n_rows * node.n_cols
    marker = board_utils.get_next_player(node.board_x, node.board_o, n_cells)

    if marker == board_utils.MARKER_X:
        board = node.board_x
        board_oppo = node.board_o
    else:
        board = node.board_o
        board_oppo = node.board_x

    for win in win_board:
        # first check if the win is possible to reach
        # should equal 0 since where there's 1 in win state, it should be empty in opposition board
        is_valid = (win & board_oppo) == 0
        if not is_valid:
            continue

        same = board & win
        score = bin(same).count('1') 
        max_score = max(score, max_score)

    return max_score


def simulate_children(node):
    children = list()
    next_marker = board_utils.get_opposite_marker(node.marker)
    for index in node.next_action_indexes:
        child = mark_cell(node, next_marker, index, append=False)
        children.append(child)
    return children

#======================================================================

def simulate(node):
    while not is_game_over(node):
        # rollout policy is just get random child node
        # randind = np.random.randint(0, len(node.next_action_indexes))
        action = node.next_action_indexes[0]
        next_marker = board_utils.get_opposite_marker(node.marker)
        node = mark_cell(node, next_marker, action, append=False)
        # children = simulate_children(node)
        # sorted_children = sorted(children, key=lambda c: get_heuristic(c))
        # get the child closest to game_over state
        # node = sorted_children[-1]

    is_over = board_utils.is_game_over(
        node.board_x,
        node.board_o,
        node.n_rows,
        node.n_cols,
        node.n_connects
    )
    return is_over


def backpropagate(node, result):
    def update(node, result):
        if node.marker == result:
            node.n_wins += 1
        elif result != ' ':
            node.n_wins -= 1
        # give some value to getting a draw to differentiate between
        # draw and lose end result
        node.n_selected += 1

    # update node
    update(node, result)
    while node.parent is not None:
        node = node.parent
        update(node, result)


def get_best_move(game):
    root = Node.make_root(game)
    # sanity check that game is not already at end state
    if is_game_over(root):
        err_msg = 'Game already over for {}, no more moves.'
        err_msg = err_msg.format(repr(root))
        logger.error(err_msg)
        raise ValueError(err_msg)

    remaining_time = SEC_LIMIT_PER_MOVE
    time_marker = time.time()
    it = 1

    n_cells = game.n_rows * game.n_cols
    marker = board_utils.get_next_player(game.board_x, game.board_o, n_cells)
    # info_msg = 'Getting best move for Player {} at {} within {} seconds'
    # info_msg = info_msg.format(marker, game, remaining_time)
    # logger.info(info_msg)

    while remaining_time > 0:
        # info_msg = 'Iteration: {}, remaining time: {:.3f}s'
        # info_msg = info_msg.format(it, remaining_time)
        # logger.info(info_msg)

        optimal_leaf = select(root, it)
        expanded_optimal = expand(optimal_leaf)

        simulation_result = simulate(expanded_optimal)
        backpropagate(expanded_optimal, simulation_result)
        it += 1
        time_check = time.time()
        taken = time_check - time_marker
        remaining_time -= taken
        time_marker = time_check

    # get best move
    # info_msg = 'Selecting best move of root node: {} with {} children'
    # info_msg = info_msg.format(root, len(root.children))
    # logger.info(info_msg)

    best_child = select_child_by_ucb(root, it)
    # info_msg = 'Best child of root: {}'.format(best_child)
    # logger.info(info_msg)
    # info_msg = 'Number of iterations: {}'.format(it)
    # logger.info(info_msg)
    # for child in best_child.children:
    #     info_msg = 'Best child child: {}'.format(child)
    #     logger.info(info_msg)
    # for child in root.children:
    #     info_msg = 'Root child: {}'.format(child)
    #     logger.info(info_msg)

    return best_child.action
