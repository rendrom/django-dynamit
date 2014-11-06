'use strict';

/* Directives */

var appDirectives = angular.module('appDirectives', []);


appDirectives.directive('fryServerError', function() {
    return {
      restrict: 'A',
      require: '?ngModel',
      link: function(scope, element, attrs, ctrl) {
        return element.on('change', function() {
          return scope.$apply(function() {
            return ctrl.$setValidity('server', true);
          });
        });
      }
    };
  });


appDirectives.directive("getInput", ['$compile', function($compile) {
    var getInput = function (fieldtype, fn) {
        if (fieldtype != 'AutoField') {
            var input = '<input type="text" class="form-control" ng-model="new.'+ fn +'">';
            switch (fieldtype) {
                case 'DateField':
                    input = '<input type="text" class="form-control" ng-model="new.'+ fn +'">';
                    break;
                case 'CharField':
                    input = '<input type="text" class="form-control" ng-model="new.'+ fn +'">';
                    break;
                case 'BooleanField':
                    input = '<input type="checkbox" class="form-control" ng-model="new.'+ fn +'">';
                    break;
            }
        return input
        }
        else {
            return '<div>---</div>';
        }
    };
    return {
        restrict: "A",
        replace: true,

        link: function (scope, element, attrs) {
            var fn = scope.fn;
            var fieldtype = scope.fieldtype[fn];
            var el = $compile(getInput(fieldtype, fn))(scope);
            scope.view = {
                editableValue: scope.value
            };
            return  element.replaceWith(el);
        }
    }
}]);


appDirectives.directive("clickToEdit", ['$compile', function($compile) {
    var getTemplate = function (fieldtype, verbosename) {
        if (fieldtype != 'AutoField') {
            var input = '<input type="text" class="form-control" ng-model="view.editableValue">';
            var dynamoTemplate;
            switch (fieldtype) {
                case 'DateField':
                    input = '<input type="text" class="form-control" ng-model="view.editableValue">';
                    break;
                case 'CharField':
                    input = '<input type="text" class="form-control" ng-model="view.editableValue">';
                    break;
                case 'BooleanField':
                    input = '<input type="checkbox" class="form-control" ng-model="view.editableValue">';
                    break;
            }
            var input_group =
                '<div class="input-group">' +
                  input +
                  '<div class="input-group-btn">'+
                    '<button class="btn btn-success" ng-click="save()" type="button"><i class="fa fa-check"></i></button>'+
                    '<button class="btn btn-danger" ng-click="disableEditor()" type="button"><i class="fa fa-times"></i></button>'+
                  '</div>'+
                '</div>';

            dynamoTemplate =
            '<div class="click-to-edit">' +
                '<div ng-hide="view.editorEnabled">' +
                    '{$ value $} ' +
                    '<a ng-show="authState.user" ng-click="enableEditor()"><i class="fa fa-pencil"></i></a>' +
                '</div>' +
                '<div ng-show="view.editorEnabled">' +
                    input_group +
                '</div>' +
            '</div>';

        }
        else {
            dynamoTemplate =
            '<div>' +
                '<div>' +
                    '{$ value $} ' +
                '</div>' +
            '</div>';

        }
        return dynamoTemplate
    };
    return {
        restrict: "A",
        replace: true,
        link: function (scope, element, attrs) {

            var fieldtype = attrs.dynamoType;
            var verbosename = attrs.dynamoName;
            var el = $compile(getTemplate(fieldtype, verbosename))(scope);
            scope.view = {
                editableValue: scope.value,
                editorEnabled: false
            };
            scope.enableEditor = function () {
                scope.view.editorEnabled = true;
                scope.view.editableValue = scope.value;
            };
            scope.disableEditor = function () {
                scope.view.editorEnabled = false;
            };
            scope.save = function () {
                scope.value = scope.view.editableValue;
                scope.dynamo[scope.dynamo.indexOf(scope.fields)][scope.key] = scope.value;
                var saved = scope.editField(scope.fields);
                scope.disableEditor();
            };
            return  element.replaceWith(el)
        }

    }
}]);
