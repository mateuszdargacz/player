/**
 * Created by camil on 29.07.15.
 */
angular.module('player')
    .directive("trackonlist", function () {
        return {
            restrict: 'E',
            templateUrl: 'angular_app/directives/trackOnList.html',
            replace: true,
            scope: {
                track: "=",
                upvote: "&",
                downvote: "&",
                votesleft: "=",
                backendurl: "=",
                user:"="

            }
        }
    }).directive("newsongpreview", function () {
        return {
            restrict: 'E',
            templateUrl: 'angular_app/directives/newSongPreview.html',
            replace: true,
            scope: {
                song: "=",
                backendurl: "="

            }
        }
    }).directive("indicator", function () {
        return {
            restrict: 'E',
            templateUrl: 'angular_app/directives/indicator.html',
            replace: true,
            scope: {
                showindicator: "="

            }
        }
    }).directive("useronindexpage", function () {
        return {
            restrict: 'E',
            templateUrl: 'angular_app/directives/userOnIndexPage.html',
            replace: true,
            scope: {
                user: "=",
                backendurl: "="

            }
        }
    }).directive("useronlistenpage", function () {
        return {
            restrict: 'E',
            templateUrl: 'angular_app/directives/userOnListenPage.html',
            replace: true,
            scope: {
                user: "=",
                backendurl: "="

            }
        }
    }).directive("uservotes", function () {
        return {
            restrict: 'E',
            templateUrl: 'angular_app/directives/userVotes.html',
            replace: true,
            scope: {
                clickeduser: "="

            }
        }
    }).directive("voteofuser", function () {
        return {
            restrict: 'E',
            templateUrl: 'angular_app/directives/voteOfUser.html',
            replace: true,
            scope: {
                clickeduser: "=",
                vote: "="
            }
        }
    }).directive("latestvote", function () {
        return {
            restrict: 'E',
            templateUrl: 'angular_app/directives/latestVote.html',
            replace: true,
            scope: {
                vote: "=",
                backendurl: "="
            }
        }
    }).directive("songtoplaylist", function () {
        return {
            restrict: 'E',
            templateUrl: 'angular_app/directives/songToPlaylist.html',
            replace: true,
            scope: {
                song: "=",
                myplaylists: "=",
                chosenplaylist: "=",
                change: "&",
                checked: "="
            }
        }
    }).directive("chatmessages", function () {
        return {
            restrict: 'E',
            templateUrl: 'angular_app/directives/chatMessage.html',
            replace: true,
            scope: {
                chatcomment: "=",
                backendurl: "=",
                dateformattoday: "&"

            }
        }
    });


