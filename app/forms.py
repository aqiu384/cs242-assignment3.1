from flask.ext.wtf import Form
from wtforms import TextField, BooleanField, TextAreaField
from wtforms.validators import Required

class PostForm(Form):
    """Form layout for a new post"""
    author = TextField('author', validators = [Required()])
    body = TextAreaField('body', validators = [Required()])
    
