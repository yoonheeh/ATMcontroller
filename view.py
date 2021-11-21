from models import Account

def showAllView(list):
   print(list)

def startView():
   print ('Please insert your card')

def insertCardErrorView():
    print("Invalid card")

def authentificationFailedView():
    print ("Authentification failed. Please enter correct password.")

def accountLockedView():
    print("Wrong authentification too many times. Your account is temporarily locked.")
    print("Please call xxx-xxx-xxxx for assistance.")

def verifyingView():
    print('Verifying...')

def enterPINView():
    print('Please enter your pin')

def selectAccountView():
    print("Please enter 'S' for savings or 'C' for checking account")

def invalidSelectionView():
    print("Please enter either 'S' or 'C'")

def chooseTransactionView(account_type):
    print("Transaction for account type {}".format(account_type))
    print("Please choose the options from below:")
    print("1: See balance")
    print("2: Make deposit")
    print("3: Withdraw cash")
    print("4: Exit")
    print("Enter 1, 2, 3 or 4 ")

def showBalanceView(balance):
    print("Your current balance: ${}".format(balance))

def makeDepositView():
    print("Please insert cash in the drawer")

def makeDepositVerifyAmountView(amount):
    print("You have inserted ${}".format(amount))

def transactionInProgressView():
    print("Transaction in progress....")

def withdrawCashView():
    print("Enter dollar amount (whole number) to withdraw")

def notEnoughATMBalanceView():
    print("There is not enough balance in the ATM to dispense cash.") 
    print("Please contact xxx-xxx-xxxx for assistance.")
    print("We apologize for inconvenience. ")

def notEnoughAccountBalanceView():
    print("There is not enough balance on your account.")

def updateAccountBalanceSuccessView():
    print("Account balance is successfully updated.")

def endView():
    print ('Thank you for using the service.')

class AccountView(object):

    def __init__(self, account):
        self.account = account
   
    def showBalance(self, account_type):
        for sub_account in self.account["sub_accounts"]:
            if sub_account["account_type"] == account_type:
                return sub_account["balance"]
        return False # account not found
