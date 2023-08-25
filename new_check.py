from datetime import datetime
import ssl
import socket
import csv
import pandas as pd

def get_days_until_expiry(hostname, port=443):
    try:
        context = ssl.create_default_context()
        with socket.create_connection((hostname, port)) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as sslsock:
                cert = sslsock.getpeercert()
                expiration_date_str = cert['notAfter']
                expiration_date = datetime.strptime(expiration_date_str, '%b %d %H:%M:%S %Y %Z')
                current_date = datetime.utcnow()
                days_until_expiry = (expiration_date - current_date).days
                return days_until_expiry
    except Exception as e:
        return None

input_csv = 'file.csv'   # Replace with the name of your input CSV file
output_csv = 'output.csv'  # Replace with the name of the output CSV file

try:
    df = pd.read_csv(input_csv)  # Read input CSV into a pandas DataFrame
    df['DaysUntilExpiry'] = df['DomainName'].apply(get_days_until_expiry)  # Apply function to calculate days until expiry

    filtered_df = df[df['DaysUntilExpiry'] <= 10]  # Filter rows with 10 days or less until expiry

    filtered_df.to_csv(output_csv, index=False)  # Write filtered DataFrame to output CSV

    print(filtered_df)
except FileNotFoundError:
    print(f"Error: Input CSV file '{input_csv}' not found.")
except Exception as e:
    print(f"Error: {e}")
