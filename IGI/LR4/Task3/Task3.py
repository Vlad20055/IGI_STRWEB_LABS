import statistics as st
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import math


class SequenceStatisticMixed:
    @staticmethod
    def mean_of_sequence(sequence):
        """Calculates the arithmetic mean of the sequence."""
        return st.mean(sequence)

    @staticmethod
    def median_of_sequence(sequence):
        """Calculates the median of the sequence."""
        return st.median(sequence) 

    @staticmethod
    def mode_of_sequence(sequence):
        """Calculates the mode of the sequence."""
        return st.mode(sequence)

    @staticmethod
    def variance_of_sequence(sequence):
        """Calculates the variance of the sequence."""
        return st.variance(sequence)

    @staticmethod
    def standard_deviation_of_sequence(sequence):
        """Calculates the standard deviation of the sequence."""
        return st.stdev(sequence)


class ArcsinEvaluator(SequenceStatisticMixed):
    @staticmethod
    def arcsin_n(x: float, n: int = 500):
        """
        Evaluate arscin(x) using n iterations.
        Return: result.
        """
        if abs(x) > 1:
            raise ValueError("x must be in the range [-1, 1]")

        pow_x = x
        frac = 1.0
        ans = pow_x
        sequence = [ans]

        for i in range(n):
            pow_x *= (x ** 2)
            frac *= (((2*i + 1) ** 2) * (2*i + 2)) / (4 * ((i+1) ** 2) * (2*i + 3))
            now = frac * pow_x
            sequence.append(ans)
            ans += now
        return ans, sequence
    

    def display(self, seq):
        fig, ax = plt.subplots()
        # plt.subplots_adjust(bottom=0.25)
        
        x_points = list(range(1, len(seq) + 1))
        ax.plot(x_points, seq, 'b-', label='Последовательность')
        
        x_math = [i/100 for i in range(-100, 101)]
        y_math = [math.asin(x) for x in x_math]
        ax.plot(x_math, y_math, 'r--', label='arcsin(x)')
        
        ax.set_aspect('equal')
        ax.grid(True)
        ax.legend()
        
        fig.suptitle('Последовательность и функция arcsin(x)', 
                    fontsize=14, 
                    fontweight='bold')
        
        ax.text(0.02, 0.95, 
            'Итерационная последовательность\nи аналитическая функция',
            transform=ax.transAxes,
            fontsize=10,
            bbox=dict(facecolor='white', alpha=0.8))
        
        
        if len(seq) > 0:
            last_x = len(seq)  # Последний индекс последовательности
            last_y = seq[-1]   # Последнее значение
            
            ax.annotate(
                'Конец последовательности',
                xy=(last_x, last_y),
                xytext=(20, 20),  # Смещение текста вправо и вверх
                textcoords='offset points',
                arrowprops=dict(
                    arrowstyle="->",
                    color="green"
                ),
                fontsize=9,
                backgroundcolor='white'
            )
        
        # Слайдер
        # 
        slider_ax = plt.axes([0.2, 0.1, 0.6, 0.03])
        slider = Slider(slider_ax, 'Прокрутка', 0, len(seq), valinit=0, valstep=1)
        
        def update(val):
            current_pos = slider.val
            ax.set_xlim(current_pos - 5, current_pos + 5)
            fig.canvas.draw_idle()
        
        slider.on_changed(update)
        
        plt.savefig("Task3/Task3.png")
        plt.show()









