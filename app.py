from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# Nastavení cesty k SQLite databázi
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ankety.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Model pro otázku
class Otazka(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200), nullable=False)
    # Vztah na odpovědi
    odpovedi = db.relationship('Odpoved', backref='otazka', lazy=True)

# Model pro odpověď
class Odpoved(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200), nullable=False)
    otazka_id = db.Column(db.Integer, db.ForeignKey('otazka.id'), nullable=False)

# Vytvoření databáze při prvním spuštění
with app.app_context():
    db.create_all()

# Hlavní stránka – výpis všech otázek
@app.route('/')
def home():
    otazky = Otazka.query.all()
    return render_template('index.html', otazky=otazky)

# Formulář pro zadání nové otázky
@app.route('/otazka', methods=['GET', 'POST'])
def otazka():
    question = None
    if request.method == 'POST':
        question = request.form['question']
        nova_otazka = Otazka(text=question)
        db.session.add(nova_otazka)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('question.html', question=question)

# Formulář a výpis odpovědí pro konkrétní otázku
@app.route('/odpoved/<int:id>', methods=['GET', 'POST'])
def odpoved(id):
    otazka = Otazka.query.get_or_404(id)
    odpoved_text = None
    if request.method == 'POST':
        odpoved_text = request.form['odpoved']
        nova_odpoved = Odpoved(text=odpoved_text, otazka_id=otazka.id)
        db.session.add(nova_odpoved)
        db.session.commit()
    return render_template('odpoved.html', otazka=otazka, odpoved=odpoved_text)

# Stránka se statistikou
@app.route('/statistika')
def statistika():
    pocet_otazek = Otazka.query.count()
    pocet_odpovedi = Odpoved.query.count()
    return render_template('statistika.html', pocet_otazek=pocet_otazek, pocet_odpovedi=pocet_odpovedi)

if __name__ == '__main__':
    app.run(debug=True)