import json
import utils

# assume that user database is stored in a json file
# in the following format

'''
{
    accounts: [{
        account_name: str,
        balance: int,
    }]
}
'''

class ATM(object):
    def __init__(self):
        self.balance = 0

    def getAccountNumber(self):
        "Read inserted card and get account number"
        account_number = input() #TODO get from machine
        return account_number
    
    def getBalance(self):
        return self.balance
    
    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        self.balance -= amount

    def getInsertedAmount(self):
        "Communicate with ATM machine to figure out how much is inserted"
        amount_inserted = input() #TODO get from machine
        return amount_inserted

    def alertBank(error_number):
        '''
        Alert bank when 
        1) there is not enough cash left on the machine
        2) something wrong with the machine
        '''
        if (error_number == 1):
            return "Not enough cash left on the machine"
        elif (error_number == 2):
            return "Something went wrong with the machine"

        return "Unknown error" 

class Account(object):
    def __init__(self):
        db_file = open('./resources/sample_db.json', 'r')
        self.db = json.load(db_file)

    def getAccount(self, account_number):
        for account in self.db["accounts"]:
            if (account["account_number"] == int(account_number)):
                self.account = account
                return account
        return False # No matching account found

    def updateDB(self, account_obj):
        db_file = open('./resources/sample_db.json', 'w')

        account_number = account_obj["account_number"]
        for account in self.db["accounts"]:
            if account["account_number"] == account_number:
                account = account_obj # update
        json.dump(self.db, db_file)
        #self.db = json.load(db_file)



    
