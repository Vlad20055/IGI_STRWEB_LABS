import Task1.Task1 as t1
import Task2.Task2 as t2
import Task3.Task3 as t3
import Task4.Task4 as t4
import Task5.Task5 as t5
from zipfile import ZipFile
import Check_input as ch


def cycle_decorator(func):
    def wrapper(*args, **kwargs):
        while True:
            want = input("Input exit to close program or any other string to start:")
            if want == "exit":
                break
            else:
                func(*args, **kwargs)
                continue
    return wrapper


@cycle_decorator
def Run_Task1():
    while True:
        old = input("Enter number of years:")
        if not ch.is_non_negative_int(old):
            print("Number of years must be non negative int!")
            continue
        else: break
    
    ds = t1.Data_service()
    target_friends = ds.get_csv(int(old))

    for friend in target_friends:
        print(friend)
    
    if len(target_friends) == 0:
        print("No such friends :(")


def Run_Task2():
    t = t2.TextAnalizer()
    print(t.text, "\n")

    print(f"Total number of sentences = {t.count_sentences()}")
    print(f"Number of narrative sentences = {t.count_narrative_sentences()}")
    print(f"Number of question sentences = {t.count_question_sentences()}")
    print(f"Number of incentive sentences = {t.count_incentive_sentences()}")
    print(f"Mean sentence length = {t.count_mean_sentence_length()}")
    print(f"Mean word length = {t.count_mean_word_length()}")
    print(f"Number of smiles = {t.count_smiles()}")

    print(f"All words that contain digits and vowel letters: {t.find_digits_vowel_words()}")
    filename = "Task2/Task2_result.txt"
    try:
        with open(filename, "w") as f:
            for word in t.find_digits_vowel_words():
                f.write(word + "\n")
    except:
        print(f"Something went wrong while reading file {filename}")
        
    zip_path = "Task2/Archive.zip"
    try:
        with ZipFile(zip_path, "w") as myzip:
            myzip.write(filename)
    except Exception as e:
        print(f"Something went wrong while archivating file {filename}")

    try:
        with ZipFile(zip_path, "r") as myzip:
            print(myzip.infolist())
    except Exception as e:
        print(f"Something went wrong while getting info about archive {zip_path}")
    

    print(f"All ariphmetic expressions = {t.find_all_ariphmetic_expressions(t.text)}")
    print(f"Shorted word started woth i/I - {t.find_shortest_word_started_with_i()}")
    string = "Hellow, I am Vlad!"
    print(f"\nString = {string}")
    print(f"Number of words in string = {t.count_number_of_words_in_string_and_print_all_words_with_odd_number_of_letters(string)}\n")
    print(f"Repeted words = {t.find_repeted_words()}")


@cycle_decorator
def Run_Task3():
    while True:
        x = input("x = ")
        if not ch.is_abs_not_more_than_one(x):
            print("Error! x must be in [-1, 1]\n")
            continue
        else:
            x = float(x)
            break

    while True:
        n = input("n = ")
        if not ch.is_positive_int(n):
            print("Error! n must be positive integer\n")
            continue
        else:
            n = int(n)
            if n > 100: n = 100
            break

    arc_eval = t3.ArcsinEvaluator()
    ans, seq = arc_eval.arcsin_n(x, n)
    print(f"arcsin({x}) = {ans}",
          f"mean = {arc_eval.mean_of_sequence(seq)}",
          f"median = {arc_eval.median_of_sequence(seq)}",
          f"mode = {arc_eval.mode_of_sequence(seq)}",
          f"variance = {arc_eval.variance_of_sequence(seq)}",
          f"stdev = {arc_eval.standard_deviation_of_sequence(seq)}",
          sep="\n")
    arc_eval.display(seq=seq)
    
    
@cycle_decorator
def Run_Task4():
    while(True):
        a = input("Side a = ")
        if not ch.is_positive_float(a):
            print("Side a must be positive float!")
            continue
        else: break
    
    while(True):
        color = input("Color = ")
        if not ch.is_color(color):
            print("No such color!")
            continue
        else: break

    label = input("Enter label: ")

    triangle = t4.Right_triangle(float(a), label, color)
    print(triangle)
    triangle.draw()


@cycle_decorator
def Run_Task5():
    m = t5.NumpyTester()
    arr1 = m.create_from_list([1, 2, 3, 4])
    arr2 = m.create_from_list([4, 3, 2, 1])

    print(f"arr1 = {arr1}")
    print(f"arr2 = {arr2}", "\n")
    print(f"Array:\n{m.create_from_list([1, 2, 3])}\n")
    print(f"Zeroes:\n{m.create_zeroes(3, 3)}\n")
    print(f"Identity:\n{m.create_identity(4)}\n")
    print(f"Indexing:\n{m.demonstrate_indexing(arr1)}\n")
    print(f"Elementwise operations:\n{m.elementwise_operations(arr1, arr2)}\n")
    print(f"Mean of arr1:\n{m.calculate_mean(arr1)}\n")
    print(f"Median of arr1:\n{m.calculate_median(arr1)}\n")
    print(f"Correlaiton of arr1 & arr2:\n{m.calculate_correlation(arr1, arr2)}\n")
    print(f"Variance of arr1:\n{m.calculate_variance(arr1)}\n")
    print(f"std of arr1:\n{m.calculate_std(arr1)}\n")

    matrix = m.create_matrix(4, 6)
    print(f"Matrix[4, 6]:\n{matrix}\n")
    print(f"Min sum of rows = {m.find_min_row_sum(matrix)}")
    print(f"Corcoef of elements with both even indexes and both odd indexes = {m.correlation_even_odd_indices(matrix)}")


# Run_Task1()
# Run_Task2()
# Run_Task3()
Run_Task4()
# Run_Task5()

    

