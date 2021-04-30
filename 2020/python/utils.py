from time import perf_counter

def timer(f):
    def inner(*args, **kwargs):
        start = perf_counter()
        val = f(*args, **kwargs)
        end = perf_counter()
        runtime = end - start
        print(f'Elapsed time: {runtime * 1000:.2f} ms')
        return val
    return inner


def bench(runs=100):

    def bench_deco(f):

        def inner(*args, **kwargs):
            total_time = 0
            for _ in range(runs or 1):
                start = perf_counter()
                val = f(*args, **kwargs)
                end = perf_counter()
                total_time += end - start
            runtime = total_time / runs
            print(f'Average time: {runtime * 1000:.2f} ms/run over {runs} runs')
            return val

        return inner
    return bench_deco


def strip_suffix(text, in_order_suffix):
    for letter in reversed(in_order_suffix):
        text = text.rstrip(letter)
    return text


def strip_prefix(text, prefix):
    for letter in prefix:
        text = text.lstrip(letter)
    return text