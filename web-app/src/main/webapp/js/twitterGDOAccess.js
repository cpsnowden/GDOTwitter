var twitterGDOAccessApp = angular.module('twitterGDOAccess',['ngRoute','dataFilter','analytics','consumers','welcome','chartApp']);

    twitterGDOAccessApp.config(function($routeProvider, RestangularProvider) {
        $routeProvider

            .when('/',{
                templateUrl:'partials/Welcome.html'
            })

            .when('/datasets',{
                templateUrl:'partials/Datasets.html'
            })

            .when('/analytics', {
                templateUrl:'partials/Analytics.html'
            })

            .when('/consumers', {
            templateUrl:'partials/TwitterConsumers.html'
            })

            .when('/charts/:dsid/:id', {
            templateUrl:'partials/Charts.html',
                controller:'chartController'
            });
        
        RestangularProvider.setBaseUrl('/API');
        RestangularProvider.setDefaultHeaders({Authorization: "Basic Y3BzMTVfYWRtaW46c2VjcmV0"});

    });

    twitterGDOAccessApp.controller('mainController', function($scope,$interval, Restangular) {
        $scope.info = "Heloooooo";

        $scope.data_services = Restangular.all('data_service').getList().$object

        //var stop = $interval(function() {
        //    console.log("Refreshed!");
        //    $scope.data_services = Restangular.all('data_service').getList().$object
        //
        //}, 10000);
        //
        //$scope.$on('$destroy', function() {
        //    $interval.cancel(stop);
        //});


    });