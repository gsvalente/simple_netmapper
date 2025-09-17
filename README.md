# Simple Network Mapper

A **quick and easy-to-use** network sweep tool written in Python for network discovery using ICMP ping requests. Perfect for penetration testing, network administration, and security assessments.

## License

This tool is provided **as-is** for educational and legitimate network administration purposes. 

**Use responsibly and only on networks you own or have explicit permission to scan.**

## Contributing

We welcome contributions! Here's how you can help:

- **Report Bugs**: Open an issue with detailed reproduction steps
- **Suggest Features**: Share your ideas for improvements
- **Submit Code**: Fork, improve, and create a pull request
- **Improve Docs**: Help make the documentation even better

---

**If this tool helped you, please consider giving it a star!**

**Questions? Issues? Feel free to open a GitHub issue or discussion.**

## Security & Legal Notice

⚠️ **IMPORTANT**: This tool is for **authorized network testing only**

- ✅ **Authorized Use**: Your own networks, penetration testing with permission
- ❌ **Unauthorized Use**: Scanning networks without explicit permission
- 📋 **Best Practice**: Always get written authorization before scanning
- 🔒 **Responsibility**: Users are responsible for compliance with local laws

## Features

- **Lightning-fast scanning** with multi-threading (up to 200 threads)
- **CIDR notation support** (e.g., `192.168.1.0/24`, `10.0.0.0/16`)
- **Highly configurable** timeout and thread count
- **Real-time progress tracking** with live updates
- **Cross-platform compatibility** (Windows, Linux, macOS)
- **Clean, professional output** with sorted results
- **Memory-efficient** - results stored in memory during scan
- **Thread-safe** operations for reliable concurrent scanning

## Requirements

- **Python 3.6+** (recommended: Python 3.8+)
- **No external dependencies** - uses only Python standard library
- **Network permissions** for ICMP ping operations

## Quick Start

### Option 1: Direct Download
1. Download `netmap.py` to your desired directory
2. Open terminal/command prompt in that directory
3. Run: `python netmap.py --help`

### Option 2: Git Clone
```bash
git clone <repository-url>
cd simple_netmap
python netmap.py --help
```

### Option 3: Make Executable (Linux/macOS)
```bash
chmod +x netmap.py
./netmap.py --help
```

## Usage

### Basic Commands

```bash
# Scan entire subnet (most common use case)
python netmap.py 192.168.1.0/24

# Scan single host
python netmap.py 192.168.1.1

# Fast scan with more threads
python netmap.py 192.168.1.0/24 -t 100

# Slower, more reliable scan
python netmap.py 192.168.1.0/24 -w 3 -t 20
```

### Command Line Options

```
usage: netmap.py [-h] [-t THREADS] [-w TIMEOUT] [-v] target

Simple Network Mapper - Quick and easy network sweep tool

positional arguments:
  target                Target network range (CIDR notation) or single IP

options:
  -h, --help            Show help message and exit
  -t, --threads THREADS Number of threads to use (default: 50, max: 200)
  -w, --timeout TIMEOUT Ping timeout in seconds (default: 1, max: 10)
  -v, --verbose         Enable verbose output (currently unused)
```

### Real-World Examples

```bash
# Home network scan
python netmap.py 192.168.1.0/24

# Corporate network scan (larger subnet)
python netmap.py 10.0.0.0/16 -t 100 -w 2

# Quick single host check
python netmap.py 8.8.8.8

# Thorough scan with conservative settings
python netmap.py 172.16.0.0/24 -t 25 -w 3

# Maximum speed scan (use with caution)
python netmap.py 192.168.0.0/16 -t 200 -w 1
```

## Sample Output

```
==================================================
    Simple Network Mapper v1.0
    Quick & Easy Network Discovery
==================================================
[*] Scanning 254 hosts in 192.168.1.0/24
[*] Using 50 threads
--------------------------------------------------
Progress: 15.7% (40/254)
[+] 192.168.1.1 is alive
[+] 192.168.1.10 is alive
[+] 192.168.1.15 is alive
[+] 192.168.1.100 is alive
Progress: 100.0% (254/254)

==================================================
[*] Scan completed in 12.34 seconds
[*] Found 4 alive hosts:
==================================================
  192.168.1.1
  192.168.1.10
  192.168.1.15
  192.168.1.100
==================================================
[*] Results saved to memory. 4 hosts discovered.
```

## Performance Guide

### Thread Configuration
| Network Size | Recommended Threads | Use Case |
|--------------|-------------------|----------|
| Single Host | 1 | Quick host check |
| /28 (16 hosts) | 10-20 | Small networks |
| /24 (254 hosts) | 50-75 | Home/office networks |
| /16 (65k hosts) | 100-200 | Large corporate networks |

### Timeout Settings
| Network Type | Recommended Timeout | Description |
|--------------|-------------------|-------------|
| Local LAN | 1 second | Fast, reliable connections |
| Remote/WAN | 2-3 seconds | Internet or slow connections |
| Unreliable | 5+ seconds | High-latency or lossy networks |

### Speed vs Reliability
- **Maximum Speed**: `-t 200 -w 1` (may miss some hosts)
- **Balanced**: `-t 50 -w 1` (default, good for most cases)
- **Maximum Reliability**: `-t 25 -w 3` (slower but catches more hosts)

## Limitations & Important Notes

- **ICMP Dependency**: Uses ICMP ping, so hosts with ping disabled won't be detected
- **Network Permissions**: Requires appropriate network permissions for ICMP operations
- **Performance Factors**: Speed depends on network latency and host response times
- **Memory Storage**: Results are stored in memory only (not saved to file)
- **Thread Limits**: Maximum 200 threads to prevent system overload

## Troubleshooting

### Linux/macOS Permission Issues
If you encounter permission errors:
```bash
# Option 1: Run with sudo
sudo python netmap.py 192.168.1.0/24

# Option 2: Set capabilities (Linux only)
sudo setcap cap_net_raw+ep /usr/bin/python3
```

### Windows Issues
- **Firewall**: Ensure Windows Firewall allows ICMP traffic
- **Admin Rights**: May need to run Command Prompt as Administrator
- **Antivirus**: Some antivirus software may block network scanning

### No Hosts Found?
1. **Verify connectivity**: `ping 8.8.8.8` to test internet connection
2. **Check target network**: Ensure the network range is correct
3. **Increase timeout**: Try `-w 3` for slower networks
4. **Reduce threads**: Try `-t 25` for more reliable scanning
5. **Test single host**: `python netmap.py <known-ip>` to verify tool works

### Common Error Messages
| Error | Solution |
|-------|---------|
| "Invalid network range" | Check CIDR notation (e.g., `192.168.1.0/24`) |
| "Permission denied" | Run with elevated privileges |
| "Timeout expired" | Increase timeout with `-w` option |
| "Thread count must be..." | Use threads between 1-200 |

## Security & Legal Notice

**IMPORTANT**: This tool is for **authorized network testing only**

- **Authorized Use**: Your own networks, penetration testing with permission
- **Unauthorized Use**: Scanning networks without explicit permission
- **Best Practice**: Always get written authorization before scanning
- **Responsibility**: Users are responsible for compliance with local laws

## Future Enhancements

Potential features for future versions:
- **File Output**: Save results to CSV, JSON, or XML
- **Port Scanning**: Basic port discovery capabilities  
- **Advanced Reporting**: Detailed scan reports with timestamps
- **Colored Output**: Enhanced visual feedback
- **GUI Version**: Graphical user interface option



### Development Setup
```bash
git clone <repository-url>
cd simple_netmap
python netmap.py --help  # Test the tool
```
