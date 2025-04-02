import Check_input as chi

def run():
    print("This program counts sum of last digits in numbers.",
          "To end sequence input 18.\n")
    while True:
        want = input("Input 'exit()' to close app.\nInput any other string to start:\n")
        if want == "exit()": break
        ans = 0
        while True:
            n = input("Input n: ")

            if (not chi.is_int(n)):
                print("Error! Number is not integer.")
                continue

            n = int(n)
            if n < 0: n = -n

            if (n == 18):
                print(f"Result = {ans}\n")
                break
            
            ans += n % 10


run()