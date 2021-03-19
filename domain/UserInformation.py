class UserInformation:
    def __init__(self, **kwargs):
        self.user_id = kwargs['user_id']
        self.user_name = kwargs['user_name']
        self.free_money_amount = kwargs['free_money_amount']
        self.total_money_amount = kwargs['total_money_amount']
        self.history_money_amount = kwargs['history_money_amount']

    def __str__(self):
        return "('{}','{}',{},{},{})".format(self.user_id, self.user_name,
                                             self.free_money_amount,
                                             self.total_money_amount,
                                             self.history_money_amount)


if __name__ == "__main__":
    user_information = UserInformation(user_id=114514, user_name="野兽先辈",
                                       free_money_amount=5, total_money_amount=50, history_money_amount=500)
    print(user_information)
