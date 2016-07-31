/**
 * Created by ChrisSnowden on 23/07/2016.
 */
var chartApp = angular.module('chartApp', ['restangular', "ng-fusioncharts", 'ngResource', 'ui.bootstrap', 'ngRoute']);

chartApp.controller('chartController', ['$scope', '$routeParams', 'Restangular', 'FullScreen',

    function ($scope, $routeParams, Restangular, FullScreen) {

        $scope.fsService = FullScreen;
        $scope.id = $routeParams.id;
        $scope.dsid = $routeParams.dsid;

        $scope.dataSource = {};
        $scope.chartReady = false;

        $scope.init = function () {

            $scope.analytics_meta = getAnalyticsDetails($scope.id, $scope.dsid);
            console.log($scope.analytics_meta);

            $scope.fsService.fsOn = !!("fs" in $routeParams && $routeParams.fs != "");
            loadChart($scope.id, $scope.dsid);
        };

        var getAnalyticsDetails = function(id, dsid) {
            return Restangular.one("dataset", dsid).one("analytics", id).get().$object;
        };

        var loadChart = function (id, dsid) {

            Restangular.one("dataset", dsid).one("analytics", id).customGET("data").then(function (result) {

                var chartType = result.details.chartType;
                console.log("Getting chart type " + chartType + " for analytics type");
                done = false;
                switch (chartType) {
                    case "pie":
                        done = get_pie_chart(result);
                        break;
                    case "line":
                        done = get_line_graph(result);
                        break;
                    case "time":
                        done = get_time_graph(result);
                        break;
                    case "bar":
                        done = get_bar_chart(result);
                        break;
                    default:
                        console.log("Unknown chart type")
                }

                $scope.chartReady = done;
            })
        };

        var map_pie_chart_data = function (raw) {
            data = [];
            angular.forEach(raw, function (value, key) {
                data.push({"label": value._id, "value": value.count})
            });
            $scope.dataSource.data = data
        };

        var map_line_data = function (raw) {

            var datasets = [];
            var category = [];
            var first = true;
            angular.forEach(raw, function (value, key) {
                var series = {"seriesname": key, "data": []};
                angular.forEach(value, function (v, k) {
                    series.data.push({"value": v});
                    if (first) {
                        category.push({"label": k})
                    }
                });
                first = false;

                datasets.push(series)
            });

            $scope.dataSource.dataset = datasets;
            $scope.dataSource.categories = [{"category": category}]

        };

        var map_time_data = function(raw) {

            var category = [];
            var temp_values = {};
            angular.forEach(raw.categories, function (value, index) {
                category.push({"label": value});
                temp_values[value] = 0;
            });

            var datasets = [];

            angular.forEach(raw.values, function (series_data, index) {
                var ttemp_values = angular.copy(temp_values);
                angular.forEach(series_data["data"], function (y, index) {
                    ttemp_values[y["dt"]] = y["count"];

                });
                var series = {"seriesname": series_data["_id"], "data": []};
                for (var key in ttemp_values) {
                    if (ttemp_values.hasOwnProperty(key)) {
                        series.data.push({"value": ttemp_values[key]});
                    }
                }
                datasets.push(series)
            });
            
            $scope.dataSource.dataset = datasets;
            $scope.dataSource.categories = [{"category": category}];
        };


        var get_bar_chart = function (data) {
            $scope.chartType = "bar2d";
            $scope.dataSource.chart = {
                "theme": "fint",
                "caption": $scope.analytics_meta.type,
                "exportEnabled": "1"
            };
            map_pie_chart_data(data.data);
            return true;

        };

        var get_line_graph = function (data) {
            $scope.chartType = "zoomline";
            $scope.dataSource.chart = {
                "drawAnchors": false,
                "labelStep": 6,
                "slantLabels": true,
                "showValues": "0",
                "theme": "fint",
                "caption": $scope.analytics_meta.type,
                "exportEnabled": "1"
            };
            map_line_data(data.data);
            return true;
        };

         var get_time_graph = function (data) {
            $scope.chartType = "zoomline";
            $scope.dataSource.chart = {
                "drawAnchors": false,
                "labelStep": 6,
                "slantLabels": true,
                "showValues": "0",
                "theme": "fint",
                "caption": $scope.analytics_meta.type,
                "exportEnabled": "1"
            };
            map_time_data(data.data);
            return true;
        };

        var get_pie_chart = function (data) {
            $scope.chartType = "doughnut2d";
            $scope.dataSource.chart = {
                "caption": $scope.analytics_meta.type,
                // "subCaption": "Los Angeles Topanga - Last month",
                "startingAngle": "310",
                "decimals": "0",
                "showLegend": "1",
                // "defaultCenterLabel": "Total revenue: $60K",
                // "centerLabel": "Revenue from $label: $value",
                "theme": "fint",
                "exportEnabled": "1"

            };

            map_pie_chart_data(data.data);
            return true;
        };


    }]);


// $scope.chart_options = {
//     "drawAnchors": false,
//     "labelStep": 6,
//     "slantLabels": true,
//     // "caption": "Sales - 2015",
//     // "captionFontSize": "30",
//     // "captionFontBold": "0",
//     // "captionPadding": "18",
//     // "baseFontSize": "14",
//     // "baseFontColor": "#e0e4e6",
//     // "baseFont": "Roboto Slab",
//     // "subcaptionFontBold": "0",
//     // "outCnvBaseFontSize": "12",
//     "canvasBgColor": "#000000",
//     "showValues": "0",
//     // "numberPrefix": "$",
//     // "showBorder": "0",
//     // "showShadow": "0",
//     // "showHoverEffect": "1",
//     // "canvasBgAlpha": "0",
//     // "paletteColors": "#00AEF5, #4EE29B",
//     // "bgColor": "#293C47",
//     // "bgAlpha": "93",
//     // "showAlternateHGridColor": "0",
//     // "showCanvasBorder": "0",
//     //
//     // // line and anchor customizations
//     // "lineThickness": "4.5",
//     // "anchorRadius": "5",
//     // "anchorBorderThickness": "3",
//     // "anchorTrackingRadius": "18",
//     //
//     // // div line cosmetics
//     // "divlineAlpha": "50",
//     // "divlineColor": "#858585",
//     // "divlineThickness": "0.5",
//     // "divLineIsDashed": "0",
//     // "divLineGapLen": "2",
//     //
//     // // axes customizations
//     // "showXAxisLine": "1",
//     // "xAxisLineThickness": "1",
//     // "xAxisLineColor": "#cdcdcd",
//     // "xAxisNameFontColor": "#8d8d8d",
//     // "yAxisNameFontColor": "#8d8d8d",
//     //
//     // // legend customizations
//     // "legendBgAlpha": "0",
//     // "legendItemFontColor": "#e0e4e6",
//     // "legendBorderThickness": "0",
//     // "legendShadow": "0",
//     // "drawCustomLegendIcon": "1",
//     // "legendPadding": "20",
//     // "legendItemFontSize": "16",
//     // "legendItemFontBold": "0",
//     //
//     // // tool tip customizations
//     // "toolTipColor": "#e0e4e6",
//     // "toolTipBorderColor": "#e0e4e6",
//     // "toolTipBorderThickness": "1.73",
//     // "toolTipBgColor": "#000000",
//     // "toolTipBgAlpha": "70",
//     // "toolTipBorderRadius": "4",
//     // "toolTipPadding": "13",
//     // "plotToolText": "<div>$seriesname <br> $label: $dataValue</div>"
// }