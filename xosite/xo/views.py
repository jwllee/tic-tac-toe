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
    if (n_rows, n_cols) == (3, 3):
        html = 'xo/3x3.html'
    elif (n_rows, n_cols) == (4, 4):
        html = 'xo/4x4.html'
    else:
        err_msg = 'Do not have html for dimension: ({}, {})'
        err_msg = err_msg.format(n_rows, n_cols)
        raise ValueError(err_msg)
    return html


@require_http_methods(['GET', 'POST'])
def game(request, pk):
    print('At game view function for game {}'.format(pk))
    game = get_object_or_404(Game, pk=pk)
    if request.method == 'POST':
        form = MoveForm(request.POST)
        if form.is_valid():
            game.play(form.cleaned_data['index'])
            game.play_auto()
            game.save()
            return redirect(game)
        else:
            pass
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
