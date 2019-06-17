class TUIMainWindow:
    def end(self):
        self.logger.info('Game end')
        if self.winner is None:
            msg = 'Draw game.'
        else:
            msg = '{!s} ({!r}) has won.'
            msg = msg.format(self.winner.name, self.winner.marker)
        self.view.display_msg(msg)

    def prompt_move(self, marker):
        msg = 'Enter move coordinate ({}): '
        msg = msg.format(self.board.CellLocation.COORDINATE_FORMAT)
        loc = None
        while loc is None or not self.board.is_cell_empty(loc):
            loc_str = self.view.get_input(msg)
            try:
                loc = self.board.CellLocation.parse(loc_str)
            except:
                self.logger.error('Parse location error: {}'.format(loc))
                loc = None
                continue
            is_empty = self.board.is_cell_empty(loc)
            self.logger.debug('{} is empty: {}'.format(loc, is_empty))
        return loc

    def start_board(self):
        while self.board.state == BoardState.ONGOING:
            self.logger.debug('Next round...')
            cur_player = self.marker2player[self._marker]

            if cur_player.is_real:
                loc = self.prompt_move(self._marker)
            else:
                loc = cur_player.get_move()

            move = Cell(self._marker, loc)
            self.board.mark_cell(move.content, move.loc)

            if not cur_player.is_real:
                msg = '{} marked {!r} at {}'
                msg = msg.format(cur_player.name,
                                 cur_player.marker,
                                 loc)
                self.view.display_msg(msg)

            # increment marker
            n_markers = len(Marker)
            self.logger.debug('no. of markers: {}'.format(n_markers))
            self._marker = Marker((self._marker + 1) % n_markers)
        self.end_board()
