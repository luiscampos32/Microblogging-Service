var el;

function charCount(e) {
    var textEntered;
    var charDisplay;
    var counter;
    //var zachcounter =0;

    textEntered = document.getElementById('inputArea').value;
    charDisplay = document.getElementById('charactersLeft');
    counter = (256 - (textEntered.length));
    charDisplay.textContent = 'Characters left: ' + counter;

}

el = document.getElementById('inputArea');
el.addEventListener('keypress', charCount,false);

$('.pure-button-primary').click(function(e){
    e.preventDefault();
    var content = $('#inputArea').val();
    $.ajax('/create/post', {
        data: {
            content: content,
            creator_id: authUserId
        },
        method: 'POST',
        success: function(response) {
            console.log('post added');
            addPost();
        },
        error: function(err) {
            alert('post failed');
        }
    });
});


function addPost() {
    var grav_hash = $('.grav-hash').attr('data-grav-hash');
    var datetime = new Date().toUTCString();
    var message = $('#inputArea').val();
    //zachcounter = zachcounter + 1;
    message = message.replace(/(www\..+?)(\s|$)/g, function(text, link) {
        return '<a href="http://' + link + '">' + link + '</a>';
    });

    var cont = {
        newPost: message,
        username: $('.user-username').attr('data-user-username'),
        timestamp: datetime,
    };

    //if (zachcounter > 20) {
        var addTmpl = '<div class="tweet pure-g"><div class="pure-u-1-6 pic"><a href="/u/{{username}}"> <img src="https://www.gravatar.com/avatar/'+grav_hash+'"></a></div><div class="tweet-container pure-u-5-6"><p class="op">' +
            '<a href="/u/{{username}}">{{username}}</a></p><p class="tweet-content">{{{newPost}}}</p>on {{timestamp}}</div>';
    //}
    //else {
    //    var addTmpl = '<div class="new-post"> {{{newPost}}} -by {{username}} on {{timestamp}}</div>';
    //}
    console.log(addTmpl);
    var msg = Mustache.render(addTmpl, cont);
    $('.pure-form #inputArea').val("");
    console.log('generated HTML: %s', msg);
    $('#new-post').prepend(msg).hide().fadeIn(1500);
}
