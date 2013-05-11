$(document).ready(function() {

    var stuff = {
        color: '#f5ebf5',
    }

    if (Modernizr.localstorage) {
        stuff.colour = localStorage['bg'];
        if (stuff.colour != undefined) {
            $('.container').css('background-color', stuff.colour);
            $('html').css('background-color', stuff.colour);
            $('#colour').css('background-color', stuff.colour);
            $('.colorpicker_current_color').css('background-color', stuff.colour);
        }
    }

    $('form').submit(function(event) {
        event.preventDefault();

        var url = $('input').val();
        if (url.substring(0, 4) != "http") {
            url = 'http://' + url;
        }

        $.ajax({
            url: '/shorten',
            type: 'POST',
            data: {
                url: url
            },
            success: function(data) {
                $('.info').html('');
                $('input').val(data.url);
                $('input').select();
            },
            error: function(xhr) {
                var data = $.parseJSON(xhr.responseText);
                $('.info').html('Error: ' + data.error);
                $('input').shake(2, 20, 350);
            }
        });
    });

    $('#colour').ColorPicker({
        color: stuff.colour,
        onShow: function (picker) {
            $(picker).fadeIn(500);
        },
        onHide: function (picker) {
            $(picker).fadeOut(500);
            if (Modernizr.localstorage) {
                localStorage['bg'] = stuff.colour;
            }
        },
        onChange: function (hsb, hex) {
            var colour = '#' + hex
            $('.container').css('background-color', colour);
            $('html').css('background-color', colour);
            $('#colour').css('background-color', colour);
            stuff.colour = colour;
        },
    });

});

// http://stackoverflow.com/a/4399433/1274612
jQuery.fn.shake = function(intShakes, intDistance, intDuration) {
    this.each(function() {
        $(this).css("position","relative"); 
        for (var x=1; x<=intShakes; x++) {
        $(this).animate({left:(intDistance*-1)}, ((intDuration/intShakes)/4))
    .animate({left:intDistance}, ((intDuration/intShakes)/2))
    .animate({left:0}, ((intDuration/intShakes)/4));
    }
  });
return this;
};
