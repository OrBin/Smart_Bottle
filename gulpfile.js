var gulp = require('gulp');
var exec = require('gulp-exec');


const FLASH_OPTIONS = {
    continueOnError: false, // default = false, true means don't emit error event
    pipeStdout: false, // default = false, true means stdout is written to file.contents
    devicePort: '/dev/ttyUSB0' // content passed to lodash.template()
};

gulp.task('build-inputs', function() {

    gulp.src('./src/common/*').pipe(gulp.dest('./build/inputs/'));
    gulp.src('./src/inputs/*').pipe(gulp.dest('./build/inputs/'));

    //gulp.src('./submodules/micropython-max7219/max7219.py').pipe(gulp.dest('./build/'));
    //gulp.src('./submodules/python_lcd/lcd/lcd_api.py').pipe(gulp.dest('./build/'));
    //gulp.src('./submodules/python_lcd/lcd/nodemcu_gpio_lcd.py').pipe(gulp.dest('./build/'));
    //gulp.src('./submodules/MPU6050-ESP8266-MicroPython/mpu6050.py').pipe(gulp.dest('./build/'));

});

gulp.task('build-outputs', function() {

    gulp.src('./src/common/*').pipe(gulp.dest('./build/outputs/'));
    gulp.src('./src/outputs/*').pipe(gulp.dest('./build/outputs/'));

    //gulp.src('./submodules/micropython-max7219/max7219.py').pipe(gulp.dest('./build/'));
    //gulp.src('./submodules/python_lcd/lcd/lcd_api.py').pipe(gulp.dest('./build/'));
    //gulp.src('./submodules/python_lcd/lcd/nodemcu_gpio_lcd.py').pipe(gulp.dest('./build/'));
    //gulp.src('./submodules/MPU6050-ESP8266-MicroPython/mpu6050.py').pipe(gulp.dest('./build/'));

});

function getFlashTask(buildDirectory) {
    return function() {
        process.chdir(buildDirectory);

        return gulp.src('./*')
            .pipe(exec('echo <%= file.path %> ', FLASH_OPTIONS))
            .pipe(exec('/opt/anaconda3/bin/ampy --port <%= options.devicePort %> put <%= file.path %> ', FLASH_OPTIONS));
    }
}

gulp.task('flash-inputs', getFlashTask('./build/inputs'));
gulp.task('flash-outputs', getFlashTask('./build/outputs'));

gulp.task('inputs', ['build-inputs', 'flash-inputs']);
gulp.task('outputs', ['build-outputs', 'flash-outputs']);
