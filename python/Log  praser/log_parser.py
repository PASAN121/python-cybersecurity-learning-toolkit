from pathlib import Path
import re   
import json

def validate_file(file):
    '''this function checks if the file exists and is a file'''
    
    file=Path(file) #convert to path object for better handling

    if not file.exists():
        print(f"Error: The file '{file}' does not exist.")
        return False
    
    if not file.is_file():
        print(f"Error: The path '{file}' is not a file.")
        return False
    return file

def read_log_file(file_path):
    
    with open(file_path, 'r',encoding="utf-8", errors='ignore') as file:
        log_data = file.readlines()
    return log_data
   

pattern =r"(\w+\s+\d+\s+\d+:\d+:\d+).*?(Failed|Accepted) password for (?:invalid user )?(\w+) from (\d+\.\d+\.\d+\.\d+)"


def parsed_log_data(line):
    
    match=re.search(pattern,line) #more flexible than the .match()
    
    if not match:
        return None
    
    timestamp, status, username, ip_address = match.groups()

    return {
        "timestamp": timestamp,
        "status": status,
        "username": username,
        "ip_address": ip_address
    }

def save_to_json(parsed_data,output_file):
    
    """
    Save parsed log entries to a JSON file.

    Args:
        parsed_data (list): List of dictionaries containing parsed log data.
        output_file (str): Name or path of the JSON file to create.
    """
    with open(output_file,"w") as file:
        json.dump(parsed_data, file, indent=4) # convert python list/dicts to json and save
        
    print(f"Saved {len(parsed_data)} entries to {output_file}")
    
    
    
def generate_summary():
    pass     
    
def main():
    log_file_path = input("Enter the path to the log file: ")
    validated_file = validate_file(log_file_path)

    if not validated_file:
        print("Exiting program due to invalid file.")
        return
    try:
        log_data = read_log_file(validated_file)
    except Exception as e:
        print(f"Error reading file:{e}")
        return
    
    # Parse log entries
    parsed_log = []
    for line in log_data:
        result = parsed_log_data(line)
        if result:
            parsed_log.append(result)

    print(f"\nParsed {len(parsed_log)} log entries")
    
    if len(parsed_log)==0:
        print("Warning: No log entries matched the pattern. Check your log file format.")
        return
        
    
    # Show first 5 entries as preview
    print("\nFirst few entries:")
    for entry in parsed_log[:5]:
        print(f"  {entry}")
    if len(parsed_log) > 5:
        print(f"  ... and {len(parsed_log) - 5} more")
         

    #create the folder where the log file lives
    output_folder = validated_file.parent / "outputs"
    output_folder.mkdir(exist_ok=True)
    output_file = output_folder / "parsed_logs.json"

    save_to_json(parsed_log, output_file)
     
    

 
            
                   
if __name__ == "__main__":
    main()
    


 