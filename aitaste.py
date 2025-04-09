
from groq import Groq
import os
import datetime
from dotenv import load_dotenv
import gradio as gr

ingredienti_comuni = [
    "Pomodoro",
    "Basilico",
    "Mozzarella",
    "Olio d'oliva",
    "Aglio",
    "Peperoncino",
    "Sale",
    "Pepe nero",
    "Origano",
    "Acciughe",
    "Capperi",
    "Funghi",
    "Zucchine",
    "Melanzane",
    "Carciofi",
    "Prosciutto crudo",
    "Salame piccante"
]

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
    Affinità chiave: Legami chimici tra gli ingredienti (max 3 punti).
    Tecnica consigliata: Metodo di cottura/preparazione ottimale.
    Composizione proposta: Nome creativo + ingredienti aggiuntivi (max 2) con motivazione scientifica.
    Suggerisci un piatto gourmet innovativo, evidenziando le sinergie chimiche e le tecniche culinarie.
    Rispondi in italiano. Mantineti il formato e la struttura della risposta, senza aggiungere altri ingredienti oltre
    a quelli inseriti dall'utente.
    """

ingredienti_selezionati = []

# Specifica il percorso del file config.env
load_dotenv(dotenv_path="config.env")

# Ora puoi accedere alla variabile d'ambiente
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
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

        content = response.choices[0].message.content.strip()
    
        #  controlla se nella risposta è presente la stringa "<think>" e rimuove quella parte
        # Se "<think>" è presente, rimuovi il contenuto tra "<think>" e "</think>"
        if "<think>" in content:
            start_index = content.index("<think>")
            end_index = content.index("</think>") + len("</think>")
            contentR = content[:start_index] + content[end_index:]
        
        return contentR.strip()

    except Exception as e:
        print("Error:", str(e))

# Funzione per inviare gli ingredienti selezionati al chatbot
def invia_ingredienti(history):
    # Combina gli ingredienti selezionati in una stringa
    input_text = ", ".join(ingredienti_selezionati)
    
    # Ottieni la risposta dal chatbot
    response = chat(prompt_setting, input_text)
    
    # Aggiorna la cronologia con il messaggio dell'utente e la risposta del chatbot
    history.append({"role": "user", "content": input_text})
    history.append({"role": "assistant", "content": response})
    
    # Restituisci il contenuto aggiornato del chatbot e la cronologia
    return history, history

# Funzione per selezionare o deselezionare un ingrediente
def toggle_ingrediente(ingredienti):
    global ingredienti_selezionati

    if isinstance(ingredienti, list):
        ingredienti_selezionati = ingredienti

    return ", ".join(ingredienti_selezionati)

# Aggiungi un ingrediente personalizzato
def aggiungi_personalizzato(ingrediente):
    global ingredienti_comuni
    #capitalize the first letter
    ingrediente = ingrediente.capitalize()
    
    if ingrediente and ingrediente not in ingredienti_comuni:
        ingredienti_comuni.append(ingrediente)
    return gr.update(choices=ingredienti_comuni)

# Rimuovi un ingrediente personalizzato
def rimuovi_personalizzato(ingredienti_da_rimuovere):
    global ingredienti_comuni, ingredienti_selezionati

    # Rimuovi gli ingredienti dalla lista degli ingredienti comuni e selezionati
    for ingrediente in ingredienti_da_rimuovere:
        if ingrediente in ingredienti_comuni:
            ingredienti_comuni.remove(ingrediente)
        if ingrediente in ingredienti_selezionati:
            ingredienti_selezionati.remove(ingrediente)

    # Sincronizza i valori selezionati con le scelte disponibili
    ingredienti_selezionati = [ingrediente for ingrediente in ingredienti_selezionati if ingrediente in ingredienti_comuni]

    # Aggiorna il CheckboxGroup e il riquadro degli ingredienti selezionati
    return gr.update(choices=ingredienti_comuni, value=ingredienti_selezionati), ", ".join(ingredienti_selezionati)

# Funzione svuota_casella per svuotare la casella di testo
def svuota_casella():
    return ""

# Interfaccia gradio
def gradio_interface(input_text):
    response = chat(prompt_setting, input_text)
    return response

# Crea l'interfaccia Gradio
ai_taste_face = gr.Interface(
    fn=gradio_interface,
    inputs="text",
    outputs="text",
    title="AI Chatbot",
    description="Chat with an AI model.",
    theme="default"
)

# Funzione per inviare il messaggio e ricevere la risposta
def send_message(message, history):
    history.append({"role": "user", "content": message})
    response = chat(prompt_setting, message)
    history.append({"role": "assistant", "content": response})
    return history, "", history

# Interfaccia Gradio
def gradio_interface():
    # Inizializza la lista di ingredienti comuni per ogni sessione
    global ingredienti_comuni
    with gr.Blocks() as demo:
        gr.Markdown("<h1 style='text-align: center;'>👩‍🍳 AiTaste - Find the best combos 👨‍🍳</h1>")
        
        with gr.Row():
            # Colonna sinistra: Chatbot
            with gr.Column(scale=2):
                chatbot_interface = gr.Chatbot(label="Chatbot", height=500, type="messages")
                history = gr.State([])
                input_textbox = gr.Textbox(
                    label="Scrivi qui il tuo messaggio",
                    placeholder="Scrivi qui il tuo messaggio...",
                    show_label=False,
                    lines=1,
                    max_lines=1
                )
                input_textbox.submit(
                    send_message,
                    inputs=[input_textbox, history],
                    outputs=[chatbot_interface, input_textbox, history]
                )
                
                submit_button = gr.Button("Invia")
                submit_button.click(
                    send_message,
                    inputs=[input_textbox, history],
                    outputs=[chatbot_interface, input_textbox, history]
                )
                         
            # Colonna destra: Ingredienti
            with gr.Column(scale=1):
                gr.Markdown("### Ingredienti selezionati")
                ingredienti_selezionati_box = gr.Textbox(
                    label="",
                     interactive=False
                )
                
                set_ingredienti_button = gr.Button("Set Ingredienti")
                #se clicco Set Ingredienti, viene inviasto il messaggio al chatbot e pulito il textbox
                set_ingredienti_button.click(
                    fn=invia_ingredienti,
                    inputs=[history],
                    outputs=[chatbot_interface, history]
                ).then(
                    fn=svuota_casella,
                    inputs=[],
                    outputs=[input_textbox]
                )
                
                gr.Markdown("### Ingredienti disponibili")
                ingredienti_pillole = gr.CheckboxGroup(
                    choices=ingredienti_comuni,
                    label="",
                    interactive=True
                )
                # Aggiungi un evento per aggiornare gli ingredienti selezionati
                ingredienti_pillole.change(
                    fn=toggle_ingrediente,
                    inputs=[ingredienti_pillole],
                    outputs=[ingredienti_selezionati_box]
                )

                input_textbox.change(
                    fn=svuota_casella,
                    inputs=[],
                    outputs=[input_textbox]
                )
                
                gr.Markdown("### Aggiungi un ingrediente personalizzato")
                nuovo_ingrediente = gr.Textbox(
                    placeholder="Inserisci un nuovo ingrediente..."
                )
               
                with gr.Row():
                    aggiungi_button = gr.Button("Aggiungi")
                    #aggiunge l'ingrediente personalizzato alla lista ingredienti_comuni e pulisce il textbox
                    aggiungi_button.click(
                        fn=aggiungi_personalizzato,
                        inputs=[nuovo_ingrediente],
                        outputs=[ingredienti_pillole]
                    ).then(
                        fn=svuota_casella,
                        inputs=[],
                        outputs=[nuovo_ingrediente]
                    )


                    rimuovi_button = gr.Button("Rimuovi")
                    rimuovi_button.click(
                        fn=rimuovi_personalizzato,
                        inputs=[ingredienti_pillole],
                        outputs=[ingredienti_pillole, ingredienti_selezionati_box]
                    )                

    return demo


if __name__ == "__main__":
    demo = gradio_interface()
    demo.launch(share=True)
    