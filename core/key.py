import secrets

GENERATED_SECRET_KEY = secrets.token_urlsafe(32)
print("Getting secret key programmatically -> ")
print(GENERATED_SECRET_KEY)