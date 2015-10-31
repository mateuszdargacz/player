/**
 * Created by camil on 11.08.15.
 */

angular.module('player')
    .controller('NewPlaylistController',
    function ($state,
              $scope,
              $location,
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

        $scope.searchsongs = function () {
            $location.url('/allsongs/' + $scope.searchterm);
        };

        $scope.showbar = function () {
            $scope.showTitles = false;
            setTimeout(function () {
                $scope.showTitles = true;
                $scope.$apply();
            }, 300)
        };

        $scope.send = function (name) {
            if (name) {
                socket.send({
                        action: 'create_playlist',
                        name: name
                    }
                );
                $location.url('/index');
            }

        };

        var socket;

        var messaged = function (data) {
            switch (data.action) {
                case 'latest_songs':
                    $scope.newSongs = data.songs
                    $scope.$digest();
                    break;
                case 'latest_votes':
                    $scope.newVotes = data.votes
                    $scope.$digest();
                    break;
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
