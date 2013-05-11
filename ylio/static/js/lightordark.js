// https://gist.github.com/larrythefox/1636338
// Determine if the background color of an element is light or dark.
(function($){
  
  $.fn.lightOrDark = function(){
    var r,b,g,hsp
      , a = this.css('background-color');
    
    if (a.match(/^rgb/)) {
      a = a.match(/^rgba?\((\d+),\s*(\d+),\s*(\d+)(?:,\s*(\d+(?:\.\d+)?))?\)$/);
      r = a[1];
      b = a[2];
      g = a[3];
    } else {
      a = +("0x" + a.slice(1).replace( // thanks to jed : http://gist.github.com/983661
          a.length < 5 && /./g, '$&$&'
        )
      );
      r = a >> 16;
      b = a >> 8 & 255;
      g = a & 255;
    }
    hsp = Math.sqrt( // HSP equation from http://alienryderflex.com/hsp.html
      0.299 * (r * r) +
      0.587 * (g * g) +
      0.114 * (b * b)
    );
    if (hsp>127.5) {
      this.addClass('light');
      this.removeClass('dark');
    } else {
      this.addClass('dark');
      this.removeClass('light');
    }
  }
  
})(jQuery);