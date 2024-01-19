# Simple HTTP Honeypot Server

## Introduction
The Simple HTTP Honeypot Server is a cybersecurity tool designed to emulate a web server for monitoring and analyzing HTTP-based interactions. It's particularly useful for understanding HTTP vulnerabilities and potential intrusion tactics. The server is built with Python and the Twisted framework, offering a robust platform for logging unauthorized access attempts and analyzing web traffic.

## Features
- **Web Server Emulation**: Simulates an HTTP server to capture and log HTTP requests.
- **Configurable Settings**: Allows customization of host, port, and target URL settings via command-line arguments.
- **Resource Inlining**: Downloads and modifies external resources like CSS, JS, and images for a more realistic emulation.
- **Extensive Logging**: Logs all incoming HTTP requests including headers, client IP, and requested paths.
- **Real-Time Monitoring**: Provides immediate insights into HTTP traffic for timely detection of suspicious activities.
- **Educational Tool**: Excellent for learning about web security and network reconnaissance techniques.

## Beta Version Notice
- **Beta Version**: Please note that this script is currently in beta. It may not be fully compatible with all websites or web services. If you encounter issues or have suggestions for improvement, feel free to push a pull request. Contributions are greatly appreciated!

## Requirements
- Python 3.x
- Twisted Python library
- BeautifulSoup4 Python library
- Requests Python library

## Installation
To set up the HTTP honeypot server, execute the following commands:

```bash
git clone https://github.com/0xNslabs/http-honeypot.git
cd http-honeypot
pip install twisted beautifulsoup4 requests
```

## Usage
Run the server with the necessary arguments for host, port, and the target URL to clone. 
By default, it binds to all interfaces (0.0.0.0) at port 80.

```bash
python3 http_honeypot.py --host 0.0.0.0 --port 80 --url https://example.com
```

## Logging
Interaction logs are stored in http_honeypot.log, providing detailed records of all HTTP requests, including source IP, requested URLs, and headers.

## Simple HTTP Honeypot in Action
![Simple HTTP Honeypot in Action](https://raw.githubusercontent.com/0xNslabs/http-honeypot/main/PoC.png)
*This image illustrates the Simple HTTP Honeypot Server capturing real-time HTTP requests.*

## Other Simple Honeypot Services

Check out the other honeypot services for monitoring various network protocols:

- [DNS Honeypot](https://github.com/0xNslabs/dns-honeypot) - Monitors DNS interactions.
- [FTP Honeypot](https://github.com/0xNslabs/ftp-honeypot) - Simulates an FTP server.
- [LDAP Honeypot](https://github.com/0xNslabs/ldap-honeypot) - Mimics an LDAP server.
- [HTTP Honeypot](https://github.com/0xNslabs/http-honeypot) - Monitors HTTP interactions.
- [HTTPS Honeypot](https://github.com/0xNslabs/https-honeypot) - Monitors HTTPS interactions.
- [NTP Honeypot](https://github.com/0xNslabs/ntp-honeypot) - Monitors Network Time Protocol interactions.
- [PostgreSQL Honeypot](https://github.com/0xNslabs/postgresql-honeypot) - Simulates a PostgreSQL database server.
- [SIP Honeypot](https://github.com/0xNslabs/sip-honeypot) - Monitors SIP (Session Initiation Protocol) interactions.
- [SSH Honeypot](https://github.com/0xNslabs/ssh-honeypot) - Emulates an SSH server.
- [TELNET Honeypot](https://github.com/0xNslabs/telnet-honeypot) - Simulates a TELNET server.

## Security and Compliance
- **Caution**: Operate this honeypot within secure, controlled settings for research and learning purposes.
- **Compliance**: Deploy this honeypot in accordance with local and international legal and ethical standards.

## License
This project is available under the MIT License. See the LICENSE file for more information.