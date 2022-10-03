import os
from dotenv import load_dotenv

load_dotenv()

my_token = os.getenv("TOKEN")

print(my_token)