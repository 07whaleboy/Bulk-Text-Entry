import os
import time
import argparse
import random
import sys

def replace_random(text):
    while '&random&' in text:
        random_num = str(random.randint(0, 32768))
        text = text.replace('&random&', random_num, 1)
    return text

def main():
    try:
        script_name = os.path.basename(__file__)  # Get the actual script filename

        # Modify the argument parser to disable the built-in help option
        parser = argparse.ArgumentParser(description="Generate text content in a file.", add_help=False)
        parser.add_argument("name", nargs="?", help="File name (automatically adds .txt extension)")
        parser.add_argument("contents", nargs="?", help="Text content to generate")
        parser.add_argument("instances", nargs="?", type=int, help="Number of times to generate the content")
        parser.add_argument("--nolog", action="store_true", help="Disable logging")

        # Handle the -? option manually
        if "-?" in sys.argv:
            print(f"Usage: {script_name} [-? / --help] [--nolog] [name] [contents] [instances]\n")
            print("Generate text content in a file.")
            print("\nPositional arguments:")
            print("  name        File name (automatically adds .txt extension)")
            print("  contents    Text content to generate")
            print("  instances   Number of times to generate the content\n")
            print("Options:")
            print("  -?, --help  show this help message and exit")
            print("  --nolog     Disable logging")
            sys.exit(0)

        args = parser.parse_args()

        if args.name is None or args.contents is None or args.instances is None:
            print("This program will generate any amount of any word or phrase in a text file.")
            name = input("What would you like the file to be called? This will automatically add a .txt extension: ")
            contents = input("What's the word or phrase you want to generate in this file?: ")

            while True:
                try:
                    instances = int(input(f"How many times do you want to generate '{contents}' in '{name}.txt'?: "))
                    break
                except ValueError:
                    print("Input is not a number. Please input a number.")
        else:
            name = args.name
            contents = args.contents
            instances = args.instances

        # Replace &random& with a random number in filename and contents
        random_nums = {}
        name = replace_random(name)
        contents = replace_random(contents)

        if args.nolog:
            log = None
        else:
            log_file = f"Output/{name}_log.txt"
            log = open(log_file, "w")

        # Initialize variables
        num = 0
        lines_per_second = 0
        total_lines = 0

        # Create 'Output' directory if it doesn't exist
        if not os.path.exists('Output'):
            os.mkdir('Output')

        # Confirmation message
        confirmation_message = f"This program will generate '{contents}' into '{name}' {instances} times when you press Enter."

        for key, value in random_nums.items():
            confirmation_message += f"\nRandom number for '{key}': {value}"

        print(confirmation_message)
        input("Press Enter to start...")

        # Start the timer
        start_time = time.time()

        # Generate the content and write to the file
        with open(f"Output/{name}.txt", "w") as file:
            if log:
                log.write("Start Time: " + time.strftime("%Y-%m-%d %H:%M:%S") + "\n")
            for _ in range(instances):
                line = contents.replace('&linecount&', str(num + 1)) + '\n'
                file.write(line)
                if log:
                    log.write(f"Generated Line {num + 1}: {line}")
                num += 1
                total_lines += 1

        # Stop the timer and calculate the time taken
        end_time = time.time()
        elapsed_time = end_time - start_time

        # Calculate lines per second
        if elapsed_time > 0:
            lines_per_second = total_lines / elapsed_time
        else:
            lines_per_second = 0

        if log:
            log.write(f"End Time: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            log.write(f"Elapsed Time: {elapsed_time:.2f} seconds\n")
            log.write(f"Average Lines Per Second: {lines_per_second:.2f} lines/s\n")
            log.close()

        print(f"Completed in {elapsed_time:.2f} seconds, with an average of {lines_per_second:.2f} lines per second.")
        if log:
            print(f"Log file '{log_file}' has been created.")
        input("Press Enter to exit...")

    except SystemExit as e:
        if e.code != 0:
            print("Switch invalid. Please use --help or -? for assistance.")
            sys.exit(1)

if __name__ == "__main__":
    main()
