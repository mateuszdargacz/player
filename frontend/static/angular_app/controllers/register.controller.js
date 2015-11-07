/**
 * Created by camil on 22.07.15.
 */

angular.module('player')
    .controller('RegisterController', function ($location, $scope, AuthenticationFactory, backendEndpoint, backendPort) {

        $scope.email = "";
        $scope.password = "";
        $scope.username = "";
        $scope.showIndicator = false;
        $scope.register = function () {
            if ($scope.email && $scope.password && $scope.username) {
                var backendurl = 'http://' + backendEndpoint + ':' + backendPort;
                $('button[type="submit"]').parent().attr('class', 'col-sm-9');
                $scope.showIndicator = true;
                AuthenticationFactory.register($scope.email, $scope.password, $scope.username, backendurl).then(check);
            }
        };

        var check = function () {
            $scope.errorCode = AuthenticationFactory.getErrorCode();
            $('button[type="submit"]').parent().attr('class', 'col-sm-12');
            $scope.showIndicator = false;
        };

        $scope.signin = function () {
            $location.url('/signin');
        }

    });
