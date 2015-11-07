/**
 * Created by camil on 31.07.15.
 */
angular.module('player')
    .factory('SocketFactory', function () {
        /**
         * @name SocketRequests
         * @desc The Factory to be returned
         */
        var SocketRequests = {
            sendUser: sendUser,
            getAllSongs: getAllSongs,
            getPlaylist: getPlaylist,
            getAllPlaylists: getAllPlaylists,
            getMyPlaylists: getMyPlaylists,
            getUsersOnline: usersOnline,
            getLatestSongs: getLatestSongs,
            getLatestVotes: getLatestVotes
        };
        return SocketRequests

        function sendUser(socket, username) {
            socket.send({
                    action: 'get_username',
                    username: username
                }
            );
        };

        function getAllSongs(socket) {
            socket.send({
                action: 'track_list',

            });
        };

        function getPlaylist(socket, id) {
            socket.send({
                action: 'get_playlist',
                playlist: id
            });
        };

        function getAllPlaylists(socket) {
            socket.send({
                action: 'get_all_playlists'
            });
        };

        function getMyPlaylists(socket) {
            socket.send({
                action: 'users_playlists'
            });
        };

        function usersOnline(socket) {
            socket.send({
                action: 'users_online',
                send: true
            });
        };

        function getLatestSongs(socket) {
            socket.send({
                    action: 'latest_songs',
                }
            );
        };

        function getLatestVotes(socket) {
            socket.send({
                    action: 'latest_votes',
                }
            );
        };

    });