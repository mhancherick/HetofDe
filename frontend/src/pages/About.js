import { useState, useEffect } from 'react';
import { useForm, ValidationError } from '@formspree/react';

function SuggestionForm({ onSuccess }) {
    const [state, handleSubmit] = useForm('mlgvpqob');
    const [suggestionType, setSuggestionType] = useState('general');
    const [word, setWord] = useState('');
    const [currentArticle, setCurrentArticle] = useState('de');
    const [correctArticle, setCorrectArticle] = useState('het');

    useEffect(() => {
        if (state.succeeded) onSuccess();
    }, [state.succeeded]);

    const needsWord = suggestionType === 'missing_word' || suggestionType === 'incorrect_article';

    return (
        <form className="suggestion-form" onSubmit={handleSubmit}>
            <input type="hidden" name="_subject" value="Het of De Suggestion" />

            <div className="form-group">
                <label htmlFor="suggestionType">Type</label>
                <select
                    id="suggestionType"
                    name="suggestionType"
                    value={suggestionType}
                    onChange={e => setSuggestionType(e.target.value)}
                >
                    <option value="general">General feedback</option>
                    <option value="missing_word">Missing word</option>
                    <option value="incorrect_article">Incorrect article</option>
                </select>
            </div>

            {needsWord && (
                <div className="form-group">
                    <label htmlFor="word">Dutch word</label>
                    <input type="text" id="word" name="word" placeholder="e.g. hond"
                        value={word} onChange={e => setWord(e.target.value)} required />
                    <ValidationError field="word" errors={state.errors} />
                </div>
            )}

            {suggestionType === 'incorrect_article' && (
                <div className="form-group form-group-inline">
                    <div>
                        <label htmlFor="currentArticle">Current article</label>
                        <select id="currentArticle" name="currentArticle"
                            value={currentArticle}
                            onChange={e => {
                                setCurrentArticle(e.target.value);
                                setCorrectArticle(e.target.value === 'de' ? 'het' : 'de');
                            }}>
                            <option value="de">de</option>
                            <option value="het">het</option>
                        </select>
                    </div>
                    <div>
                        <label htmlFor="correctArticle">Correct article</label>
                        <select id="correctArticle" value={correctArticle} disabled>
                            <option value="de">de</option>
                            <option value="het">het</option>
                        </select>
                        <input type="hidden" name="correctArticle" value={correctArticle} />
                    </div>
                </div>
            )}

            <div className="form-group">
                <label htmlFor="message">Details</label>
                <textarea id="message" name="message" rows="4" placeholder="Any additional context..." />
                <ValidationError field="message" errors={state.errors} />
            </div>

            <ValidationError errors={state.errors} />

            <button type="submit"
                disabled={state.submitting || (needsWord && !word.trim())}
                className="suggestion-submit">
                {state.submitting ? 'Sending…' : 'Send suggestion'}
            </button>
        </form>
    );
}

function About() {
    const [formKey, setFormKey] = useState(0);
    const [showSuccess, setShowSuccess] = useState(false);

    function handleSuccess() {
        setShowSuccess(true);
        setFormKey(k => k + 1);
    }

    return (
        <main className="container">
            <h1>About Het of De</h1>
            <p>One of the more difficult aspects of studying Dutch is determining the definite article
                for nouns. There are rules, but there are so many exceptions to those rules that it's
                better to ignore those rules entirely. Many of the online dictionaries that I found are in Dutch,
                and the English based dictionaries did not allow me to easily determine what the article is.
            </p>

            <p>I created Het of De to provide people learning Dutch a quick way to look up the article of a noun.
                I hope you find this site useful!
            </p>

            <p>Dutch data was sourced from <a href="https://kaikki.org">kaikki.org</a>. Many thanks to Tatu Ylonen for this resource!
            </p>

            <p>If you're interested in diving into the code, here is a link to the <a href="https://github.com/mhancherick/HetofDe">Github repo!</a></p>

            <p>Have a suggestion or found an error? Use the form below.</p>
            {showSuccess && <p className="form-status success">Thanks for your suggestion!</p>}
            <SuggestionForm key={formKey} onSuccess={handleSuccess} />
        </main>
    )
}

export default About
