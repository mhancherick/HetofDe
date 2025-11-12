from flask import Flask, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

#http://localhost:5000
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
        return {
            'word': result[0],
            'article': result[1],
            'source': result[2],
            'found': True
        }
    else:
        return {
            'word': word,
            'found': False
        }

if __name__ == "__main__":
    app.run(debug=True)