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
            const response = await fetch(`http://localhost:5000/api/lookup/${word.trim()}`);
            const data = await response.json();
            
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
            setResult('Error connecting to server');
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
                searchWord();
            }
        }}
        />
        <button id="searchBtn" onClick={searchWord}>Search</button>
        
        <div id="result" className={resultClass}>{result}</div>
    </main>
    )
}

export default Home