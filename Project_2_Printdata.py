import json #Reads JSON data

def main():
    file = open("Project_2.json", "r") #Opens the JSON file for reading
    DATA = json.load(file) #Loads the info into a python dictionary
    file.close()

    print("====≽ Machine Name ≼====") 
    print(DATA["machine_name"]) #Value for the hostname loaded from the JSON file

    print("\n====≽ Users and Groups ≼====")
    for user in DATA["users_and_groups"]: #Loops through the userlist
        print(user["username"] + " : " + user["group"]) #FoPrinsrmats the username and UID

    print("\n====≽ Processor Info ≼====")
    CPU = DATA["processor_info"] #Loads JSON dictionary and prints the output with its label
    print("Vendor ID: " + CPU["vendor_id"])
    print("Model: " + CPU["model"]) #"+" is used to connect the strings
    print("Model Name: " + CPU["model_name"])
    print("Cache: " + CPU["cache"])

    print("\n====≽ Services ≼====")
    for item in DATA["service_status"]:
        print(item["name"] + " : " + item["status"]) #Loops through the service list and prints the status
