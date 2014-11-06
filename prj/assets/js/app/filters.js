'use strict';

/* Filters */

var appFilters = angular.module('appFilters', []);


appFilters.filter('frytruncate', function () {
    return function (text, length, end) {
        if (text!==undefined) {
            if (isNaN(length))
                length = 10;

            if (end === undefined)
                end = "...";
            if (text.length <= length || text.length - end.length <= length) {

                return text;
            }
            else {
                return String(text).substring(0, length - end.length) + end;
            }
        }
    };
});

