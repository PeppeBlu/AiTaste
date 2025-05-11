import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv(dotenv_path="config.env")

prompt_setting = os.getenv("PROMPT_SETTING")

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

ingredienti_comuni = [
    "Uova",
    "Latte",
    "Latte vegetale",
    "Formaggio",
    "Mozzarella",
    "Yogurt",
    "Burro",
    "Margarina",
    "Passata di pomodoro",
    "Salsa barbecue",
    "Maionese",
    "Ketchup",
    "Senape",
    "Carote",
    "Zucchine",
    "Cipolla",
    "Aglio",
    "Mele",
    "Banane",
    "Limone",
    "Prosciutto cotto",
    "Prosciutto crudo",
    "Tonno in scatola",
    "Patatine fritte surgelate",
    "Spinaci surgelati",
    "Verdure miste surgelate",
    "Pasta sfoglia",
    "Pasta brisée",
    "Parmigiano",
    "Grana padano",
    "Tofu",
    "Hummus",
    "Insalata in busta"
]

ingredienti_selezionati = []

