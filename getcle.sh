cle=$(tr -dc 'A-Za-z0-9' < /dev/urandom | head -c 32)
echo $cle > key.txt
echo $cle