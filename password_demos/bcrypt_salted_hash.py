import bcrypt
password = b"studyhard"
# Hash a password for the first time, with a certain number of rounds
salt = bcrypt.gensalt(14)
hashed = bcrypt.hashpw(password, salt)
print(salt)
print(hashed)

# Check a plain text string against the salted, hashed digest
bcrypt.checkpw(password, hashed)


# Trying some new hash values and keys

hashed = b'$2b$14$EFOxm3q8UWH8ZzK1h.WTZeRcPyr8/X0vRfuL3/e9z7AKIMnocurBG'
password1=b"securepassword"
password2=b"learningisfun"
salt=bcrypt.gensalt(14)
# hashed1=bcrypt.hashpw(password,salt)

print(bcrypt.checkpw(password2,hashed))

