var myApp = angular.module('dataFilter', ['restangular', 'ngResource', 'ui.bootstrap', 'ngRoute'])

    .config(function ($httpProvider, RestangularProvider) {
        
        RestangularProvider.setBaseUrl('/API');
        RestangularProvider.setDefaultHeaders({Authorization: "Basic Y3BzMTVfYWRtaW46c2VjcmV0"});

    })

    .controller('DataFilterCtrl', function ($scope, $window, $q, $interval, Restangular) {

        $scope.adminEnabled = false;
        $scope.sortType = 'endDate';
        $scope.sortReverse = false;

        $scope.$watch('adminEnabled', function () {
            $scope.adminEnableText = !$scope.adminEnabled ? 'Enable Admin' : 'Disable Admin';
        });

        $scope.datasets = Restangular.all('dataset').getList().$object;

        $scope.sortType = 'endDate';
        $scope.sortReverse = false;

        $scope.datasetForm = {
            show: false,
            dataset: {}
        };

        $scope.toggleDatasetForm = function () {
            $scope.datasetForm.show = !$scope.datasetForm.show;
        };

        $scope.clearForm = function () {
            $scope.datasetForm.dataset = {}
        };


        $scope.refreshTable = function () {
            $scope.datasets = Restangular.all('dataset').getList().$object
        };

        //var stop = $interval(function() {
        //    console.log("Refreshed!");
        //    $scope.refreshTable()
        //
        //}, 10000);
        //
        //$scope.$on('$destroy', function() {
        //    $interval.cancel(stop);
        //});

        //$interval($scope.refreshTable, 10000);

        $scope.addDataset = function (dataset) {
            console.log(dataset);
            if (dataset != undefined) {
                if (typeof(dataset.tags) == "string") {
                dataset.tags = dataset.tags.split(/[ ,]+/);
                }
                console.log(dataset);

                Restangular.all('dataset').post(dataset).then(function(){
                    console.log("Dataset requested");
                }, function() {
                    console.log("Error requesting dataset");
                });
            }

        };

        $scope.duplicate = function (dataset) {

            var new_dataset = {};
            new_dataset.type = dataset.type;
            new_dataset.description = dataset.description;
            new_dataset.limitType = dataset.limitType;
            new_dataset.limit = dataset.limit;
            new_dataset.tags = dataset.tags;

            $scope.datasetForm.show = true;
            $scope.datasetForm.dataset = new_dataset;


        };

        $scope.startDataset = function (dataset) {

            Restangular.one("dataset",dataset.id).customPUT({'status': 'ORDERED'},"status").then(function(){
                console.log("Dataset request start");
            }, function() {
                console.log("Error requesting dataset start");
            });

            $scope.refreshTable();

        };

        $scope.deleteDataset = function (dataset) {

            Restangular.one("dataset", dataset.id).remove().then(function(){
                $scope.refreshTable();
            })
        };

        $scope.stopDataset = function (dataset) {


            Restangular.one("dataset",dataset.id).customPUT({'status': 'STOPPED'},"status").then(function(){
                console.log("Dataset request stop");
            }, function() {
                console.log("Error requesting dataset stop");
            });

            $scope.refreshTable();
        }

    });