angular.module('player')
    .controller('ChatController', function ($state, $scope, $location, AuthenticationFactory, SocketFactory,
                                            backendEndpoint, backendPort, ChatFactory) {
        $scope.backendurl = 'http://' + backendEndpoint + ':' + backendPort;
        $scope.showTitles = true;
        var socket, heightDivStart, heightDivPrev, goToPx, scroll, heightLastMessage1, heightLastMessage2;
        var heightLastMessage, heightChatSendMsg, heightDivNav, heightDivHeader, audio;

        $scope.showbar = function () {
            $scope.showTitles = false;
            setTimeout(function () {
                $scope.showTitles = true;
                $scope.$apply();
            }, 300)
        }

        var scrollAnimate = function () {
            $("#chatboxall").animate({scrollTop: $('#chatboxall')[0].scrollHeight}, 1000);

        }

        var getPositionScroll = function () {
            heightChatSendMsg = $("#chatform").height();
            heightDivHeader = $(".bg-white-only").height();
            heightDivNav = $(".nav").height();

            if (scroll > (heightDivStart - heightLastMessage - heightChatSendMsg - heightDivHeader - heightDivNav - 401)) {
                scrollAnimate();
            }
        };


        $scope.sendmessagefront = function () {

            if ($scope.chatboxsendnew) {
                socket.send({
                        action: 'new_message_front',
                        newmessage: $scope.chatboxsendnew

                    }
                );
                $scope.chatboxsendnew = "";
            }
        };

        var scrollOnTop = function () {
            var newtmp = $scope.chatComments.length;
            socket.send({
                    action: 'load_messages_previous',
                    lengthChatComment: newtmp
                }
            );
        };

        $('#comment_box').keypress(function (event) {
            // Check the keyCode and if the user pressed Enter (code = 13)
            if (event.keyCode == 13) {
                $scope.sendmessagefront();
                scrollAnimate();
            }
        });


        $("#chatboxall").scroll(function (event) {
            scroll = $('#chatboxall').scrollTop();
            heightDivStart = $("#chatboxall .tab-content").height();
            if (scroll === 0) {
                scrollOnTop();
            }

        });

        $scope.dateformattoday = function (vardate) {
            return ChatFactory.dateformattodayservice(vardate);
        }


        var newMsgSound = function (userNamePlay) {
            if (userNamePlay !== $scope.user.username) {
                audio.play();
            }

        };

        var checkAuthenticatedAccount = function () {
            if (!AuthenticationFactory.isAuthenticated()) {
                $location.url('/signin');
            }
            $scope.user = AuthenticationFactory.getAuthenticatedAccount();
        };
        checkAuthenticatedAccount();

        audio = new Audio('/static/MusikTemplate/sound/message.mp3');

        var connected = function () {
            socket.subscribe('chat');
            SocketFactory.sendUser(socket, $scope.user.username);
            SocketFactory.getUsersOnline(socket);
        };

        var messaged = function (data) {
            switch (data.action) {
                case 'users_online':
                    $scope.usersOnline = data.users;
                    $scope.$digest();
                    break;

                case 'chatBackEnd':
                    $scope.chatComments = data.chat_field;
                    $scope.$digest();
                    $('#chatboxall').scrollTop($('#chatboxall')[0].scrollHeight);
                    break;
                case 'chatBackEndOneMessage':
                    heightLastMessage1 = $("#chatboxall .tab-content").height();
                    $scope.chatComments.push(data.chat_field);
                    $scope.$digest();
                    heightLastMessage2 = $("#chatboxall .tab-content").height();
                    heightLastMessage = heightLastMessage2 - heightLastMessage1;
                    getPositionScroll();
                    newMsgSound(data.chat_field.username);
                    break;
                case 'loadMessagePrevious':
                    $scope.chatComments = data.chat_field.concat($scope.chatComments);
                    $scope.$digest();
                    heightDivPrev = $("#chatboxall .tab-content").height();
                    goToPx = heightDivPrev - heightDivStart;
                    $("#chatboxall").scrollTo(goToPx);
                    break;
                default :
                    console.log(' No such action: ' + data.action);
            }
        };

        var start = function () {

            socket = new io.Socket(backendEndpoint);
            socket.connect();
            socket.on('connect', connected);
            socket.on('message', messaged);

        };

        start();
    });

$.fn.scrollTo = function (target, options, callback) {
    if (typeof options == 'function' && arguments.length == 2) {
        callback = options;
        options = target;
    }
    var settings = $.extend({
        scrollTarget: target,
        offsetTop: 50,
        duration: 50,
        easing: 'swing'
    }, options);
    return this.each(function () {
        var scrollPane = $(this);
        var scrollTarget = (typeof settings.scrollTarget == "number") ? settings.scrollTarget : $(settings.scrollTarget);
        var scrollY = (typeof scrollTarget == "number") ? scrollTarget : scrollTarget.offset().top + scrollPane.scrollTop() - parseInt(settings.offsetTop);
        scrollPane.animate({scrollTop: scrollY}, parseInt(settings.duration), settings.easing, function () {
            if (typeof callback == 'function') {
                callback.call(this);
            }
        });
    });
};

