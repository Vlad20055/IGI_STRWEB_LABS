import Check_input as chi
import math

def arcsin_eps(x: float, eps: float):
    """
    Evaluate arscin(x) with accuracy eps.
    Return: (result, number of iterations).
    """
    if abs(x) > 1:
        raise ValueError("x must be in the range [-1, 1]")

    i = 0
    now = x
    result = now
    
    while abs(now) >= eps:
        now *= (((2*i + 1) ** 2) * (2*i + 2)) / (4 * ((i+1) ** 2) * (2*i + 3)) * (x ** 2)
        result += now
        i += 1
        if i == 500:
            break
    return result, i


def arcsin_n(x: float, n: int = 500):
    """
    Evaluate arscin(x) with n iterations.
    Return: result.
    """
    if abs(x) > 1:
        raise ValueError("x must be in the range [-1, 1]")

    pow_x = x
    frac = 1.0
    ans = pow_x

    for i in range(n):
        pow_x *= (x ** 2)
        frac *= (((2*i + 1) ** 2) * (2*i + 2)) / (4 * ((i+1) ** 2) * (2*i + 3))
        ans += frac * pow_x
    return ans


def run():
    print("This app evaluate arcsin(x) with accuracy eps.\n")
    while True:
        want = input("Input 'exit()' to close the app\nInput any other string to start:\n")
        if want == "exit()": break

        x = input("x = ")
        if not chi.is_abs_not_more_than_one(x):
            print("Error! x must be in [-1, 1]\n")
            continue
        x = float(x)

        eps = input("eps = ")
        if not chi.is_float(eps):
            print("Error! eps must be float type.\n")
            continue
        eps = float(eps)

        ans, n = arcsin_eps(x, eps)
        print(f"\nx = {x}", f"n = {n}", f"arcsin(x) = {ans}", f"Math.asin(x) = {math.asin(x)}", f"eps = {eps}", "\n", sep = "\n")


run()







