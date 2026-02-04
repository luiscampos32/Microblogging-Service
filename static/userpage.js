var followButtonState = {
    'followers': {
        text: 'Unfollow',
        action: 'destroy'
    },
    'following': {
        text: 'Unfollow',
        action: 'retract'
    },
    'followed': {
        text: 'Follow',
        highlighted: true,
        action: 'accept'
    },
    'self': {
        text: 'Yourself',
        disabled: true
    },
    'none': {
        text: 'Follow',
        highlighted: true,
        action: 'request'
    }
};

function setupButton(button) {
    var state = $(button).attr('data-state');
    var config = followButtonState[state];
    $(button).text(config.text);
    if (config.disabled) {
        $(button).attr('disabled', true);
    } else {
        $(button).removeAttr('disabled');
    }
    $(button).addClass(state);
    if (config.highlighted) {
        $(button).addClass('pure-button-primary');
    } else {
        $(button).removeClass('pure-button-primary');
    }
}

function onFollowClick() {
    var button = $(this);
    var state = $(this).attr('data-state');
    var action = followButtonState[state].action;
    var url = '/follows/' + action;
    $.ajax(url, {
        data: {
            follower_id: authUserId,
            followee_id: parseInt($('#profile-shell').attr('data-user-id'), 10),
            _csrf_token: csrfToken
        },
        method: 'POST',
        success: function(response) {
            button.removeClass('pending');
            button.attr('data-state', response.new_state);
            setupButton(button);
        },
        error: function(err) {
            button.removeClass('pending');
            button.addClass('failed');
        }
    });
    button.addClass('pending');
}

$('button.follow').each(function() {
    setupButton(this);
    $(this).on('click', onFollowClick)
});
