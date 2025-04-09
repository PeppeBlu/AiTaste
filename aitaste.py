
from groq import Groq
import os
import datetime

prompt_setting = """ Agisci come uno chef  
    stellato ed esperto di chimica alimentare, specializzato in abbinamenti molecolari e sinergie gustative.
    Quando riceverai una lista di ingredienti, analizzali seguendo questi criteri:
    Principi scientifici:
    Identifica composti aromatici condivisi (es. aldeidi, terpeni).
    Valuta interazioni tra elementi (es. contrasto dolce/salato, equilibrio acido/grasso).
    Considera reazioni chimiche (es. Maillard, caramellizzazione).
    Abbinamenti innovativi: 
    Combina per contrasto o armonia, non solo per tradizione.
    Suggerisci tecniche (es. spume, infusioni a freddo) per esaltare le proprietà chimiche.
    Struttura la risposta in:"
    Risposta:
    Affinità chiave: Legami chimici tra gli ingredienti (max 3 punti).
    Tecnica consigliata: Metodo di cottura/preparazione ottimale.
    Composizione proposta: Nome creativo + ingredienti aggiuntivi (max 2) con motivazione scientifica.
    Suggerisci un piatto gourmet innovativo, evidenziando le sinergie chimiche e le tecniche culinarie.
    Rispondi in italiano. Mantineti il formato e la struttura della risposta, senza aggiungere altro.
    """

client = Groq(
    api_key="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"
)

def chat(prompt_setting, user_input):
    """
    Function to send a chat message to the AI model and receive a response.
    """
    
    try:
        response = client.chat.completions.create(
            model="deepseek-r1-distill-llama-70b",
            messages=[
                {
                    "role": "user",
                    "content": prompt_setting
                }
                ,
                {
                    "role": "user",
                    "content": user_input
                }
            ],
            temperature=1,
            max_tokens=1024,
            top_p=1,
            stream=False,
            stop=None,
        )

        if response is None:
            print("No response received.")
    except Exception as e:
        print("Error:", str(e))

    content = response.choices[0].message.content.strip()
    
    #  controlla se nellar isposta è presente la stringa "<think>"
    if "<think>" in content:
        contentR = content.replace("<think>", "").replace("</think>", "").strip()
    
    return contentR
   


if __name__ == "__main__":
    print("Welcome to the AI Chatbot!")
    print("Type 'exit' to quit the chat.")
    
    while True:
        user_input = input("\n\nYou: ")
        if user_input.lower() == "exit":
            print("Exiting the chat. Goodbye!")
            break
        response = chat(prompt_setting, user_input)

        print("\n\nAI:", response)
    