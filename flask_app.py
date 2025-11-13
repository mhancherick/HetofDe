from flask import Flask, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

@app.route("/")
def dictionary():
    return "<p>Dutch Dictionary API</p>"

@app.route("/api/lookup/<word>")
def api_lookup(word):
    result = lookup_word(word)
    return jsonify(result)

def lookup_word(word):
    connection = sqlite3.connect("dutch_nouns.db")
    cursor = connection.cursor()

    word = word.lower()

    cursor.execute("SELECT * FROM dictionary WHERE word = ?", (word,))
    result = cursor.fetchone()
    connection.close()
    if result:
        article = result[1]
        # If there are english translations available, include
        if len(result) > 3:
            english = result[3]
        else:
            english = None

        if article == 'de':
            patterns = {
                'definite': f'de {word}',
                'demonstrative': f'deze/die {word}',
                'adjective': f'een grote {word}',
                'relative': f'de {word} die...'
            }
        else:
            patterns = {
                'definite': f'het {word}',
                'demonstrative': f'dit/dat {word}',
                'adjective': f'een groot {word}',
                'relative': f'det {word} dat...'
            }

        return {
            'word': result[0],
            'article': article,
            'source': result[2],
            'english': english,
            'patterns': patterns,
            'found': True
        }
    else:
        return {
            'word': word,
            'found': False
        }

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)