# Replace domain1.com and domain2.com with your domain names
domains=("google.com")

for domain in "${domains[@]}"; do
    expiration_date=$(openssl s_client -connect "$domain":443 2>/dev/null | openssl x509 -noout -dates | grep "notAfter" | cut -d= -f2)
    echo "Domain: $domain - Expiry Date: $expiration_date"
done
