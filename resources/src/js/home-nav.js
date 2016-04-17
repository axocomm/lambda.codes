'use strict';

var HOME_NAV_SELECTOR = '#home-nav-items > li';
var TITLE_SELECTOR = '#home-title';

var fadeTitle = function (newTitle) {
  var $title = $(TITLE_SELECTOR).first();
  $title.fadeOut(300, function () {
    $(this).text(newTitle).fadeIn(300);
  });
};

var onNavItemHover = function ($el) {
  var itemTitle = $el.data('title');
  fadeTitle(itemTitle);
};

$(document).ready(function () {
  $(HOME_NAV_SELECTOR).mouseover(function () {
    onNavItemHover($(this));
  }).mouseout(function () {
    fadeTitle('xyzy');
  });
});
