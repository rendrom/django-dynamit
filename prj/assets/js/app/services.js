'use strict';

/* Services */

var appServices = angular.module('appServices', ['ngResource']);

appServices.service('authState', function () {
    return {
        user: undefined,
        is_superuser: undefined
    };
});

appServices.service('appConf', function () {
    return {
        nextPage: null,
        getElementIndex: function(id, elements){
                return _.indexOf(
                    elements,
                    _.findWhere(elements, {id: id})
                );
            }
    };
});

appServices.factory('api', ["$resource", function($resource){
    function add_auth_header(data, headersGetter){
        var headers = headersGetter();
        headers['Authorization'] = ('Basic ' + btoa(data.username +
            ':' + data.password));
    }
    return {
        auth: $resource('/api/auth\\/', {}, {
            login:  {method: 'POST', transformRequest: add_auth_header},
            logout: {method: 'DELETE'}
        }),
        dynamicmodels: $resource('/api/dynamicmodel\\/', {}, {
            query:  {method: 'GET', isArray: true},
            create: {method: 'POST'},
            delete: {method: 'DELETE', url: '/api/dynamicmodel/:id/'}
        }),
        dynamo: $resource('/api/:model/', {}, {
            query:  {method: 'GET' },
            create: {method: 'POST'},
            update: {method: 'PUT', url: '/api/:model/:id/'},
            delete: {method: 'DELETE', url: '/api/:model/:id/'}
        })
    };
}]);

angular.module('ngResource').config(["$provide", "$httpProvider", function($provide, $httpProvider) {
        $provide.decorator('$resource', ["$delegate", function($delegate) {
            return function() {
                if (arguments.length > 0) {  // URL
                    arguments[0] = arguments[0].replace(/\/$/, '\\/');
                }

                if (arguments.length > 2) {  // Actions
                    angular.forEach(arguments[2], function(action) {
                        if (action && action.url) {
                            action.url = action.url.replace(/\/$/, '\\/');
                        }
                    });
                }
                return $delegate.apply($delegate, arguments);
            };
        }]);

        $provide.factory('resourceEnforceSlashInterceptor', function() {
            return {
                request: function(config) {
                    config.url = config.url.replace(/[\/\\]+$/, '/');
                    return config;
                }
            };
        });
        $httpProvider.interceptors.push('resourceEnforceSlashInterceptor');
    }
]);