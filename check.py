from datetime import datetime
import OpenSSL
import ssl
import socket
import csv

def get_days_until_expiry(hostname, port=443):
    try:
        cert = ssl.get_server_certificate((hostname, port))
        x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert)
        expiration_bytes = x509.get_notAfter()
        timestamp = expiration_bytes.decode('utf-8')
        expiration_date = datetime.strptime(timestamp, '%Y%m%d%H%M%SZ')
        current_date = datetime.utcnow()
        days_until_expiry = (expiration_date - current_date).days
        return days_until_expiry
    except Exception as e:
        return None

input_csv = 'file.csv'   # Replace with the name of your input CSV file
output_csv = 'output2.csv'  # Replace with the name of the output CSV file

try:
    with open(input_csv, 'r') as infile, open(output_csv, 'w', newline='') as outfile:
        reader = csv.DictReader(infile)
        writer = csv.writer(outfile)
        writer.writerow(["DomainName", "DaysUntilExpiry"])  # Write header to the output CSV

        for row in reader:
            hostname = row["DomainName"]
            days_until_expiry = get_days_until_expiry(hostname)
            if days_until_expiry is not None and days_until_expiry <= 10:
                writer.writerow([hostname, days_until_expiry])
                print(f"Domain: {hostname}, Days until expiry: {days_until_expiry} days")

except FileNotFoundError:
    print(f"Error: Input CSV file '{input_csv}' not found.")
except Exception as e:
    print(f"Error: {e}")
