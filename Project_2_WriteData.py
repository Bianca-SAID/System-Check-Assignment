"""
PSEUDOCODE:
1. Import the platform, os, and json modules to define the functions
2. Define the machine_name function to return hostname
3. Define the users_and_groups function
4. Define the get_cpu_info function
5. Define the get_service_status function
6. Implement the main() function
"""
import platform #Module provides access to platform details (hardware and OS)
import json #Manages JSON data into a readable format
import os #Retrieve service status from the OS

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
                group = parts[2] #UID from /etc/passwd
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






#         """
#         Im a technician checking 50 linux laptops individually, ill write two scripts to automate collecting systeminfo and printing it out
#         1. Project_2_WriteData.py
#         - Needs to collect systeminfo and save it to a json file
#         *Machine name
#         *List of all users and the groups they belong to sorted alphabetically by username
#         *CPU info from /proc/info
#         *Service Status (names and if theyre active)
#         *save it all into Project_2.json
        
#         2. Project_2_PrintData.py
#         - Needs to read the json file and print it nicely
#         ex. ==== Machine Name ====
#         my-laptop

#         ==== Users and Groups ====
#         alice: wheel, users
#         bob: users

#         ==== Processor Information ====
#         vendor_id: GenuineIntel
#         model: 158
#         model_name: Intel(R) Core(TM) i7-8565U CPU @ 1.80GHz
#         cache: 8192 KB

#         ==== Service Status ====
#         ssh.service: active
#         bluetooth.service: inactive
# """


# def get_cpu_info():
#     try:
#         with open("/proc/cpuinfo", "r") as f:
#             CPU = {}
#             for line in f:
#                 if "vendor_id" in line and "vendor_id" not in CPU:
#                     CPU["vendor_id"] = line.split(":")[1].strip()
#                 elif line.startswith("model") and "model" not in CPU:
#                     CPU["model"] = line.split(":")[1].strip()
#                 elif "model name" in line and "model_name" not in CPU:
#                     CPU["model_name"] = line.split(":")[1].strip()
#                 elif "cache size" in line and "cache" not in CPU:
#                     CPU["cache"] = line.split(":")[1].strip()
#                 if len(CPU) == 4:
#                     break
#             return CPU
#     except:
#         return {"error": "Could not read CPU info"}