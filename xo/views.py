from django.views.decorators.http import require_http_methods
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.http import HttpResponse, HttpResponseRedirect


from .forms import NewGameForm, MoveForm
from .models import Game


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
                game.play(form.cleaned_data['index'])
                game.save()
            return redirect(game)
        else:
            err_msg = 'MoveForm invalid, should not happen'
            raise ValueError(err_msg)
    else:
        game.play_auto()
        game.save()

    html = get_board_html(game.n_rows, game.n_cols)
    return render(request, html, {
        'game': game
    })


def board_3x3(request):
    context = {}
    return render(request, 'xo/3x3.html', context)


def board_4x4(request):
    context = {}
    return render(request, 'xo/4x4.html', context)
