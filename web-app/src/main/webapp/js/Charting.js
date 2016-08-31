/**
 * Created by ChrisSnowden on 04/08/2016.
 */
var chartApp = angular.module('chartApp', ['restangular', "ng-fusioncharts", 'ngResource', 'ui.bootstrap', 'ngRoute', 'ngSanitize'])

    .config(function (RestangularProvider) {
        RestangularProvider.setBaseUrl('/API');
        RestangularProvider.setFullResponse(true);
        RestangularProvider.setDefaultHeaders({Authorization: "Basic Y3BzMTVfYWRtaW46c2VjcmV0"});
    })

    .controller('chartController', ['$scope', '$routeParams', 'Restangular', 'FullScreen', '$sce', function ($scope, $routeParams, Restangular, FullScreen, $sce) {

        $scope.fsService = FullScreen;
        $scope.id = $routeParams.id;
        $scope.dsid = $routeParams.dsid;
        $scope.chartReady = false;

        $scope.Download = true;

        $scope.IframeManager = {
            Show: function (url) {
                $scope.IframeManager.Url = url;
            },
            Hide: function () {
                $scope.IframeManager.Url = null;
            }
        };

        $scope.init = function () {

            $scope.analytics_meta = getAnalyticsDetails($scope.id, $scope.dsid);
            $scope.fsService.fsOn = !!("fs" in $routeParams && $routeParams.fs != "");
            loadChart($scope.id, $scope.dsid);
        };

        var getAnalyticsDetails = function (id, dsid) {
            return Restangular.one("dataset", dsid).one("analytics", id).get().$object;
        };

        var loadChart = function (id, dsid) {
            Restangular.one("dataset", dsid).one("analytics", id).customGET("data/dl?type=html_id").then(function (result) {
                var file = new Blob([result.data], {type: result.headers("mimetype")});
                var url = window.URL.createObjectURL(file);
                $scope.IframeManager.Show($sce.trustAsResourceUrl(url));
                $scope.chartReady = true;
            });
        };


    }]);