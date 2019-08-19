function onSuccess(data) {
    var move = data.move;
    if (move) {
        var rowInd = move.row_ind;
        var colInd = move.col_ind;
        var marker = move.marker;
        var gameId = move.game_id;

        var msg = "Player " + marker + " marked (" + rowInd + ", " + colInd + ")";
        console.log(msg);

        // get the button and mark it
        var rowFilter = 'div.row#' + rowInd;
        var nth = colInd + 1;
        var colFilter = ':nth-child(' + nth + ')';

        // Some debugging
        // var row = $(rowFilter);
        // console.log('Row index: ' + row.prop('id'));

        var row = $(rowFilter);
        var form = row.children(colFilter).children('form');
        console.log(form.prop('tagName'));

        var formRowInd = form.find('input[name="row_index"]').prop('value');
        var formColInd = form.find('input[name="col_index"]').prop('value');
        var msg = 'Form (' + formRowInd + ", " + formColInd + ')';
        console.log(msg);

        // replace it since it's now been marked
        var replacement = '<div class="square">' + marker + '</div>';
        form.replaceWith(replacement);
    }

    // update messages
    var msgDiv = $('div#message');
    msgDiv.empty();
    var newMsgDiv = '<div>' + data.message + '</div>';
    msgDiv.append(newMsgDiv);

    if (data.is_game_over) {
        // add the new game url
        var newGameUrl = msgDiv.attr('new-game-url');
        console.log('New game url: ' + newGameUrl);
        var newGameLink = '<a href="' + newGameUrl + '" id="message">Start a new game.</a>'
        msgDiv.append(newGameLink);
    }
    else {
        // update next_player for all forms
        $('input[name="next_player"]').prop('value', data.next_player);

        // re-enable buttons
        $("div.board button:submit").prop("disabled", false);
    }
}


$(document).ready(function() {
    console.log('Page ready!');
    // might need to make request if current player is an AI
    var form = $('form');

    if (form) {
        console.log(form);
        var player_type = form.find('input[name="next_player_type"]').prop('value');
        console.log('Next player type: ' + player_type);

        if (player_type && player_type != 'human') {
            var url = form.attr('board-update-url');
            // just use the form but remove the row and col indexes
            $.ajax({
                url: url,
                data: form.serialize(),
                dataType: 'json',
                success: onSuccess
            });
        }
    }
});


$(document).on('click', 'button.cell', function(e) {
    // replace the button with div
    var clicked = e.currentTarget;
    var form = $(clicked).closest('form');
    var cur_player_type = form.find('input[name="cur_player_type"]').prop('value');
    var cur_marker = form.find('input[name="cur_player"]').prop('value');
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

    // send json query
    var url = form.attr('board-update-url');
    console.log('Board update URL: ' + url);
    $.ajax({
        url: url,
        data: form.serialize(),
        dataType: 'json',
        success: onSuccess,
    });

    // change message to last_marker is thinking, if last_marker is AI
    console.log('Current player type: ' + cur_player_type);
    if (cur_player_type != 'human') {
        var msg = "Player " + cur_marker + " is thinking...";
        var msgDiv = '<div id="message">' + msg + '</div>';
        $('div #message').empty();
        $('div #message').append(msgDiv);
        console.log(msg);
    }
});
