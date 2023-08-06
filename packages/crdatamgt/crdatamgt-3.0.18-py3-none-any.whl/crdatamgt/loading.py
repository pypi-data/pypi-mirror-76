import os
import sys


class loading():
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"



    def __init__(self, total, current=1, additional_text=None):
        self.totals = total
        self.current = current
        if additional_text:
            self.additional_text = additional_text
        else:
            self.additional_text = f"Compiling data: \n\n\n"


    def __iter__(self):
        return self

    def __next__(self):
        if self.current < self.totals:
            self.current += 1
            self.clear()
            print(self.__repr__())
        else:
            pass

    def __repr__(self):
        complete = max(int((self.current / self.totals) * 100), 1)
        left = 100 - complete
        cur_rep = f"[{self.OKGREEN}{''.join(['*' for _ in range(complete)])}{self.ENDC}"
        left_rep = f"{self.FAIL}{''.join('-' for _ in range(left))}{self.ENDC}] "
        sys.stdout.flush()
        return f" {cur_rep + left_rep}"

    def clear(self):
        if os.name in ('nt', 'dos'):
            os.system('cls')
        else:
            print("\n") * 120