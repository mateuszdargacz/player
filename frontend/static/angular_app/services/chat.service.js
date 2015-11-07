angular.module('player')
    .factory('ChatFactory', function () {


        var ChatRequests = {

            dateformattodayservice: dateformattodayservice

        };

        return ChatRequests


        function dateformattodayservice (vardate){

            var newdate = new Date(vardate.date_chat);
            var ss = newdate.getSeconds();
            var mm = newdate.getMinutes();
            var hh = newdate.getHours();
            var dd = newdate.getDate();
            var mc = newdate.getMonth() + 1;
            var yy = newdate.getFullYear();

            if (ss < 10) {
                ss = '0' + ss.toString()
            }
            if (mm < 10) {
                mm = '0' + mm.toString()
            }
            if (dd < 10) {
                dd = '0' +dd.toString()
            }
            if (mc < 10) {
                mc = '0' +mc.toString()
            }
            var onlytime = hh.toString() + ":" + mm.toString() + ":" + ss.toString();
            var onlydate = yy.toString() + "-" + mc.toString() + "-" + dd.toString() + "  ";

            var today = new Date();
            var todaydd = today.getDate();

            if (dd == todaydd) {
                return "Today " + onlytime;
            } else {
                return onlydate + onlytime;
            }

        }


    });