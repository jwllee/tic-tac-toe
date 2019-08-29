import random

from django import forms
from django.core.exceptions import ImproperlyConfigured, ValidationError

from .models import Game, BoardState
from .players import get_player


def validate_player_type(player_type):
    if player_type == 'human':
        return True
    try:
        return get_player(player_type) is not None
    except (ImproperlyConfigured, ImportError):
        err_msg = 'Unknown player type: {}'.format(player_type)
        print('Validation error: {}'.format(err_msg))
        raise ValidationError(err_msg)


PLAYER_TYPES = [
    ('human', 'Human'),
    ('xo.players.RandomPlayer', 'Random player'),
    ('xo.players.MinimaxPlayer', 'Minimax player')
]


class NewGameForm(forms.Form):
    is_kriegspiel = forms.BooleanField(required=False)
    n_rows = forms.IntegerField(initial=3, min_value=3, max_value=5)
    n_cols = forms.IntegerField(initial=3, min_value=3, max_value=5)
    n_connects = forms.IntegerField(initial=3, min_value=3, max_value=5)
    player_x = forms.CharField(widget=forms.Select(choices=PLAYER_TYPES))
    player_o = forms.CharField(widget=forms.Select(choices=PLAYER_TYPES[::-1]))

    def create(self):
        players = [
            self.cleaned_data['player_x'], 
            self.cleaned_data['player_o'],
        ]
        return Game.objects.create(
            player_x=players[0],
            player_o=players[1],
            board_x=0,
            board_o=0,
            n_rows=self.cleaned_data['n_rows'],
            n_cols=self.cleaned_data['n_cols'],
            n_connects=self.cleaned_data['n_connects'],
            is_kriegspiel=self.cleaned_data['is_kriegspiel']
        )

    def clean(self):
        cleaned_data = super().clean()
        n_rows = cleaned_data['n_rows']
        n_cols = cleaned_data['n_cols']
        n_connects = cleaned_data['n_connects']
        player_x = cleaned_data['player_x']
        player_o = cleaned_data['player_o']

        # check that n_connects is valid
        max_dim = max(n_rows, n_cols)
        if n_connects > max_dim:
            err_msg = 'No. of connects: {} to win cannot be larger than maximum dimension: {}'
            err_msg = err_msg.format(n_connects, max_dim)
            raise ValidationError(
                err_msg,
                code='invalid'
            )

#         if player_x != 'human' and player_o != 'human':
#             err_msg = 'Not supporting two AI playing yet.'
#             raise ValidationError(
#                 err_msg,
#                 code='invalid'
#             )
 

class MoveForm(forms.Form):
    row_index = forms.IntegerField(min_value=0)
    col_index = forms.IntegerField(min_value=0)
