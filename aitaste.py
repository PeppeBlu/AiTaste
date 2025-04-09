"""
import openai
import gradio as gr
from dotenv import load_dotenv
import os

# Configura OpenRouter con la tua API key
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

openai.api_base = "https://openrouter.ai/api/v1"

# Lista di ingredienti comuni
ingredienti_comuni = ["Sale", "Pepe", "Olio", "Aglio", "Cipolla", "Pomodoro", "Basilico", "Origano", "Zucchero", "Farina"]

# Lista per gli ingredienti selezionati
ingredienti_selezionati = []

# Funzione per aggiungere o rimuovere un ingrediente
def toggle_ingrediente(ingredienti):
    global ingredienti_selezionati
    print(f"Ingredienti selezionati prima dell'aggiornamento: {ingredienti_selezionati}")
    if isinstance(ingredienti, list):
        ingredienti_selezionati = ingredienti
    print(f"Ingredienti selezionati dopo l'aggiornamento: {ingredienti_selezionati}")
    return ", ".join(ingredienti_selezionati)

# Funzione per aggiungere un ingrediente personalizzato
def aggiungi_personalizzato(ingrediente):
    global ingredienti_comuni
    #capitalize the first letter
    ingrediente = ingrediente.capitalize()
    
    if ingrediente and ingrediente not in ingredienti_comuni:
        ingredienti_comuni.append(ingrediente)
    return gr.update(choices=ingredienti_comuni)

def rimuovi_personalizzato(ingredienti_da_rimuovere):
    global ingredienti_comuni, ingredienti_selezionati

    # Debug: Verifica gli ingredienti da rimuovere
    print(f"Ingredienti da rimuovere: {ingredienti_da_rimuovere}")

    # Rimuovi gli ingredienti dalla lista degli ingredienti comuni
    for ingrediente in ingredienti_da_rimuovere:
        if ingrediente in ingredienti_comuni:
            ingredienti_comuni.remove(ingrediente)
        if ingrediente in ingredienti_selezionati:
            ingredienti_selezionati.remove(ingrediente)

    # Debug: Stato aggiornato delle liste
    print(f"Ingredienti comuni aggiornati: {ingredienti_comuni}")
    print(f"Ingredienti selezionati aggiornati: {ingredienti_selezionati}")

    # Sincronizza i valori selezionati con le scelte disponibili
    ingredienti_selezionati = [ingrediente for ingrediente in ingredienti_selezionati if ingrediente in ingredienti_comuni]
    
    # Restituisci solo i valori attesi dai componenti
    return gr.update(choices=ingredienti_comuni), ", ".join(ingredienti_selezionati)

# Funzione per inviare gli ingredienti selezionati al chatbot
def invia_ingredienti(history):
    input_text = ", ".join(ingredienti_selezionati)
    return chatbot(input_text, history)

def svuota_casella():
    # Restituisce una stringa vuota per pulire la casella di testo
    return ""

# Chatbot esistente
def chatbot(input_text, history):
    if history is None:
        history = []

    # Costruisci la storia per OpenAI
    openai_history = [{"role": "system",
                        "content": (
                            "Sei un esperto di cucina molecolare e gastronomia scientifica. Il tuo compito è aiutare l'utente ad abbinare ingredienti in modo armonioso, "
                            "tenendo conto delle compatibilità chimiche, delle molecole aromatiche condivise e dell'equilibrio tra gusto, aroma e texture. "
                            "Quando l'utente inserisce uno o più ingredienti, suggerisci combinazioni efficaci, senza proporre una vera e propria ricetta, ma comportandoti in modo "
                            "abbastanza rigoroso, mantenendoti nei limiti di un linguaggio tecnico e scientifico. Spiegando in breve perché chimicamente gli ingredienti si abbinano bene. "
                            "Non usare emoji o espressioni colloquiali." 
                            "Non essere troppo discorsivo, ma piuttosto sintetico e preciso creando schemi visivi facilmente leggibili. "
                            "Non usare mai la parola 'ricetta' e non proporre mai una ricetta. "
                        )}] 
    for user_msg, assistant_msg in history:
        openai_history.append({"role": "user", "content": user_msg})
        openai_history.append({"role": "assistant", "content": assistant_msg})

    # Aggiungi l'input dell'utente
    openai_history.append({"role": "user", "content": input_text})

    response = openai.ChatCompletion.create(
        model="openai/gpt-3.5-turbo",
        messages=openai_history,
        temperature=0.7,
        max_tokens=1000,
    )

    assistant_reply = response.choices[0].message.content

    # Aggiungi nuova coppia user/assistant
    history.append([input_text, assistant_reply])

    return history, history

# Interfaccia Gradio
def gradio_interface():
    # Inizializza la lista di ingredienti comuni per ogni sessione
    global ingredienti_comuni
    with gr.Blocks() as demo:
        gr.Markdown("<h1 style='text-align: center;'>👩‍🍳AiTaste - Find the best combos👨‍🍳</h1>")
        
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
                submit_button = gr.Button("Invia")

                # Bind chatbot interactions
                submit_button.click(
                    fn=chatbot,
                    inputs=[input_textbox, history],
                    outputs=[chatbot_interface, history]
                ).then(
                    fn=lambda: "",  # Clear the input text box
                    inputs=[],
                    outputs=[input_textbox]
                )
                input_textbox.submit(
                    fn=chatbot,
                    inputs=[input_textbox, history],
                    outputs=[chatbot_interface, history]
                ).then(
                    fn=lambda: "",  # Clear the input text box
                    inputs=[],
                    outputs=[input_textbox]
                )
                  

            # Colonna destra: Ingredienti
            with gr.Column(scale=1):
                gr.Markdown("### Ingredienti selezionati")
                ingredienti_selezionati_box = gr.Textbox(
                    label="",
                    interactive=False
                )
                set_ingredienti_button = gr.Button("Set Ingredienti")
                set_ingredienti_button.click(
                    fn=invia_ingredienti,
                    inputs=[history],
                    outputs=[chatbot_interface, history]
                )
                
                gr.Markdown("### Ingredienti disponibili")
                ingredienti_pillole = gr.CheckboxGroup(
                    choices=ingredienti_comuni,
                    label="",
                    interactive=True
                )
                ingredienti_pillole.change(
                    fn=toggle_ingrediente,
                    inputs=[ingredienti_pillole],
                    outputs=[ingredienti_selezionati_box]
                )

                gr.Markdown("### Aggiungi un ingrediente personalizzato")
                nuovo_ingrediente = gr.Textbox(
                    placeholder="Inserisci un nuovo ingrediente..."
                )
               
                with gr.Row():
                    aggiungi_button = gr.Button("Aggiungi")
                    rimuovi_button = gr.Button("Rimuovi")
                
                # Bind enter with the button
                nuovo_ingrediente.submit(
                    fn=aggiungi_personalizzato,
                    inputs=[nuovo_ingrediente],
                    outputs=[ingredienti_pillole]
                ).then(
                    fn=svuota_casella,  # Pulisce la casella di testo
                    inputs=[],
                    outputs=[nuovo_ingrediente]
                )
                
                aggiungi_button.click(
                    fn=aggiungi_personalizzato,
                    inputs=[nuovo_ingrediente],
                    outputs=[ingredienti_pillole]
                ).then(
                    fn=svuota_casella,  # Pulisce la casella di testo
                    inputs=[],
                    outputs=[nuovo_ingrediente]
                )

                # Bind "Rimuovi" button
                rimuovi_button.click(
                    fn=rimuovi_personalizzato,
                    inputs=[ingredienti_pillole],  # Prende gli ingredienti selezionati dalle checkbox
                    outputs=[ingredienti_pillole, ingredienti_selezionati_box]  # Aggiorna le checkbox e il riquadro degli ingredienti selezionati
                ).then(
                    fn=svuota_casella,  # Pulisce la casella di testo
                    inputs=[],
                    outputs=[nuovo_ingrediente]
                )
                                


    return demo

if __name__ == "__main__":
    demo = gradio_interface()
    demo.launch()

"""
