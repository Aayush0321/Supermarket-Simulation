# Panagiotis Petsallari 001294962 F1
import time
from collections import deque
import threading


class CheckoutLane:
    """Creates Checkout Lane Object"""
    PRINT_LOCK = threading.Lock()  # Defines PRINT_LOCK as Lock function of threading

    def __init__(self, lane_id, capacity):
        """Initializes CheckoutLane with lane_id and capacity."""
        timestamp = time.time()
        self.lane_id = lane_id  # Identifier of Lane
        self.status = 'closed'  # Lane status is closed by default
        self.customers = deque()  # Queue to manage customers
        self.capacity = capacity  # Maximum number of customers the lane can hold

    def lane_usage(self):
        """Calculates total number of items in customers' baskets."""
        usage = 0
        for cust in self.customers:  # Uses this usage value ot determine the shortest queue
            usage += cust.item_in_basket
        if self.lane_is_full():  # Increasing the value of a Full lane, so it never gets selected
            usage += 150
        elif self.status == 'closed':  # Closed lane has some value as to not open the first available closed lane
            usage += 100               # until all other lanes have usage value over
        return usage

    def lane_is_full(self):
        """Returns boolean value on whether lane is full"""
        return len(self.customers) == self.capacity

    def lane_close(self):
        """Closes lane if no customers are present."""
        if self.is_empty():  # Is initiated each time lanes are processed
            self.status = 'closed'

    def is_empty(self):
        """Checks if lane is empty."""
        return len(self.customers) == 0

    def open_lane(self):
        """Opens lane"""
        self.status = 'open'

    def close_lane(self):
        """Closes lane"""
        self.status = 'closed'

    def process_customer(self):
        """Processes the first customer in the lane."""
        with CheckoutLane.PRINT_LOCK:  # Allows multiple threads to access Print resource
            if self.customers:         # and to prevent interference from other threads
                customer = self.customers[0]    # processes the first customer
                if customer.item_in_basket > 0:  # checks if it's basket is empty(0)
                    customer.item_in_basket -= 2  # Decrement remaining items in the basket
                    current_time_formatted = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                    print(f"[{current_time_formatted}] Processing customer {customer.id} in lane {self.lane_id}")
                    #  Prints the time at processing and the lane at which it is being processed
                elif customer.item_in_basket <= 0:  # Customer leaves lane when items are zero
                    completed_customer = self.customers.popleft()
                    current_time_formatted = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                    print(
                        f"[{current_time_formatted}] Customer {completed_customer.id} finished "
                        f"checking out from lane {self.lane_id}")

    def add_customer(self, customer):
        """Adds the customer to a Lane"""
        with CheckoutLane.PRINT_LOCK:
            # Adds a customer to the lane if there's capacity, otherwise indicates the lane is full.
            # Opens the lane if it's currently closed.
            if self.status == 'closed':
                self.open_lane()
            if len(self.customers) < self.capacity:
                self.customers.append(customer)  # Add the customer to the lane
            else:
                print("Lane is full. Customer cannot be added.")


class RegularLane(CheckoutLane):
    """Initializing a lane with capacity of 5 people"""
    def __init__(self, lane_id):
        """Inherits from Parent Class Checkout Lane"""
        super().__init__(lane_id, capacity=5)

    def display_lane_status(self):
        """Displays Lane Status"""
        with CheckoutLane.PRINT_LOCK:
            # Code to display the current status of the lane with "Regular" prefix
            status = "Open" if self.status == 'open' else "Closed"
            customers_in_line = ''.join(['*' for _ in self.customers])  # visualizes customers as Stars
            print(f"Regular Lane {self.lane_id} [{status}] - Customers: {customers_in_line}")


class SelfServiceLane(CheckoutLane):
    """Initializing a lane with capacity of 15 people"""
    def __init__(self, lane_id):
        super().__init__(lane_id, capacity=15)

    def process_customer(self):
        """Processes the first customer in the lane for Self service lanes."""
        # This code is duplicated ,so we can have different processing speeds for regular lanes and self-checkout lanes
        with CheckoutLane.PRINT_LOCK:
            if self.customers:
                customer = self.customers[0]  # processes the first customer
                if customer.item_in_basket > 0:   # checks if it's basket is empty(0)
                    customer.item_in_basket -= 1  # Decrement remaining items in the basket
                    current_time_formatted = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                    print(f"[{current_time_formatted}] Processing customer {customer.id} in lane {self.lane_id}")
                    #  Prints the time at processing and the lane at which it is being processed
                elif customer.item_in_basket <= 0:      # Customer leaves lane when items are zero
                    completed_customer = self.customers.popleft()
                    current_time_formatted = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                    print(
                        f"[{current_time_formatted}] Customer {completed_customer.id} finished "
                        f"checking out from lane {self.lane_id}")

        # code duplication here and regular lane

    def display_lane_status(self):
        """Displays Lane Status"""
        with CheckoutLane.PRINT_LOCK:
            # Code to display the current status of the lane with "Self Service Checkout" prefix
            status = "Open" if self.status == 'open' else "Closed"
            customers_in_line = ''.join(['*' for _ in self.customers])  # visualizes customers as Stars
            print(f"Self Service Checkout Lane {self.lane_id} [{status}] - Customers: {customers_in_line}")
            print(f'______________________ \n')
