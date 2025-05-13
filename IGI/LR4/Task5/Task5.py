import numpy as np

class NumpyTester:
    @staticmethod
    def create_matrix(n: int, k: int) -> np.ndarray:
        """Создание матрицы n x k со случайными целыми числами (0-100)"""
        return np.random.randint(0, 101, size=(n, k))

    @staticmethod
    def create_from_list(lst: list) -> np.ndarray:
        """Создание массива из списка"""
        return np.array(lst)

    @staticmethod
    def create_zeroes(n, k):
        return np.zeros((n, k))
    
    @staticmethod
    def create_identity(n):
        return np.identity(n)
    

    @staticmethod
    def demonstrate_indexing(arr) -> dict:
        """Демонстрация индексации и срезов"""
        return {
            'first_element': arr[0],
            'last_element': arr[-1],
            'every_second_element': arr[::2]
        }

    @staticmethod
    def elementwise_operations(a, b) -> dict:
        """Поэлементные операции с массивами"""
        return {
            'addition': a + b,
            'multiplication': a * b,
            'sin_of_elements': np.sin(a)
        }

    @staticmethod
    def calculate_mean(arr: np.ndarray, axis=None) -> float:
        """Вычисление среднего значения"""
        return np.mean(arr, axis=axis)

    @staticmethod
    def calculate_median(arr: np.ndarray, axis=None) -> float:
        """Вычисление медианы"""
        return np.median(arr, axis=axis)

    @staticmethod
    def calculate_correlation(arr1: np.ndarray, arr2: np.ndarray):
        """Вычисление корреляционной матрицы"""
        return np.corrcoef(arr1, arr2)[0, 1]

    @staticmethod
    def calculate_variance(arr: np.ndarray, axis=None) -> float:
        """Вычисление дисперсии"""
        return np.var(arr, axis=axis)

    @staticmethod
    def calculate_std(arr: np.ndarray, axis=None) -> float:
        """Вычисление стандартного отклонения"""
        return np.std(arr, axis=axis)
    
    @staticmethod
    def find_min_row_sum(matrix) -> float:
        """
        Находит минимальное значение среди сумм элементов всех строк матрицы.
        
        Параметры:
        - matrix: список списков (двумерная матрица)
        
        Возвращает:
        - Минимальная сумма элементов строки
        """
        np_matrix = np.array(matrix)
            
        row_sums = np.sum(np_matrix, axis=1)
        return np.min(row_sums)
    
    @staticmethod
    def correlation_even_odd_indices(matrix) -> float:
        """
        Вычисляет коэффициент корреляции Пирсона между элементами:
        - С чётными индексами строк и столбцов (0, 2, 4...)
        - С нечётными индексами строк и столбцов (1, 3, 5...)
        
        Параметры:
        - matrix: список списков (двумерная матрица)
        
        Возвращает:
        - Коэффициент корреляции или None, если вычисление невозможно
        """
        np_matrix = np.array(matrix)
        
        if np_matrix.ndim != 2:
            raise ValueError("Матрица должна быть двумерной")
        
        # Выбор элементов с чётными и нечётными индексами
        even_elements = np_matrix[::2, ::2].flatten()
        odd_elements = np_matrix[1::2, 1::2].flatten()
        
        # Проверка на возможность вычисления корреляции
        if len(even_elements) == 0 or len(odd_elements) == 0:
            return None
        
        # Вычисление корреляции
        corr_matrix = np.corrcoef(even_elements, odd_elements)
        return corr_matrix[0, 1]
    




