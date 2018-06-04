var gulp = require('gulp');
var tap = require('gulp-tap');
var path = require('path');

gulp.task('build', function() {

    gulp.src('./src/*').pipe(gulp.dest('./build/'));

    gulp.src('./submodules/micropython-max7219/max7219.py').pipe(gulp.dest('./build/'));
    gulp.src('./submodules/python_lcd/lcd/lcd_api.py').pipe(gulp.dest('./build/'));
    gulp.src('./submodules/python_lcd/lcd/nodemcu_gpio_lcd.py').pipe(gulp.dest('./build/'));

});

gulp.task('flash', ['build'], function() {

    process.chdir('./build');

    gulp.src('./*')
        .pipe(tap(function(file, t) {
            let relativePath = path.relative('.', file.path);
            console.log('Flashing', relativePath);
            // TODO actually flash the files
        }));

});

gulp.task('default', ['build', 'flash']);
