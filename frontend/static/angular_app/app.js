/**
 * Created by michal on 7/21/15.
 */
angular
    .module('player', [
        'ui.router',
        'ngCookies',
        'angularUtils.directives.dirPagination',
        'ngSanitize'
    ])
    .constant('path', {
        images: "/static/images/",
        views: "/static/angular_app/templates",
        ctrls: "/static/angular_app/templates/ctrls",
        tmpl: "/static/MusikTemplate"
    })
    .constant('backendEndpoint', '37.187.58.217')
    .constant('backendPort', '9001')
    //.constant('backendEndpoint', '127.0.0.1')
    //.constant('backendPort', '9000')
    .config(function ($stateProvider, $urlRouterProvider, $httpProvider, $animateProvider, path) {
        $urlRouterProvider.otherwise("/index");
        $urlRouterProvider.when('', '/index');

        $stateProvider
            .state('signin', {
                url: "/signin",
                templateUrl: path.tmpl + '/signin.html',
                controller: 'LoginController'
            }).state('signup', {
                url: "/signup",
                templateUrl: path.tmpl + '/signup.html',
                controller: 'RegisterController'
            }).state('listen_playlist', {
                url: "/listen/:id",
                templateUrl: path.tmpl + '/listen.html',
                controller: 'ListenController'
            }).state('listen', {
                url: "/listen",
                templateUrl: path.tmpl + '/listen.html',
                controller: 'ListenController'
            }).state('index', {
                url: "/index",
                templateUrl: path.tmpl + '/main.html',
                controller: 'IndexController'
            }).state('add', {
                url: "/add",
                templateUrl: path.tmpl + '/add.html',
                controller: 'AddController'

            }).state('allsongs', {
                url: "/allsongs",
                templateUrl: path.tmpl + '/allsongs.html',
                controller: 'AllSongsController'
            }).state('allsongssearch', {
                url: "/allsongs/:searchterm",
                templateUrl: path.tmpl + '/allsongs.html',
                controller: 'AllSongsController'
            }).state('newplaylist', {
                url: "/newplaylist",
                templateUrl: path.tmpl + '/newplaylist.html',
                controller: 'NewPlaylistController'
            }).state('allplaylists', {
                url: "/allplaylists",
                templateUrl: path.tmpl + '/allplaylists.html',
                controller: 'AllPlaylistsController'
            }).state('chat', {
                url: "/chat",
                templateUrl: path.tmpl + '/chat.html',
                controller: 'ChatController'
            });

    })
    .run(function run($http, $rootScope, $location) {
        (function () {

            // Override the SocketIO constructor to provide a default
            // value for the port, which is added to os.environ in the
            // runserver_socketio management command.
            var prototype = io.Socket.prototype;
            io.Socket = function (host, options) {
                options = options || {};
                options.port = options.port || 9000;
                return prototype.constructor.call(this, host, options);
            };

            // We need to reassign all members for the above to work.
            for (var name in prototype) {
                io.Socket.prototype[name] = prototype[name];
            }

            // Arrays are transferred as individual messages in Socket.IO,
            // so we put them into an object and check for the __array__
            // message on the server to handle them consistently.
            var send = io.Socket.prototype.send;
            io.Socket.prototype.send = function (data) {
                if (data.constructor == Array) {
                    channel = data[0] == '__subscribe__' || data[0] == '__unsubscribe__';
                    if (!channel) {
                        data = ['__array__', data];
                    }
                }
                return send.call(this, data);
            };

            // Set up the subscription methods.
            io.Socket.prototype.subscribe = function (channel) {
                this.send(['__subscribe__', channel]);
                return this;
            };
            io.Socket.prototype.unsubscribe = function (channel) {
                this.send(['__unsubscribe__', channel]);
                return this;
            };
            $http.defaults.xsrfHeaderName = 'X-CSRFToken';
            $http.defaults.xsrfCookieName = 'csrftoken';


        })();


    })

;