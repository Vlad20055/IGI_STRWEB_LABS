def my_range(first=0, last=0, step=1):
    now  = first
    while now < last:
        yield now
        now += step


r = my_range(1, 11)

for i in r:
    print(i, end=" ")

for i in r:
    print(i, end=" ")




