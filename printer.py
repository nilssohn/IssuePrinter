from subprocess import Popen
import json, requests, datetime, dateutil.parser, pytz
#Main function prompts the user for what they want to print in the repo
def main():
	'''This could be changed at a later period, but they would need to make sure
		the repo is valid
	'''
	base_url = "https://api.github.com/repos/chtinahow/cocktail-curator/issues"
	query_param = ""
	exit_code = "0"
	user_input = ""
	json_data = ""

	#This is the while loop that continues to prompt until exit code 0 is inputted
	while user_input != exit_code:
            print("1) Print All Issues")
            print("2) Print Issues By Assignee")
            print("3) Check New Issues By Creation Date")
            user_input = raw_input("Enter an input (0 to exit):\n")

            if user_input == "1":
                query_param = ""
                json_data = requests.get(base_url + query_param).json()
                formatted_data = filter_data(json_data)
                send_to_printer(formatted_data)
            elif user_input == "2":
                query_param = "?assignee=" + raw_input("Input the user id: ")
                json_data = requests.get(base_url + query_param).json()
                formatted_data = filter_data(json_data)
                send_to_printer(formatted_data)
            elif user_input == "3":
                json_data = requests.get(base_url + query_param).json()
                formatted_data = filter_by_time(json_data)
                send_to_printer(formatted_data)
'''
	This filters tickets by the given time. It checks the current time
	and subtracts it from 30 minutes. If a updated_at is within that timedelta
	it will print the ticket
'''
def filter_by_time(json_data):
    size = len(json_data)
    new_tickets = []
    time = datetime.datetime.utcnow().replace(tzinfo = pytz.utc)
    prev30 = time - datetime.timedelta(minutes=30)
    #look at the curl command
    for issueNumber in range(0,size):
        obj = {}
        ticket_time = dateutil.parser.parse(json_data[issueNumber]["updated_at"])
        if(ticket_time <= time and ticket_time >= prev30 ):
            obj["url"] = json_data[issueNumber]["url"].encode()
	    obj["title"] = json_data[issueNumber]["title"].encode()
	    obj["body"] = json_data[issueNumber]["title"].encode()
	    if (json_data[issueNumber]["assignee"] != None):
                obj["assignee"] = json_data[issueNumber]["assignee"]["login"].encode()
            new_tickets.append(obj)
    #json_data
    return new_tickets

# filter_data takes out the wanted information for the given tickets
def filter_data(json_data):
	size = len(json_data)
	filtered_data = []
	i = 0

	for i in range(0, size):
                obj = {}
		obj["url"] = json_data[i]["url"].encode()
		obj["title"] = json_data[i]["title"].encode()
		obj["body"] = json_data[i]["title"].encode()
		if (json_data[i]["assignee"] != None):
                    obj["assignee"] = json_data[i]["assignee"]["login"].encode()
		filtered_data.append(obj)
	return filtered_data

#Function sends given ticket information to the printer
def send_to_printer(data):
        size = len(data)
		#If no tickets make it through to the printer
        if(size == 0):
            print("Nothing to print")
        for i in range(0, size):
			#Checks to see if a ticket has an assignee or not
            if("assignee" in data[i]):
                data_str = data[i]["title"] + "\n" + data[i]["assignee"] + "\n" + data[i]["url"] + "\n"
            else:
                data_str = data[i]["title"] + "\n" + data[i]["url"] + "\n"
			#These next two lines are how the print commands are sent to the printer with needed info
            command = "echo \"" + data_str + "\" | lpr"
            Popen(command, shell=True)

if __name__ == "__main__":
	main()
