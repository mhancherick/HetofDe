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
    rows = cursor.fetchall()
    connection.close()
    if rows:
        results = []
        for row in rows:
            article = row[1]
            english = row[3] if len(row) > 3 else None

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
                    'relative': f'het {word} dat...'
                }

            results.append({
                'article': article,
                'source': row[2],
                'english': english,
                'patterns': patterns,
            })

        return {
            'word': rows[0][0],
            'found': True,
            'results': results,
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