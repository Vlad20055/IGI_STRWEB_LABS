import Check_input as chi

def count_digits(s: str) -> int:

    ans = 0

    for symb in s:
        if symb.isdigit(): ans += 1

    return ans


def count_vowel_letters(s: str) -> int:

    ans = 0

    for symb in s:
        if symb in 'aeiouAEIOU': ans += 1

    return ans


import random as r

def generate_random_string_with_digits_and_letters(n: int) -> str:
    symbols = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789" # 26 + 26 + 10 = 62 symbols

    def index_generator(): # my generator
            for _ in range(n):
                yield r.randint(0, 61)
    
    sequence = index_generator()
    ans = ""

    for i in sequence:
        ans += symbols[i]
    
    return ans


def run():

    def display_result(s: str):
        print(f"String = {s}")
        print(f"String has {count_digits(s)} digits.")
        print(f"String has {count_vowel_letters(s)} vowel letters.\n")

    print("This program counts number of vowel letters and digits in string.\n")
    
    while True:
        want = input("Enter 0 to generate a random string.\n"
                    "Enter 1 to enter your string.\n"
                    "Enter 'exit()' to close the app.\n")
        if want == "exit()": break
        elif want == "0":
            length = input("Enter lengh:")
            if (not chi.is_non_negative_int(length)):
                print("Error!\n")
                continue
            s = generate_random_string_with_digits_and_letters(int(length))
            display_result(s)
        elif want == "1":
            s = input("Enter string:")
            display_result(s)
        else:
            print("Error!\n")
            continue


run()



