import db_tools
import tools


class receipt:

    def __init__(self, flat: str, date: str, amount: str, mode: str, ref: str = None):
        self.flat = flat
        self.date = date
        self.amount = amount
        self.mode = mode
        self.ref = ref