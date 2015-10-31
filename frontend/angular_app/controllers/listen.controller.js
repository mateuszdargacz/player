/**
 * Created by camil on 28.07.15.
 */

angular.module('player')
    .controller('ListenController'
    , function ($state,
                $scope,
                $location,
                $stateParams,
                $sce,
                AuthenticationFactory,
                SocketFactory,
                backendEndpoint,
                backendPort) {
        $scope.playlist = false;
        $scope.clickeduser = false;
        $scope.backendurl = 'http://' + backendEndpoint + ':' + backendPort;

        var disconected = false;
        var voted = false;
        var socket;
        var timer;
        var currenttime = 0;
        var duration = 0;
        var end = false;
        $scope.showTitles = true;
        $scope.isplaying = false;
        $scope.currenttrack = "";
        $scope.muted = false;
        $scope.volume = 1;
        $scope.progress = 0;
        $scope.YTlink = "";
        var YTplayer;
        var audio = null;
        var SCwidget;
        var SCend = false;

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
        }

        $scope.disconnect = function () {
            disconected = true;
            if (socket) {
                socket.disconnect();
            }
        }

        $scope.searchsongs = function () {
            $location.url('/allsongs/' + $scope.searchterm);
        };

        $scope.showbar = function () {
            $scope.showTitles = false;
            setTimeout(function () {
                $scope.showTitles = true;
                $scope.$apply();
            }, 300)
        }

        $scope.main = function () {
            $scope.disconnect();
            $location.url('/index');
        }

        $scope.userSelected = function (user) {
            if ($scope.clickeduser === user) {
                $scope.clickeduser = false;
            }
            else {
                $scope.clickeduser = user;
            }
        }

        $scope.upvote = function (track) {
            voted = true;
            socket.send({
                action: 'up_vote',
                playlist: $stateParams.id,
                track: track.id
            });
        }

        $scope.downvote = function (track) {
            voted = true;
            socket.send({
                action: 'down_vote',
                playlist: $stateParams.id,
                track: track.id
            });
        }

        $scope.play = function () {
            if (!$scope.isplaying && !end) {
                if ($scope.currenttrack.type == 'file') {
                    audio.play();
                    audio.volume = $scope.volume;
                    if (!timer) {
                        timerFunction();
                    }
                }
                else if ($scope.currenttrack.type == 'youtube') {
                    if (!YTplayer) {
                        YTplayer = new YT.Player('YTplayer', {
                            events: {
                                // call this function when player is ready to use
                                'onReady': onPlayerReady
                            }
                        });
                    }
                    else {
                        YTplayer.playVideo();
                        if (!timer) {
                            timerFunction();
                        }
                    }
                }
                else if ($scope.currenttrack.type == 'soundcloud') {
                    if (!SCwidget) {
                        SCwidget = SC.Widget(document.getElementById('SCplayer'));
                    }
                    setTimeout(function () {
                        SCwidget.play();
                        if (!timer) {
                            timerFunction();
                        }
                    }, 2000);

                }
                socket.send({
                    action: 'playing_now',
                    playlist: $stateParams.id,
                    track: $scope.currenttrack.id
                });
                $scope.isplaying = true;

            }
            return false;
        }

        $scope.pause = function () {
            if ($scope.isplaying) {
                if ($scope.currenttrack.type == 'file') {
                    audio.pause();
                }
                else if ($scope.currenttrack.type == 'youtube') {
                    YTplayer.pauseVideo();
                }
                else if ($scope.currenttrack.type == 'soundcloud') {
                    SCwidget.pause();
                }
                $scope.isplaying = false;
                if (timer) {
                    clearInterval(timer);
                    timer = null;
                }
            }
            return false;
        }

        $scope.nexttrack = function () {
            if ($scope.isplaying) {
                if ($scope.currenttrack.type == 'file') {
                    audio.pause();
                }
                else if ($scope.currenttrack.type == 'youtube') {
                    YTplayer.pauseVideo();
                }
                else if ($scope.currenttrack.type == 'soundcloud') {
                    SCwidget.pause();
                }
                if (timer) {
                    clearInterval(timer);
                    timer = null;
                }
                $scope.isplaying = false;
                played();
                choosetrack();
                setTimeout(function () {
                    $scope.play();
                    SCwidget.setVolume($scope.volume);
                }, 2000);
            }
            else {
                if (timer) {
                    clearInterval(timer);
                    timer = null;
                }
                played();
            }
        }

        $scope.mute = function () {
            if ($scope.muted) {
                if ($scope.isplaying) {
                    if ($scope.currenttrack.type == 'file') {
                        audio.muted = false;
                    }
                    else if ($scope.currenttrack.type == 'youtube') {
                        YTplayer.unMute();
                        YTplayer.setVolume(100);
                    }
                    else if ($scope.currenttrack.type == 'soundcloud') {
                        SCwidget.setVolume(1);
                    }
                }
                $scope.muted = false;
                $scope.volume = 1;
            }
            else {
                if ($scope.isplaying) {
                    if ($scope.currenttrack.type == 'file') {
                        audio.muted = true;
                    }
                    else if ($scope.currenttrack.type == 'youtube') {
                        YTplayer.setVolume(0);
                        YTplayer.mute();
                    }
                    else if ($scope.currenttrack.type == 'soundcloud') {
                        SCwidget.setVolume(0);
                    }
                }
                $scope.muted = true;
                $scope.volume = 0;
            }
            socket.send({
                action: 'set_volume',
                playlist: $stateParams.id,
                volume: $scope.volume
            });
        }

        $scope.changeVolume = function ($event) {
            if ($scope.isplaying && !$scope.muted) {
                var value = ($event.layerX - angular.element($event.target).prop('offsetLeft')) / 110;
                if ($scope.currenttrack.type == 'file') {
                    audio.volume = value;
                }
                else if ($scope.currenttrack.type == 'youtube') {
                    YTplayer.setVolume(100 * value);
                }
                else if ($scope.currenttrack.type == 'soundcloud') {
                    SCwidget.setVolume(value);

                }
                $scope.volume = value;
                socket.send({
                    action: 'set_volume',
                    playlist: $stateParams.id,
                    volume: $scope.volume
                });
            }
            else if (!$scope.isplaying) {
                var value = ($event.layerX - angular.element($event.target).prop('offsetLeft')) / 110;
                $scope.volume = value;
                socket.send({
                    action: 'set_volume',
                    playlist: $stateParams.id,
                    volume: $scope.volume
                });

            }
        }

        var timerFunction = function () {
            timer = setInterval(function () {
                if ($scope.currenttrack.type == 'file') {
                    timeSec = Math.round(audio.currentTime % 60);
                    timeMin = Math.floor(audio.currentTime / 60);
                    durationSec = Math.round(audio.duration % 60);
                    durationMin = Math.floor(audio.duration / 60);

                    $scope.formattedTime = formatTime(timeSec, timeMin, durationSec, durationMin);
                    $scope.progress = audio.currentTime * 100 / audio.duration;

                    if (audio.ended) {
                        clearInterval(timer);
                        timer = null;
                        $scope.isplaying = false;
                        played();
                        choosetrack();
                        $scope.play();
                    }
                }
                else if ($scope.currenttrack.type == 'youtube') {
                    timeSec = Math.round(YTplayer.getCurrentTime() % 60);
                    timeMin = Math.floor(YTplayer.getCurrentTime() / 60);
                    durationSec = Math.round(YTplayer.getDuration() % 60);
                    durationMin = Math.floor(YTplayer.getDuration() / 60);
                    $scope.formattedTime = formatTime(timeSec, timeMin, durationSec, durationMin);
                    $scope.progress = YTplayer.getCurrentTime() * 100 / YTplayer.getDuration();

                    if (YTplayer.getPlayerState() == 0) {
                        clearInterval(timer);
                        timer = null;
                        $scope.isplaying = false;
                        played();
                        choosetrack();
                        $scope.play();
                        YTplayer.setVolume(100 * $scope.volume);
                    }
                }
                else if ($scope.currenttrack.type == 'soundcloud') {
                    SCwidget.isPaused(function (p) {
                        if (p && $scope.isplaying && !SCend) {
                            SCend = true;
                            clearInterval(timer);
                            timer = null;
                            $scope.isplaying = false;
                            played();
                            choosetrack();
                            setTimeout(function () {
                                $scope.play();
                                SCwidget.setVolume($scope.volume);
                            }, 2000);

                        }
                    });
                    SCwidget.getDuration(function (d) {
                            duration = d / 1000;
                        }
                    );
                    SCwidget.getPosition(function (p) {
                        currenttime = p / 1000;
                        if (currenttime > 1) {
                            SCend = false;
                        }
                    });
                    timeSec = Math.round(currenttime % 60);
                    timeMin = Math.floor(currenttime / 60);
                    durationSec = Math.round(duration % 60);
                    durationMin = Math.floor(duration / 60);
                    $scope.formattedTime = formatTime(timeSec, timeMin, durationSec, durationMin);
                    $scope.progress = currenttime * 100 / duration;
                }
                $scope.$apply();
            }, 500);
        }

        var formatTime = function (timeSec, timeMin, durationSec, durationMin) {
            if (timeSec < 10) {
                timeSec = "0" + timeSec;
            }
            if (durationSec < 10) {
                durationSec = "0" + durationSec;
            }
            return (timeMin + ":" + timeSec + "/" + durationMin + ":" + durationSec);
        }

        var choosetrack = function () {
            if (!$scope.isplaying) {
                end = true;
                for (var i = 0; i < $scope.playlist.track_list.length; ++i) {
                    if (!$scope.playlist.track_list[i].was_played_today) {
                        $scope.currenttrack = $scope.playlist.track_list[i];
                        end = false;
                        break;
                    }
                }
                if (!end) {
                    if ($scope.currenttrack.type == 'file') {
                        audio = new Audio('http://' + backendEndpoint + ':' + backendPort + $scope.currenttrack.file);
                    }
                    else if ($scope.currenttrack.type == 'youtube') {
                        var link = $scope.currenttrack.link.toString();
                        var videoId = link.split('v=')[1];
                        var ampersandPosition = videoId.indexOf('&');
                        if (ampersandPosition != -1) {
                            videoId = videoId.substring(0, ampersandPosition);
                        }
                        $scope.YTlink = "https://www.youtube.com/embed/" + videoId + "?enablejsapi=1";
                    }
                    else if ($scope.currenttrack.type == 'soundcloud') {
                        $scope.SClink = 'http://w.soundcloud.com/player/?url=' + $scope.currenttrack.link.toString() + '&show_artwork=false&liking=false&sharing=false&auto_play=false';
                    }
                }
            }
        }

        var played = function () {
            for (var i = 0; i < $scope.playlist.track_list.length; ++i) {
                if ($scope.currenttrack.id === $scope.playlist.track_list[i].id) {
                    $scope.playlist.track_list[i].was_played_today = true;
                }
            }
            socket.send({
                    action: 'was_played',
                    playlist: $scope.playlist.id,
                    track: $scope.currenttrack.id
                }
            );
        }

        angular.element(document).ready(function () {
            // Inject YouTube API script
            var tag = document.createElement('script');
            tag.src = "//www.youtube.com/player_api";
            document.body.appendChild(tag);
            var firstScriptTag = document.getElementsByTagName('script')[0];
            firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);
        });


        function onPlayerReady(event) {
            YTplayer.playVideo();
            YTplayer.setVolume(100 * $scope.volume);
            if (!timer) {
                timerFunction();
            }

        };

        var checkOnline = function () {
            if ($scope.followers && $scope.usersOnline) {
                for (var f = 0; f < $scope.followers.length; ++f) {
                    for (var u = 0; u < $scope.usersOnline.length; ++u) {
                        if ($scope.followers[f].id === $scope.usersOnline[u].id) {
                            $scope.followers[f].online = true;
                            break;
                        }
                        else {
                            $scope.followers[f].online = false;
                        }
                    }
                }
            }
        };

        var messaged = function (data) {
            switch (data.action) {
                case 'get_playlist':
                    if (data.text.id == $stateParams.id) {
                        if (voted || !$scope.playlist) {
                            $scope.votesLeft = data.votes_left;
                        }
                        $scope.followers = data.followers;
                        $scope.playlist = data.text;
                        $scope.playlist.track_list.sort(function (a, b) {
                            return parseInt(b.total_relative_votes) - parseInt(a.total_relative_votes);
                        })

                        $scope.$digest();
                        checkOnline();
                        if ($scope.clickeduser) {
                            for (var u = 0; u < $scope.followers.length; ++u) {
                                if ($scope.followers[u].id === $scope.clickeduser.id) {
                                    $scope.clickeduser = $scope.followers[u];
                                }
                            }
                        }
                        $scope.$digest()
                        choosetrack();
                    }
                    break;
                case 'users_online':
                    $scope.usersOnline = data.users;
                    $scope.$digest();
                    checkOnline();
                    break;
                case 'users_playlists':
                    $scope.myplaylists = data.text;
                    $scope.$digest();
                    break;
                case 'set_volume':
                    if (data.playlist === $stateParams.id) {
                        $scope.volume = data.volume;
                        $scope.muted = $scope.volume === 0;
                        if ($scope.isplaying) {
                            if ($scope.currenttrack.type == 'file') {
                                audio.volume = $scope.volume;
                            }
                            else if ($scope.currenttrack.type == 'youtube') {
                                YTplayer.setVolume(100 * $scope.volume);
                            }
                            else if ($scope.currenttrack.type == 'soundcloud') {
                                SCwidget.setVolume($scope.volume);

                            }
                        }
                        $scope.$digest();
                    }
                    break;
                case 'playing_now':
                    if (data.playlist === $stateParams.id) {
                        for (var t = 0; t < $scope.playlist.track_list.length; ++t) {
                            if ($scope.playlist.track_list[t].id == data.track) {
                                $scope.playingTrack = $scope.playlist.track_list[t];
                                break;
                            }
                        }
                        $scope.$apply();
                    }
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
            SocketFactory.getPlaylist(socket, $stateParams.id);
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

        $scope.trustSrc = function (src) {
            return $sce.trustAsResourceUrl(src);
        }

    }
)
;
