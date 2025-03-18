import circle as cr
import square as sq

r = float(input("Введите радиус круга:"))
a = float(input("Введите сторону квадрата:"))

print("Периметр круга = ", cr.perimeter(r))
print("Площадь круга = ", cr.area(r))

print("Периметр квадрата = ", sq.perimeter(a))
print("Площадь квадрата = ",sq.area(a))
