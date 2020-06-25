import db_tools


class receipt:

    def __init__(self, flat: str, date: str, month: str, amount: float, fine: float, mode: str, month_till: str = None, ref: str = None):
        self.flat = flat
        self.date = date
        self.month = month
        self.month_till = month_till
        self.amount = amount
        self.fine = fine
        self.mode = mode
        self.ref = ref

    def add_to_db(self):
        db_tools.add_to_db(table='records', attributes=[self.date, self.flat, self.month, self.month_till, self.amount,
                                                        self.fine, self.mode, self.ref])