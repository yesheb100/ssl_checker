from datetime import datetime
import OpenSSL
import ssl
import socket
import csv

#hostname = 'portal.voicealerts.com'
port = 443

filename = open('file.csv', 'r')
file = csv.DictReader(filename)

domain = []
expire = []
for col in file:
    domain.append(col['DomainName'])


    
    
for hostname in domain:
    
    try:
        cert = ssl.get_server_certificate((hostname, port))
        x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert)
        expiration_bytes = x509.get_notAfter()

    
        timestamp = expiration_bytes.decode('utf-8')
        expiration_date = datetime.strptime(timestamp, '%Y%m%d%H%M%SZ')
    
        current_date = datetime.utcnow()
        days_until_expiry = (expiration_date - current_date).days
        if days_until_expiry <=10:
            expire.append(hostname)
    #print(f"SSL Certificate for {hostname} expires on: {expiration_date.date().isoformat()}")
    #print(f"Days until expiry: {days_until_expiry} days")
    except socket.gaierror as e:
        print(f"Error resolving hostname: {e}")
    except Exception as e:
        print(f"Error: {e}")
print(expire)
'''except socket.gaierror as e:
    print(f"Error resolving hostname: {e}")
except Exception as e:
    print(f"Error: {e}")
'''