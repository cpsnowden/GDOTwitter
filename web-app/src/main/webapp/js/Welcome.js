var myApp = angular.module('welcome', ['restangular', 'ngResource', 'ui.bootstrap', 'ngRoute'])

    .config(function ($httpProvider, RestangularProvider) {
        RestangularProvider.setBaseUrl('/API');
        RestangularProvider.setDefaultHeaders({Authorization: "Basic Y3BzMTVfYWRtaW46c2VjcmV0"});

    })

    .controller('WelcomeCtrl', function ($scope, $window, $q, $interval, Restangular) {

    });