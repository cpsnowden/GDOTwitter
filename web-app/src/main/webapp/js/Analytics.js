var myApp = angular.module('analytics', ['restangular', 'ngResource', 'ui.bootstrap', 'ngRoute'])

    .config(function (RestangularProvider) {
        RestangularProvider.setBaseUrl('/API');
        RestangularProvider.setFullResponse(true);
        RestangularProvider.setDefaultHeaders({Authorization: "Basic Y3BzMTVfYWRtaW46c2VjcmV0"});
    })

    .controller('AnalyticsCtrl', ["$scope", "$window", "$interval", "Restangular", function ($scope, $window, $interval, Restangular) {

        $scope.datasets = Restangular.all('dataset').getList({status: "READY_FOR_ANALYTICS"}).$object;
        $scope.deleteEnabled = false;
        $scope.sortType = 'endDate';
        $scope.sortReverse = false;
        $scope.selected = {};
        $scope.$watch('deleteEnabled', function () {
            $scope.deleteEnabledText = !$scope.deleteEnabled ? 'Enable Delete' : 'Disable Delete';
        });

        $scope.analyticsForm = {
            show: false,
            order: {
                specialised_args: {}
            },
            dataset: {},
            options: {},
            subType: {}
        };

        $scope.refreshSubTable = function () {

            $scope.datasets.forEach(function (e) {
                e.analytics = $scope.getAnalytics(e)
            })
        };

        $scope.chart = function (a) {
            var url = 'http://' + $window.location.host + '#/charts/' + a.dataset_id + "/" + a.id;
            $window.open(url, '_blank');

        };

        $scope.refreshTable = function () {
            $scope.datasets = Restangular.all('dataset').getList({status: "READY_FOR_ANALYTICS"}).$object

        };

        $scope.reset = function () {
        $scope.selected = {};
    };

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

        $scope.getAnalytics = function (dataset) {
            return Restangular.one("dataset", dataset.id).getList('analytics').$object
        };

        $scope.cancel = function () {
            $scope.analyticsForm = {
                show: false,
                order: {
                    specialised_args: {}
                },
                dataset: {},
                options: {},
                subType: {}
            }
        };

        $scope.orderAnalytics = function (dataset) {
            $scope.get_options();
            $scope.analyticsForm.order.id = dataset.id;
            $scope.analyticsForm.order.description = "MConsole_" + new Date().toLocaleString();
            $scope.analyticsForm.show = true;
            $scope.analyticsForm.dataset = dataset;
        };

        $scope.getTemplate = function (analytics) {

            if (analytics.id === $scope.selected.id) return 'edit';
            else return 'display';
        };
        $scope.editAnalytics = function (analytics) {
            $scope.selected = angular.copy(analytics);
        };
        $scope.saveUpdate = function (dataset, aid) {

            console.log("Saving");
            console.log($scope.selected.description);
            $scope.updateDescription(dataset.id, aid, $scope.selected.description);
            $scope.reset();
            dataset.analytics = $scope.getAnalytics(dataset)


        };


        $scope.updateDescription = function (dsid, id, description) {
            Restangular.one("dataset", dsid).one("analytics", id).customPUT({'description': description}).then(function () {
                console.log("Description updated");
            }, function () {
                console.log("Error updating description");
            });
        };

        $scope.newAnalytics = function (order) {

            console.log(order);
            Restangular.one("dataset", order.id).post("analytics", order);
            $scope.analyticsForm.dataset.analytics = $scope.getAnalytics($scope.analyticsForm.dataset);
            $scope.cancel()

        };

        $scope.get_options = function () {
            Restangular.all('analytics_options').getList().then(
                function (options) {
                    $scope.analyticsForm.options = Restangular.stripRestangular(options.data)
                }
            )
        };

        $scope.addNewChoice = function (name) {
            $scope.analyticsForm.order.specialised_args[name].push({"name": "", "tags": []})
        };


        $scope.removeChoice = function (name, n) {
            console.log($scope.analyticsForm.order.specialised_args[name].splice(n, 1))
        };

        $scope.selectClass = function () {

            for (var i = 0; i < $scope.analyticsForm.options.length; i++) {
                o = $scope.analyticsForm.options[i];
                if (o.classification == $scope.analyticsForm.order.classification) {
                    $scope.analyticsForm.subTypes = o.types
                }
            }
            $scope.analyticsForm.specialised_args = [];
            $scope.analyticsForm.order.specialised_args = {};

        };

        $scope.selectType = function () {

            type = $scope.analyticsForm.order.type;
            types = $scope.analyticsForm.subTypes;
            for (var i = 0; i < types.length; i++) {
                option = types[i];
                if (option.type == type) {
                    $scope.analyticsForm.specialised_args = option.args;
                    for (var j = 0; j < option.args.length; j++) {
                        setting = option.args[j];
                        if (setting.type == "datetime") {
                            $scope.analyticsForm.order.specialised_args[setting.name] = new Date(
                                $scope.analyticsForm.dataset[setting.default_dataset_field]
                            )
                        } else if (setting.type == "integer"
                            || setting.type == "string"
                            || setting.type == "boolean"
                            || setting.type == "dictionary_list"
                            || setting.type == "enum") {
                            $scope.analyticsForm.order.specialised_args[setting.name] = setting.default
                        }

                    }
                }
            }
            console.log($scope.analyticsForm)
        };

        $scope.getDownloadOptions = function (item) {
            Restangular.oneUrl("tempit", item.uri_data).get().then(function (result) {
                var analyticsDataOptions = Restangular.stripRestangular(result.data);
                var downloadOptions = analyticsDataOptions.urls;
                options = [];
                for (var k in downloadOptions) {
                    if (downloadOptions.hasOwnProperty(k) && downloadOptions[k] != null) {
                        options.push({"name": k, "value": downloadOptions[k]})
                    }
                }
                item.downloadOptions = options;
                item.defaultDownload = analyticsDataOptions.prefered_url
            });


        };

        $scope.download = function (analytics) {

            Restangular.one("dataset", analytics.dataset_id).one("analytics", analytics.id).customGET("data").then(function (res) {

                console.log(res);
                options = Restangular.stripRestangular(res.data);
                console.log(options);

                angular.forEach(options, function (url, key) {
                    if (url != null) {
                        console.log("Requesting " + key + " " + url);
                        Restangular.oneUrl("temp", url).get().then(function (result) {
                            console.log(result);
                            console.log(result.headers("Content-Disposition"));
                            var fname = result.headers("Content-Disposition").split(';')[1].trim().split("=")[1].trim();
                            console.log(fname);
                            data = result.data;
                            if (result.headers("mimetype") == "application/json") {
                                data = Restangular.stripRestangular(data);
                                data = JSON.stringify(data)
                            }
                            console.log("Saving " + fname);
                            saveAs(new Blob([data], {type: result.headers("mimetype")}), fname);

                        })
                    }
                });
            })
        };

        $scope.downloadItem = function (url) {
            console.log(url);
            Restangular.oneUrl("temp", url).get().then(function (result) {

                var fname = result.headers("Content-Disposition").split(';')[1].trim().split("=")[1].trim();
                data = result.data;
                console.log(result.headers("mimetype"))
                if (result.headers("mimetype") == "application/json") {
                    data = Restangular.stripRestangular(data);
                    data = JSON.stringify(data)
                }
                console.log("Saving " + fname);
                saveAs(new Blob([data], {type: result.headers("mimetype")}), fname);
            })
        };

        $scope.delete = function (analytics, dataset) {
            // var msgbox = $dialog.messageBox('Delete Item', 'Are you sure?', [{
            //     label: 'Yes, I\'m sure',
            //     result: 'yes'
            // }, {label: 'Nope', result: 'no'}]);
            // msgbox.open().then(function (result) {
            //     if (result === 'yes') {
            Restangular.one("dataset", analytics.dataset_id).one('analytics', analytics.id).remove().then(function () {
                dataset.analytics = $scope.getAnalytics(dataset)
            });
            //     }
            // })
        };


        $scope.print_p = function (p) {
            console.log(p)
        };

    }]);