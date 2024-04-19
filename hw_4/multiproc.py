import multiprocessing
from random_array import arr
import time


def calculate_partial_sum(arr, start, end, result_queue):
    partial_sum = sum(arr[start:end])
    result_queue.put(partial_sum)


if __name__ == "__main__":
    start_time = time.time()
    num_processes = 8
    chunk_size = len(arr) // num_processes
    chunks = [(i * chunk_size, (i + 1) * chunk_size) for i in range(num_processes)]
    chunks[-1] = (chunks[-1][0], len(arr))

    result_queue = multiprocessing.Queue()

    processes = []
    for start, end in chunks:
        process = multiprocessing.Process(target=calculate_partial_sum, args=(arr, start, end, result_queue))
        process.start()
        processes.append(process)

    for process in processes:
        process.join()

    total_sum = 0
    while not result_queue.empty():
        total_sum += result_queue.get()

    print(f"Общая сумма элементов массива: {total_sum} подсчитана за {time.time() - start_time} секунд")
