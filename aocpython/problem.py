class AOCProblem:
    def __init__(self, data, log):
        self.data = data
        self.log = log

    def common(self):
        pass

    def do_part(self, part):
        self.common()
        getattr(self, f'part{part}')()