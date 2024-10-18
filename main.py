import random
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import requests  # Import requests for API calls

time_frame = 18  
check_point_sz = 3  # time_frame divisible by check_point_sz

class CPiX:
    def __init__(self):
        self.products = {}

    def initialize_product(self, product_name):
        self.products[product_name] = {
            'p_values': [0] * (1 + time_frame // 2),
            'counter': [0] * (1 + time_frame // 2),
            'c_values': [0] * (1 + time_frame // (2 * check_point_sz)),
            'g_value': 0
        }

    def update_values(self, s, product_name, new_value):
        if product_name not in self.products:
            self.initialize_product(product_name)

        product_data = self.products[product_name]
        p = ((s - 1) % time_frame) + 1
        round = (s + time_frame - 1) // time_frame
        p_index = (p + 2 - 1) // 2
        c_index = (p + 2 * check_point_sz - 1) // (2 * check_point_sz)

        if 1 <= p_index < len(product_data['p_values']):
            if round > product_data['counter'][p_index]:
                product_data['p_values'][p_index] = new_value
                product_data['counter'][p_index] = round
            elif round == product_data['counter'][p_index]:
                product_data['p_values'][p_index] = max(product_data['p_values'][p_index], new_value)

            if 1 <= c_index < len(product_data['c_values']):
                start_index = (c_index - 1) * check_point_sz + 1
                end_index = start_index + check_point_sz
                product_data['c_values'][c_index] = max(product_data['p_values'][start_index:end_index])

        product_data['g_value'] = max(product_data['c_values'][1:])  # Update G-value

    def get_values(self, product_name):
        if product_name in self.products:
            product_data = self.products[product_name]
            return {
                "P-values": product_data['p_values'][1:],
                "C-values": product_data['c_values'][1:],
                "G-value": product_data['g_value']
            }
        else:
            return None

    def top_k_products(self, k):
        g_values = {product: data['g_value'] for product, data in self.products.items()}
        top_k = sorted(g_values.items(), key=lambda item: item[1], reverse=True)[:k]
        return top_k

# Initialize CPiX instance
cpix = CPiX()

def generate_unique_nearby_shuffled_sequence(length, shuffle_window=2):
    sequence = list(range(1, length + 1))
    shuffled_sequence = []
    used_seconds = set()

    for i in range(length):
        start = max(1, i - shuffle_window)
        end = min(length + 1, i + shuffle_window + 1)
        available_options = [num for num in range(start, end) if num not in used_seconds]

        if available_options:
            chosen_value = random.choice(available_options)
            shuffled_sequence.append(chosen_value)
            used_seconds.add(chosen_value)

    return shuffled_sequence

# Generate a unique nearby shuffled sequence of numbers
unique_nearby_shuffled_sequence = generate_unique_nearby_shuffled_sequence(70, shuffle_window=2)

# Define products
products = ['Product A', 'Product B','Product C', 'Product D']

# Prepare to write to CSV
csv_file = 'g_values.csv'
header = ['Time', 'Product', 'G-Value']
with open(csv_file, 'w') as f:
    f.write(','.join(header) + '\n')  # Write header

# Function to fetch real-world data from JSONPlaceholder
def fetch_real_world_data(product_name):
    # Here we can use the post ID as a proxy for product name
    url = f'https://jsonplaceholder.typicode.com/posts/{random.randint(1, 100)}'
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        print(f"Fetched data for {product_name}: {data}")
        return data['id']  # Example value; you can adjust based on your needs
    else:
        print(f"Failed to fetch data for {product_name}")
        return random.randint(1, 100)  # Fallback to random value

# Function to print summary of updates
def print_summary(s, top_k):
    print(f"After update at time {s}s:")
    for product, g_value in top_k:
        print(f"{product}: G-value = {g_value}")
    print("-" * 30)

# Process each number in the unique nearby shuffled sequence
for s in unique_nearby_shuffled_sequence:
    for product in products:
        value = fetch_real_world_data(product)  # Fetch real-world data
        
        cpix.update_values(s, product, value)  # Update the values for each product
    
    # Retrieve the top K products based on G-values after each second
    top_k = cpix.top_k_products(2)  # Get the top 2 products
    print_summary(s, top_k)
    
    # Update the CSV file with the G-values
    for product, g_value in top_k:
        with open(csv_file, 'a') as f:  # Append to the CSV file
            f.write(f"{s},{product},{g_value}\n")

    time.sleep(1)  # Delay for 1 second 