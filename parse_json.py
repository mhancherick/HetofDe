# Dutch dictionary obtained from kaikki.org

import json

class DutchParser:
    def __init__(self, filename):
        self._filename = filename

    def get_filename(self):
        return self._filename
    
    def print_nouns(self):
        """
        A simple function to test out the JSON parsing
        """

        processed_words = 0
        processed_nouns = 0
        nouns_with_gender = 0
        skipped_examples = []
        

        with open(self._filename, 'r', encoding='utf-8') as file:
            for line_number, line in enumerate(file):

                if processed_words % 10000 == 0 and processed_words != 0:
                    print(f"Processed {processed_words} words")
                    print(f"Noun count: {processed_nouns}")

                try:
                    entry = json.loads(line)
                except json.JSONDecodeError:
                    print(f"Could not parse line {line_number}")
 

                word = entry.get('word', '').strip().lower()
                tags = entry.get('tags', [])
                lang_code = entry.get('lang_code', '').strip().lower()
                word_type = entry.get('pos', '').strip().lower()


                if not word:
                    continue

                processed_words += 1

                if not self.is_valid_noun(word, lang_code, word_type):
                    continue

                if not tags:
                    continue
                    
                article = self.determine_article(tags)

                processed_nouns += 1

                if article:
                    nouns_with_gender += 1
                else:
                    if tags and len(skipped_examples) < 100:
                        skipped_examples.append((word, tags))


        print(f"Noun count: {processed_nouns}")
                    

             


    def is_valid_noun(self, word, lang_code, word_type):
        """
        TODO: Implement
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
        TODO: implement
        """

        # Dimunitives supersede all considerations
        if 'diminutive' in tags:
            return 'het'

        if 'masculine' in tags or 'feminine' in tags or 'common-gender' in tags:
            return 'de'
        elif 'neuter' in tags:
            return 'het'
        else:
            return None


        
if __name__ == "__main__":
    parser = DutchParser('nl-extract.jsonl')
    parser2 = DutchParser('kaikki.org-dictionary-Dutch-by-pos-noun.jsonl')
    parser.print_nouns()
