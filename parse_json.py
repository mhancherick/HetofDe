# Dutch dictionary obtained from kaikki.org

import json, sqlite3, os

class DutchParser:
    def __init__(self, filename):
        self._filename = filename

    def get_filename(self):
        return self._filename
    
    def db_exists(self, db_path='dutch_nouns.db'):
        """
        Determines if the database has been created

        :param db_path: the filepath of the database

        :return: None
        """
        if os.path.exists(db_path):
            return True
        else:
            return False
    
    def create_database(self, db_path='dutch_nouns.db'):
        """
        Parses the JSON file, processes the data, and adds the data to a database

        :param db_path: the filepath for the database

        :return: None
        """
        processed_words = 0
        processed_nouns = 0

        # Create DB connection
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        
        # Create table
        cursor.execute('DROP TABLE IF EXISTS dictionary')
        cursor.execute('''
        CREATE TABLE dictionary (
            word TEXT NOT NULL,
            article TEXT NOT NULL,
            article_source TEXT NOT NULL,
            english TEXT,
            UNIQUE(word, article)
            )
        ''')

        with open(self._filename, 'r', encoding='utf-8') as file:
            for line_number, line in enumerate(file):

                # Provides processing progress in the console
                if processed_words % 10000 == 0 and processed_words != 0:
                    print(f"Processed {processed_words} words")

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
                    cursor.execute('INSERT OR IGNORE INTO dictionary (word, article, article_source, english) VALUES (?, ?, ?, ?)',
                        (word, article, article_source, english))
                except sqlite3.Error as error:
                    print(f"Error inserting word '{word}'")
                    print(error)
                    continue
                
                processed_nouns += 1

        print(f"Processed {processed_words} words")
        print(f"Noun count: {processed_nouns}")
        print("FINISHED PROCESSING WORD LIST")

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

        # Dimunitives supersede all considerations
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

        :return: True if the word is diminutive, False otherwisee
        """
        if word.endswith('je'):
            return True

        return False
    
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

        cursor.execute("SELECT * FROM dictionary LIMIT 10")
        word_rows = cursor.fetchall()
                
        print(f"Total words in DB: {total}")
        print(f"Total 'de' words: {de_count}")
        print(f"Total 'het' words: {het_count}")
        print("Sample of words:")
        for row in word_rows:
            print(row)

if __name__ == "__main__":
    db_path = 'dutch_nouns.db'
    json_path = 'nl-extract.jsonl'
    parser = DutchParser(json_path)

    parser.create_database(db_path)
    parser.test_db(db_path)
