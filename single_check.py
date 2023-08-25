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
print(get_days_until_expiry("hr.noveltysoft.com"))    