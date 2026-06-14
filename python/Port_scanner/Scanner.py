import json
import socket
import argparse


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
        
    valid_ip = args.target_ip
    valid_sp = args.start_port
    valid_ep =  args.end_port
    
    
    # Port scanning loop       
    for port in range(valid_sp,valid_ep+1):
        if scan(valid_ip,port):
            print(f"From {valid_ip} port {port} is open")
    
    
            
        
        
    
    


if __name__ == "__main__":
    main()