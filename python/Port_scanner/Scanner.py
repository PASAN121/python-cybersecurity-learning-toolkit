import json
import socket
import argparse
#import threading
from datetime import datetime
import os
from concurrent.futures import ThreadPoolExecutor, as_completed


def ip_sp_ep_validator(ip,sp,ep):
    """
    Validates:
    - IPv4 format
    - Port range correctness
    """
    
    
    ip_parts=ip.split(".") #split ip to parts
 
    #validate IP
    if len(ip_parts) != 4:
        print("Invalid Ip address")
        return False

    for part in ip_parts:
        try:
            if not 0 <= int(part) <= 255:
                print("Invalid IP address")
                return False
        except ValueError:
            print("Invalid IP address")
            return False

  
    # Validate ports
    try:
        start_port = sp
        end_port = ep

        if end_port < start_port:
            print("Error: start port must be less than or equal to end port")
            return False

    except ValueError:
        print("Invalid port number")
        return False

    return True



def scan(ip,port):
    """
    TCP connect scan for a single port.
    """   
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM) #for create tcp connection(full handshake)
    s.settimeout(1)

    try:
        result = s.connect_ex((ip,port)) #create tcp connection(only make connection no checker)

        if result ==0: #0 means connect successfully (full handshake)
            return True
        
        else:
            return False
        
    except socket.error:
        return False
    
    finally:
        s.close()
 
def grab_banner(ip,port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)

        s.connect((ip, port))   
        
        banner=s.recv(1024).decode(errors="ignore").strip()
        
        s.close()
        
        if banner:
            return banner
        else:
            return "No banner received"

    except:
        return "No banner / filtered / timeout"         
        
        
        
   
               
#threading  worker
def scan_worker(ip, port):
    if scan(ip, port):
        banner = grab_banner(ip, port)

        return {
            "port": port,
            "status": "Open",
            "banner": banner
        }

    return None
        
def save_latest(data):
    file_name = "reports/latest_scan.json"

    with open(file_name, "w") as f:
        json.dump(data, f, indent=2)


def save_history(data):
    os.makedirs("reports/history", exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_name = f"reports/history/scan_{timestamp}.json"

    with open(file_name, "w") as f:
        json.dump(data, f, indent=2)
        
        
def run_scan(ip, start_port, end_port):
    results = []
    total = end_port - start_port + 1
    completed = 0

    print(f"\nScanning {total} ports...\n")

    with ThreadPoolExecutor(max_workers=100) as executor:

        futures = {
            executor.submit(scan_worker, ip, port): port
            for port in range(start_port, end_port + 1)
        }

        for future in as_completed(futures):
            completed += 1
            print(f"\rProgress: {completed}/{total}", end="")

            result = future.result()
            if result:
                results.append(result)

    print("\nScan completed.\n")
    return results

def main():
    """
    CLI entry point for the port scanner.
    """
    parser = argparse.ArgumentParser(
        description="Simple Port Scanner"
    )

    #arguments for process
    parser.add_argument("target_ip", help="Target IP address")
    parser.add_argument("start_port", type = int ,help="Starting port")
    parser.add_argument("end_port", type = int, help="Ending port") #no later casting

    args = parser.parse_args()

    # Validate inputs before scanning
    if not ip_sp_ep_validator(args.target_ip, args.start_port, args.end_port):
        print("Validation failed. Exiting.")
        return

    print(f"Target IP: {args.target_ip}")
    print(f"Port Range: {args.start_port} - {args.end_port}")
    print("-" * 40)
        
 
    '''
    #proper result with collector
    
    threads=[]
    

    for port in range(args.start_port, args.end_port + 1):
        t=threading.Thread(target=scan_worker,args=(args.target_ip,port,open_ports))
        threads.append(t)
        t.start()
        
    #wait for all threads to finish
    
    for t in threads:
        t.join()
    '''
    
    results = run_scan(
        args.target_ip,
        args.start_port,
        args.end_port
    )

    #output moved OUT of loop
    print("\nOpen Ports + Services:\n")

    for r in sorted(results, key=lambda x: x["port"]):
        print(f"Port {r['port']} is {r['status']}")
        print(f"    Banner: {r['banner']}\n")
        
   
    save_latest(results)
    save_history(results)

    
            
        
        
    
    


if __name__ == "__main__":
    main()