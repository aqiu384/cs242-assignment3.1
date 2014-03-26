from app import db 

BODY_LENGTH = 200
AUTHOR_LENGTH = 20
    
class Post(db.Model):
    """Schema for post table in database"""
    id = db.Column(db.Integer, primary_key = True)  #Unique identification number
    pid = db.Column(db.Integer, default = 0)        #Parent of reponse comment, 0 if top-level comment
    author = db.Column(db.String(AUTHOR_LENGTH))    #Author name
    body = db.Column(db.String(BODY_LENGTH))        #Post body
    timestamp = db.Column(db.DateTime)              #Time of post

    def __repr__(self):
        return '<Post %r>' % (self.body)