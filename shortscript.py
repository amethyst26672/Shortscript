
import sys
import os
import importlib.util


# Function to parse instructions from a file
def parse_instructions(file_path):
    instructions = []
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split(
                ' ', 1)  # Split the line into instruction and arguments
            if len(parts) == 2:
                instructions.append((parts[0], parts[1]))
            else:
                instructions.append((parts[0], None))
    return instructions


# Function to execute parsed instructions
def execute_instructions(instructions):
    for instruction, args in instructions:
        if instruction == 'PRINT':
            print(args)
        elif instruction == 'ADD':
            numbers = args.split()
            result = int(numbers[0]) + int(numbers[1])
            print(result)
        elif instruction == 'SUBTRACT':
            numbers = args.split()
            result = int(numbers[0]) - int(numbers[1])
            print(result)
        elif instruction == 'MULTIPLY':
            numbers = args.split()
            result = int(numbers[0]) * int(numbers[1])
            print(result)
        elif instruction == 'DIVIDE':
            numbers = args.split()
            result = int(numbers[0]) / int(numbers[1])
            print(result)
        else:
            # Attempt to load and execute a custom function
            execute_custom_function(instruction, args)


# Function to dynamically import and execute custom functions
def execute_custom_function(function_name, args_string):
    function_folder = 'functions'
    if not os.path.exists(function_folder):
        print(f"The '{function_folder}' folder does not exist.")
        return

    function_file = f"{function_name}.py"
    function_path = os.path.join(function_folder, function_file)

    if not os.path.isfile(function_path):
        print(f"No function found matching '{function_name}'.")
        return

    spec = importlib.util.spec_from_file_location(function_name, function_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    if hasattr(module, function_name):
        func = getattr(module, function_name)
        if callable(func):
            # Split the args_string into a list of arguments
            args_list = args_string.split(
                ', ')  # Assuming arguments are comma-separated
            func(
                *args_list)  # Use * to unpack the list into separate arguments
        else:
            print(f"'{function_name}' is not callable.")
    else:
        print(f"No function named '{function_name}' was found.")


# Main function to tie everything together
def main():
    if len(sys.argv) > 1:
        file_path = sys.argv[
            1]  # Get the file path from command line arguments
    else:
        print("Usage: python shortscript.py <file_path>")
        sys.exit(1)  # Exit the program if no file path is provided

    instructions = parse_instructions(file_path)
    execute_instructions(instructions)


if __name__ == "__main__":
    main()
