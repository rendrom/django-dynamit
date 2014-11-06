module.exports = function (grunt) {

    grunt.initConfig({
            pkg: grunt.file.readJSON('package.json'),
            ngAnnotate: {
                options: {
                    singleQuotes: true
                },
                app: {
                    files: [
                        {
                            expand: true,
                            src: 'prj/assets/js/app/*.js'
                        }
                    ]
                }
            }
        }
    );

    grunt.loadNpmTasks('grunt-ng-annotate');
    grunt.registerTask('default', ["ngAnnotate"]);

};