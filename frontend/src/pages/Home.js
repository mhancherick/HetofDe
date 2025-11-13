import { useState } from 'react';


function Home() {

    const [word, setWord] = useState('')
    const [result, setResult] = useState('')
    const [resultClass, setResultClass] = useState('')

    async function searchWord() {

        if (!word.trim() || word.trim().length < 2) {
            setResult('Please enter a word')
            setResultClass('')
            return
        }

        setResult('Searching')
        setResultClass('')

        try {
            const response = await fetch(`${process.env.REACT_APP_API_URL}/api/lookup/${word.trim()}`)
            const data = await response.json()
            
            if (data.found) {
                setResult(data.article)
                setResultClass(data.article)
            }
            else {
                setResult('Word not found')
                setResultClass('not-found')
            }
        } 
        catch (error) {
            setResult('Error connecting to server')
            setResultClass('');
            console.error(error);
        }
    }

    return (
        <main className="container">
            <h1>Het of De?</h1>
            <p>Enter a Dutch noun to find its article</p>
            
            <input type="text" 
                id="wordInput" 
                placeholder="Enter noun here!"
                value={word}
                onChange={(e) => setWord(e.target.value)}
                onKeyDown={(e) => {
                    if (e.key === 'Enter') {
                        searchWord()
                    }
                }}
            />
            <button id="searchBtn" onClick={searchWord}>Search</button>
            
            <div id="result" className={resultClass}>
                {result?.searching && 'Searching...'}
                {result?.error && result.error}
                {result?.found && (
                    <div>
                        <h2>{result.article}</h2>
                        {result.english && <p className="translation">English: {result.english}</p>}
                        <div className="patterns">
                            <p><strong>Definite article:</strong> {result.patterns.definite}</p>
                            <p><strong>Demonstrative:</strong> {result.patterns.demonstrative}</p>
                            <p><strong>Indefinite + adjective:</strong> {result.patterns.adjective}</p>
                            <p><strong>Relative pronoun:</strong> {result.patterns.relative}</p>
                        </div>
                    </div>
                )}
            </div>
        </main>
    )
}

export default Home