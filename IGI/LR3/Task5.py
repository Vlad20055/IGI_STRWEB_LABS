import Check_input as chi

def max_abs_element_decorator(func):
    def wrapper(*args):
        max_abs_element = max(*args, key=abs)
        print(f"Max_abs_element in list is {max_abs_element}.")
        result = func(*args)
        return result
    return wrapper


def index_of_last_even(lst: list):
    ind = -1

    for i in range(len(lst)):
        if lst[i] % 2 == 0: ind = i

    return ind


@max_abs_element_decorator
def sum_before_last_even(lst: list):
    ans = 0
    last_index = index_of_last_even(lst)

    for i in range(last_index):
        ans += lst[i]

    return ans


def run():
    print("This program:\n"
    "1) Finds element that has maximum absalut value:\n"
    "2) Counts the sum of elements before last even element in list\n"
    "ALL NUMBERS IN LIST MUST BE INTEGERS!!!\n")

    while True:
        want = input("Enter 'exit()' to close app.\nEnter any other string to start:\n")
        if want == "exit()": break
        length = input("Enter number of elements:")

        if (not chi.is_non_negative_int(length)):
            print("Error!\n")
            continue

        length = int(length)

        if (length == 0):
            print("Error! It must be positive!\n")
            continue

        lst = []
        for _ in range(length):
            n = input("Input n: ")

            if not chi.is_int(n):
                print("Error! Number must be integer. Try again.\n")
                break
            
            n = int(n)
            lst.append(n)
        else:
            print(f"List = {lst}")
            print(f"Result: {sum_before_last_even(lst)}\n")


run()

