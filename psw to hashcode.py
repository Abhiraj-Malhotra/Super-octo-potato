import bcrypt

# Declaring our password
password = b'AbhMa058'

# Adding the salt to password
salt = bcrypt.gensalt()
# Hashing the password
hashed = bcrypt.hashpw(password, salt)

# printing the salt
print("Salt :")
print(salt)

# printing the hashed
print("Hashed")
print(hashed)


import crypt

hashed = '$2b$12$v6CP.62vrITxjpHYJbIbmudZxWS/zCFLAOsuqSnsDDZCjcjlStCIq'

psw = crypt.hashpw(hashed)
print(psw)