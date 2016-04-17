'use strict';

var gulp = require('gulp');
var sass = require('gulp-sass');
var cleanCss = require('gulp-clean-css');
var del = require('del');

var manifest = {
  scss: ['resources/src/scss/styles.scss']
};

var dest = {
  css: 'resources/public/css'
};

gulp.task('clean', function () {
  return del([dest.css]);
});

gulp.task('scss', function () {
  return gulp.src(manifest.scss)
    .pipe(sass().on('error', sass.logError))
    .pipe(cleanCss())
    .pipe(gulp.dest(dest.css));
});

gulp.task('build', ['scss']);

gulp.task('default', ['build']);

gulp.task('d', ['default'], function () {
  return gulp.watch(manifest.scss, ['default']);
});
