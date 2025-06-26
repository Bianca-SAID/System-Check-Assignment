"""
PSEUDOCODE:
1. Import the platform, os, grp, and json modules to define the functions.
2. Define the machine_name function to return hostname.
3. Define the users_and_groups function.
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
5. Define the get_service_status function.
- Use os.popen to run systemctl list-units to display all active units
- Split the words by line
- Save the name and status to a list
- Append each dictionary to the list and return once finished
6. Implement the main() function.
7. Create main function in PrintData.py to read and display the .json file contents.
"""
import platform #Module provides access to platform details (hardware and OS)
import json #Manages JSON data into a readable format
import os #Retrieve service status from the OS
import grp #Provides access to the UNIX group database

def get_machine_name():
    return platform.node() #Uses platform to get machine name

def get_users_and_groups():
    try:
        with open("/etc/passwd", "r") as f: #Reads user data in read mode
            lines = f.readlines()
            output = [] #Creates an output list to store the user  dictionaries
            for line in sorted(lines):
                parts = line.split(":") #Splits lines at ":"
                name = parts[0] #Retrieves username
                group = []
                
                for groups in grp.getgrall(): #Iterates through groups and returns a list
                    if name in groups.gr_mem or int(parts[3]) == groups.gr_gid:#Checks if a user belongs to a group using GID
                        group.append(groups.gr_name) #Appends the name to that group if it matches

                output.append({
                    "username": name,
                    "group": group
                })#Adds user info to the output list
            return output 
    except:
        return [{"!ERROR!": "Couldn't read user information"}] #Error if a file can't be read

def get_cpu_info():
    try:
        CPU = { #Dictionary stores the vendor id, model, cache, and model name
            "vendor_id": "",
            "model": "",
            "model_name": "",
            "cache": ""
        }
        file = open("/proc/cpuinfo", "r") #Opens file to read processor info
        for line in file:
            if "vendor_id" in line:
                if CPU["vendor_id"] == "":
                    CPU["vendor_id"] = line.split(":")[1].strip() #Indexing and split to retrieve the value
            if "model name" in line:
                if CPU["model_name"] == "":
                    CPU["model_name"] = line.split(":")[1].strip()
            if line.startswith("model"):
                if CPU["model"] == "":
                    # Just check that it's not already filled, no other logic
                    parts = line.split(":")
                    if len(parts) > 1:
                        CPU["model"] = parts[1].strip()
            if "cache size" in line:
                if CPU["cache"] == "":
                    CPU["cache"] = line.split(":")[1].strip()
            if CPU["vendor_id"] != "" and CPU["model"] != "" and CPU["model_name"] != "" and CPU["cache"] != "":
                break #Loops through the lines and breaks once all 4 values are identified
        file.close() 
        return CPU
    except:
        return {"!ERROR!": "Couldn't read the CPU information"} #Error message if the CPU cannot be read

def get_service_status():
    try:
        services = [] #Houses the service dictionary  
        text = os.popen("systemctl list-units --type=service --no-pager").read() #Runs the linux command using os module
        lines = text.split("\n") #Splits at each newline
        for line in lines:
            parts = line.split() #Splits lines into parts to extract 4 values
            if len(parts) >= 4: #Stores to services if the parts have 4 lines
                name = parts[0]
                status = parts[3]
                service = {
                    "name": name, #Extracts service name
                    "status": status #Extracts process status
                }
                services.append(service) #Adds to the dictionary
        return services
    except:
        return [{"!ERROR!": "Couldn't get the service status"}] #Error message if status is not retrieveable

def main():
    DATA = { #Distionary stores the functions and assigns a name
        "machine_name": get_machine_name(),
        "users_and_groups": get_users_and_groups(),
        "processor_info": get_cpu_info(),
        "service_status": get_service_status()
    }

    f = open("Project_2.json", "w") #Creates and writes to a JSON
    json.dump(DATA, f) #If not existent, the file is created
    f.close() #File closed manually
    print("System information saved to Project_2.json")

main()
