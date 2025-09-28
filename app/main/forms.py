# usando Flask-WTF, crie uma classe EmailForm com um campo TextAreaField (para o conteúdo do e-mail) e um SubmitField.
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired, ValidationError, Optional

class EmailForm(FlaskForm):
    content = TextAreaField('Conteúdo do Email', validators=[Optional()])
    file = FileField('Ou faça upload de um arquivo (.txt ou .pdf)', 
                     validators=[Optional(), FileAllowed(['txt', 'pdf'], 'Apenas arquivos .txt e .pdf são permitidos!')])
    submit = SubmitField('Classificar Email')
    
    def __init__(self, *args, **kwargs):
        super(EmailForm, self).__init__(*args, **kwargs)
    
    def validate(self, extra_validators=None):
        # Chama a validação padrão primeiro
        if not super().validate(extra_validators):
            return False
        
        # Validação customizada: pelo menos um dos campos deve estar preenchido
        if not self.content.data or not self.content.data.strip():
            if not self.file.data:
                self.content.errors.append('Você deve inserir o conteúdo do email ou fazer upload de um arquivo.')
                self.file.errors.append('Você deve inserir o conteúdo do email ou fazer upload de um arquivo.')
                return False
        
        return True
    