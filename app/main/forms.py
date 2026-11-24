from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField
from wtforms.validators import DataRequired, Length


class AlunoForm(FlaskForm):
    name = StringField(
        'Cadastre o novo Aluno:',
        filters=[lambda value: value.strip() if value else value],
        validators=[
            DataRequired(message='Informe o nome do aluno.'),
            Length(max=64, message='O nome deve ter no máximo 64 caracteres.'),
        ],
    )
    role = SelectField(
        'Disciplina associada:',
        coerce=int,
        validators=[DataRequired(message='Selecione uma disciplina.')],
        validate_choice=True,
    )
    submit = SubmitField('Cadastrar')
