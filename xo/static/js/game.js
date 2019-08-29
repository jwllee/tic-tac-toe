function onSuccess(data) {
    var move = data.move;
    if (move) {
        var rowInd = move.row_ind;
        var colInd = move.col_ind;
        var marker = move.marker;
        var gameId = move.game_id;

        // var msg = "Player " + marker + " marked (" + rowInd + ", " + colInd + ")";
        //console.log(msg);

        // get the button and mark it
        var table = $('table')[0];
        var cell = $(table).find('tr:eq(' + rowInd + ') td:eq(' + colInd + ')');

        // Some debugging
        // var row = $(rowFilter);
        // console.log('Table: ' + table.tagName);
        // var cellRowInd = cell.attr('row-ind');
        // var cellColInd = cell.attr('col-ind');
        // console.log('Row index: ' + cellRowInd + ', col index: ' + cellColInd);

        var form = cell.children('form');
        // console.log(form.tagName);

        // replace it since it's now been marked
        var replacement = '<div class="square">' + marker + '</div>';
        form.replaceWith(replacement);
    }

    // update messages
    var msgDiv = $('div #message');
    msgDiv.empty();
    var newMsgDiv = '<div class="row justify-content-center">' + data.message + '</div>';
    msgDiv.append(newMsgDiv);

    if (data.is_game_over) {
        // add the new game url
        var newGameUrl = $('div .board').attr('new-game-url');
        console.log('New game url: ' + newGameUrl);
        var newGameLink = '<a href="' + newGameUrl + '" class="row justify-content-center" id="message-link">Start a new game.</a>'
        msgDiv.append(newGameLink);
    }
    else {
        // update next_player for all forms
        $('input[name="next_player"]').prop('value', data.next_player);
        $('div .board').attr('next-player-type', data.next_player_type);
        $('div .board').attr('next-player', data.next_player);

        // check if next player is AI
        var nextPlayerType = data.next_player_type;
        if (nextPlayerType != 'human') {
            $("table button").prop("disabled", true);
            var url = $('div .board').attr('board-update-url');
            var gameId = $('div .board').attr('game-id');
            
            // change message to thinking
            var curMarker = $('div .board').attr('next-player');
            var msg = 'Player ' + curMarker + ' is thinking...';
            var msgDiv = '<div class="row justify-content-center">' + msg + '</div>';
            $('div.col#message').empty();
            $('div.col#message').append(msgDiv);

            var requestData = {
                'game_id': gameId,
                'csrfmiddlewaretoken': Cookies.get('csrftoken'),
            }
            $.ajax({
                url: url,
                data: requestData,
                dataType: 'json',
                success: onSuccess,
            });
        }
        else {
            $("table button").prop("disabled", false);
            console.log('Re-enabled all buttons');
        }
    }
}


$(document).on('click', 'table button', function(e) {

    // replace the button with div
    var clicked = e.currentTarget;
    var form = $(clicked).closest('form');
    var cur_player_type = form.find('input[name="cur_player_type"]').prop('value');
    var marker = form.find('input[name="next_player"]').prop('value');
    var gameId = form.find('input[name="game_id"]').prop('value');
    var rowInd = form.find('input[name="row_index"]').prop('value');
    var colInd = form.find('input[name="col_index"]').prop('value');
    var replacement = '<div class="square">' + marker + '</div>';
    form.replaceWith(replacement);

    var msg = "Game " + gameId + ": button (" + rowInd + ", " + colInd + ") clicked.";
    console.log(msg);

    // disable all buttons from being clicked
    $(".board :submit").prop("disabled", true);

    // change message to last_marker is thinking, if last_marker is AI
    if (cur_player_type != 'human') {
        // change message to player is thinking
        var curMarker = $('div .board').attr('next-player');
        var msg = 'Player ' + curMarker + ' is thinking...';
        var msgDiv = '<div class="row justify-content-center">' + msg + '</div>';
        $('div.col#message').empty();
        $('div.col#message').append(msgDiv);
    }

    // send json query
    var url = form.attr('board-update-url');
    console.log('Board update URL: ' + url);
    $.ajax({
        url: url,
        data: form.serialize(),
        dataType: 'json',
        success: onSuccess,
    });
});


$(document).ready(function() {
    console.log('On page ready');

    // check if current player is an AI
    var nextPlayerType = $("div .board").attr('next-player-type');
    console.log('Next player type: ' + nextPlayerType);
    var url = $("div .board").attr('board-update-url');
    var gameId = $("div .board").attr('game-id');
    console.log('Game id: ' + gameId);

    var data = {
        'game_id': gameId,
        'csrfmiddlewaretoken': Cookies.get('csrftoken'),
    };

    if (nextPlayerType != 'human') {
        $("table button").prop("disabled", true);
        console.log('Disabled all buttons');

        // change message to player is thinking
        var curMarker = $('div .board').attr('next-player');
        var msg = 'Player ' + curMarker + ' is thinking...';
        var msgDiv = '<div class="row justify-content-center">' + msg + '</div>';
        $('div.col#message').empty();
        $('div.col#message').append(msgDiv);

        // send request for move
        $.ajax({
            url: url,
            data: data,
            dataType: 'json',
            success: onSuccess,
        });
    }
});
