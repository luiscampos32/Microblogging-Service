import flask

from init import app, db
import models


def check_request():
    token = flask.session['csrf_token']
    if flask.request.form['_csrf_token'] != token:
        flask.abort(400)
    if flask.session.get('auth_user') != int(flask.request.form['follower_id']):
        app.logger.warn('requesting user %s not logged in (%s)',
                        flask.request.form['follower_id'],
                        flask.session.get('auth_user'))
        flask.abort(403)


@app.route('/follows/request', methods=['POST'])
def follow():
    check_request()
    init = int(flask.request.form['follower_id'])
    other = int(flask.request.form['followee_id'])
    fol = models.Follow.query.filter_by(follower_id=init,
                                        followee_id=other).first()
    if fol is None:
        fol = models.Follow()
        fol.follower_id = init
        fol.followee_id = other
        db.session.add(fol)
        db.session.commit()

    unfol = models.Follow.query.filter_by(follower_id=other,
                                        followee_id=init).first()
    if unfol is None:
        return flask.jsonify({'new_state': 'following'})
    else:
        return flask.jsonify({'new_state': 'followers'})


@app.route('/follows/destroy', methods=['POST'])
def unfollow():
    check_request()
    init = flask.request.form['follower_id']
    other = flask.request.form['followee_id']
    fs = models.Follow.query.filter_by(follower_id=init,
                                           followee_id=other).first()
    if fs is not None:
        db.session.delete(fs)
        db.session.commit()

    ofs = models.Follow.query.filter_by(follower_id=other,
                                            followee_id=init).first()
    if ofs is None:
        # nothing!
        return flask.jsonify({'new_state': 'none'})
    else:
        # they still have their open request to us
        return flask.jsonify({'new_state': 'followed'})


@app.route('/follows/accept', methods=['POST'])
def accept_friendship():
    return follow()


@app.route('/follows/retract', methods=['POST'])
def retract_friendship():
    return unfollow()


@app.route('/create/post', methods=['POST'])
def create_post():
    print(flask.request.form['content'])
    print(int(flask.request.form['creator_id']))

    content = flask.request.form['content']
    uid = flask.request.form['creator_id']

    post = models.Post()
    post.content = content
    post.creator_id = uid
    db.session.add(post)
    db.session.commit()

    return flask.jsonify({'result': 'ok'})
