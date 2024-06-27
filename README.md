# Orient Speedtest Program
Description of the Orient Speedtest Program
The Orient Speedtest Program is a Python application designed to measure your internet speed and record the results over time. 
It offers several functionalities:

Speed Testing: Performs speed tests using the speedtest-cli tool and retrieves download and upload speeds in Mbps.
Data Recording: Saves the test results, including download/upload speeds, timestamps, server information, and geographical location (latitude/longitude) to a CSV file for historical tracking.
User Interface: Creates a graphical summary window using Tkinter to display the latest speed test results (download and upload speeds) after each test.
Scheduling: Allows users to schedule repeated speed tests at specific intervals (in minutes) and durations (in days) for monitoring internet performance over time.
User Interaction: Provides a user-friendly interface to configure test intervals and durations before initiating the speed testing process.
Error Handling: Includes error handling mechanisms to catch potential issues during speed tests or location data retrieval and displays informative messages to the user.
Main Functions of the Program:
run_speedtest(): This function executes the speed test using speedtest-cli, retrieves the results, processes them (extracting speeds, converting units, adding timestamps and location data), and saves them to the CSV file. It then displays a summary window with the latest download and upload speeds.
get_user_input(): This function creates a user interface using Tkinter to gather user input for the desired interval and duration of the repeated speed tests. It validates the input and triggers the run_tests() function with the provided parameters.
show_summary(): This function displays a summary window upon completion of scheduled tests or user request for exit. It presents the total number of tests run, start and end times, and prompts for confirmation before closing the program. 4. run_tests(): This function schedules the execution of speed tests based on the user-provided interval and duration. It controls the number of repetitions, manages the starting time, and displays the final summary window.
main_root: This is the main Tkinter root window, initially hidden using withdraw(). It serves as the starting point for the application and initiates the user input process through get_user_input().
Overall, the Orient Speedtest Program offers a user-friendly and informative way to measure and track your internet speed performance over time.

This Python application measures your internet speed and records the results over time.

## Features

- Performs speed tests using `speedtest-cli`
- Saves results (download/upload speeds, timestamps, server info, location) to a CSV file
- Displays a graphical summary window with latest speeds after each test
- Allows scheduling repeated tests at user-defined intervals and durations

## Technologies

- Python
- Tkinter
- Fegma
- VS Code

## Installation
Additional Considerations
Speedtest Configuration:

Make sure the compiled executable includes speedtest-cli and can access it. 
If speedtest-cli requires additional binaries or configurations, include them in the package.
Environment Variables:

If speedtest-cli depends on environment variables or other configurations,
 ensure these are set up correctly on the target machine.
Dependencies:

Verify that all dependencies (requests, tkinter, etc.) are included in the build.
 PyInstaller typically handles this automatically, but you may need to verify and test
 the output executable.
(If applicable, provide steps on how to install required libraries)

## Usage

(Explain how to run the speed test program)

## Screenshots

[Optional: Include screenshots of your Figma design or Tkinter UI]

## Contributing

(If applicable, explain how others can contribute to your project)
