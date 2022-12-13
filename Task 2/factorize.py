from multiprocessing import Process
from multiprocessing import Pool, cpu_count
from time import time


def factorize(*args):
    result = []
    for el in args:
        result.append([number for number in range(1, el + 1) if el % number == 0])
    
    return result


if __name__ == '__main__':
    t1 = time()
    result = factorize(128, 255, 99999, 10651060)
    print(f'Synchronous method: {time() - t1}')
    print(result)

    n = cpu_count()
    t2 = time()
    with Pool(processes=n) as pool:
        result = pool.map(factorize, (128, 255, 99999, 10651060))
    print(f'Multiprocessing method: {time() - t2}')
    print(list(result))