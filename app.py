from flask import Flask, jsonify
import csv

app = Flask(__name__)

def load_data():
    with open('bible.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        data = [row for row in reader]
    return data

@app.route('/biblia/<livro>/<int:capitulo>', methods=['GET'])
@app.route('/biblia/<livro>/<int:capitulo>/', methods=['GET'])
def get_versiculos(livro, capitulo):
    data = load_data()
    versiculos = []
    for row in data:
        if row['book'] == livro and int(row['chapter']) == capitulo:
            versiculo = {
                'book': row['book'],
                'chapter': row['chapter'],
                'verse': row['verse'],
                'text': row['text']
            }
            versiculos.append(versiculo)
    if versiculos:
        versiculos = sorted(versiculos, key=lambda x: int(x['verse']))
        return jsonify(versiculos)
    else:
        return jsonify({'message': 'Versículos não encontrados'}), 404

@app.route('/biblia/<livro>/<int:capitulo>/<int:versiculo>', methods=['GET'])
@app.route('/biblia/<livro>/<int:capitulo>/<int:versiculo>/', methods=['GET'])
def get_versiculo(livro, capitulo, versiculo):
    data = load_data()
    for row in data:
        if row['book'] == livro and int(row['chapter']) == capitulo and int(row['verse']) == versiculo:
            versiculo = {
                'book': row['book'],
                'chapter': row['chapter'],
                'verse': row['verse'],
                'text': row['text']
            }
            return jsonify(versiculo)
    return jsonify({'message': 'Versículo não encontrado'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
