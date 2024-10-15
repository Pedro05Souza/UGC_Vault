__all__ = ['User']

class User():

    __slots__ = ['__user_id', '__balance']

    def __init__(self, user_id, balance):
        self.__user_id = user_id
        self.__balance = balance

    @property
    def user_id(self):
        return self.__user_id
    
    @property
    def balance(self):
        return self.__balance
    
    @balance.setter
    def balance(self, value):
        self.__balance = value

    def __str__(self):
        return f"User {self.__user_id} has {self.__balance} coins."
