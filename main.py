import random
import time

time_frame = 18  
check_point_sz = 3  # time_frame divisible by check_point_sz

class CPiX:
    def __init__(self):
        self.products = {}  # Dictionary to hold data for each product

    def initialize_product(self, product_name):
        self.products[product_name] = {
            'p_values': [0] * (1 + time_frame // 2),
            'counter': [0] * (1 + time_frame // 2),
            'c_values': [0] * (1 + time_frame // (2 * check_point_sz)),
            'g_value': 0
        }

    def update_values(self, s, product_name, new_value):
        # Ensure the product is initialized
        if product_name not in self.products:
            self.initialize_product(product_name)

        product_data = self.products[product_name]

        # Constrain time s to be within the range of 1 to 30
        p = ((s - 1) % time_frame) + 1

        # Calculate indices for p and c
        round = (s + time_frame - 1) // time_frame  # Corrected integer division
        p_index = (p + 2 - 1) // 2  # p index (1-based for user, 0-based for array)
        c_index = (p + 2 * check_point_sz - 1) // (2 * check_point_sz)  # c index

        # Update p-value (skip 0th index)
        if 1 <= p_index < len(product_data['p_values']):
            if round > product_data['counter'][p_index]:
                product_data['p_values'][p_index] = new_value
                product_data['counter'][p_index] = round
            elif round == product_data['counter'][p_index]:
                product_data['p_values'][p_index] = max(product_data['p_values'][p_index], new_value)

            # Update c-value based on the maximum of the corresponding p-values
            if 1 <= c_index < len(product_data['c_values']):
                start_index = (c_index - 1) * check_point_sz + 1
                end_index = start_index + check_point_sz
                product_data['c_values'][c_index] = max(product_data['p_values'][start_index:end_index])

        # Update g-value based on the maximum of the c-values
        product_data['g_value'] = max(product_data['c_values'][1:])  # Get the maximum of the c-values

    def get_values(self, product_name):
        if product_name in self.products:
            product_data = self.products[product_name]
            return {
                "P-values": product_data['p_values'][1:],  # Skip the 0th index for display
                "C-values": product_data['c_values'][1:],  # Skip the 0th index for display
                "G-value": product_data['g_value']
            }
        else:
            return None

    def top_k_products(self, k):
        # Get G-values for all products
        g_values = {product: data['g_value'] for product, data in self.products.items()}

        # Sort products by G-value in descending order and get the top K
        top_k = sorted(g_values.items(), key=lambda item: item[1], reverse=True)[:k]
        return top_k


# Example usage
cpix = CPiX()

def generate_unique_nearby_shuffled_sequence(length, shuffle_window=2):
    sequence = list(range(1, length + 1))  # Create a sorted list from 1 to length
    shuffled_sequence = []
    used_seconds = set()

    for i in range(length):
        start = max(1, i - shuffle_window)
        end = min(length + 1, i + shuffle_window + 1)
        available_options = [num for num in range(start, end) if num not in used_seconds]

        if available_options:
            chosen_value = random.choice(available_options)
            shuffled_sequence.append(chosen_value)
            used_seconds.add(chosen_value)  # Mark this second as used

    return shuffled_sequence


# Generate a unique nearby shuffled sequence of numbers from 1 to 30
unique_nearby_shuffled_sequence = generate_unique_nearby_shuffled_sequence(70, shuffle_window=2)

# Process each number in the unique nearby shuffled sequence with a delay of 1 second between each
products = ['Product A', 'Product B', 'Product C']  # Example product names

for s in unique_nearby_shuffled_sequence:
    for product in products:
        value = random.randint(1, 100)  # Generate a random value
        cpix.update_values(s, product, value)  # Update the values for each product
        print(f"After update at time {s}s for {product} with value {value}:")
        print(cpix.get_values(product))
    
    # Retrieve the top K products based on G-values after each second
    top_k = cpix.top_k_products(2)  # Change the number to get more or fewer products
    print("Top K Products based on G-values after update:")
    for product, g_value in top_k:
        print(f"{product}: G-value = {g_value}")

    time.sleep(1)  # Delay for 1 second
