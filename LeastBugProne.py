from datetime import datetime
import OpenSSL
import ssl
import socket
import csv
'''least bug prone code'''

def get_days_until_expiry(hostname, port=443):
    try:
        socket.setdefaulttimeout(15)  
        cert = ssl.get_server_certificate((hostname, port))
        x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert)
        expiration_bytes = x509.get_notAfter()
        timestamp = expiration_bytes.decode('utf-8')
        expiration_date = datetime.strptime(timestamp, '%Y%m%d%H%M%SZ')
        current_date = datetime.utcnow()
        days_until_expiry = (expiration_date - current_date).days
        return days_until_expiry
    except socket.timeout:
        return "Connection Timed out"
    except Exception as e:
        return None, str(e)

input_csv = 'file.csv'   
output_csv = 'output2.csv' 
error_csv = 'error.csv'

try:
    with open(input_csv, 'r') as infile, open(output_csv, 'w', newline='') as outfile, open(error_csv, 'w', newline='') as errorfile:
        reader = csv.DictReader(infile)
        writer = csv.writer(outfile)
        error_writer = csv.writer(errorfile)
        writer.writerow(["DomainName", "DaysUntilExpiry"]) 
        error_writer.writerow(["DomainName", "Error"])  

        for row in reader:
            hostname = row["DomainName"]
            days_until_expiry = get_days_until_expiry(hostname)
            if isinstance(days_until_expiry, int):  
                if days_until_expiry <= 10:
                    writer.writerow([hostname, days_until_expiry])
                    print(f"Domain: {hostname}, Days until expiry: {days_until_expiry} days")
                else:
                    print("greater than 10")
            else:
                error_writer.writerow([hostname, days_until_expiry])
                print(f"Error processing domain {hostname}: {days_until_expiry}")

except FileNotFoundError:
    print(f"Error: Input CSV file '{input_csv}' not found.")
except Exception as e:
    print(f"Error: {e}")
