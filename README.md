# System-Check-Assignment
In this assignment, I am acting as a Linux technician at a company. My task is to write two scripts that retrieves processor information from a linux computer and write it to a JSON file. The JSON file will be read by my second script and the output written to my screen. 

PSEUDOCODE:
1. Import the platform, os, and json modules to define the functions

2. Define the machine_name function to return hostname
- platform.node()

3. Define the users_and_groups function
- Read the lines and split(":") line by line
- Fetch the username and GUID
- Store the output in a dictionary
- Sort the lines by alphabetusing sorted
- Return the results as a list

4. Define the get_cpu_info function
- Open /proc/info and read it by line
- Implement conditions to save and display the value if the line contains system information
- When the four values are returned stop the process
- Return the CPU information dictionary

5. Define the get_service_status function
- Use os.popen to run systemctl list-units to display all active units
- Split the words by line
- Save the name and status to a list
- Append each dictionary to the list and return once finished

6. Implement the main() function
- Simply, the main function calls the program functions so it canrun
- Information is saved into one dictionary, located in a JSON
