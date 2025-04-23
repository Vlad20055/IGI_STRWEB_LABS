import re
import statistics as st

class TextAnalizer:
    def __init__(self):
        self.text = self.read_text(filename="Task2/Task2.txt")

    def read_text(self, filename):
        try:
            with open(filename, "r") as f:
                return f.read()
        except:
            print(f"Something went wrong while reading {filename}")

    def count_sentences(self):
        pattern = r"[.!?]"
        matches = re.findall(pattern, self.text)
        return len(matches)
    
    def count_narrative_sentences(self):
        pattern = r"\."
        matches = re.findall(pattern, self.text)
        return len(matches)
    
    def count_question_sentences(self):
        pattern = r"\?"
        matches = re.findall(pattern, self.text)
        return len(matches)
    
    def count_incentive_sentences(self):
        pattern = r"\!"
        matches = re.findall(pattern, self.text)
        return len(matches)
    
    def count_mean_sentence_length(self):
        pattern = r"[^.!?]*[.?!]"
        matches = re.findall(pattern, self.text)
        lengths = []
        for sent in matches:
            cur_matches = re.findall(r"\w", sent)
            lengths.append(len(cur_matches))
        return st.mean(lengths)
    
    def count_mean_word_length(self):
        matches = re.findall(r"\w+", self.text)
        lengths = [len(word) for word in matches]
        return st.mean(lengths)

    def count_smiles(self):
        pattern = r"[;:]-*([\(\)\[\]])\1*"
        matches = re.findall(pattern, self.text)
        return len(matches)
    
    def find_digits_vowel_words(self):
        words = re.findall(r"\w+", self.text)
        ans = []
        for word in words:
            if len(re.findall(r"\d", word)) > 0 and len(re.findall(r"[aouieyAOUIEY]", word)) > 0:
                ans.append(word)
        return ans
    
    @staticmethod
    def find_all_ariphmetic_expressions(string):
        pattern = r"\-?\d+\.?\d*\s*[\+\-\*\/]\s*\-?\d+\.?\d*"
        ar_exprs = re.findall(pattern, string)
        return ar_exprs
    
    @staticmethod
    def count_number_of_words_in_string_and_print_all_words_with_odd_number_of_letters(string):
        words = re.findall(r"\w+", string)
        print(f"Words with odd number of letters = {[word for word in words if len(word) % 2 == 1]}")
        return len(words)
    
    def find_shortest_word_started_with_i(self):
        words = re.findall("\w+", self.text)
        return min([word for word in words if word[0] == "i" or word[0] == "I"], key=lambda x : len(x))

    def find_repeted_words(self):
        words = list(map(lambda x : x.lower(), re.findall("\w+", self.text)))
        return list(set([word for word in words if words.count(word) > 1]))

    

