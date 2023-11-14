from uuid import uuid4
import itertools
import pickle

"""
Persistent teller -> save data when done, quit, next time load your data after making your bank
"""

class Person:

    # I want to give people unique ids at my bank
    def __init__(self, first_name, last_name, age=0):
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.id = uuid4().hex


class Account:

    # I want to generate an account number when its created
    new_account_number = itertools.count()

    # I should update this to make sure owner_id is a customer(Person) id
    def __init__(self, owner_id, account_type, balance=0):
        self.owner = owner_id
        self.account_type = account_type
        self.balance = balance
        self.number = next(Account.new_account_number)


class Bank:

    def __init__(self, name):
        self.name = name
        self.bank_id = uuid4().hex
        self.accounts = []
        self.customers = []

    def add_customer(self, person: Person) -> bool:
        if person in self.customers:
            return False
        else:
            self.customers.append(person)
            return True

    def create_account(self, person: Person, acct_type: str, initial_deposit: int):

        # For now, this is how I'm getting owner id of a customer linked to an account at creation
        acct_owner_id = getattr(person, 'id')
        create_new_account = Account(acct_owner_id, acct_type, initial_deposit)
        self.accounts.append(create_new_account)
        return create_new_account.number

    def delete_account(self, acct_num: int):

        for account in self.accounts:
            if account.number == acct_num:
                self.accounts.pop(account)

    def deposit_money(self, acct_num: int, amount: int):

        for account in self.accounts:
            if account.number == acct_num:
                account.balance = account.balance + amount

    def withdraw_money(self, acct_num: int, amount: int):

        for account in self.accounts:
            if account.number == acct_num:
                account.balance = account.balance - amount

    def get_balance(self, acct_num: int):
        acct_balance = 'No Balance'
        for account in self.accounts:
            if account.number == acct_num:
                acct_balance = account.balance / 100

        return acct_balance

    def save_data(self):
        customers_to_write = self.customers
        PersistenceUtils.write_pickle('bank_customers.pkl', customers_to_write)
        accounts_to_write = self.accounts
        PersistenceUtils.write_pickle('bank_accounts.pkl', accounts_to_write)

    def load_data(self):

        self.customers = PersistenceUtils.load_pickle('bank_customers.pkl')
        self.accounts = PersistenceUtils.load_pickle('bank_accounts.pkl')


class PersistenceUtils:

    @staticmethod
    def write_pickle(file_to_write: str, list_to_write: list):

        with open(file_to_write, 'wb') as f:
            pickle.dump(list_to_write, f)
            f.close()

    @staticmethod
    def load_pickle(file_to_load: str) -> list:

        with open(file_to_load, 'rb') as f:
            temp_list = pickle.load(f)

        return temp_list


"""
Test program to play with the functions and classes
"""
if __name__ == '__main__':

    person_bob = Person('Bob', 'Smith', 34)
    person_karen = Person('Karen', 'Jones', 45)
    person_kevin = Person('Kevin', 'Johnson', 56)

    my_bank = Bank("Mike's Bank")

    my_bank.add_customer(person_bob)
    my_bank.add_customer(person_karen)
    my_bank.add_customer(person_kevin)

    acct_1 = my_bank.create_account(person_bob, 'CHECKING', 34382)
    acct_2 = my_bank.create_account(person_bob, 'SAVING', 50000)
    acct_3 = my_bank.create_account(person_karen, 'CHECKING', 232450)
    acct_4 = my_bank.create_account(person_bob, 'MONEYMARKET', 1000000)

    print(f'Accounts Auto-generated IDs: {acct_1}, {acct_2}, {acct_3}, {acct_4}')

    print(f'Account 0 balance was: {my_bank.get_balance(acct_1)}')
    my_bank.deposit_money(acct_1, 42525)
    test_balance = my_bank.get_balance(acct_1)
    print(f'Account 0 balance is: {test_balance}\n')

    print(f'Account 2 balance was: {my_bank.get_balance(acct_3)}')
    my_bank.deposit_money(acct_3, 40075)
    test_balance2 = my_bank.get_balance(acct_3)
    print(f'Account 2 balance is: {test_balance2}\n')

    print(f'Account 1 balance was: {my_bank.get_balance(acct_2)}')
    my_bank.withdraw_money(acct_2, 10000)
    test_balance3 = my_bank.get_balance(acct_2)
    print(f'Account 1 balance is: {test_balance3}')
