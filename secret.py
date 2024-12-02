import secrets

SECRET_KEY = secrets.token_hex(32)  # تولید یک کلید 32 بایتی به صورت هگزادسیمال
print(SECRET_KEY)