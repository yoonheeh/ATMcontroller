from models import Account, ATM
import view, utils
import getpass

class Controller(object):
    def __init__(self):
        self.atm = ATM()
        self.accountDB = Account()
        self.authorized = False
        self.authFailCount = 0

    def start(self):
        view.startView()
        self.insertCard()

    def insertCard(self):
        user_input = self.atm.getAccountNumber()
        account = self.accountDB.getAccount(user_input)
        if (account != False): 
            self.av = view.AccountView(account)
            self.account = account
            self.enterPIN()
        else:
            view.insertCardErrorView()
            self.start() # restart

    def enterPIN(self):
        view.enterPINView()
        user_input = getpass.getpass()
        token = utils.encrypt(user_input)
        view.verifyingView()
        if not (self.account["account_locked"]):
            if self.account["access_token"] == token:
                self.authorized = True # should be in account?
                self.selectAccount()
            else:
                self.authFailCount += 1
                view.authentificationFailedView()
                if (self.authFailCount < 3):
                    self.enterPIN()
                else:
                    self.account["account_locked"] = True
                    self.accountDB.updateDB(self.account)
                    view.accountLockedView()
                    self.endTransaction()

    def selectAccount(self):
        view.selectAccountView()
        user_input = input()
        if (user_input == "s" or user_input == "S"):
            self.account_type = "Savings"
            self.chooseTransaction()
        elif (user_input == "c" or user_input == "C"):
            self.account_type = "Checking"
            self.chooseTransaction()
        else:
            view.invalidSelectionView()
            self.selectAccount()
    
    def chooseTransaction(self):
        "Allow users to choose which transaction they want to perform"
        view.chooseTransactionView(self.account_type)
        user_input = input()
        if (user_input == "1"):
            self.showBalance()
        elif (user_input == "2"):
            self.makeDeposit()
        elif (user_input == "3"):
            self.withdrawCash()
        elif (user_input == "4"):
            self.endTransaction()
        else:
            print("invalid input")
            self.chooseTransaction()

    def showBalance(self):
        if (self.authorized):
            balance = self.av.showBalance(self.account_type)
            view.showBalanceView(balance)
            self.chooseTransaction()

    def makeDeposit(self):
        if (self.authorized):
            view.makeDepositView()
            amount_inserted = int(self.atm.getInsertedAmount())
            view.makeDepositVerifyAmountView(amount_inserted)
            view.transactionInProgressView()

            # update account balance
            self.updateAccountBalance(amount_inserted)

            # update ATM balance
            self.atm.deposit(amount_inserted)
            
            # Return to main menu
            self.chooseTransaction()

    def getAccountBalance(self):
        for sub_account in self.account["sub_accounts"]:
            if sub_account["account_type"] == self.account_type:
                return sub_account["balance"]

    def updateAccountBalance(self, amount_inserted):
        for sub_account in self.account["sub_accounts"]:
            if sub_account["account_type"] == self.account_type:
                sub_account["balance"] += amount_inserted

        self.accountDB.updateDB(self.account)
        view.updateAccountBalanceSuccessView()

        # show updated balance
        view.showBalanceView(self.av.showBalance(self.account_type))

    def withdrawCash(self):
        if (self.authorized):
            view.withdrawCashView()
            user_input = input()
            view.transactionInProgressView()

            # update ATM balance
            amount_entered = -1 * int(user_input)

            # check account and ATM balance before dispensing 
            if ((self.atm.getBalance() + amount_entered >= 0) and (self.getAccountBalance() + amount_entered >= 0)):
                self.atm.withdraw(amount_entered)
                self.updateAccountBalance(amount_entered)
                self.chooseTransaction()
            elif (self.getAccountBalance() + amount_entered < 0):
                view.notEnoughAccountBalanceView()
                self.endTransaction()
            elif (self.atm.getBalance() + amount_entered < 0):
                view.notEnoughATMBalanceView()
                self.atm.alertBank(1)
                self.endTransaction()

    def endTransaction(self):
        view.endView()
        self.start()

if __name__ == "__main__":
    controller = Controller()
    controller.start()