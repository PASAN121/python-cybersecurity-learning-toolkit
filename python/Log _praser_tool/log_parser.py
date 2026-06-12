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
    
    
    
def generate_summary(parsed_data):
    '''Generate attack/failed summary'''
    
    from collections import Counter
    
    if not parsed_data:
        return None
    
    total=len(parsed_data)
    failed=sum(1 for entry in parsed_data if entry['status']=='Failed')
    accepted= total - failed
    
    ip_counts = Counter(entry['ip_address'] for entry in parsed_data if entry['status'] == 'Failed')
    user_counts = Counter(entry['username'] for entry in parsed_data if entry['status'] == 'Failed')

    summary = {
        "total_attempts": total,
        "failed_attempts": failed,
        "accepted_attempts": accepted,
        "failed_percentage": round((failed / total) * 100, 2) if total else 0,
        "unique_ips": len(set(entry['ip_address'] for entry in parsed_data)),
        "unique_usernames": len(set(entry['username'] for entry in parsed_data)),
        "top_5_attacker_ips": ip_counts.most_common(5),
        "top_5_targeted_users": user_counts.most_common(5)
    }

    return summary
    
    
     
    
        
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
     
    
    summary = generate_summary(parsed_log)
    summary_file = output_folder / "summary.json"
    with open(summary_file, 'w') as f:
        json.dump(summary, f, indent=4)
    print(f"Summary saved to {summary_file.resolve()}")
 
            
                   
if __name__ == "__main__":
    main()
    


 