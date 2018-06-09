var path = require('path');
var gulp = require('gulp');
var exec = require('gulp-exec');

gulp.task('build', function() {

    gulp.src('./src/*').pipe(gulp.dest('./build/'));

    gulp.src('./submodules/micropython-max7219/max7219.py').pipe(gulp.dest('./build/'));
    gulp.src('./submodules/python_lcd/lcd/lcd_api.py').pipe(gulp.dest('./build/'));
    gulp.src('./submodules/python_lcd/lcd/nodemcu_gpio_lcd.py').pipe(gulp.dest('./build/'));

});

gulp.task('flash', function() {

    process.chdir('./build');

    var options = {
        continueOnError: false, // default = false, true means don't emit error event
        pipeStdout: false, // default = false, true means stdout is written to file.contents
        devicePort: '/dev/ttyUSB0' // content passed to lodash.template()
    };

    return gulp.src('./*')
        .pipe(exec('echo <%= file.path %> ', options))
        .pipe(exec('/opt/anaconda3/bin/ampy --port <%= options.devicePort %> put <%= file.path %> ', options));

});

gulp.task('default', ['build', 'flash']);
