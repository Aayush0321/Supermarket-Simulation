# Aayush Pittie 001328860 F2
# Panagiotis Petsallari 001294962 F1
# The code for F3 below was done jointly by both of the members and the contribution was equal
import time
import random
from Lanes import SelfServiceLane, RegularLane
from Customer import Customer
import threading


class Supermarket:
    """Main Simulation Class"""
    PRINT_LOCK = threading.Lock()

    def __init__(self):
        """Initialises Lanes and No. of initial customers"""
        self.regular_lanes = [RegularLane(i) for i in range(1, 6)]  # Creating 5 Regular Lanes
        self.self_service_lane = [SelfServiceLane(6)]  # Creating 1 Self-service Lanes
        self.regular_lanes[0].open_lane()  # Starts the simulation with two open lanes
        self.self_service_lane[0].open_lane()
        self.initial_customers = random.randint(1, 10)  # Initial Customers
        self.customer_counter = self.initial_customers  # Counts the total customers processed

    def are_all_lanes_full(self):
        """Checks are all Regular lanes Full"""
        return all(lane.lane_is_full() for lane in self.regular_lanes)

    def generate_initial_customers(self):
        """Generates and Displays initial customers"""
        for _ in range(self.initial_customers):
            customer = Customer(cid=f"C{_}")
            x = self.enter_lane(customer)  # Add them to a lane
            customer.display_customer_details(x)

    def enter_lane(self, customer):
        """Adds customers to lanes"""
        if customer.item_in_basket < 10 and not self.self_service_lane[0].lane_is_full():
            self.self_service_lane[0].add_customer(customer)  # Adds customer with less than 10 items only
            return True
        else:
            processing_time = [lane.lane_usage() for lane in self.regular_lanes]
            x = processing_time.index(min(processing_time))
            regular_lane_with_shortest_queue = self.regular_lanes[x]
            # Finds the shortest lane for customer to join
            regular_lane_with_shortest_queue.add_customer(customer)  # Adds customer to the shortest lane
            return f"Regular Lane {x + 1}"

    def lane_saturation(self):
        """Calculates total customers Standing in line"""
        users = 0
        for lane in self.regular_lanes:  # Iterates over all lanes to add the customers up
            users = users + (len(lane.customers))
        users += len(self.self_service_lane[0].customers)
        return users

    def generate_customers(self):
        """Generates customers with unique iD"""
        while True:
            if self.lane_saturation() <= 40 and not self.are_all_lanes_full():
                # Generates only when there is a space for  the customer to join in the lane
                customer = Customer(cid=f"C{self.customer_counter}")
                self.customer_counter += 1  # Increments the no. of customer generated
                x = self.enter_lane(customer)  # Enters the customer into a lane
                customer.display_customer_details(x)  # Displays the customer details
                time.sleep(random.randint(1, 10))  # Generates a customer randomly between 1 and 10 Seconds
            else:
                print(f"Lane Saturation is {instance.lane_saturation() / 0.4} %")  # Dividing by 0.4 as 40 customers
                time.sleep(5)  # If all the lanes are full it waits for 5s and checks the Saturation again
                continue   # This allows customers to be processed

    def lane_management(self):
        """Manages all the Functions of the Lane Such as:
        Processing the Customer
        Displaying Lane Status
        Closing Empty Lane"""
        while True:
            for lane in self.regular_lanes + self.self_service_lane:
                lane.process_customer()  # This processes the customer
                lane.lane_close()  # This will close the lane if it's empty
            with Supermarket.PRINT_LOCK:
                for lanes in self.regular_lanes:
                    lanes.display_lane_status()  # Displays status of Regular lanes, lane by lane
                self.self_service_lane[0].display_lane_status()  # Displays status of Self service lane
                time.sleep(5)  # This defines the speed of the simulation

    def simulation(self, total_customers, duration):
        """Initialises the Total customers to be generated and the Duration of the Simulation
        Also calls all the Starting methods and Starts threading"""
        start_time = time.time()  # Start time is defined from real time clock
        end_time = start_time + duration
        self.generate_initial_customers()  # Calls the function to generate the initial customers
        customer_generation = threading.Thread(target=self.generate_customers)
        lane_generation = threading.Thread(target=self.lane_management)
        # Threads the two main Methods Customer Generation and lane management allowing both to execute independently
        # of each other. It also allows the ability to have different speeds at which
        # Lanes are processed or customers are generated
        customer_generation.daemon = True
        lane_generation.daemon = True
        current_time = 0  # Initialising for the While Loop
        lane_generation.start()  # Starts the first thread
        time.sleep(0.5)  # Time gap so the threads don't interfere as they have different phases
        customer_generation.start()  # Second thread starts
        while current_time < end_time and self.customer_counter < total_customers:
            # While loop that runs until Duration or Total customers is reached
            current_time = time.time()  # Updates the current time
            if current_time > end_time or self.customer_counter >= total_customers:
                print(
                    f"Simulation ended. Duration: {current_time - start_time:.2f} seconds, "
                    f"Customers processed: {self.customer_counter}")
                # End statement that tells the Customers processed in how much time
                raise KeyboardInterrupt  # Raises error to terminate the main loop


if __name__ == "__main__":
    instance = Supermarket()  # creates an instance of the simulation
    # want to take as an input?
    try:
        instance.simulation(total_customers=50, duration=400)  # Calls the simulation
    except KeyboardInterrupt:  # Allows manual termination using Keyboard interrupt error
        print(f"Simulation Ended")  # Final Message
        print(f"Lane Saturation at the time of Ending {instance.lane_saturation() / 0.4} %")
        # Lane saturation in percentage at the end of the simulation
