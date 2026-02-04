import hashlib
import datetime
from init import app, db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50))
    email = db.Column(db.String(50), unique=True)
    pw_hash = db.Column(db.String(50))
    location = db.Column(db.String(100))
    bio = db.Column(db.String(300))

    def follow_state(self, other):
        if self.id == other:
            return 'self'
        follow = Follow.query.filter_by(follower_id=self.id, followee_id=other).first()
        reverse = Follow.query.filter_by(follower_id=other, followee_id=self.id).first()
        if follow and reverse:
            return 'followers'
        elif follow:
            #  self is following
            return 'following'
        elif reverse:
            return 'followed'
        else:
            return 'none'

    @property
    def grav_hash(self):
        hash = hashlib.md5()
        hash.update(self.email.strip().lower().encode('utf8'))
        return hash.hexdigest()

    @property
    def jsonable(self):
        return {
            'id': self.id,
            'grav_hash': self.grav_hash,
            'username': self.username,
            'location': self.location,
            'bio': self.bio
        }


class Follow(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    follower_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    followee_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    follower = db.relationship('User', foreign_keys=[follower_id])
    followee = db.relationship('User', foreign_keys=[followee_id])



class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text())
    timestamp = db.Column(db.DateTime, default=datetime.datetime.now)
    photo = db.Column(db.BLOB)
    photo_type = db.Column(db.String(50))

    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    creator = db.relationship('User', backref='posts')


User.friends = db.relationship('User', secondary='follow',
                               primaryjoin=User.id==Follow.follower_id,
                               secondaryjoin=User.id==Follow.followee_id)

db.create_all(app=app)