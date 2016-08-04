

var myApp = angular.module('analytics', ['restangular','ngResource', 'ui.bootstrap','ngRoute'])

    .config(function(RestangularProvider) {
        RestangularProvider.setBaseUrl('/API');
        RestangularProvider.setFullResponse(true);
        RestangularProvider.setDefaultHeaders({Authorization:  "Basic Y3BzMTVfYWRtaW46c2VjcmV0"});
    })

    .controller('AnalyticsCtrl',function($scope, $window, $q, $interval, Restangular,uibDateParser, $location) {

    $scope.datasets = Restangular.all('dataset').getList({status:"READY_FOR_ANALYTICS"}).$object;

    $scope.sortType = 'endDate';
    $scope.sortReverse = false;

    $scope.analyticsForm = {
        show: false,
        order: {
            specialised_args:{}
        },
        dataset:{},
        options:{},
        subType:{}
    };

    $scope.refreshSubTable = function(){
        //$scope.refreshTable()
        $scope.datasets.forEach(function(e) {
            e.analytics = $scope.getAnalytics(e)
        })
    };

    $scope.chart = function(a){

        // $window.open('http://localhost:8080/#/charts/' + a.dataset_id + "/" + a.id, '_blank');
        var url = 'http://' + $window.location.host + '#/charts/' + a.dataset_id + "/" + a.id;
        $window.open(url, '_blank');
    }

    $scope.refreshTable = function(){
        $scope.datasets = Restangular.all('dataset').getList({status:"READY_FOR_ANALYTICS"}).$object

    }

    ////$interval($scope.refreshSubTable, 10000);
    //var stop = $interval(function() {
    //    console.log("Refreshed!");
    //    $scope.refreshSubTable()
    //
    //}, 10000);
    //
    //$scope.$on('$destroy', function() {
    //    $interval.cancel(stop);
    //});

    $scope.getAnalytics = function(dataset) {
        return Restangular.one("dataset",dataset.id).getList('analytics').$object
    }

    $scope.cancel = function () {
        $scope.analyticsForm = {
            show: false,
            order: {
                specialised_args:{}
            },
            dataset:{},
            options:{},
            subType:{}
        }
    };

    $scope.orderAnalytics = function(dataset) {
        $scope.get_options();
        $scope.analyticsForm.order.id = dataset.id;
        $scope.analyticsForm.show = true;
        $scope.analyticsForm.dataset = dataset;
    };

    $scope.newAnalytics = function(order) {

        console.log(order);
        Restangular.one("dataset",order.id).post("analytics",order);
        $scope.analyticsForm.dataset.analytics = $scope.getAnalytics($scope.analyticsForm.dataset);
        $scope.cancel()

    };

    $scope.get_options = function() {
        Restangular.all('analytics_options').getList().then(
            function(options){
                $scope.analyticsForm.options = Restangular.stripRestangular(options.data)
            }
        )
    };

    $scope.addNewChoice = function(name) {
        $scope.analyticsForm.order.specialised_args[name].push({"name":"","tags":[]})
    };


    $scope.removeChoice = function(name, n) {
        console.log($scope.analyticsForm.order.specialised_args[name].splice(n,1))
    }

    $scope.selectClass = function() {

        for (var i = 0; i < $scope.analyticsForm.options.length; i++) {
            o = $scope.analyticsForm.options[i];
            if (o.classification == $scope.analyticsForm.order.classification) {
                $scope.analyticsForm.subTypes = o.types
            }
        }
        $scope.analyticsForm.specialised_args = [];
        $scope.analyticsForm.order.specialised_args = {};

    };

    $scope.selectType = function() {

        type = $scope.analyticsForm.order.type;
        types = $scope.analyticsForm.subTypes;
        for (var i = 0; i < types.length; i++) {
            option = types[i];
            if (option.type == type) {
                $scope.analyticsForm.specialised_args = option.args;
                for(var j=0;j < option.args.length; j++) {
                    setting = option.args[j];
                    if(setting.type == "datetime") {
                        $scope.analyticsForm.order.specialised_args[setting.name] = new Date(
                            $scope.analyticsForm.dataset[setting.default_dataset_field]
                        )
                    } else if(setting.type =="integer"
                        || setting.type =="string"
                        || setting.type =="boolean"
                        || setting.type == "dictionary_list"
                        || setting.type == "enum") {
                        $scope.analyticsForm.order.specialised_args[setting.name] = setting.default
                    }

                }
            }
        }
    };

    $scope.download = function(analytics) {

        Restangular.one("dataset",analytics.dataset_id).one("analytics",analytics.id).customGET("data").then(function(res) {

            console.log(res);
            options = Restangular.stripRestangular(res.data);
            console.log(options);

            angular.forEach(options, function (url, key) {
                if(url != null) {
                    console.log("Requesting " + key + " " + url);
                    Restangular.oneUrl("temp", url).get().then(function (result) {
                        console.log(result)
                        console.log(result.headers("Content-Disposition"))
                        var fname = result.headers("Content-Disposition").split(';')[1].trim().split("=")[1].trim();
                        console.log(fname)
                        data = result.data
                        if(result.headers("mimetype") == "application/json"){
                            data = Restangular.stripRestangular(data)
                            data = JSON.stringify(data)
                        }
                        console.log("Saving " + fname)
                        saveAs(new Blob([data], {type: result.headers("mimetype")}), fname);

                    })
                }
            });
        })
    };

    $scope.delete = function(analytics,dataset) {
        Restangular.one("dataset",analytics.dataset_id).one('analytics',analytics.id).remove().then(function(){
            dataset.analytics = $scope.getAnalytics(dataset)
        });
    };

    $scope.print_p = function(p) {
        console.log(p)
    }
    
});