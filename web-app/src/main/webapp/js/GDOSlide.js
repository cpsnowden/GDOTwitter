var myApp = angular.module('GDOSlide', ['restangular', 'ngResource', 'ui.bootstrap', 'ngRoute'])

    .config(function (RestangularProvider) {
        RestangularProvider.setBaseUrl('/API');
        // RestangularProvider.setFullResponse(true);
        RestangularProvider.setDefaultHeaders({Authorization: "Basic Y3BzMTVfYWRtaW46c2VjcmV0"});
    })

    .controller('GDOSlideCtrl', ["$scope", "$window", "$interval", "Restangular", function ($scope, $window, $interval, Restangular) {

        $scope.gdoWidth = 16;
        $scope.gdoHeight = 4;

        $scope.gdo_nodes = [];
        $scope.selected_nodes = [];
        $scope.sections = [];
        $scope.savedSections = [];
        $scope.currentSlide = {
            "sections": [],
            "description": "MConsole_" + new Date().toLocaleString()
        };
        $scope.getDataSets = function () {
            return Restangular.all('dataset').getList().$object
        };
        $scope.getAnalytics = function (dataSetId) {
            return Restangular.one("dataset", dataSetId).getList('analytics').$object
        };

        $scope.dataSets = $scope.getDataSets();

        $scope.findDataSet = function (id) {
            for (var i = 0; i < $scope.dataSets.length; ++i) {
                if ($scope.dataSets[i].id == id) {
                    return $scope.dataSets[i]
                }
            }
            return null;
        };

        $scope.selectedDataSet = null;
        $scope.slides = [{"description": "Test", "nSections": 10}];

        $scope.init = function () {
            $scope.resetNodes();
        };

        $scope.resetNodes = function () {
            $scope.gdo_nodes = [];
            for (var j = 0; j < $scope.gdoHeight; ++j) {
                var row = [];
                for (var i = 0; i < $scope.gdoWidth; ++i) {
                    row.push({"row": j, "col": i, "isSelected": false, "sectionId": -1, "section": null})
                }
                $scope.gdo_nodes.push(row);
            }
        };

        $scope.canCreateSection = function () {
            if ($scope.selected_nodes.length <= 0) {
                return false;
            }
            var rowStart = Math.min.apply(Math, $scope.selected_nodes.map(function (o) {
                return o.row;
            }));
            var rowEnd = Math.max.apply(Math, $scope.selected_nodes.map(function (o) {
                return o.row;
            }));
            var colStart = Math.min.apply(Math, $scope.selected_nodes.map(function (o) {
                return o.col;
            }));
            var colEnd = Math.max.apply(Math, $scope.selected_nodes.map(function (o) {
                return o.col;
            }));

            for (var r = rowStart; r <= rowEnd; ++r) {
                for (var c = colStart; c <= colEnd; ++c) {
                    if ($scope.gdo_nodes[r][c].sectionId >= 0) {
                        return false;
                    }
                }
            }
            return true;
        };

        $scope.canCreateSlide = function () {
            if ($scope.currentSlide.sections.length <= 0 ||
                $scope.currentSlide.description == "") {
                return false;
            }
            for (var i = 0; i < $scope.currentSlide.sections.length; ++i) {
                if ($scope.currentSlide.sections[i].dataSetId == undefined ||
                    $scope.currentSlide.sections[i].analyticsId == undefined) {
                    return false;
                }
            }
            return true;
        };

        var getId = function (row, col) {
            return row * $scope.width + col;
        };


        $scope.createSection = function () {
            var rowStart = Math.min.apply(Math, $scope.selected_nodes.map(function (o) {
                return o.row;
            }));
            var rowEnd = Math.max.apply(Math, $scope.selected_nodes.map(function (o) {
                return o.row;
            }));
            var colStart = Math.min.apply(Math, $scope.selected_nodes.map(function (o) {
                return o.col;
            }));
            var colEnd = Math.max.apply(Math, $scope.selected_nodes.map(function (o) {
                return o.col;
            }));
            var newSection = {
                "id": $scope.sections.length,
                "nodes": [],
                "rowStart": rowStart,
                "rowEnd": rowEnd,
                "colStart": colStart,
                "colEnd": colEnd
            };
            for (var r = rowStart; r <= rowEnd; ++r) {
                for (var c = colStart; c <= colEnd; ++c) {
                    $scope.gdo_nodes[r][c].sectionId = newSection.id;
                    $scope.gdo_nodes[r][c].isSelected = false;
                    newSection.nodes.push($scope.gdo_nodes[r][c])
                }
            }
            $scope.selected_nodes = [];
            $scope.currentSlide.sections.push(newSection);
        };


        $scope.selectNode = function (node) {
            if (node.sectionId == -1) {
                var index = $scope.selected_nodes.indexOf(node);
                if (index != -1) {
                    $scope.selected_nodes.splice(index, 1);
                    node.isSelected = false;
                } else {
                    $scope.selected_nodes.push(node);
                    node.isSelected = true;
                }
            }
        };

        $scope.selectDataSet = function (section, dataSet) {
            section.dataSetId = dataSet.id;
            section.dataset = Restangular.stripRestangular(dataSet);
            dataSet.possibleAnalytics = $scope.getAnalytics(dataSet.id);
        };

        $scope.selectAnalytics = function (section, analytics) {
            section.analyticsId = analytics.id;
            section.analytics = Restangular.stripRestangular(analytics);
        };

        $scope.deleteSection = function (section) {
            var index = $scope.currentSlide.sections.indexOf(section);
            for (var i = 0; i < section.nodes; ++i) {
                section.nodes[i].sectionId = -1
            }
            $scope.currentSlide.sections.splice(index, 1);

        };

        $scope.createSlide = function () {
            // Restangular.stripRestangular($scope.currentSlide)
            console.log($scope.currentSlide);


            Restangular.all('slide').post($scope.currentSlide).then(function () {
                console.log("Slide creation requested");
                $scope.currentSlide = {
                    "sections": [],
                    "description": "MConsole_" + new Date().toLocaleString()
                };
                $scope.resetNodes();
                $scope.slides = $scope.getSlides();
            }, function () {
                console.log("Error requesting dataset");
            });
        };

        $scope.getSlides = function () {
            return Restangular.all('slide').getList().$object
        };

        $scope.slides = $scope.getSlides();

        $scope.print = function () {
            console.log($scope.slides)
        };

        $scope.delete = function (slide) {
            Restangular.one("slide", slide.id).remove().then(function () {
                $scope.slides = $scope.getSlides();
            });

        }

    }]);