var Chat = (function() {
  var _socket;

  function init(socket) {
    _socket = socket;

/*    $('form').submit(function() {
      var name = $.trim($('input[name="name"]').val());
      var message = $.trim($('input[name="message"]').val());
      if (!name.length) {
        alert("No name :(");
      } else if (!message.length) {
        $('input[name="message"]').focus();
      } else {
        _socket.send_json({name: name, message: message});
        $('input[name="message"]').val('');
        $('input[name="message"]').focus();
      }
      return false;
    });*/


    $(document).on('click' , '.accept' , function () {
        var parentData = $(this).parents("div.drop-down-row:first");
        var preserve_html = parentData.html();
        var invite_no =  $(this).val();
        parentData.html('<center><img style="margin-top:7px;" src="/static/assets/images/anim_loading_16x16.gif" /></center>');
        $.ajax({
            type: "post",
            url: "/accept-or-ignore/",
            data: {'invite_no': invite_no, 'query': "accept"}
        }).done(function (msg) {
                if (msg['message'] == "bad data!")
                    parentData.html(preserve_html);
                else
                {
                    _socket.send_json({notification_id: msg['notificationid']});
                    parentData.html(msg['message'])
                }
            });
    });


  }

  return {
     init: init
  };

})();

SockJS.prototype.send_json = function(data) {
  this.send(JSON.stringify(data));
};

var initsock = function(callback)
{
    sock = new SockJS('http://' + SOCK.host + ':' + SOCK.port + '/' + SOCK.channel);

    sock.onmessage = function (e) {
    console.log('message', e.data);
    if ($('#goodOne').val() == e.data['of_whom'])
    {
        var genHtml = '<div class="drop-down-row"> <div style="visibility: hidden;" class="row-left-part"><span class="icon-tick"></span></div><div class="row-middle-part">' + e.data['des'] + '</div></div>'
        $('#user-notifications .content-drop-down-body').prepend( genHtml );
        //$('#notification-shower').html(parseInt(($('#notification-shower').html()) + 1).toString());
        $('#notification-shower').show();
    }
    };

    sock.onclose = function() {
        console.log('closed :(');
    };

    sock.onopen = function() {
    console.log('open');
    if (sock.readyState !== SockJS.OPEN) {
        throw "Connection NOT open";
    }
        callback(sock);
    };

};


$(function() {
  initsock(function(socket) {
    Chat.init(socket);
  });
});
