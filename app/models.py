from . import db

DISCIPLINAS = ('DSWA5', 'GPSA5', 'IHCA5', 'SODA5', 'PJIA5', 'TCOA5')


class Disciplina(db.Model):
    __tablename__ = 'disciplinas'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(5), unique=True, nullable=False)
    alunos = db.relationship('Aluno', back_populates='disciplina')

    def __repr__(self):
        return '<Disciplina %r>' % self.nome


class Aluno(db.Model):
    __tablename__ = 'alunos'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(64), nullable=False)
    disciplina_id = db.Column(
        db.Integer, db.ForeignKey('disciplinas.id'), nullable=False
    )
    disciplina = db.relationship('Disciplina', back_populates='alunos')

    def __repr__(self):
        return '<Aluno %r>' % self.nome
