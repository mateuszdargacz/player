/**
 * Created by camil on 22.07.15.
 */

angular.module('player')
    .controller('RegisterController', function ($location, $scope, AuthenticationFactory, backendEndpoint, backendPort) {

        $scope.email = "";
        $scope.password = "";
        $scope.username = "";

        $scope.register = function () {
            if ($scope.email && $scope.password && $scope.username) {
                var backendurl = 'http://' + backendEndpoint + ':' + backendPort;
                AuthenticationFactory.register($scope.email, $scope.password, $scope.username, backendurl).then(check);
            }
        };

        var check = function () {
            $scope.errorCode = AuthenticationFactory.getErrorCode();
        };

        $scope.signin = function () {
            $location.url('/signin');
        }

    });
