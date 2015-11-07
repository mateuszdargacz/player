/**
 * Created by camil on 22.07.15.
 */

angular.module('player')
    .controller('LoginController', function ($state, $scope, $location, AuthenticationFactory, backendEndpoint, backendPort) {

        /**
         * @name activate
         * @desc Actions to be performed when this controller is instantiated
         */
        var activate = function () {
            // If the user is authenticated, they should not be here.
            if (AuthenticationFactory.isAuthenticated()) {
                $location.url('/listen');
            }
        };
        $scope.showIndicator = false;

        activate();

        var backendurl = 'http://' + backendEndpoint + ':' + backendPort;

        /**
         * @name login
         * @desc Log the user in
         */
        $scope.login = function () {
            if ($scope.email && $scope.password) {
                $scope.showIndicator = true;
                // HOTFIX insted of watcher it's show/hide
                $('button[type="submit"]').parent().attr('class', 'col-sm-9');
                AuthenticationFactory.login($scope.email, $scope.password, backendurl).then(check)

            }
        };

        var check = function () {
            $scope.errorCode = AuthenticationFactory.getErrorCode();
            // HOTFIX insted of watcher it's show/hide
            $('button[type="submit"]').parent().attr('class', 'col-sm-12');
            $scope.showIndicator = false;

        };

        $scope.signup = function () {
            $location.url('/signup');
        };


    }
)
;
