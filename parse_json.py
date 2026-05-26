# Dutch dictionary obtained from kaikki.org

import gzip, json, sqlite3, os, sys

class DutchParser:
    def __init__(self, filename):
        self._filename = filename

    def get_filename(self):
        return self._filename

    def create_database(self, db_path='dutch_nouns.db', reset=True):
        """
        Parses the source JSONL file and inserts Dutch nouns into the database.
        When reset=True, drops and recreates the table first (used for the primary source).
        When reset=False, appends to an existing table (used for supplementary sources).

        :param db_path: the filepath for the database
        :param reset: whether to drop and recreate the table before inserting
        """
        processed_words = 0
        processed_nouns = 0

        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        if reset:
            cursor.execute('DROP TABLE IF EXISTS dictionary')
            cursor.execute('''
            CREATE TABLE dictionary (
                word TEXT NOT NULL,
                article TEXT NOT NULL,
                article_source TEXT NOT NULL,
                english TEXT,
                plural TEXT,
                UNIQUE(word, article)
                )
            ''')

        print(f"Processing {self._filename}...")

        open_fn = gzip.open if self._filename.endswith('.gz') else open
        with open_fn(self._filename, 'rt', encoding='utf-8') as file:
            for line_number, line in enumerate(file):

                if processed_words % 10000 == 0 and processed_words != 0:
                    print(f"  {processed_words} words processed")

                try:
                    entry = json.loads(line)
                except json.JSONDecodeError:
                    print(f"Could not parse line {line_number}")
                    continue

                word = entry.get('word', '').strip().lower()
                tags = entry.get('tags', [])
                head_templates = entry.get('head_templates', [])
                lang_code = entry.get('lang_code', '').strip().lower()
                word_type = entry.get('pos', '').strip().lower()
                english = self.get_english(entry)
                plural = self.get_plural(entry)
                if plural is None and word.endswith('je'):
                    plural = word + 's'

                if not word:
                    continue

                processed_words += 1

                if not self.is_valid_noun(word, lang_code, word_type):
                    continue

                if not tags and self.is_diminutive(word):
                    article = 'het'
                    article_source = 'inferred'
                elif tags:
                    article = self.determine_article(tags)
                    article_source = 'tags'
                    if not article:
                        article = self.determine_article_from_templates(head_templates)
                        if article:
                            article_source = 'head_templates'
                else:
                    article = self.determine_article_from_templates(head_templates)
                    if article:
                        article_source = 'head_templates'
                    else:
                        continue

                if not article:
                    continue

                try:
                    cursor.execute('''
                        INSERT INTO dictionary (word, article, article_source, english, plural)
                        VALUES (?, ?, ?, ?, ?)
                        ON CONFLICT(word, article) DO UPDATE SET
                            plural = CASE WHEN dictionary.plural IS NULL AND excluded.plural IS NOT NULL
                                          THEN excluded.plural
                                          ELSE dictionary.plural END
                    ''', (word, article, article_source, english, plural))
                except sqlite3.Error as error:
                    print(f"Error inserting word '{word}'")
                    print(error)
                    continue

                processed_nouns += 1

        print(f"  Done — {processed_words} words scanned, {processed_nouns} nouns added")

        connection.commit()
        connection.close()

    def is_valid_noun(self, word, lang_code, word_type):
        """
        Determines if the word is a valid Dutch noun

        :param word: the word to evaluate
        :param lang_code: the language code of the word
        :param word_type: the type of word (noun, adverb, etc.)

        :return: True if the word is a valid Dutch Noun, False otherwise
        """
        if lang_code != 'nl':
            return False

        if word_type != 'noun':
            return False

        # Skips phrases
        if ' ' in word:
            return False

        return True

    def determine_article(self, tags):
        """
        Determines what Dutch article should be used with the word

        :param tags: an array of tags for the word

        :return: The proper article for the word. Returns None if no article can be determined
        """

        # Diminutives supersede all considerations
        if 'diminutive' in tags:
            return 'het'

        # Determines article based on primary tag
        for tag in tags:
            if tag in ['masculine', 'feminine', 'common-gender']:
                return 'de'
            elif tag == 'neuter':
                return 'het'

        return None

    def determine_article_from_templates(self, head_templates):
        """
        Extracts the Dutch article from head_templates as a fallback when tags lack gender info.
        Handles both explicit 'de'/'het' args and gender-letter shorthands (m/f/c → de, n → het).

        :param head_templates: the head_templates list from a kaikki.org entry

        :return: 'de', 'het', or None
        """
        de_letters = {'m', 'f', 'c'}

        for template in head_templates:
            if not str(template.get('name', '')).startswith('nl-noun'):
                continue
            args = template.get('args', {})
            first_arg = str(args.get('1', '')).strip().lower()
            if first_arg in ('de', 'het'):
                return first_arg
            if first_arg in de_letters:
                return 'de'
            if first_arg == 'n':
                return 'het'

        return None

    def is_diminutive(self, word):
        """
        Determines if the word is a diminutive, which is always a "het" word

        :param word: the word to evaluate

        :return: True if the word is diminutive, False otherwise
        """
        if word.endswith('je'):
            return True

        return False

    def get_plural(self, entry):
        """
        Extracts the plural form from the entry's forms array.

        :param entry: a JSON entry for a Dutch word

        :return: the plural form string, or None if not available
        """
        for form in entry.get('forms', []):
            tags = form.get('tags', [])
            if 'plural' not in tags or 'diminutive' in tags:
                continue
            value = form.get('form', '').strip().rstrip(',').strip()
            if value and not value.startswith('('):
                return value
        return None

    def get_english(self, entry):
        """
        Gets the English translation(s) from the entry

        :param entry: a JSON entry for a Dutch word

        :return: English translation(s) or None if there aren't any
        """

        translations = entry.get('translations', [])
        english_translations = []
        seen = set()

        for translation in translations:
            if translation.get('lang_code') == 'en':
                english_word = translation.get('word')
                if english_word and english_word not in seen:
                    english_translations.append(english_word)
                    seen.add(english_word)

        if not english_translations:
            return None

        return ', '.join(english_translations)

    def test_db(self, db_path='dutch_nouns.db'):
        """
        Prints basic statistics and a sample of words from the database

        :param db_path: the filepath of the database

        :return: None
        """
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        cursor.execute("SELECT COUNT(*) FROM dictionary")
        total = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM dictionary WHERE article = 'de'")
        de_count = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM dictionary WHERE article = 'het'")
        het_count = cursor.fetchone()[0]

        cursor.execute("SELECT article_source, COUNT(*) FROM dictionary GROUP BY article_source")
        sources = cursor.fetchall()

        cursor.execute("SELECT COUNT(*) FROM dictionary WHERE plural IS NOT NULL")
        plural_count = cursor.fetchone()[0]

        cursor.execute("SELECT * FROM dictionary LIMIT 10")
        word_rows = cursor.fetchall()

        print(f"\nTotal words in DB: {total}")
        print(f"Total 'de' words: {de_count}")
        print(f"Total 'het' words: {het_count}")
        print(f"Words with plural: {plural_count} ({plural_count * 100 // total}%)")
        print(f"By source: {dict(sources)}")
        print("Sample of words:")
        for row in word_rows:
            print(row)

        connection.close()


def apply_corrections(db_path='dutch_nouns.db', corrections_path='corrections.json'):
    """
    Inserts manually curated word→article mappings for words that all automated
    sources failed to capture. Uses INSERT OR IGNORE so it never overwrites
    authoritative source data.

    Each entry can be either:
      "word": "article"
      "word": {"article": "de/het", "english": "..."}
    """
    if not os.path.exists(corrections_path):
        return

    with open(corrections_path, 'r', encoding='utf-8') as f:
        corrections = json.load(f)

    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    added = 0

    for word, value in corrections.items():
        if word.startswith('_'):
            continue
        if isinstance(value, str):
            article, english = value, None
        else:
            article = value.get('article', '')
            english = value.get('english', None)
        if article not in ('de', 'het'):
            continue
        try:
            cursor.execute(
                'INSERT OR IGNORE INTO dictionary (word, article, article_source, english) VALUES (?, ?, ?, ?)',
                (word.lower().strip(), article, 'manual', english)
            )
            if cursor.rowcount:
                added += 1
        except sqlite3.Error:
            pass

    connection.commit()
    connection.close()
    print(f"  Corrections applied — {added} new entries from {corrections_path}")


def apply_exclusions(db_path='dutch_nouns.db', exclusions_path='exclusions.json'):
    """
    Removes known-bad word+article pairs from the database.
    """
    if not os.path.exists(exclusions_path):
        return

    with open(exclusions_path, 'r', encoding='utf-8') as f:
        exclusions = json.load(f)

    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    removed = 0

    for entry in exclusions:
        word = entry.get('word', '').lower().strip()
        article = entry.get('article', '')
        if not word or article not in ('de', 'het'):
            continue
        cursor.execute('DELETE FROM dictionary WHERE word = ? AND article = ?', (word, article))
        removed += cursor.rowcount

    connection.commit()
    connection.close()
    print(f"  Exclusions applied — {removed} entries removed from {exclusions_path}")


def apply_plural_corrections(db_path='dutch_nouns.db', corrections_path='plural_corrections.json'):
    """
    Updates plural forms for words where source data is missing or incorrectly tagged.
    Only fills in words that currently have no plural — never overwrites existing data.
    """
    if not os.path.exists(corrections_path):
        return

    with open(corrections_path, 'r', encoding='utf-8') as f:
        corrections = json.load(f)

    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    updated = 0

    for word, plural in corrections.items():
        if word.startswith('_'):
            continue
        cursor.execute(
            'UPDATE dictionary SET plural = ? WHERE word = ? AND plural IS NULL',
            (plural, word.lower().strip())
        )
        updated += cursor.rowcount

    connection.commit()
    connection.close()
    print(f"  Plural corrections applied — {updated} entries updated from {corrections_path}")


def apply_diminutive_translations(db_path='dutch_nouns.db'):
    """
    For inferred diminutive words (-je) with no English translation, tries to
    inherit a translation from the base word with " (diminutive)" appended.

    Tries suffix rules in order: -etje, -tje, -je
    Only updates words that still have no English after all other steps.
    """
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    cursor.execute("SELECT word FROM dictionary WHERE article_source = 'inferred' AND english IS NULL")
    diminutives = [row[0] for row in cursor.fetchall()]

    updated = 0
    for word in diminutives:
        base = None
        for suffix, replacement in [('etje', ''), ('tje', ''), ('je', '')]:
            if word.endswith(suffix):
                candidate = word[:-len(suffix)] + replacement
                cursor.execute('SELECT english FROM dictionary WHERE word = ? AND english IS NOT NULL LIMIT 1', (candidate,))
                row = cursor.fetchone()
                if row:
                    base = row[0]
                    break

        if base:
            cursor.execute(
                "UPDATE dictionary SET english = ? WHERE word = ? AND article_source = 'inferred' AND english IS NULL",
                (f"{base} (diminutive)", word)
            )
            updated += cursor.rowcount

    connection.commit()
    connection.close()
    print(f"  Diminutive inheritance — {updated} translations filled from base forms")


if __name__ == "__main__":
    db_path = 'dutch_nouns.db'
    # Default to nl-extract.jsonl; pass additional files as extra args to supplement
    source_files = sys.argv[1:] if len(sys.argv) > 1 else ['nl-extract.jsonl']

    for i, json_path in enumerate(source_files):
        parser = DutchParser(json_path)
        parser.create_database(db_path, reset=(i == 0))

    apply_corrections(db_path)
    apply_exclusions(db_path)
    apply_plural_corrections(db_path)
    apply_diminutive_translations(db_path)
    DutchParser(source_files[0]).test_db(db_path)
