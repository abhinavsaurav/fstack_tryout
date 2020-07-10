import hashlib 

# Load the NIST list of 10,000 most commonly used passwords
with open('nist_10000.txt', newline='') as bad_passwords:
    nist_bad = bad_passwords.read().split('\n')
print(nist_bad[1:10])


# example hash
word = 'blueberry'
hashlib.md5(word.encode()).hexdigest()

# Finding the hashed passwords for the leaked data HERE!!! 
hashed_bad_pass={}
leaked_users_table = {
    'jamie': {
        'username': 'jamie',
        'role': 'subscriber',
        'md5': '203ad5ffa1d7c650ad681fdff3965cd2'
    }, 
    'amanda': {
        'username': 'amanda',
        'role': 'administrator',
        'md5': '315eb115d98fcbad39ffc5edebd669c9'
    }, 
    'chiaki': {
        'username': 'chiaki',
        'role': 'subscriber',
        'md5': '941c76b34f8687e46af0d94c167d1403'
    }, 
    'viraj': {
        'username': 'viraj',
        'role': 'employee',
        'md5': '319f4d26e3c536b5dd871bb2c52e3178'
    },
}
for passw in nist_bad:
    hashed_value=hashlib.md5(passw.encode()).hexdigest()
    hashed_bad_pass[hashed_value]=passw
passw_recovered={}
for key in leaked_users_table.keys():
    if leaked_users_table[key]['md5'] in hashed_bad_pass.keys():
#         print(leaked_users_table[key]['md5'],"::",hashed_bad_pass[leaked_users_table[key]['md5']])
        passw_recovered[key]=hashed_bad_pass[leaked_users_table[key]['md5']]
print(passw_recovered)