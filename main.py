import random
import time

 
time_frame=18  
check_point_sz = 3 # time_frame divisible by check_point_sz



class CPiX:

    def __init__(self):
        self.p_values = [0] * (1+ time_frame//2)  # Initialize 10 p-values (0th index will be unused)
        self.counter = [0] *  (1+ time_frame//2)    # Track the round
        self.c_values = [0] * (1+ time_frame//(2*check_point_sz))     # Initialize 4 c-values (0th index will be unused)
        self.g_value = 0            # Initialize g value to 0

    def update_values(self, s, new_value):
        # Constrain time s to be within the range of 1 to 30
         
        p = ((s - 1) % time_frame) + 1

        # Calculate indices for p and c
        round = (s + time_frame - 1) // time_frame  # Corrected integer division
        p_index = (p + 2 - 1) // 2   # p index (1-based for user, 0-based for array)
        c_index = (p + 2*check_point_sz - 1) // (2*check_point_sz)    # c index (1-based for user, 0-based for array)

        # Update p-value (skip 0th index)
        if 1 <= p_index < len(self.p_values):
            if round > self.counter[p_index]:
                self.p_values[p_index] = new_value  # Corrected assignment
                self.counter[p_index] = round
            elif round ==self.counter[p_index] :
                self.p_values[p_index] = max(self.p_values[p_index], new_value)

            # Update c-value based on the maximum of the corresponding p-values
            if 1 <= c_index < len(self.c_values):
                # Calculate the start index for p_values based on c_index
                start_index = (c_index - 1) * check_point_sz + 1  # Calculate start index for p_values
                end_index = start_index + check_point_sz  # Get the next three p_values

                # Update c_value with the maximum of the corresponding p_values
                self.c_values[c_index] = max(self.p_values[start_index:end_index])

        # Update g-value based on the maximum of the c-values
        self.g_value = max(self.c_values[1:])  # Get the maximum of the c-values

    def get_values(self):
        return {
            "P-values": self.p_values[1:],  # Skip the 0th index for display
            "C-values": self.c_values[1:],  # Skip the 0th index for display
            "G-value": self.g_value
        }


# Example usage
cpix = CPiX()

def generate_unique_nearby_shuffled_sequence(length, shuffle_window=2):
    sequence = list(range(1, length + 1))  # Create a sorted list from 1 to length
    shuffled_sequence = []

    # Keep track of used seconds
    used_seconds = set()

    for i in range(length):
        # Determine the range for shuffling
        start = max(1, i - shuffle_window)  # Ensure it starts from 1
        end = min(length + 1, i + shuffle_window + 1)  # Ensure it ends at length + 1

        # Get available options within the shuffle window that haven't been used
        available_options = [num for num in range(start, end) if num not in used_seconds]

        if available_options:
            chosen_value = random.choice(available_options)
            shuffled_sequence.append(chosen_value)
            used_seconds.add(chosen_value)  # Mark this second as used

    return shuffled_sequence


# Example usage
cpix = CPiX()

# Generate a unique nearby shuffled sequence of numbers from 1 to 30
unique_nearby_shuffled_sequence = generate_unique_nearby_shuffled_sequence(70, shuffle_window=2)

# Process each number in the unique nearby shuffled sequence with a delay of 3 seconds between each
for s in unique_nearby_shuffled_sequence:
    value = random.randint(1, 100)  # Generate a random value
    cpix.update_values(s, value)     # Update the values
    print(f"After update at time {s}s with value {value}:")
    print(cpix.get_values())
    time.sleep(1)  # Delay for 1 seconds