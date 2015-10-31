/**
 * Created by camil on 11.08.15.
 */

angular.module('player')
    .controller('AddController',
    function ($state,
              $scope,
              $location,
              $http,
              AuthenticationFactory,
              SocketFactory,
              backendEndpoint,
              backendPort) {

        $scope.backendurl = 'http://' + backendEndpoint + ':' + backendPort;
        $scope.showTitles = true;
        var disconected = false;
        var check = function () {
            // If the user is authenticated, they should not be here.
            if (!AuthenticationFactory.isAuthenticated()) {
                $location.url('/signin');
            }
            $scope.user = AuthenticationFactory.getAuthenticatedAccount();
        }

        check();


        $scope.logout = function () {
            AuthenticationFactory.unauthenticate();
            $scope.disconnect();
            $location.url('/signin');
        };

        $scope.disconnect = function () {
            disconected = true;
            if (socket) {
                socket.disconnect();
            }
        };

        $scope.showbar = function () {
            $scope.showTitles = false;
            setTimeout(function () {
                $scope.showTitles = true;
                $scope.$apply();
            }, 300)
        };

        $scope.searchsongs = function () {
            $location.url('/allsongs/'+$scope.searchterm);
        };

        $scope.send = function () {
            return $http.post($scope.backendurl + '/api/v1/music/add/', {
                title: $scope.title,
                artist: $scope.artist,
                link: $scope.link,
                added_by: $scope.user.id,
                playlist: $scope.chosenplaylist.id

            }).then(sendSuccessFn, sendErrorFn);

        };

        sendSuccessFn = function (data, status, headers, config) {
            $scope.disconnect();
            $location.url('/index');
        };

        sendErrorFn = function (data, status, headers, config) {
            console.log("Error!!!");
        };

        var socket;

        var messaged = function (data) {
            switch (data.action) {
                case 'users_online':
                    $scope.usersOnline = data.users;
                    $scope.$digest();
                    break;
                case 'users_playlists':
                    $scope.myplaylists = data.text;
                    $scope.$digest();
                    break;
                default :
                    break;
            }
        };

       var reconnect = function () {
            if (!disconected) {
                socket = new io.Socket(backendEndpoint);
                socket.connect();
                socket.on('connect', connected);
                socket.on('message', messaged);
                socket.on('disconnect', reconnect);
                socket.timeout = 1000000000;
            }
        };

        var connected = function () {

            socket.subscribe('player');
            SocketFactory.sendUser(socket, $scope.user.username);
            SocketFactory.getUsersOnline(socket);
            SocketFactory.getMyPlaylists(socket);
        };

        var start = function () {
            socket = new io.Socket(backendEndpoint);
            socket.connect();
            socket.on('connect', connected);
            socket.on('message', messaged);
            socket.on('disconnect', reconnect);
            socket.timeout = 1000000000;
        };
        start();

    })
;
