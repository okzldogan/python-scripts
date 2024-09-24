import secrets

# Generate random strong password
def generate_password():
    # Characters to be used in the password
    CHARS="0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz!?-_+" 

    # The password should have at least 1 of the characts in special_chars
    special_chars = "-_+"

    more_special_chars = "!?"

    PASSWORD_LENGTH=14

    pwd = ''
    # Create a password until it has at least 1 of the characters in special_chars and more_special_chars

    while not any(c in pwd for c in special_chars) or not any(c in pwd for c in more_special_chars):
        pwd = ''
        for i in range(PASSWORD_LENGTH):
            pwd += ''.join(secrets.choice(CHARS))
        
    return pwd
