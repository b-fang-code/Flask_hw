import asyncio
from random_array import arr
import time


async def calculate_partial_sum(arr, start, end):
    partial_sum = sum(arr[start:end])
    return partial_sum


async def main():
    start_time = time.time()
    num_chunks = 4
    chunk_size = len(arr) // num_chunks
    chunks = [(i * chunk_size, (i + 1) * chunk_size) for i in range(num_chunks)]
    chunks[-1] = (chunks[-1][0], len(arr))

    tasks = [calculate_partial_sum(arr, start, end) for start, end in chunks]
    partial_sums = await asyncio.gather(*tasks)

    # Вычисляем общую сумму
    total_sum = sum(partial_sums)

    print(f"Общая сумма элементов массива: {total_sum} подсчитана за {time.time() - start_time} секунд")


asyncio.run(main())
