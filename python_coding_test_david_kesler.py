"""

Completed by David Kesler, thedavidkesler@gmail.com, 2018-06-13
"""


class SalesRep(object):
    """
    Models a sales representative. Sales representatives know
    their own names and which accounts are assigned to them.
    """
    def __init__(self, first_name, last_name, accounts=None):
        self.first_name = first_name
        self.last_name = last_name
        self._accounts = []

        if accounts:
            self._accounts.extend(accounts)

    def __str__(self):
        return "{self.first_name} {self.last_name}".format(self=self)

    def get_accounts(self):
        return self._accounts

    def add_account(self, account):
        self._accounts.append(account)
        account.set_sales_rep(self)

    def remove_account(self, account):
        self._accounts.remove(account)
        account.set_sales_rep(None)

      
class MarketSegment(object):
    """
    Models a MarketSegment. MarketSegments know their name and contain an
    iterable of the Accounts they're related to.
    """
    def __init__(self, name, accounts=None):
        self.name = name
        self._accounts = []
        if accounts:
            self._accounts.extend(accounts)

    def __str__(self):
        return "{self.name}".format(self=self)

    def get_accounts(self):
        return self._accounts

    def add_account(self, account):
        """
        Validates that the same account name has not already been added to market segment.
        """
        i = 0
        for account_item in self._accounts:
            if account_item.name == account.name:
                i += 1
        if i == 0:
            self._accounts.append(account)

    def remove_account(self, account):
        self._accounts.remove(account)
        

class Account(object):
    """
    Models an account. Accounts know their name, the sales rep they're
    assigned to, and the market segments they're a part of.
    """
    def __init__(self, name, sales_rep=None, market_segments=None):
        self.name = name
        self._sales_rep = sales_rep
        self._market_segments = []
        self._children = []

        if market_segments:
            self._market_segments.extend(market_segments)       

    def __str__(self):
        return "{self.name}".format(self=self)

    def get_sales_rep(self):
        return self._sales_rep
    
    def set_sales_rep(self, sales_rep):
        self._sales_rep = sales_rep

    def set_market_segments(self, segments):
        """
        Checks list of market segments associated with account and, if name matches, removes
        account from each market segment with which it is currently associated.
        """       
        for market_segment in self._market_segments:
            i = 0
            for account in market_segment._accounts:
                if self.name == market_segment._accounts[i].name:
                    market_segment.remove_account(self)
                    i += 1
        """
        Deletes any duplicates in new list of associated market segments.
        """       
        segments_no_dupes = []
        for market_segment in segments:
            if market_segment not in segments_no_dupes:
                segments_no_dupes.append(market_segment)
        """
        Associates list(without duplicates) of market segments
        to account and account to market segments.
        """                                    
        self._market_segments = segments_no_dupes

        for market_segment in segments_no_dupes:
            market_segment.add_account(self)
            
        """
        Keeps track of subclass instances.
        """ 
    def add_child(self, child):
        self._children.append(child);
        

class ChildAccount(Account):
    def __init__(self, parent_account, name, sales_rep=None, market_segments=None):
        self.name = name
        self._sales_rep = sales_rep
        self._market_segments = []
        self._children = []
        
        if market_segments:
            self._market_segments.extend(market_segments)
        else:
            self._market_segments = parent_account._market_segments

        if sales_rep:
            self._sales_rep = sales_rep
        else:
            self._sales_rep = parent_account._sales_rep
        """
        keeps track of subclass instances.
        """ 
        parent_account.add_child(self)


def print_tree(account):
    """
    print_tree could certainly be more DRY. With more time I'd refactor it so that the repeated code for building
    the string and printing were in their own functions. Also, print_tree does not currently protect against null values in sales_rep.
    """

    market_segment_string = ""
    for market_segment in account._market_segments:
        market_segment_string += market_segment.name + ', '

    market_segment_string = market_segment_string[:-2]
        
    print('{0:s} ({1:s}): {2:s} {3:s}'.format(account.name, market_segment_string, account._sales_rep.first_name, account._sales_rep.last_name))

    for child in account._children:
        market_segment_string = ""
        for market_segment in child._market_segments:
            market_segment_string += market_segment.name + ', '

        market_segment_string = market_segment_string[:-2]
        
        print('    {0:s} ({1:s}): {2:s} {3:s}'.format(child.name, market_segment_string, child._sales_rep.first_name, child._sales_rep.last_name))

        for grand_child in child._children:
            market_segment_string = ""
            for market_segment in grand_child._market_segments:
                market_segment_string += market_segment.name + ', '

            market_segment_string = market_segment_string[:-2]
        
            print('        {0:s} ({1:s}): {2:s} {3:s}'.format(grand_child.name, market_segment_string, grand_child._sales_rep.first_name, grand_child._sales_rep.last_name))


"""

SQL schema:

NOTE: for PostgreSQL. I'm not sure which version of SQL you're using, so I went with the one I know.

CREATE TABLE sales_rep ( 
ID SERIAL PRIMARY KEY,
first_name VARCHAR(50), 
last_name VARCHAR(50));

CREATE TABLE account ( 
ID SERIAL PRIMARY KEY,
sales_rep_id INT REFERENCES sales_rep,
name VARCHAR(100));

CREATE TABLE market_segment ( 
ID SERIAL PRIMARY KEY,
name VARCHAR(100));

CREATE TABLE market_segment_account ( 
ID SERIAL PRIMARY KEY,
market_segment_id INT REFERENCES market_segment,
account_id INT REFERENCES account);

SQL statement:

NOTE: To fulfill the requirement, market_segment_account.market_segment_id would be the id of "Consumer Goods" in the market_segment table.
    
SELECT account.name, sales_rep.first_name, sales_rep.last_name 
FROM account
JOIN sales_rep
ON account.sales_rep_id = sales_rep.id
JOIN market_segment_account 
ON account.id = market_segment_account.account_id
WHERE market_segment_account.market_segment_id = 1;

NOTE: Dummy data for testing:

"""
david = SalesRep("David","Kesler")
bob = SalesRep("Bob","Arino")
jane = SalesRep("Jane","Dough")
widgets = MarketSegment("Widgets")
sprokets = MarketSegment("Sprokets")
whoozits = MarketSegment("Whoozits")
account1 = Account("Account 1")
account2 = Account("Account 2")
account3 = Account("Account 3")
account1.set_market_segments([sprokets, widgets, whoozits])
account1.set_sales_rep(david)
whoozits.add_account(account2)
whoozits.add_account(account3)
child_account = ChildAccount(account1, "Child Account")
child_account.set_market_segments([sprokets, whoozits])
grand_child_account1 = ChildAccount(child_account, "Grandchild 1 Account", bob)
grand_child_account2 = ChildAccount(child_account, "Grandchild 2 Account")
grand_child_account1.set_market_segments([widgets])
child_account2 = ChildAccount(account1, "Child Account 2")
two_grand_child_account1 = ChildAccount(child_account2, "2 Grandchild 1 Account", jane)
two_grand_child_account2 = ChildAccount(child_account2, "2 Grandchild 2 Account")
two_grand_child_account2.set_market_segments([whoozits])
child_account2.set_market_segments([sprokets])
print_tree(account1)
