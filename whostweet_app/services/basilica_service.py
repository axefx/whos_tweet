import basilica
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("BASILICA_API_KEY")

connection = basilica.Connection(API_KEY)
