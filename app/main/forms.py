# usando Flask-WTF, crie uma classe EmailForm com um campo TextAreaField (para o conteúdo do e-mail) e um SubmitField.
from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired, ValidationError

class EmailForm(FlaskForm):
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Submit')
    def __init__(self, *args, **kwargs):
        super(EmailForm, self).__init__(*args, **kwargs)
        self.content.label = 'Email Content'
        self.submit.label = 'Submit'
    def validate_content(self, field):
        if not field.data.strip():
            raise ValidationError('Content cannot be empty or just whitespace.')
        return field.data
    