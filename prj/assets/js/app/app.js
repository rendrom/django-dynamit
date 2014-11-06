'use strict';

/* App Module */

var app = angular.module('app', [
  'ngRoute',
  'appDirectives',
  'appFilters',
  'appControllers',
  'appServices',
  'ngAnimate'
]);

app.config(["$httpProvider", function($httpProvider){
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
        $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    }]);

app.config(["$animateProvider", function($animateProvider) {
  $animateProvider.classNameFilter(/animate/);
}]);

app.config(["$routeProvider", function($routeProvider) {
    $routeProvider.
      when('/', {
        templateUrl: 'static/partials/hello.html'
      }).
      when('/dynamo/:model', {
        templateUrl: 'static/partials/dynamo.html',
        controller: 'dynamoController'
      }).
      when('/newmodel/', {
        templateUrl: 'static/partials/newmodel.html'
      }).

      otherwise({
        redirectTo: '/'
      });
  }]);


//app.run(['$rootScope', 'appConf', function ($rootScope, appConf ) {
//    $rootScope.$on("$locationChangeSuccess",function(event, next, current) {
//
//
//    });
//}]);


app.config(["$interpolateProvider", function($interpolateProvider) {
    $interpolateProvider.startSymbol('{$');
    $interpolateProvider.endSymbol('$}');
}]);

