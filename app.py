from flask import Flask, render_template, request

app = Flask(__name__)

# seznam pro ukládání otázek
otazky = []
# seznam pro ukládání odpovědí (každá položka je seznam odpovědí k jedné otázce)
odpovedi = []

@app.route('/')
def home():
    return render_template('index.html', otazky=otazky, odpovedi=odpovedi)

@app.route('/otazka', methods=['GET', 'POST'])
def otazka():
    question = None
    if request.method == 'POST':
        question = request.form['question']
        otazky.append(question)  # Přidá otázku do seznamu
        odpovedi.append([])      # Přidá prázdný seznam odpovědí pro novou otázku
    return render_template('question.html', question=question)

@app.route('/odpoved/<int:id>', methods=['GET', 'POST'])
def odpoved(id):
    odpoved_text = None
    if 0 <= id < len(otazky):
        otazka = otazky[id]
        if request.method == 'POST':
            odpoved_text = request.form['odpoved']
            odpovedi[id].append(odpoved_text)  # Uloží odpověď k otázce
        return render_template('odpoved.html', otazka=otazka, odpoved=odpoved_text, vsechny_odpovedi=odpovedi[id])
    else:
        return render_template('odpoved.html', otazka=None, odpoved=None, vsechny_odpovedi=[])
        
@app.route('/statistika')
def statistika():
    pocet_otazek = len(otazky)
    pocet_odpovedi = sum(len(o) for o in odpovedi)
    return render_template('statistika.html', pocet_otazek=pocet_otazek, pocet_odpovedi=pocet_odpovedi)

if __name__ == '__main__':
    app.run(debug=True)