# Напишите программу на Python, которая будет находить
# сумму элементов массива из 1000000 целых чисел.
# Пример массива: arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, ...]
# Массив должен быть заполнен случайными целыми числами от 1 до 100.
# При решении задачи нужно использовать многопоточность,
# многопроцессорность и асинхронность.
# В каждом решении нужно вывести время выполнения
# вычислений.

import threading
from random_array import arr
import time


def calculate_partial_sum(arr, start, end, result):
    partial_sum = sum(arr[start:end])
    result.append(partial_sum)


start_time = time.time()

num_threads = 8
chunk_size = len(arr) // num_threads
chunks = [(i * chunk_size, (i + 1) * chunk_size) for i in range(num_threads)]
chunks[-1] = (chunks[-1][0], len(arr))

results = []

threads = []
for start, end in chunks:
    thread = threading.Thread(target=calculate_partial_sum, args=(arr, start, end, results))
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()

total_sum = sum(results)

print(f"Общая сумма элементов массива: {total_sum} подсчитана за {time.time() - start_time} секунд")
