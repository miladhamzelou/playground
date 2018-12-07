openssl ecparam -name prime256v1 -genkey -noout -out user1.key
openssl ec -in user1.key -pubout -out user1.pub
