from pathlib import Path

# Create a Path object for the directory
directory = Path('.')

# Use iterdir() to list contents
for item in directory.iterdir():
    print(item)
