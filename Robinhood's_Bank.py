class Transaction:
    def __init__(self,account_no,amount,transaction_type):
        self.account_no = account_no
        self.amount = amount
        self.transaction_type = transaction_type
        
#------------------------End of Transaction Class-----------------------
        
class Account:
    def __init__(self,account_type,account_no):
        self.account_type = account_type
        self.balance = 0
        self.account_no = account_no
        self.loan_taken = 0
#------------------------End of Account Class-----------------------
        
class User:
    def __init__(self,name,email,address,account_type,password,bank):
        self.name = name
        self.email = email
        self.password = password
        self.address = address
        self.account_type = account_type
        bank.create_account(self)

    def deposit(self,amount,bank):
        bank.deposit(self,amount)

    def withdraw(self,amount,bank):
        bank.withdraw(self,amount)

    def show_balance(self):
        return self.account.balance
    
    def show_transactions(self,bank):
        bank.check_transactions(self.account.account_no)

    def apply_loan(self,amount,bank):
        bank.apply_loan(self,amount)

    def transfer_money(self,to_account,amount,bank):
        bank.transfer_money(self,to_account,amount)
    
    def __repr__(self):
        return f"Name: {self.name}, Email: {self.email}, Address: {self.address}, Account Number: {self.account.account_no}, Account Info: {self.account.account_type}, Balance: {self.account.balance}"
    
#--------------------------------End of User Class------------------------------
    
class Admin:
    def __init__(self,name,email,password,bank):
        self.name = name
        self.email = email
        self.password = password
        self.bank = bank
        self.bank.create_admin(self)

    def create_account(self,name,email,address,account_type,password):
        User(name,email,address,account_type,password,self.bank)

    def show_bank_balance(self):
        print(f"Bank Balance: {self.bank.get_bank_balance}")

    def show_total_loan_amount(self):
        self.bank.show_total_loan_amount()

    def show_users_accounts(self):
        self.bank.show_users_accounts()

    def on_loan_status(self):
        self.bank.on_loan_status()

    def off_loan_status(self):
        self.bank.off_loan_status()

    def delete_account(self,account_no):
        self.bank.delete_account(account_no)

    def __repr__(self):
        return f"Name: {self.name}, Email: {self.email}, Bank: {self.bank.bank_name}"

#------------------------End of Admin Class-----------------------


class Bank:
    def __init__(self,name,address,initial_amount) -> None:
        self.__name = name
        self.__address = address
        self.__admins = {} # email:admin
        self.__users = {} # account_no:user
        self.__transactions = {} # account_no:[transactions]
        self.__account_no = 1000
        self.__loans = {} # account_no:loan_amount
        self.__isLoanAvailable = True
        self.__bank_balance = initial_amount

    @property
    def bank_name(self):
        return self.__name
    
    @property
    def get_bank_balance(self):
        return self.__bank_balance
    
#------------------------Common-----------------------
    def create_account(self,user):
        account = Account(user.account_type,str(self.__account_no))
        user.account = account
        self.__users[account.account_no] = user
        self.__transactions[account.account_no] = []
        self.__loans[account.account_no] = 0
        self.__account_no+=1
        print(f"Account created successfully with account number {account.account_no}")
        
    
    def authenticate_user(self,user_name,password,type):
        if type=="admin":
            if user_name in self.__admins:
                if self.__admins[user_name].password==password:
                    return self.__admins[user_name]
                else:
                    print("Invalid Password")
            else:
                print("Admin not found")
        elif type=="user":
            if user_name in self.__users:
                if self.__users[user_name].password==password:
                    return self.__users[user_name]
                else:
                    print("Invalid Password")
            else:
                print("User not found")
        else:
            print("Invalid Type")


#---------------------------USER---------------------------
    def deposit(self,user,amount):
        if amount<=0:
            print("Invalid Amount") 
        else:
            user.account.balance+=amount
            self.__bank_balance+=amount
            transaction = Transaction(user.account.account_no,amount,"Credit")
            self.__transactions[user.account.account_no].append(transaction)
            print(f"Amount {amount} deposited successfully")

    def withdraw(self,user,amount):
        if amount<=0:
            print("Invalid Amount")
        elif user.account.balance<amount:
            print("Withdrawal amount exceeded")
        elif self.__bank_balance < amount:
            print("The bank is bankrupt and cannot process this withdrawal.")
        else:
            user.account.balance-=amount
            self.__bank_balance-=amount
            transaction = Transaction(user.account.account_no,amount,"Debit")
            self.__transactions[user.account.account_no].append(transaction)
            print(f"Amount {amount} withdrawn successfully")

    def check_transactions(self,account_no):
        if self.__transactions[account_no]==[]:
            print("No transactions made yet")
        else:
            print(f"Transaction Type\tAmount")
            for transaction in self.__transactions[account_no]:
                print(f"{transaction.transaction_type}\t\t\t{transaction.amount}")

    def apply_loan(self,user,amount):
        if self.__isLoanAvailable:
            if user.account.loan_taken==2:
                print("Cannot take more than 2 loans") 
            elif amount>0:
                if self.__bank_balance>=amount:
                    user.account.loan_taken+=1
                    user.account.balance+=amount
                    self.__bank_balance-=amount
                    self.__loans[user.account.account_no] += amount
                    transaction = Transaction(user.account.account_no,amount,"Credit")
                    self.__transactions[user.account.account_no].append(transaction)
                    print(f"Loan of {amount} credited successfully")
                else:
                    print("Bank cannot provide loan of this amount")
            else:
                print("Invalid Loan Amount")
        else:
            print("Loan not available")
    
    def transfer_money(self,from_account,to_account,amount):
        if amount<=0:
            print("Invalid Amount")
        elif from_account.account.balance<amount:
            print("Insufficient Balance to transfer")
        else:
            if to_account in self.__users:
                to_account = self.__users[to_account]
                from_account.account.balance-=amount
                to_account.account.balance+=amount
                transaction = Transaction(from_account.account.account_no,amount,"Debit")
                self.__transactions[from_account.account.account_no].append(transaction)
                transaction = Transaction(to_account.account.account_no,amount,"Credit")
                self.__transactions[to_account.account.account_no].append(transaction)
                print(f"Amount {amount} transferred successfully")
            else:
                print("Account does not exist")


#-----------------------ADMIN-----------------------
    def create_admin(self,admin):
        self.__admins[admin.email] = admin
        print("Admin created successfully")

    def delete_account(self,account_no):
        if account_no in self.__users:
            del self.__users[account_no]
            del self.__transactions[account_no]
            del self.__loans[account_no]
            print("Account deleted successfully")
        else:
            print("Account does not exist")

    def show_users_accounts(self):
        print("-----------------------------Users Accounts----------------------------")
        print("Name\t\tEmail\t\tAddress\t\tAccount Number\t\tAccount Type")
        for account_no in self.__users:
            user = self.__users[account_no]
            print(f"{user.name}\t\t{user.email}\t\t{user.address}\t\t{user.account.account_no}\t\t\t{user.account.account_type}")

    
    def show_total_loan_amount(self):
        total_loan_amount = 0
        print("-----------------------------Total Loan Amount----------------------------")
        print("Account Number\tLoan Amount")
        for account_no in self.__loans:
            if self.__loans[account_no]>0:
                print(f"{account_no}\t\t{self.__loans[account_no]}")
            total_loan_amount+=self.__loans[account_no]
        print(f"Total Loan Amount: {total_loan_amount}")

    def on_loan_status(self):
        if self.__isLoanAvailable:
            print("Loan is already available")
        else:
            self.__isLoanAvailable = True
            print("Loan is now available")
    
    def off_loan_status(self):
        if self.__isLoanAvailable:
            self.__isLoanAvailable = False
            print("Loan is now unavailable")
        else:
            print("Loan is already unavailable")
        
#-----------------------End of Bank Class-----------------------

        

# create a bank
bank = Bank("Robinhood's Bank","England",1000000)

# create an admin
admin = Admin("admin","admin","admin",bank)

# create some users
user1 = User("Rahim","test1","England","Savings Account","test1",bank)
user2 = User("Karim","test2","England","Current Account","test2",bank)
user3 = User("Miti","test3","England","Savings Account","test3",bank)
user4 = User("Mahi","test4","England","Current Account","test4",bank)
user5 = User("Jannat","test5","England","Savings Account","test5",bank)

user1.deposit(10000,bank)



def show_user_panel(user):
    print(f"-------Welcome {user.name}---------")
    while True:
        print("1. Deposit")
        print("2. Withdraw")
        print("3. Show Balance")
        print("4. Show Transactions")
        print("5. Apply Loan")
        print("6. Transfer Money")
        print("0. Logout")
        choice = input("Enter your choice: ")
        if choice=="1":
            amount = float(input("Enter Amount: "))
            user.deposit(amount,bank)
        elif choice=="2":
            amount = float(input("Enter Amount: "))
            user.withdraw(amount,bank)
        elif choice=="3":
            print(f"Balance: {user.show_balance()}")
        elif choice=="4":
            user.show_transactions(bank)
        elif choice=="5":
            amount = float(input("Enter Amount: "))
            user.apply_loan(amount,bank)
        elif choice=="6":
            to_account = input("Enter Account Number: ")
            amount = float(input("Enter Amount: "))
            user.transfer_money(to_account,amount,bank)
        elif choice=="0":
            break
        else:
            print("Invalid Choice")
        print()

def admin_panel(admin):
    print(f"-------Welcome {admin.name}---------")
    while True:
        print("1. Create Account")
        print("2. Show Bank Balance")
        print("3. Show Total Loan Amount")
        print("4. Show Users Accounts")
        print("5. On Loan Status")
        print("6. Off Loan Status")
        print("7. Delete Account")
        print("0. Logout")
        choice = input("Enter your choice: ")
        if choice=="1":
            name = input("Enter Name: ")
            email = input("Enter Email: ")
            address = input("Enter Address: ")

            print("Select Account Type")
            print("1. Savings Account")
            print("2. Current Account")
            acc_type=input("Enter your choice: ")
            while acc_type not in ["1","2"]:
                print("Invalid Choice")
                acc_type=input("Enter your choice: ")
            if acc_type=="1":
                account_type = "Savings Account"
            else:
                account_type = "Current Account"
            password = input("Enter Password: ")
            admin.create_account(name,email,address,account_type,password)
        elif choice=="2":
            admin.show_bank_balance()
        elif choice=="3":
            admin.show_total_loan_amount()
        elif choice=="4":
            admin.show_users_accounts()
        elif choice=="5":
            admin.on_loan_status()
        elif choice=="6":
            admin.off_loan_status()
        elif choice=="7":
            admin.show_users_accounts()
            account_no = input("Enter Account Number: ")
            admin.delete_account(account_no)
        elif choice=="0":
            break
        else:
            print("Invalid Choice")
        print()



while True:
    print(f"------Welcome to {bank.bank_name} ------")
    print("1. Admin")
    print("2. User")
    print("3. Exit")
    choice = input("Enter your choice: ")

    if choice=="1":
        email = input("Enter Email: ")
        password = input("Enter Password: ")
        admin = bank.authenticate_user(email,password,"admin")
        if admin:
            admin_panel(admin)
        else:
            print("Invalid Credentials")
            
    elif choice=="2":
        print("1. Create Account")
        print("2. Login")
        choice = input("Enter your choice: ")
        if choice=="1":
            name = input("Enter Name: ")
            email = input("Enter Email: ")
            address = input("Enter Address: ")

            print("Select Account Type")
            print("1. Savings Account")
            print("2. Current Account")
            acc_type=input("Enter your choice: ")
            while acc_type not in ["1","2"]:
                print("Invalid Choice")
                acc_type=input("Enter your choice: ")
            if acc_type=="1":
                account_type = "Savings Account"
            else:
                account_type = "Current Account"
            password = input("Enter Password: ")
            user = User(name,email,address,account_type,password,bank)
            show_user_panel(user)
        elif choice=="2":
            account_number = input("Enter Account Number: ")
            password = input("Enter Password: ")
            user = bank.authenticate_user(account_number,password,"user")
            if user:
                show_user_panel(user)
            else:
                print("Invalid Credentials")
        else:
            print("Invalid Choice")
        print()
    elif choice=="3":
        break
    else:
        print("Invalid Credentials")
    print()

