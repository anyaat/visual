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