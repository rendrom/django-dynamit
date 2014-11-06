// Avoid `console` errors in browsers that lack a console.
(function() {
    var method;
    var noop = function () {};
    var methods = [
        'assert', 'clear', 'count', 'debug', 'dir', 'dirxml', 'error',
        'exception', 'group', 'groupCollapsed', 'groupEnd', 'info', 'log',
        'markTimeline', 'profile', 'profileEnd', 'table', 'time', 'timeEnd',
        'timeStamp', 'trace', 'warn'
    ];
    var length = methods.length;
    var console = (window.console = window.console || {});

    while (length--) {
        method = methods[length];

        // Only stub undefined methods.
        if (!console[method]) {
            console[method] = noop;
        }
    }
}());

var glowOptions = {
    delay : '2000',
    type : 'success',
    offset: 60,
    z_index: 2000,
    placement: {
        align: 'center'
    },
    animate: {
        enter: 'animated fadeInRight',
        exit: 'animated fadeOutRight'
    }
};

$("#fileInput").fileinput({
	browseClass: "btn btn-default btn-block",
	showCaption: false,
	showRemove: false,
	showUpload: false,
    browseLabel:'Выберите файл'
});

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});


/**
 * change AngularJS data outside the scope
 * @param {string} elem Dom ID under ngController
 * @param {object} apply Dict of scope param to change
 */
function applyScope (elem, apply) {
    var feature = document.getElementById(elem);
    if (feature) {
        var scope = angular.element(feature).scope();
        scope.safeApply = function(fn) {
          var phase = this.$root.$$phase;
          if(phase == '$apply' || phase == '$digest') {
            if(fn && (typeof(fn) === 'function')) {
              fn();
            }
          } else {
            this.$apply(fn);
          }
        };
        scope.safeApply(function() {
            for (var fry in apply) {
                if (apply.hasOwnProperty(fry)) {
                    var key_name = fry.split(".");
                    if (key_name.length == 1)
                        scope[fry] = apply[fry];
                    else if (key_name.length == 2) {
                        scope[key_name[0]][key_name[1]] = apply[fry];
                    }
                }
            }
        });
    }
}
