'use strict';

function fadeTitle(newTitle) {
  var $title = $('#home-title').first();
  $title.fadeOut(300, function () {
    $(this).text(newTitle).fadeIn(300);
  });
}

function onNavItemHover($el) {
  var itemTitle = $el.data('title');
  fadeTitle(itemTitle);
};

function setupHomeHover(siteTitle) {
  $(function () {
    if ($(window).width() > 600) {
      $('#home-nav-items > li').mouseover(function () {
        onNavItemHover($(this));
      }).mouseout(function () {
        fadeTitle(siteTitle);
      });
    }
  });
}
