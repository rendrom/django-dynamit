'use strict';

/* Controllers */

var appControllers = angular.module('appControllers', []);

appControllers.controller('appController', ["$scope", "appConf", "api", "authState", function($scope, appConf, api, authState) {
    $scope.authState = authState;
    $scope.getCredentials = function(){
        return {username: $scope.username, password: $scope.password};
    };
    $scope.login = function(){
        api.auth.login($scope.getCredentials()).
            $promise.
            then(function(data){
                $('#loginModal').modal('hide');
                $.growl("Добро пожаловать на сайт, <b>"+data.username+"</b>!",glowOptions);
                authState.user = data.username;
                authState.is_superuser = data.is_superuser
            }).
            catch(function(data){
                glowOptions.type = 'danger';
                glowOptions.delay = '3000';
                $.growl(data.data.detail,glowOptions);
            });
    };
    $scope.logout = function(){
        api.auth.logout(function(){
            $('#loginModal').modal('hide');
            $.growl("До свидания, <b>"+authState.user+"</b>!",glowOptions);
            authState.user = undefined;
            authState.is_superuser = undefined;
        });
    };
    $scope.togglemenu = function() {
        $("#wrapper").toggleClass("toggled");
    }
}]);

appControllers.controller('dynamoListCtrl', ["$scope", "$http","appConf", "api", function($scope, $http, appConf, api) {
        $scope.dynamos = {};
        $scope.getDynamo = function(){
            api.dynamicmodels.query(function (data) {
                $scope.dynamo = data;
            });
        };
        $scope.getDynamo();
    }]);

appControllers.controller('dynamoController', ["$scope", "$routeParams","appConf", "api", function($scope, $routeParams, appConf, api) {
        $scope.dynamo = {};
        $scope.new = {};
        $scope.getDynamoDetail = function () {
            api.dynamo.query({model: $routeParams.model},function (data) {
                $scope.verbosename = data.meta.verbose_name;
                $scope.fieldtype = data.meta.fieldtype;
                $scope.dynamo = data.features;
            });
        };
        $scope.getDynamoDetail();
        $scope.editField = function(data) {
            api.dynamo.update({model:$routeParams.model, id:data.id}, data, function (data) {
                glowOptions.delay = '2000';
                $.growl("Объект №: "+ data.id+" обновлён", glowOptions);
                return true;
            }, function (error) { return false; })
        };
        $scope.createNew = function() {
            var data = $scope.new;
            api.dynamo.create({model:$routeParams.model}, data, function(data) {
                $scope.dynamo.push(data);
                $scope.new = {};
                glowOptions.delay = '2000';
                $.growl("Объект №: "+ data.id +" добавлен", glowOptions);
            }, function (error) {})
        };
        $scope.deleteRow = function(data) {
            api.dynamo.delete({model:$routeParams.model, id:data.id}, data, function (data) {
                glowOptions.delay = '2000';
                $.growl("Объект №: "+ data.id+" удалён", glowOptions);
                $scope.dynamo.splice(appConf.getElementIndex(data.id, $scope.dynamo), 1);
                return true;
            }, function (error) { return false; })
        }
    }]);

