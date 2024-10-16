import random
import time

class CPiX:
    def __init__(self):
        self.p_values = [0] * 10  # Initialize 10 p-values (0th index will be unused)
        self.g_values = [0] * 4    # Initialize 4 g-values (0th index will be unused)
        self.t_value = 0           # Initialize t value to 0

    def update_values(self, s, new_value):
        # Constrain time s to be within the range of 1 to 18
        if s > 18:
            s = 18

        # Calculate indices for p and g
        p_index = (s + 2 - 1) // 2  # p index (1-based for user, 0-based for array)
        g_index = (s + 6 - 1) // 6   # g index (1-based for user, 0-based for array)

        # Update p-value (skip 0th index)
        if 1 <= p_index < len(self.p_values):
            self.p_values[p_index] = max(self.p_values[p_index], new_value)

        # Update g-value (skip 0th index)
        if 1 <= g_index < len(self.g_values):
            self.g_values[g_index] = max(self.g_values[g_index], self.p_values[p_index])
        else:
            print(f"Warning: g_index {g_index} is out of bounds.")

        # Update t-value only if g_index is valid
        if 1 <= g_index < len(self.g_values):
            self.t_value = max(self.t_value, self.g_values[g_index])

    def get_values(self):
        return {
            "P-values": self.p_values[1:],  # Skip the 0th index for display
            "G-values": self.g_values[1:],  # Skip the 0th index for display
            "T-value": self.t_value
        }


# Example usage
cpix = CPiX()

# Process 18 random updates with a delay of 3 seconds between each
for s in range(1, 19):
    value = random.randint(1, 100)  # Generate a random value
    cpix.update_values(s, value)     # Update the values
    print(f"After update at time {s}s with value {value}:")
    print(cpix.get_values())
    time.sleep(3)  # Delay for 3 seconds
