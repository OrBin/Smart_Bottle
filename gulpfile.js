var childProcess = require('child_process');
var process = require('process');
var gulp = require('gulp');
var exec = require('gulp-exec');
var log = require('fancy-log');

const FLASH_OPTIONS = {
    continueOnError: false, // default = false, true means don't emit error event
    pipeStdout: false, // default = false, true means stdout is written to file.contents
    devicePort: '/dev/ttyUSB0' // content passed to lodash.template()
};

gulp.task('kill-microrepl', function () {

    psCommand = 'ps -eo pid,cmd | grep "microrepl.py ' + FLASH_OPTIONS.devicePort + '" | grep -v grep';

    try {
        stdout = childProcess.execSync(psCommand);
    } catch (Error) {
        log("No MicroREPL running");
        return;
    }

    output = stdout.toString();
    outputFields = output.split(' ').filter(field => field.length > 0);
    microreplPid = outputFields[0];
    log("Found MicroREPL running with pid " + microreplPid);

    process.kill(microreplPid);
    log("Killed MicroREPL with pid " + microreplPid);

});

gulp.task('build-inputs', function() {

    gulp.src('./src/common/*').pipe(gulp.dest('./build/inputs/'));
    gulp.src('./src/inputs/*').pipe(gulp.dest('./build/inputs/'));

    //gulp.src('./submodules/MPU6050-ESP8266-MicroPython/mpu6050.py').pipe(gulp.dest('./build/inputs/'));

});

gulp.task('build-outputs', function() {

    gulp.src('./src/common/*').pipe(gulp.dest('./build/outputs/'));
    gulp.src('./src/outputs/*').pipe(gulp.dest('./build/outputs/'));

    gulp.src('./submodules/micropython-tm1637/tm1637.py').pipe(gulp.dest('./build/outputs/'));

});

function getFlashTask(buildDirectory) {
    return function() {
        process.chdir(buildDirectory);

        return gulp.src('./*')
            .pipe(exec('echo <%= file.path %> ', FLASH_OPTIONS))
            .pipe(exec('/opt/anaconda3/bin/ampy --port <%= options.devicePort %> put <%= file.path %> ', FLASH_OPTIONS));
    }
}

gulp.task('flash-inputs', ['kill-microrepl'], getFlashTask('./build/inputs'));
gulp.task('flash-outputs', ['kill-microrepl'], getFlashTask('./build/outputs'));

gulp.task('inputs', ['build-inputs', 'flash-inputs']);
gulp.task('outputs', ['build-outputs', 'flash-outputs']);
