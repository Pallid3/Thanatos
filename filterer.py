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

# testing
# f = PhraseFilter()
# f.add_phrase(["create", "mod", "when"])
# f.add_phrase(["badword", "kiisu"])

# print(f.contains_banned("please create a mod when you can")) 
# print(f.contains_banned("mod create something else when"))
# print(f.contains_banned("create mod now"))
# print(f.contains_banned("badword goes here"))
# print(f.contains_banned("badword"))
# print(f.contains_banned("kiisu badword"))
# print(f.contains_banned("kiisu create mod owo"))

# '''returned:
# True
# True
# False
# False
# False
# True
# False
# ''' # excpeted values
