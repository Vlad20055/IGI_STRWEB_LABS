s = "So she was considering in her own mind, as well as she could, for the hot day made her feel very sleepy and stupid, whether the pleasure of making a daisy-chain would be worth the trouble of getting up and picking the daisies, when suddenly a White Rabbit with pink eyes ran close by her."

def count_4letters_words(s: str) -> int:
    ans = 0
    now = 0

    for symb in s:
        if symb == " " or symb == "," or symb == ".":
            if now == 4: ans += 1
            now = 0
            continue
        now += 1
    
    return ans


def count_vowel_consonant_equal_words(s: str):
    positions = []
    words = []
    word = ""
    vowel = 0
    consonant = 0
    pos = 1

    for symb in s:
        if symb == " " or symb == "," or symb == ".":
            if vowel > 0 and vowel == consonant: 
                positions.append(pos)
                words.append(word)
            if symb == " ": pos += 1
            word = ""
            vowel = 0
            consonant = 0
            continue
        word += symb
        if symb in "aeiouAEIOU": vowel += 1
        if symb in "bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ": consonant += 1

    return words, positions


def sort_words_in_revers_order(s: str):
    words = []
    word = ""

    for symb in s:
        if symb == " " or symb == "," or symb == ".":
            if not word == "": words.append(word)
            word = ""
            continue
        word += symb

    words.sort(key=len, reverse=True)
    return words


def run():
    print("This program:\n"
    "1) counts number of 4-letter words\n"
    "2) find words with the same number of vowel and consonant letters and their positions\n"
    "3) sorts words in revers order according to their length\n")

    while True:
        want = input("Enter 'exit()' to close the app\nEnter any other string to start:\n")
        if want == "exit()": break
        print(f"Number of 4-letter words = {count_4letters_words(s)}")
        print(f"Words with the same number of vowel and consonant letters and their positions:")
        print(count_vowel_consonant_equal_words(s))
        print("Sorted words in revers order according to their length:")
        print(sort_words_in_revers_order(s), "\n")

run()

        
        



