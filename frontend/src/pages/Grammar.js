function Grammar() {
    return (
        <main className="container">
            <h1>Dutch Grammar</h1>
            <p>Dutch grammar has different rules based on the gender of the noun. Though they are not super complex,
                they can trip up a beginner Dutch learner.
            </p>
            <h3>Dutch Gender and Definite Articles</h3>
            <p>There are two genders for Dutch nouns: neuter and common. English only has one definite article (the),
                while Dutch has two. Neuter nouns use "het" for their
                definite article, while common nouns use "de" for their definite article. It is most helpful
                to learn the definite article of a noun while learning that noun, as there is no easy, foolproof
                way to determine the gender of a noun via rules.
            </p>
            <h3>Demonstrative Pronouns</h3>
            <p>Similar to English, Dutch demonstrative pronouns follow a near/far distinction. In English, this
                looks like this/these (for near things) and that/those (for far things). Dutch differs in that the 
                pronouns also depend on the gender of the noun. For "de" words, use deze (for near) and die (for far) 
                in both singular and plural. For "het" words in the singular, use dit (for near) and dat (for far). 
                All plural nouns use deze/die regardless of whether they were originally "het" or "de" words.
            </p>
            <h3>Indefinite + Adjective</h3>
            <p>In English, adjective endings never change. In Dutch, adjectives add an "e" ending in most cases, 
                with one important exception: when modifying a singular "het" word with an indefinite article (een) 
                or no article, the adjective stays in its base form. We will use "groot" (large) and "blauw" (blue) 
                to demonstrate.
            </p>
            <p>For example: "A big horse" translates to "Een groot paard", because paard is a "het" word.
                But "A big apple" translates to "Een grote appel", because appel is a "de" word. Similarly, 
                "A blue house" is "Een blauw huis" (het word), while "A blue car" is "Een blauwe auto" (de word).
                Note that with definite articles, ALL adjectives take the -e ending: "Het grote paard" and 
                "De grote appel" both use "grote".
            </p>
            <h3>Relative Pronouns</h3>
            <p>Dutch relative pronouns follow the same gender pattern as demonstrative pronouns. In English, we use 
                "who," "which," or "that" regardless of the noun. In Dutch, the relative pronoun must match the gender 
                of the noun it refers to. For "het" words in the singular, use "dat". For "de" words, use "die". 
                All plural nouns use "die" regardless of their original gender.
            </p>
            <p>For example: "The book that I read" translates to "Het boek dat ik lees", because boek is a "het" word. 
                But "The apple that I eat" translates to "De appel die ik eet", because appel is a "de" word.
            </p>
        </main>
    )
}
export default Grammar