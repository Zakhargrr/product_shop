# скрипт программы для 1-го задания
def print_numbers(n):
    for i in range(n + 1):
        for j in range(i):
            print(i, end='')


n = int(input("Введите количество элементов последовательности: "))
print_numbers(n)