# It was a pleasure talking to you today. As we discussed, here's the task that you need to code so I can share it with my developers.
 
# Use case:
# A Lenmo borrower would like to borrower $5,000.00 on paying them back on 6 months period. One of Lenmo investors has offered him 15% Annual Interest Rate. A $3.00 Lenmo fee will be added to the total loan amount to be paid by the investor.  
 
# Requirements:
# You are required to develop a code using Python language for the following flow;
 
# The borrower submits a loan request including the above loan amount and loan period 
# The investor will submit an offer with the above interest rate
# The borrower will accept the offer
# Check if the investor has sufficient balance in their account before they fund the loan
# The loan will be funded successfully and the loan status will be changed to `Funded` 
# The loan payment will be scheduled successfully on the system
# Once all the payments are successfully paid, the loan status will be `Completed`  

class OpenMarket:
	borrowers = {}
	investors = {}
	loans = {}
	loan_requests = {}

	def generate_id():
		return uuid.uuid4()

	# creates a borrower and adds to the borrowers dictionary
	#    returns the id of the created borrower
	def create_borrower(self, name):
		new_borrower = Borrower(name)
		new_borrower_id = id(new_borrower)
		self.borrowers[new_borrower_id] = new_borrower
		print 'A borrower named ' + name + ' with id ' + str(new_borrower_id) +' was added in the system'
		return new_borrower_id

	# processes an borrower depositing money to increase the borrower's balance
	#    returns the True if successful and False otherwise
	def borrower_deposits(self, borrower_id, amount):
		if borrower_id in self.borrowers:
			borrower = self.borrowers[borrower_id]
			borrower.deposits(amount)
			print 'A borrower depositing was successful. New balance is ' + str(borrower.get_balance())
			return True
		else:
			print 'An borrower depositing cannot be processed. Cannot find the borrower with id ' + str(borrower_id) + ' in the system.'
			return False

	# creates an investor and adds to the investors dictionary
	#    returns the id of the created investor
	def create_investor(self, name):
		new_investor = Investor(name)
		new_investor_id = id(new_investor)
		self.investors[new_investor_id] = new_investor
		print 'An investor named ' + name + ' with id ' + str(new_investor_id) +' was added in the system'
		return new_investor_id

	# processes an investor depositing money to increase the investor's balance
	#    returns the True if successful and False otherwise
	def investor_deposits(self, investor_id, amount):
		if investor_id in self.investors:
			investor = self.investors[investor_id]
			investor.deposits(amount)
			print 'An investor depositing was successful. New balance is ' + str(investor.get_balance())
			return True
		else:
			print 'An investor depositing cannot be processed. Cannot find the investor with id ' + str(investor_id) + ' in the system.'
			return False

	# print balances of all borrowers and investors
	def print_balances(self):
		print '\n*****'
		print 'Borrowers:'
		for borrower_id in self.borrowers:
			borrower = self.borrowers[borrower_id]
			print borrower.name + " has a balance of " + str(borrower.get_balance())
		print '\nInvestors:'
		for investor_id in self.investors:
			investor = self.investors[investor_id]
			print investor.name + " has a balance of " + str(investor.get_balance())
		print '*****\n'


	# processes a loan request and adds it to the loan_requests dictionary
	#    returns the id of the created loan request if successful and False otherwise
	def submit_loan_request(self, borrower_id, amount, period):
		if borrower_id in self.borrowers:
			borrower = self.borrowers[borrower_id]
			new_loan_request = Loan_Request(borrower, amount, period)
			new_loan_request_id = id(new_loan_request)
			self.loan_requests[new_loan_request_id] = new_loan_request
			print 'A loan request with id ' + str(new_loan_request_id) + ' was processed in the system. The loan amount is ' + str(amount) + ' and loan period is ' + str(period) + '. It was submitted by a borrower named ' + borrower.name + ' with id ' + str(borrower_id)
			return new_loan_request_id
		else:
			print 'A loan request cannot be processed. Cannot find a borrower in the system with id ' + str(borrower_id)
			return False

	# processes an investor offering an interest rate to a loan request
	#    returns True if successful and False otherwise
	def investor_offers(self, investor_id, loan_request_id, interest_rate):
		if loan_request_id in self.loan_requests and investor_id in self.investors:
			loan_request = self.loan_requests[loan_request_id]
			investor = self.investors[investor_id]
			if not loan_request.is_offered():
				loan_request.set_interest_rate(interest_rate, investor)
				print 'An investor named ' + investor.name + ' with id ' + str(investor_id) + ' has successfully offered an interest rate of ' + str(interest_rate) + ' to a loan request with id ' + str(loan_request_id)
				return True
			else:
				print 'An investor offer cannot be processed. Loan request with id ' + str(loan_request_id) + ' already has an offer'
				return False
		else:
			print 'An investor offer cannot be processed. Either cannot find a loan request with id ' + str(loan_request_id) + ' or an investor with id ' + str(investor_id) + ' in the system.'
			return False

	# processes that the borrower accepts the investor offer by checking if investor has sufficient balance
	#   returns the id of the loan if succesful and False otherwise
	def borrower_accepts(self, loan_request_id):
		if loan_request_id in self.loan_requests:
			loan_request = self.loan_requests[loan_request_id]
			borrower = loan_request.get_borrower()
			investor = loan_request.get_investor()
			amount = loan_request.get_amount()
			period = loan_request.get_period()
			interest_rate = loan_request.get_interest_rate()
			investor_balance = investor.get_balance()
			if not loan_request.is_matched():
				if amount <= investor_balance:
					loan_request.set_matched()
					new_loan = Loan(borrower, investor,amount, period, interest_rate)
					new_loan_id = id(new_loan)
					self.loans[new_loan_id] = new_loan
					borrower.borrows(amount)
					investor.loans(amount)
					print 'A borrower accepting was successful. New accepted loan with id ' + str(new_loan_id)+ ' was processed in the system. The loan balance is ' + str(new_loan.get_amount()) + ' to be paid in ' + str(period) +' months'
					return new_loan_id
				else: 
					print 'A borrower accepting cannot be processed. The investor named ' + investor.name + ' has insufficient funds.'
					return False
			else:
				print 'A borrower accepting cannot be processed. Loan request with id ' + str(loan_request_id) + ' already has been matched'
				return False
		else:
			print 'A borrower accepting cannot be processed. Cannot find a loan request with id ' + str(loan_request_id) + ' in the system.'
			return False

	# processes that the borrower paying the loan. Also checks if borrower has sufficient balance before paying
	#   returns True if succesful and False otherwise
	def borrower_pays(self, loan_id):
		if loan_id in self.loans:
			loan = self.loans[loan_id]
			borrower = loan.get_borrower()
			investor = loan.get_investor()
			amount = loan.get_amount()
			borrower_balance = borrower.get_balance()
			if amount <= borrower_balance:
				borrower.pays(amount)
				investor.gets_paid(amount)
				loan.set_completed()
				print 'A borrower paying was successful. Loan with id ' + str(loan_id)+ ' was paid in full amount.'
				return True
			else: 
				print 'A borrower paying cannot be processed. The borrower named ' + borrower.name + ' has insufficient funds.'
				return False
		
		else:
			print 'A borrower paying cannot be processed. Cannot find a loan  with id ' + str(loan_id) + ' in the system.'
			return False


class Borrower:
	balance = 0
	loan_list = []
	name = None
	def __init__(self, name):
		self.name = name
	def borrows(self, amount): self.balance += amount
	def pays(self, amount): self.balance -= amount
	def deposits(self, amount): self.balance += amount
	def get_balance(self): return self.balance

class Investor:
	balance = 0
	loan_list = []
	name = None
	def __init__(self, name):
		self.name = name
	def get_balance(self): return self.balance
	def deposits(self, amount): self.balance += amount
	def gets_paid(self, amount): self.balance += amount
	def loans(self, amount): self.balance -= amount

class Loan_Request:
	borrower = None
	investor = None
	amount = None
	period = None # in months
	interest_rate = None
	offered = False
	matched = False
	def __init__(self, borrower, amount, period):
		self.borrower = borrower
		self.amount = amount
		self.period = period
	def set_interest_rate(self, interest_rate, investor):
		self.interest_rate = interest_rate
		self.offered = True
		self.investor = investor
	def is_offered(self): return self.offered
	def is_matched(self): return self.matched
	def get_borrower(self): return self.borrower
	def get_investor(self): return self.investor
	def get_amount(self): return self.amount
	def get_period(self): return self.period
	def get_interest_rate(self): return self.interest_rate
	def set_matched(self): self.matched = True

class Loan:
	borrower = None
	investor = None
	amount = None
	period = None # in months
	status = 'Funded'
	def __init__(self, borrower, investor,amount, period,interest_rate):
		self.borrower = borrower
		self.investor = investor
		self.period = period
		amount_with_interest = amount * pow(1 + interest_rate,period/12.0)
		fee = max(3,0.01 * (amount_with_interest))
		self.amount = amount_with_interest + fee
	def get_amount(self): return self.amount
	def get_borrower(self): return self.borrower
	def get_investor(self): return self.investor
	def set_completed(self): self.status = 'Completed'

# initialize the market
market = OpenMarket();
bryan_id = market.create_borrower(name='Bryan')
ian_id = market.create_investor(name='Ian')
market.print_balances()

# loan request
loan_request_id = market.submit_loan_request(bryan_id, 5000, 6)
market.investor_offers(ian_id, loan_request_id, 0.15)
market.print_balances()

# loan approval
market.investor_deposits(ian_id, 5000)
market.print_balances()
loan_id = market.borrower_accepts(loan_request_id)
market.print_balances()

# loan repayment
market.borrower_deposits(bryan_id, 1000)
market.print_balances()
market.borrower_pays(loan_id)
market.print_balances()



