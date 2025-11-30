/*
* Greedy Navigation
*
* http://codepen.io/lukejacksonn/pen/PwmwWV
*
* Enhanced to be truly adaptive - only hides items when they don't fit
*/

var defined = function(o) {
  return typeof o !== 'undefined' && o !== null;
};

var $nav = $('#site-nav');
var $btn = $('#site-nav button');
var $vlinks = $('#site-nav .visible-links');
var $hlinks = $('#site-nav .hidden-links');

var breaks = [];

function updateNav() {
  // Get available space (accounting for button if visible)
  var availableSpace = $btn.hasClass('hidden') ? $nav.width() : $nav.width() - $btn.outerWidth(true) - 10;

  // Get the total width of visible links
  var visibleWidth = 0;
  $vlinks.children().each(function() {
    visibleWidth += $(this).outerWidth(true);
  });

  // The visible list is overflowing the nav
  if (visibleWidth > availableSpace && $vlinks.children().length > 1) {
    // Record the width of the list
    breaks.push(visibleWidth);

    // Move last item to the hidden list (but keep site title)
    $vlinks.children().last().prependTo($hlinks);

    // Show the dropdown btn
    if ($btn.hasClass('hidden')) {
      $btn.removeClass('hidden');
    }

    // Recur to check if more items need to be hidden
    updateNav();
  } else {
    // Check if there's space to restore an item
    if (breaks.length > 0 && defined($hlinks.children().first().outerWidth(true))) {
      var nextItemWidth = $hlinks.children().first().outerWidth(true);

      // There is space for another item in the nav
      if (availableSpace > visibleWidth + nextItemWidth + 10) {
        // Move the item to the visible list
        $hlinks.children().first().appendTo($vlinks);
        breaks.pop();

        // Check if more items can be restored
        updateNav();
      }
    }

    // Hide the dropdown btn if hidden list is empty
    if ($hlinks.children().length === 0) {
      $btn.addClass('hidden');
      $hlinks.addClass('hidden');
    }
  }

  // Keep counter updated
  $btn.attr("count", $hlinks.children().length);
}

// Window listeners
$(window).resize(function() {
  updateNav();
});

$btn.on('click', function() {
  $hlinks.toggleClass('hidden');
  $(this).toggleClass('close');
});

// Initial call after a short delay to ensure DOM is ready
$(document).ready(function() {
  // Run immediately
  updateNav();

  // Run again after fonts are loaded (widths may change)
  if (document.fonts && document.fonts.ready) {
    document.fonts.ready.then(function() {
      updateNav();
    });
  }

  // Fallback: run again after a short delay
  setTimeout(updateNav, 100);
  setTimeout(updateNav, 500);
});
