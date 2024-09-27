# Aayush Pittie 001328860 F2
import random
from Lanes import CheckoutLane


class Customer:
    """ Creates Customer Object"""
    def __init__(self, cid):
        """ Initializes Customers with Customer ID."""
        self.id = cid  # Unique identifier of Customer
        self.item_in_basket = self.random_number_of_items()  # Generating random number of items in basket
        self.lottery_result = self.check_lottery_tkt()  # Lottery result for the customer
        self.self_checkout_time = self.checkout_time(6)  # Check out time at Self-service till
        self.cash_checkout_time = self.checkout_time(4)  # Check out time at Cashier till

    def check_lottery_tkt(self):
        """Checks if a customer wins a lottery ticket"""
        if self.item_in_basket >= 10 and random.random() < 0.1:  # The number of items should be >= 10
            result = "Winner"                                     # Sets a 10% Probability to win a ticket
        else:
            result = "Hard luck, no lottery ticket this time"
        return result

    def checkout_time(self, checkout_time_per_item):
        # Calculate the checkout time for the customer based on their items
        return self.item_in_basket * checkout_time_per_item

    def display_customer_details(self, lane):
        """Prints the customer details in a Set Format"""
        with CheckoutLane.PRINT_LOCK:  # Allows multiple threads to access Print resource
            print("Customer details")  # and to prevent interference from other threads
            print(f"ID: {self.id}")
            print(f"Items in basket: {self.item_in_basket}")
            print(f"Lottery ticket result: {self.lottery_result}")
            if self.item_in_basket < 10 and lane:  # Prints depending upon which lane they are likely to go
                print(f"Time to process basket at self checkout till: {self.self_checkout_time} Secs")
                print('Customer added to Self Checkout Lane 6')

            else:
                print(f"Time to process basket at cashier till: {self.cash_checkout_time} Secs")
                print(f"Customer added to {lane}")
            print('______________________')
            print(f'______________________ \n')

    @staticmethod
    def random_number_of_items():
        """Calculates the Items in basket of a Customer randomly"""
        if random.choice([True, False]):   # This method allows more customers with less than 10 items to be generated
            return random.randint(10, 30)  # Can be modified to have more or less of a type of customer
        else:  # Currently 50% chance to have less than 10 items which can be modified
            return random.randint(1, 10)  # with changing the amount of true values in the list
