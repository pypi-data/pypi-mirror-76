class loading:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"

    def __init__(self, total, current=1, additional_text=None, size=33):
        self.totals = total
        self.current = current
        if additional_text:
            self.additional_text = additional_text
        else:
            self.additional_text = f"Compiling data"
        self.size = size

    def __iter__(self):
        return self

    def __next__(self):
        if self.current < self.totals:
            self.current += 1
            print(self.__repr__(), sep=" ", end="", flush=True)
        else:
            print(f"\t{self.HEADER}Finished{self.ENDC}")

    def __repr__(self):
        complete = max(int((self.current / self.totals) * self.size), 1)
        left = self.size - complete
        cur_rep = f"[{self.OKGREEN}{''.join(['=' for _ in range(complete)])}{self.ENDC}"
        left_rep = f"{self.FAIL}{''.join('-' for _ in range(left))}{self.ENDC}] "
        return f"\r{self.OKBLUE}{self.additional_text}{self.ENDC}\t{cur_rep + left_rep}{self.BOLD}{round(complete*(100/self.size), 1)}{self.ENDC}%"
