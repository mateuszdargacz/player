/**
 * Created by camil on 06.07.15.
 */


angular.module('player')
    .factory('AuthenticationFactory', function ($cookies, $http) {
        /**
         * @name Authentication
         * @desc The Factory to be returned
         */
        var Authentication = {
            getAuthenticatedAccount: getAuthenticatedAccount,
            isAuthenticated: isAuthenticated,
            login: login,
            logout: logout,
            getErrorCode: getErrorCode,
            register: register,
            setAuthenticatedAccount: setAuthenticatedAccount,
            unauthenticate: unauthenticate
        };

        return Authentication;

        ////////////////////
        var errorCode = false;

        function getErrorCode(){
            return errorCode
        }
        /**
         * @name login
         * @desc Try to log in with email `email` and password `password`
         * @param {string} email The email entered by the user
         * @param {string} password The password entered by the user
         * @returns {Promise}
         * @memberOf authentication.services
         */
        function login(email, password, backendurl) {

            return $http.post(backendurl+'/api/v1/auth/login/', {
                email: email, password: password
            }).then(loginSuccessFn, loginErrorFn);

            /**
             * @name loginSuccessFn
             * @desc Set the authenticated account and redirect to index
             */
            function loginSuccessFn(data, status, headers, config) {

                Authentication.setAuthenticatedAccount(data.data);
                window.location = '#/';

            }

            /**
             * @name loginErrorFn
             */
            function loginErrorFn(data, status, headers, config) {
                errorCode = data ? data.data ? data.data.message: 0:0;
            }
        }

        /**
         * @name logout
         * @desc Try to log the user out
         * @returns {Promise}
         * @memberOf authentication.services
         */
        function logout(backendurl) {
            return $http.post(backendurl + '/api/v1/auth/logout/')
                .then(logoutSuccessFn, logoutErrorFn);

            /**
             * @name logoutSuccessFn
             * @desc Unauthenticate and redirect to index with page reload
             */
            function logoutSuccessFn(data, status, headers, config) {
                Authentication.unauthenticate();

                window.location = '/';
            }

            /**
             * @name logoutErrorFn
             * @desc Log "Epic failure!" to the console
             */
            function logoutErrorFn(data, status, headers, config) {
                errorCode = data.data.message;
            }
        }


        /**
         * @name register
         * @desc Try to register a new user
         * @param {string} email The email entered by the user
         * @param {string} password The password entered by the user
         * @param {string} username The username entered by the user
         * @returns {Promise}
         * @memberOf authentication.services
         */
        function register(email, password, username, backendurl) {

            return $http.post(backendurl+'/api/v1/users/', {
                username: username,
                password: password,
                confirm_password: password,
                email: email

            }).then(registerSuccessFn, registerErrorFn);

            /**
             * @name registerSuccessFn
             * @desc Log the new user in
             */
            function registerSuccessFn(data, status, headers, config) {
                console.log("Registered");
                Authentication.login(email, password,backendurl);
            }

            /**
             * @name registerErrorFn
             * @desc Log "Epic failure!" to the console
             */
            function registerErrorFn(data, status, headers, config) {
                errorCode = data.data.message;
            }
        }

        /**
         * @name getAuthenticatedAccount
         * @desc Return the currently authenticated account
         * @returns {object|undefined} Account if authenticated, else `undefined`
         * @memberOf authentication.services
         */
        function getAuthenticatedAccount() {
            if (!$cookies.get('authenticatedAccount')) {
                return;
            }

            return JSON.parse($cookies.get('authenticatedAccount'));
        }

        /**
         * @name isAuthenticated
         * @desc Check if the current user is authenticated
         * @returns {boolean} True is user is authenticated, else false.
         * @memberOf authentication.services
         */
        function isAuthenticated() {
            return !!$cookies.get('authenticatedAccount');
        }

        /**
         * @name setAuthenticatedAccount
         * @desc Stringify the account object and store it in a cookie
         * @param {Object} user The account object to be stored
         * @returns {undefined}
         * @memberOf authentication.services
         */
        function setAuthenticatedAccount(account) {
            a = account;
            authaccount = {
                id: a.id,
                username: a.username,
                email: a.email,
                get_avatar: a.get_avatar,
                __proto__: a.__proto__

            }
            $cookies.put('authenticatedAccount', JSON.stringify(authaccount));
        }

        /**
         * @name unauthenticate
         * @desc Delete the cookie where the user object is stored
         * @returns {undefined}
         * @memberOf authentication.services
         */
        function unauthenticate() {
            $cookies.remove('authenticatedAccount');
        }

    });