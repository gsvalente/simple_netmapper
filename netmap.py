#!/usr/bin/env python3
"""
Simple Network Mapper - A quick and easy network sweep tool
Author: Pentesting Tool
Description: Performs network discovery using ICMP ping requests
"""

import subprocess
import threading
import argparse
import ipaddress
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import platform

class NetworkMapper:
    def __init__(self, max_threads=50, timeout=1):
        self.max_threads = max_threads
        self.timeout = timeout
        self.alive_hosts = []
        self.lock = threading.Lock()
        self.total_hosts = 0
        self.scanned_hosts = 0
        
    def ping_host(self, ip):
        """Ping a single host to check if it's alive"""
        try:
            # Determine ping command based on OS
            if platform.system().lower() == "windows":
                cmd = ["ping", "-n", "1", "-w", str(self.timeout * 1000), str(ip)]
            else:
                cmd = ["ping", "-c", "1", "-W", str(self.timeout), str(ip)]
            
            # Execute ping command
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=self.timeout + 2)
            
            with self.lock:
                self.scanned_hosts += 1
                progress = (self.scanned_hosts / self.total_hosts) * 100
                print(f"\rProgress: {progress:.1f}% ({self.scanned_hosts}/{self.total_hosts})", end="", flush=True)
            
            if result.returncode == 0:
                with self.lock:
                    self.alive_hosts.append(str(ip))
                    print(f"\n[+] {ip} is alive")
                return str(ip)
            
        except subprocess.TimeoutExpired:
            with self.lock:
                self.scanned_hosts += 1
        except Exception as e:
            with self.lock:
                self.scanned_hosts += 1
            
        return None
    
    def scan_network(self, network_range):
        """Scan a network range for alive hosts"""
        try:
            network = ipaddress.ip_network(network_range, strict=False)
            hosts = list(network.hosts())
            
            # If it's a single host, include it
            if network.num_addresses == 1:
                hosts = [network.network_address]
            
            self.total_hosts = len(hosts)
            print(f"[*] Scanning {self.total_hosts} hosts in {network_range}")
            print(f"[*] Using {min(self.max_threads, self.total_hosts)} threads")
            print("-" * 50)
            
            start_time = time.time()
            
            # Use ThreadPoolExecutor for concurrent pings
            with ThreadPoolExecutor(max_workers=min(self.max_threads, self.total_hosts)) as executor:
                futures = [executor.submit(self.ping_host, host) for host in hosts]
                
                # Wait for all threads to complete
                for future in as_completed(futures):
                    future.result()
            
            end_time = time.time()
            scan_duration = end_time - start_time
            
            print(f"\n\n" + "=" * 50)
            print(f"[*] Scan completed in {scan_duration:.2f} seconds")
            print(f"[*] Found {len(self.alive_hosts)} alive hosts:")
            print("=" * 50)
            
            if self.alive_hosts:
                for host in sorted(self.alive_hosts, key=lambda x: ipaddress.ip_address(x)):
                    print(f"  {host}")
            else:
                print("  No alive hosts found")
            
            print("=" * 50)
            
        except ValueError as e:
            print(f"[!] Invalid network range: {e}")
            return False
        except KeyboardInterrupt:
            print(f"\n[!] Scan interrupted by user")
            return False
        except Exception as e:
            print(f"[!] Error during scan: {e}")
            return False
        
        return True

def main():
    parser = argparse.ArgumentParser(
        description="Simple Network Mapper - Quick and easy network sweep tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python netmap.py 192.168.1.0/24          # Scan entire subnet
  python netmap.py 192.168.1.1-50          # Scan range (not implemented yet)
  python netmap.py 192.168.1.1             # Scan single host
  python netmap.py 10.0.0.0/16 -t 100      # Use 100 threads
  python netmap.py 192.168.1.0/24 -w 2     # 2 second timeout
        """
    )
    
    parser.add_argument(
        "target",
        help="Target network range (CIDR notation) or single IP"
    )
    
    parser.add_argument(
        "-t", "--threads",
        type=int,
        default=50,
        help="Number of threads to use (default: 50)"
    )
    
    parser.add_argument(
        "-w", "--timeout",
        type=int,
        default=1,
        help="Ping timeout in seconds (default: 1)"
    )
    
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose output"
    )
    
    args = parser.parse_args()
    
    # Validate arguments
    if args.threads < 1 or args.threads > 200:
        print("[!] Thread count must be between 1 and 200")
        sys.exit(1)
    
    if args.timeout < 1 or args.timeout > 10:
        print("[!] Timeout must be between 1 and 10 seconds")
        sys.exit(1)
    
    # Print banner
    print("=" * 50)
    print("    Simple Network Mapper v1.0")
    print("    Quick & Easy Network Discovery")
    print("=" * 50)
    
    # Create mapper instance and start scan
    mapper = NetworkMapper(max_threads=args.threads, timeout=args.timeout)
    
    try:
        success = mapper.scan_network(args.target)
        if success:
            print(f"\n[*] Results saved to memory. {len(mapper.alive_hosts)} hosts discovered.")
        else:
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n[!] Scan interrupted by user")
        sys.exit(1)

if __name__ == "__main__":
    main()