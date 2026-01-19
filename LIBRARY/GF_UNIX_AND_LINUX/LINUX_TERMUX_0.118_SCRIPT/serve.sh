#! /bin/bash
# Create By GF 2025-10-30 19:35

sshd
echo "OpenSSH ......... OK"

php-fpm -D
echo "PHP-FPM ......... OK"

nginx
echo "Nginx ........... OK"

pg_ctl -D /data/data/com.termux/files/home/data/pg_data start
echo "PostgreSQL ...... OK"

# EOF Signed by GF.
