var myApp = angular.module('GDOSlide', ['restangular', 'ngResource', 'ui.bootstrap', 'ngRoute'])

    .config(function (RestangularProvider) {
        RestangularProvider.setBaseUrl('/API');
        RestangularProvider.setFullResponse(true);
        RestangularProvider.setDefaultHeaders({Authorization: "Basic Y3BzMTVfYWRtaW46c2VjcmV0"});
    })

    .controller('GDOSlideCtrl', ["$scope", "$window", "$interval", "Restangular", function ($scope, $window, $interval, Restangular) {

        $scope.gdoWidth = 16;
        $scope.gdoHeight = 4;

        $scope.gdo_nodes = [];
        $scope.selected_nodes = [];
        $scope.sections = [];
        $scope.savedSections = [];
        $scope.currentSlide = {"description":null, "sections":[], "description":"MConsole_" + new Date().toLocaleString()}
        $scope.getDataSets = function () {
            return Restangular.all('dataset').getList().$object
        };
       $scope.getAnalytics = function(dataSetId) {
            return Restangular.one("dataset", dataSetId).getList('analytics').$object
        };

        $scope.dataSets = $scope.getDataSets();
        $scope.selectedDataSet = null;
        $scope.slides = [{"description": "Test", "nSections": 10}];
        
        $scope.init = function () {
            for (var j = 0; j < $scope.gdoHeight; ++j) {
                var row = [];
                for (var i = 0; i < $scope.gdoWidth; ++i) {
                    row.push({"row": j, "col": i, "isSelected": false, "sectionId": -1, "section": null})
                }
                $scope.gdo_nodes.push(row);
            }
        };
        
        $scope.saveSection = function(){
            $scope.currentSlide.sections.push($scope.selectedSection)
            $scope.selectedSection = null
        };
        
        $scope.createSection = function () {

            var rowStart = Math.min.apply(Math,$scope.selected_nodes.map(function(o){return o.row;}));
            var rowEnd = Math.max.apply(Math,$scope.selected_nodes.map(function(o){return o.row;}));
            var colStart = Math.min.apply(Math,$scope.selected_nodes.map(function(o){return o.col;}));
            var colEnd = Math.max.apply(Math,$scope.selected_nodes.map(function(o){return o.col;}));
            var newSection = {"id": $scope.sections.length, "nodes":[], "rowStart": rowStart, "rowEnd": rowEnd, "colStart": colStart, "colEnd": colEnd};
            for (var i = 0; i < $scope.selected_nodes.length; ++i) {
                $scope.selected_nodes[i].sectionId = newSection.id;
                $scope.selected_nodes[i].isSelected = false;
                // $scope.selected_nodes[i].section = newSection;

            }
            newSection.nodes = $scope.selected_nodes;
            $scope.sections.push(newSection);
            $scope.selectedSection = newSection;
            $scope.selected_nodes = [];
            console.log($scope.sections);
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
        
        $scope.selectDataSet = function(dataSet){
            $scope.selectedDataSet = dataSet;
            $scope.selectedSection.dataSetId = dataSet.id;
            $scope.selectedDataSet.possibleAnalytics = $scope.getAnalytics(dataSet.id);
        };

        $scope.selectAnalytics = function(analytics){
            $scope.selectedSection.analyticsId = analytics.id;

        };
        
        $scope.createSlide = function(){
            console.log($scope.currentSlide)
            Restangular.all('slide').post($scope.currentSlide).then(function(){
                console.log("slide creation requested");
                $scope.currentSlide = {"description":null, "sections":[], "description":"MConsole_" + new Date().toLocaleString()}
                $scope.slides = $scope.getSlides();
                }, function() {
                    console.log("Error requesting dataset");
                });
        }

        $scope.getSlides = function(){
            return  Restangular.all('slide').getList().$object
        }

        $scope.slides = $scope.getSlides();

        $scope.print = function(){
            console.log($scope.slides)
        }

        $scope.delete = function(slide){
            Restangular.one("slide", slide.id).remove().then(function () {
                $scope.slides = $scope.getSlides();
            });

        }

    }]);