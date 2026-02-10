class Word_list:
    def __init__(self, banned_list=None):
        self.banned_list = banned_list if banned_list else []
    
    def add_banned(self, word):
        if word not in self.banned_list:
            self.banned_list.append(word)
        
    def remove_banned(self, word):
        if word in self.banned_list:
            self.banned_list.remove(word)
    
    def contains_banned(self, text):
        for banned in self.banned_list:
            if banned.lower() in text.lower():  # fixed missing ()
                return True
        return False

class Filter(Word_list):
    def __init__(self, banned_list=None, double_list=None):
        super().__init__(banned_list)
        self.double_list = double_list if double_list else []

    def add_list(self, lst):
        if lst not in self.double_list:
            self.double_list.append(lst)

    def contains_multi_word(self, text):
        text_lower = text.lower()
        for phrase in self.double_list:
            # check if all words in phrase exist in text, in any order
            if all(word.lower() in text_lower for word in phrase):
                return True
        return False

f = Filter(banned_list=["badword"])
f.add_list(["create", "mod", "when"])
f.add_list(["badword", "kiisu"])

print(f.contains_multi_word("please create a mod when you can")) 
print(f.contains_multi_word("mod create something else when"))
print(f.contains_multi_word("create mod now"))
print(f.contains_multi_word("badword goes here"))
print(f.contains_multi_word("badword"))
print(f.contains_multi_word("kiisu badword"))
print(f.contains_multi_word("kiisu create mod owo"))

'''returned:
True
True
False
False
False
True
False
''' # excpeted values