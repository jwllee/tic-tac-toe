from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import ensure_csrf_cookie
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse


from .forms import NewGameForm, MoveForm
from .models import Game
from .utils import make_logger
from xo.board_utils import MARKER_O, MARKER_X


logger = make_logger('views.py')


@require_http_methods(['GET', 'POST'])
def index(request):
    if request.method == 'POST':
        form = NewGameForm(request.POST)
        if form.is_valid():
            game = form.create()
            game.save()
            url = game.get_absolute_url()
            print('Redirect to {}'.format(url))
            return redirect(game)
    else:
        form = NewGameForm()
    return render(request, 'xo/new_game.html', {'form': form})


def get_board_html(n_rows, n_cols):
    if n_rows == 3 and n_cols == 3:
        html = 'xo/3x3.html'
    elif n_rows == 4 and n_cols == 4:
        html = 'xo/4x4.html'
    elif n_rows == 5 and n_cols == 5:
        html = 'xo/5x5.html'
    else:
        err_msg = 'Do not have html for dimension: ({}, {})'
        err_msg = err_msg.format(n_rows, n_cols)
        raise ValueError(err_msg)
    info_msg = 'Getting board ({}x{}) html: {}'
    info_msg = info_msg.format(n_rows, n_cols, html)
    print(info_msg)
    return html


@require_http_methods(['GET', 'POST'])
def game(request, pk):
    info_msg = 'Game request method: {} for game {}'
    info_msg = info_msg.format(request.method, pk)
    print(info_msg)
    game = get_object_or_404(Game, pk=pk)
    if request.method == 'POST':
        form = MoveForm(request.POST)
        if form.is_valid():
            if game.is_next_player_human():
                row_ind = form.cleaned_data['row_index']
                col_ind = form.cleaned_data['col_index']
                game.play_xy(row_ind, col_ind)
                game.save()
            return redirect(game)
        else:
            err_msg = 'MoveForm invalid, should not happen'
            raise ValueError(err_msg)
    else:
        # game.play_auto()
        game.save()

    board_width = (game.n_cols + 1) * 90 - 10
    print('Board width: {}'.format(board_width))

    # html = get_board_html(game.n_rows, game.n_cols)
    html = 'xo/nxn.html'
    context = {
        'game': game,
        'board_width': board_width,
    }
    return render(request, html, context)


@ensure_csrf_cookie
def board_update(request):
    info_msg = 'Board update view function called'
    logger.info(info_msg)

    # get info
    game_id = request.GET.get('game_id', -1)
    row_ind = int(request.GET.get('row_index', -1))
    col_ind = int(request.GET.get('col_index', -1))
    player = request.GET.get('next_player', None)

    info_msg = 'Game {}: cell ({}, {}) marked with {}'
    info_msg = info_msg.format(game_id,
                               row_ind, col_ind,
                               player)
    logger.info(info_msg)

    # update game state
    game = get_object_or_404(Game, pk=game_id)
    if not (row_ind == -1 or col_ind == -1):
        game.play_xy(row_ind, col_ind)

    try:
        info_msg = 'Trying to play next auto'
        logger.info(info_msg)
        move = game.play_next_auto()
    except:
        move = None
    game.save()

    # make message
    if game.is_game_over == MARKER_X:
        msg = 'Player X wins!'
    elif game.is_game_over == MARKER_O:
        msg = 'Player O wins!'
    elif game.is_game_over == ' ':
        msg = 'Game drawn.'
    else:
        msg = "Player {}'s turn"
        msg = msg.format(game.next_player)

    data = {
        'message': msg,
        'move': move,
        'is_game_over': game.is_game_over,
        'game_id': game_id,
        'next_player': game.next_player,
        'next_player_type': game.next_player_type,
    }
    info_msg = 'JSON response: ' + str(data)
    logger.info(info_msg)
    return JsonResponse(data)


def board_3x3(request):
    context = {}
    return render(request, 'xo/3x3.html', context)


def board_4x4(request):
    context = {}
    return render(request, 'xo/4x4.html', context)
