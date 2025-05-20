from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/otazka', methods=['GET', 'POST'])
def otazka():
    question = None
    if request.method == 'POST':
        question = request.form['question']
    return render_template('question.html', question=question)

if __name__ == '__main__':
    app.run(debug=True)