'use strict';

// :hover apparently doesn't work in iOS
$('nav#main ul li').hover(function () {
  $(this).addClass('hover');
}, function () {
  $(this).removeClass('hover');
});
