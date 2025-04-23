import math as m
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

class Figure:
    def __init__(self, label):
        self.label = label
    
    def square(self):
        pass


class Figure_color:
    def __init__(self, color):
        self.inside_color = color

    @property
    def color(self):
        return self.inside_color
    
    @color.setter
    def color(self, color):
        self.inside_color = color


class Rectangle(Figure):
    def __init__(self, width, height, label, color="green"):
        super().__init__(label)
        self.color = Figure_color(color)
        self.width = width
        self.height = height
    
    def square(self):
        return self.width * self.height
    

class Circle(Figure):
    def __init__(self, radius, label, color="green"):
        super().__init__(label)
        self.color = Figure_color(color)
        self.radius = radius

    def square(self):
        return m.pi * self.radius * self.radius


class Romb(Figure):
    def __init__(self, diag1, diag2, label, color="green"):
        super().__init__(label)
        self.color = Figure_color(color)
        self.diag1 = diag1
        self.diag2 = diag2

    def square(self):
        return self.diag1 * self.diag2 * 0.5
    

class Square(Figure):
    def __init__(self, a, label, color="green"):
        super().__init__(label)
        self.color = Figure_color(color)
        self.a = a

    def square(self):
        return self.a * self.a
    

class Right_triangle(Figure):
    def __init__(self, a, label, color="green"):
        super().__init__(label)
        self.color = Figure_color(color)
        self.a = a

    def __str__(self):
        return "Right triangle:\n  Side a = {}\n  Color = {}\n  Square = {}".format(self.a, self.color.color, self.square())
    
    def square(self):
        return self.a * self.a * m.sqrt(3) / 4
    
    def draw(self):
        height = self.a * m.sqrt(3) / 2 
        vertices = [
            [0, 0],          
            [self.a, 0],     
            [self.a / 2, height]
        ]
        
        fig, ax = plt.subplots()
        triangle = Polygon(vertices, closed=True, color=self.color.color)
        
        ax.add_patch(triangle)
        ax.set_xlim(0, self.a)
        ax.set_ylim(0, height)
        ax.axis("on")
        ax.set_aspect('equal')
        ax.set_title(label=self.label)

        plt.savefig("Task4/Task4.png")
        plt.show()




