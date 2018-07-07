var childProcess = require('child_process');
var process = require('process');
var gulp = require('gulp');
var exec = require('gulp-exec');
var log = require('fancy-log');

const PYMINIFIER_PATH = '/opt/anaconda3/bin/pyminifier';
const AMPY_PATH = '/opt/anaconda3/bin/ampy';
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

function getMinificationTask(buildDirectory) {
    return function() {
        let minificationCommand = PYMINIFIER_PATH + ' --use-tabs' +
            ' --destdir ' + buildDirectory +
            ' --obfuscate ' + buildDirectory + '/*.py';
        let stdout = childProcess.execSync(minificationCommand);
        let outputLines = stdout.toString().split('\n').slice(0, -1);

        for (let i = 0; i < outputLines.length; i++) {
          log('pyminifier:', outputLines[i]);
        }
    }
}

function getFlashTask(buildDirectory) {
    return function() {
        process.chdir(buildDirectory);

        return gulp.src('./*')
            .pipe(exec('echo <%= file.path %> ', FLASH_OPTIONS))
            .pipe(exec(AMPY_PATH + ' --port <%= options.devicePort %> put <%= file.path %> ', FLASH_OPTIONS));
    }
}

gulp.task('minify-inputs', getMinificationTask('./build/inputs'));
gulp.task('minify-outputs', getMinificationTask('./build/outputs'));

gulp.task('flash-inputs', ['kill-microrepl'], getFlashTask('./build/inputs'));
gulp.task('flash-outputs', ['kill-microrepl', 'minify-outputs'], getFlashTask('./build/outputs'));

gulp.task('inputs', ['build-inputs', 'flash-inputs']);
gulp.task('outputs', ['build-outputs', 'flash-outputs']);