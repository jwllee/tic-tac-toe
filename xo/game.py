from xo.utils import *
from xo.board.utils import *
from xo.board.flat import *


class Game:
    def __init__(self, board, players):
        self.logger = make_logger(Game.__name__)
        self.players = players
        self.marker2player = dict()
        self.board = board
        self._marker = Marker.CIRCLE
        self.observers = list()

    #------------------------------------------------------------ 
    # Observer pattern
    #------------------------------------------------------------ 
    def register_observer(self, obs):
        self.observers.append(obs)

    def remove_observer(self, obs):
        self.observers.remove(obs)

    def notify_observers(self, type_, data):
        for obs in self.observers:
            obs.update(type_, data)

    #------------------------------------------------------------ 
    # Properties
    #------------------------------------------------------------ 
    @property
    def cur_marker(self):
        return self._marker

    @property
    def cur_player(self):
        return self.marker2player[self.cur_marker]

    @property
    def cur_player(self):
        return self.marker2player[self.cur_marker]

    @property
    def ongoing(self):
        return self.board.state == BoardState.ONGOING

    @property
    def winner(self):
        marker_int = self.board.state - BoardState.CIRCLE_WIN
        winner = None
        if marker_int >= 0:
            marker = Marker(marker_int)
            winner = self.marker2player[marker]
        return winner

    def setup(self):
        for marker, player in zip(Marker, self.players):
            player.board = self.board
            player.marker = marker
            self.marker2player[marker] = player
        self._marker = Marker.CIRCLE
        self.logger.debug('marker2player: {}'.format(self.marker2player))

    def prompt_move(self):
        if self.cur_player.is_real:
            msg = 'Enter move coordinate ({}): '
            msg = msg.format(CellLocation2d.COORDINATE_FORMAT)
            data = {
                NotificationKey.MESSAGE: msg,
                NotificationKey.MARKER: self.cur_marker,
                NotificationKey.PLAYER: self.cur_player
            }
            self.notify_observers(NotificationType.PROMPT_MOVE, data)
        else:
            loc = self.cur_player.get_move()
            self.do_move(str(loc))

    def start(self):
        self.setup()
        self.prompt_move()

    def get_result_msg(self):
        if self.ongoing:
            raise ValueError('Game is still ongoing!')
        if self.winner is None:
            msg = 'Draw game.'
        else:
            msg = '{!s} ({!r}) has won.'
            msg = msg.format(self.winner.name, self.winner.marker)
        return msg

    def end(self):
        # display end game message
        data = {
            NotificationKey.MESSAGE: self.get_result_msg(),
            NotificationKey.STATE: self.board.state
        }
        self.notify_observers(NotificationType.GAME_END, data)
    
    def do_move(self, loc_str):
        if not self.ongoing:
            raise ValueError('Game not ongoing!')

        # check valid move
        loc = None
        try:
            self.logger.info('Parsing loc: {}'.format(loc_str))
            loc = CellLocation2d.parse(loc_str)
        except Exception as e:
            self.logger.error('Parse location {} error: {}'.format(loc_str, e))
            # prompt move again
            self.prompt_move()
            return 

        if not self.board.is_cell_empty(loc):
            self.prompt_move()
            return

        self.board.mark_cell(self.cur_marker, loc)
        if not self.cur_player.is_real:
            msg = '{} marked {!r} at {}'
            msg = msg.format(self.cur_player.name,
                             self.cur_player.marker,
                             loc)
            self.logger.info(msg)

        # prompt view to update view
        data = {
            NotificationKey.BOARD: self.board
        }
        self.notify_observers(NotificationType.BOARD_UPDATE, data)

        # increment marker
        n_markers = len(Marker)
        self.logger.debug('no. of markers: {}'.format(n_markers))
        self._marker = Marker((self._marker + 1) % n_markers)

        if not self.ongoing:
            self.end()
        else:
            self.prompt_move()
