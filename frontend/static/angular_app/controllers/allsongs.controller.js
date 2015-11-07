/**
 * Created by camil on 12.08.15.
 */

angular.module('player')
    .controller('AllSongsController',
    function ($state,
              $scope,
              $location,
              $stateParams,
              AuthenticationFactory,
              SocketFactory,
              backendEndpoint,
              backendPort) {

        $scope.backendurl = 'http://' + backendEndpoint + ':' + backendPort;

        $scope.showTitles = true;
        $scope.status = 'Add song to playlist';
        var disconected = false;
        var check = function () {
            // If the user is authenticated, they should not be here.
            if (!AuthenticationFactory.isAuthenticated()) {
                $location.url('/signin');
            }
            $scope.user = AuthenticationFactory.getAuthenticatedAccount();
        }



        if ($stateParams.searchterm) {
            $scope.searchterm = $stateParams.searchterm;
        }

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

        $scope.change = function (song, checked) {
            if (!$scope.listOfChecked) {
                $scope.listOfChecked = [];
            }
            if (!checked) {
                $scope.listOfChecked.push(song.id);
            }
            else {
                var i = $scope.listOfChecked.indexOf(song.id);
                if (i > -1) {
                    $scope.listOfChecked.splice(i, 1);
                }
            }
        };

        $scope.send = function (chosenplaylist) {
            if (chosenplaylist && $scope.listOfChecked.length > 0) {
                var i = 0;
                sendTimer = setInterval(function () {
                    if (i >= $scope.listOfChecked.length) {
                        setTimeout(function () {
                            clearInterval(sendTimer);
                            $scope.disconnect();
                            $location.url('/index');
                            $scope.$apply();
                        }, 700);

                    }
                    else {
                        socket.send({
                            action: 'add_to_playlist',
                            track: $scope.listOfChecked[i],
                            playlist: chosenplaylist.id
                        });
                        i++;
                        $scope.status = "Successfully assigned " + i + " to " + chosenplaylist.name;
                        $scope.$apply();

                    }
                }, 200);
            }
        };

        var socket;

        var messaged = function (data) {
            switch (data.action) {
                case 'track_list':
                    $scope.allsongs = data.tracks;
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
            SocketFactory.getAllSongs(socket);
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
