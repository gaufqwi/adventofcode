from time import perf_counter_ns

class AOCProblem:
    def __init__(self, data, log):
        self.data = data
        self.log = log
        self.starttime = perf_counter_ns()

    def elapsed(self):
        t = perf_counter_ns() - self.starttime
        return f'{t/1e9:.2f}'

    def common(self):
        pass

    def do_part(self, part):
        self.common()
        getattr(self, f'part{part}')()
        print(f'Total execution time was {self.elapsed()}')