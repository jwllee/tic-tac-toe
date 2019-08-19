$(document).ready(function() {
    $(".cell").click(function(event) {
        var form = $(this).closest('form');
        var rowInd = form.find('input[name="row_index"]').prop('value');
        var colInd = form.find('input[name="col_index"]').prop('value');
        var value = form.find('input[name="next_player"]').prop('value');
        var msg = "Button (" + value + ") at (" + rowInd + ", " + colInd + ") clicked";

        // paint the next player immediately
        // $(this).css('opacity', 1);
        // $(this).text(value);
        console.log(msg);

        // should send GET request for next move
    });
});
