'use strict';

var gulp = require('gulp');
var sass = require('gulp-sass');
var cleanCss = require('gulp-clean-css');
var del = require('del');
var uglify = require('gulp-uglify');

var manifest = {
  scss: ['resources/src/scss/**/*.scss'],
  js: ['resources/src/js/home-nav.js',
       'resources/src/js/navigation.js']
};

var dest = {
  css: 'resources/public/css',
  js: 'resources/public/js'
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

gulp.task('js', function () {
  return gulp.src(manifest.js)
    .pipe(uglify())
    .pipe(gulp.dest(dest.js));
});

gulp.task('build', ['scss', 'js']);

gulp.task('default', ['build']);

gulp.task('d', ['default'], function () {
  var srcFiles = [].concat.apply(manifest.scss, manifest.js);
  return gulp.watch(srcFiles, ['default']);
});
