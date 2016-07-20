var myApp = angular.module('consumers', ['restangular', 'ngResource', 'ui.bootstrap', 'ngRoute'])

    .config(function ($httpProvider, RestangularProvider) {

        //$httpProvider.defaults.headers.common['Authorization'] = "Basic Y3BzMTVfYWRtaW46c2VjcmV0";
        RestangularProvider.setBaseUrl('/API');
        RestangularProvider.setDefaultHeaders({Authorization: "Basic Y3BzMTVfYWRtaW46c2VjcmV0"});

    })

    .controller('ConsumerCtrl', function ($scope, $window, $q, $interval, Restangular) {

        $scope.consumers = Restangular.all('twitter_consumer').getList().$object


        $scope.refreshTable = function () {
            $scope.consumers = Restangular.all('twitter_consumer').getList().$object
        };

        $scope.addConsumer = function () {

            Restangular.all('twitter_consumer').post().then(function(){
                console.log("Consumer requested");
            }, function() {
                console.log("Error requesting consumer");
            });

            $scope.refreshTable()
        };

        $scope.deleteConsumer = function (consumer) {

            Restangular.one("twitter_consumer", consumer.id).remove().then(function(){
                $scope.refreshTable();
            })
            $scope.refreshTable()
        };

        var stop = $interval(function() {
            console.log("Refreshed!");
            $scope.refreshTable()

        }, 10000);
    });