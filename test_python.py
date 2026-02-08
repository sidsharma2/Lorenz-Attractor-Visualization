
import sys
import os

print("Hello from Python!")
print(f"Python Info: {sys.version}")
print(f"Current Directory: {os.getcwd()}")

# Simple calculation
a = [1, 2, 3, 4, 5]
squared = [x**2 for x in a]
print(f"Squared list: {squared}")
