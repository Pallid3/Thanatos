class PhraseFilter:
    def __init__(self, banned_phrases=None):
        self.banned_phrases = banned_phrases if banned_phrases else []

    def add_phrase(self, phrase):
        if phrase not in self.banned_phrases:
            self.banned_phrases.append(phrase)

    def contains_banned(self, text):
        text_lower = text.lower()
        for phrase in self.banned_phrases:
            if all(word.lower() in text_lower for word in phrase):
                return True
        return False
