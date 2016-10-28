var words = new Bloodhound({
  datumTokenizer: Bloodhound.tokenizers.whitespace,
  queryTokenizer: Bloodhound.tokenizers.whitespace,
  prefetch: 'https://raw.githubusercontent.com/anyaat/webdev-practice/master/2016/bnc_vocab.json'
});

$('#queryform .typeahead').typeahead(null, {
  name: 'words',
  source: words
});


$(document).ready(function() {

    $('form.form-inline').on('submit', function(event) {

        $.ajax({
            data : {
                name : $('#nameInput').val(),
                word : $('#wordInput').val()
            },
            type : 'POST',
            url : '/ajax/count'
        })
        .done(function(data) {

            if (data.error) {
                $('#error-alert').text(data.error).show();
                $('#successAlert').text('Success!').hide();
            }
            else {
                $('#successAlert').text('Success!').fadeIn(50).delay(300).fadeOut(300);
                $('#success').html('<h2>Hi, ' + data.input[1] + '! Your word is "' + data.input[0] + '".</h2>');
                $('#error-alert').hide();
            }

        });

        event.preventDefault();

    });

});


function start_long_task() {
    div = $('<div class="progress"><div></div><div>0%</div><div>***</div><div>&nbsp;</div></div><hr>');
    $('#progress').append(div);
    var nanobar = new Nanobar({
        bg: '#44f',
        target: div[0].childNodes[0]
    });
    $.ajax({
        type: 'POST',
        url: '/ajax/longtask',
        success: function(data, status, request) {
            status_url = request.getResponseHeader('Location');
            update_progress(status_url, nanobar, div[0]);
        },
        error: function() {
            alert('Unexpected error');
        }
    });
}
function update_progress(status_url, nanobar, status_div) {
    $.getJSON(status_url, function(data) {
        percent = parseInt(data['current'] * 100 / data['total']);
        nanobar.go(percent);
        $(status_div.childNodes[1]).text(percent + '%');
        $(status_div.childNodes[2]).text(data['status']);
        if (data['state'] != 'PENDING' && data['state'] != 'PROGRESS') {
            if ('result' in data) {
                $('#finished').html('<h2>The task is done successfully.</h2><p>The result is the following: <ol><li>' + data['result'][0] + '</li><li>' + data['result'][1] + '</li><li>' + data['result'][2] + '</li><li>' + data['result'][3] + '</li><li>' + data['result'][4] + '</li><li>' + data['result'][5] + '</li><li>' + data['result'][6] + '</li><li>' + data['result'][7] + '</li><li>' + data['result'][8] + '</li><li>' + data['result'][9] + '</li></ol></p>');
            }
        }
        else {
            setTimeout(function() {
                update_progress(status_url, nanobar, status_div);
            }, 2000);
        }
    });
}

$(document).ready(function() {
    $('#start-bg-job').click(start_long_task);
});




// window.onbeforeunload = function() {
//     return "Hey there!";
//  };

// $('#select-model')
//   .submit( function(event) {
//     $.ajax( {
//       url: '/',
//       type: 'POST',
//       // data: new FormData($("form-id")[0]),
//       data : {
//                 model : $('#model-input').val(),
//             },
//       processData: false,
//       contentType: false
//     } );
//     .done(function(data) {

//         if (data.error) {
//             $('#errorAlert').text(data.error).show();
//             $('#successAlert').hide();
//         }
//         else {
//             $('#successAlert').text(data.name).show();
//             $('#errorAlert').hide();
//         }
//     });
//     event.preventDefault();
// });

// if ($('#single-vis').css('background-attachment')!=="local") { 
//     // will return the default value of 'scroll' in older browsers
//     $('#single-vis').on('scroll',function() {
//         $main = $(this);
//         $main.css({ 
//             'background-attachment': 'fixed',
//             'background-position': '0px '+(0-$main.scrollTop())+'px' 
//              // firefox doesn't support 'background-position-y'
//         });
//     });
// }; // end if


// $("#lang_select").change(function() {
//     var lang_id = $(this).find(":selected").val();
//     var request = $.ajax({
//         type: 'GET',
//         url: '/models/' + lang_id + '/',
//     });
//     request.done(function(data){
//         var option_list = [["", "--- Select One ---"]].concat(data);

//         for (var i = 0; i < option_list.length; i++) {
//             $("#model_select").append(
//                 $("<option></option>").attr(
//                     "value", option_list[i][0]).text(option_list[i][1])
//             );
//         }
//     });
// });