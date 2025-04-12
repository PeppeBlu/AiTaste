
from groq import Groq
import os
from dotenv import load_dotenv
import gradio as gr


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

load_dotenv(dotenv_path="config.env")

prompt_setting = os.getenv("PROMPT_SETTING")

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# controlla variabili d'ambiente e chiave API
def health_check():
    if prompt_setting is None:
        raise ValueError("La variabile d'ambiente 'PROMPT_SETTING' non è stata trovata nel file config.env.")
    if client is None:
        raise ValueError("La variabile d'ambiente 'GROQ_API_KEY' non è stata trovata nel file config.env.")

    # Verifica se la chiave API è valida
    try:
        client.models.list()
    except Exception as e:
        raise ValueError("La chiave API non è valida o non è stata trovata nel file config.env.") from e
    
    return True

# invia input al modello e riceve la risposta
def chat(prompt_setting, history):
    """
    Function to send a chat message to the AI model and receive a response.
    """
    messages = [{"role": "system", "content": prompt_setting}] + history

    try:
        response = client.chat.completions.create(
            model="deepseek-r1-distill-llama-70b",
            messages = messages, 
            temperature=1,
            max_tokens=2048,
            top_p=1,
            stream=False,
            stop=None,
        )

        content = response.choices[0].message.content.strip()
    
        if "<think>" in content:
            start_index = content.index("<think>")
            end_index = content.index("</think>") + len("</think>")
            contentR = content[:start_index] + content[end_index:]
        
        return contentR.strip()

    except Exception as e:
        print("Error:", str(e))

# seleziona o deseleziona un ingrediente
def toggle_ingrediente(ingredienti):
    global ingredienti_selezionati

    if isinstance(ingredienti, list):
        ingredienti_selezionati = ingredienti

    return ", ".join(ingredienti_selezionati)

# aggiunge un ingrediente personalizzato
def aggiungi_personalizzato(ingrediente):
    global ingredienti_comuni
    #capitalize the first letter
    ingrediente = ingrediente.capitalize()
    
    if ingrediente and ingrediente not in ingredienti_comuni:
        ingredienti_comuni.append(ingrediente)
    return gr.update(choices=ingredienti_comuni)

# rimuove un ingrediente personalizzato
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

# svuota la casella di testo
def svuota_casella():
    return ""

# mostra l'input dell'utente nella chat
def show_user_input(history, input_text):
    history.append({"role": "user", "content": input_text})
    return history, history

# mostra l'input degli ingredienti nella chat
def show_ingredient_input(history):
    input_text = ", ".join(ingredienti_selezionati)
    history.append({"role": "user", "content": input_text})

    return history

# invia il messaggio al modello e riceve la risposta
def send_message(message, history):
    response = chat(prompt_setting, history)
    history.append({"role": "assistant", "content": response})
    return history, history

# invia gli ingredienti selezionati al chatbot
def invia_ingredienti(history):
    # Combina gli ingredienti selezionati in una stringa
    
    input_text = ", ".join(ingredienti_selezionati)
    # Ottieni la risposta dal chatbot
    response = chat(prompt_setting, history)
    
    # Aggiorna la cronologia con il messaggio dell'utente e la risposta del chatbot
    history.append({"role": "assistant", "content": response})
    
    # Restituisci il contenuto aggiornato del chatbot e la cronologia
    return history, history

# switch tra due interfacce
def from_to_interface():
    return gr.update(visible=False), gr.update(visible=True)

# autenticazione
def user_login(username, password):
    if True:
        # Nascondi il login e mostra la chat
        return gr.update(visible=True), gr.update(visible=False), ""
    else:
        # Mostra un messaggio di errore
        return gr.update(visible=False), gr.update(visible=True), "Credenziali errate"

# mostra la pagina di registrazione dopo la registrazione
def user_login_after_sign_up(username, password):
    if True:
        # Nascondi il login e mostra la chat
        return gr.update(visible=True), gr.update(visible=False), "", username


# interfaccia del chatbot
def chatbot_interface():
    # Inizializza la lista di ingredienti comuni per ogni sessione
    global ingredienti_comuni
    with gr.Blocks(title="AiTaste", fill_width=True) as app:
        gr.Markdown("<h1 style='text-align: center;'>👩‍🍳 AiTaste - Find the best combos 👨‍🍳</h1>", elem_id="title")
        
        chat = gr.Row(visible=False)
        signup = gr.Column(visible=False, elem_id="signup_column")
        login = gr.Column(visible=True, elem_id="login_column")

        with chat:
            # Colonna sinistra: Chatbot
            with gr.Column(scale=3):
                chatbot_interface = gr.Chatbot(label="Chatbot", height=750, type="messages")
                history = gr.State([])
                input_textbox = gr.Textbox(
                    label="Scrivi qui il tuo messaggio",
                    placeholder="Scrivi qui il tuo messaggio...",
                    show_label=False,
                    lines=1,
                    max_lines=1
                )
                input_textbox.submit(
                    fn=show_user_input,
                    inputs=[history, input_textbox],
                    outputs=[history, chatbot_interface]
                ).then(
                    send_message,
                    inputs=[input_textbox, history],
                    outputs=[chatbot_interface, history]
                ).then(
                    fn=svuota_casella,
                    inputs=[],
                    outputs=[input_textbox]
                )
                
                submit_button = gr.Button("Invia Messaggio")
                submit_button.click(
                    fn=show_user_input,
                    inputs=[history, input_textbox],
                    outputs=[history, chatbot_interface]
                ).then(
                    send_message,
                    inputs=[input_textbox, history],
                    outputs=[chatbot_interface, history]
                ).then(
                    fn=svuota_casella,
                    inputs=[],
                    outputs=[input_textbox]
                )
                         
            # Colonna destra: Ingredienti
            with gr.Column(scale=2):
                gr.Markdown("### Ingredienti selezionati")
                ingredienti_selezionati_box = gr.Textbox(
                    label="",
                    interactive=False
                )
                
                set_ingredienti_button = gr.Button("Invia Ingredienti")
                #se clicco Set Ingredienti, viene inviasto il messaggio al chatbot e pulito il textbox
                set_ingredienti_button.click(
                    fn=show_ingredient_input,
                    inputs=[history],
                    outputs=[chatbot_interface]
                ).then(
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
                # Aggiungi un evento per aggiornare gli ingredienti selezionati
                ingredienti_pillole.change(
                    fn=toggle_ingrediente,
                    inputs=[ingredienti_pillole],
                    outputs=[ingredienti_selezionati_box]
                )
                
                gr.Markdown("### Aggiungi un ingrediente personalizzato")
                nuovo_ingrediente = gr.Textbox(
                    placeholder="Inserisci un nuovo ingrediente...",
                    label=""
                )
                nuovo_ingrediente.submit(
                    fn=aggiungi_personalizzato,
                    inputs=[nuovo_ingrediente],
                    outputs=[ingredienti_pillole]
                ).then(
                    fn=svuota_casella,
                    inputs=[],
                    outputs=[nuovo_ingrediente]
                )
               
                with gr.Row():
                    aggiungi_button = gr.Button("Aggiungi ingrediente")

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

                with gr.Row():
                    logout_button = gr.Button("LogOut", elem_id="logout_button")
                    logout_button.click(
                        fn=from_to_interface,
                        inputs=[],
                        outputs=[chat, login]
                    )
   
        
        with login:
            gr.Markdown("### Accedi al tuo account")
            with login:
                login_username = gr.Textbox(label="Nome utente", 
                                            placeholder="Inserisci il tuo nome utente")
                password = gr.Textbox(label="Password", 
                                      type="password", 
                                      placeholder="Inserisci la tua password")
            
            login_button = gr.Button("Accedi")
            sign_in_button = gr.Button("Registrati")
            error_box = gr.Textbox(visible=False, interactive=False, show_label=False)

            login_button.click(
                fn=user_login,
                inputs=[login_username, password],
                outputs=[chat, login, error_box]
            )

            sign_in_button.click(
                fn=from_to_interface,
                inputs=[],
                outputs=[login, signup]
            )


        with signup:
            gr.Markdown("### Registrati per un nuovo account")
            with signup:
                username_signup = gr.Textbox(label="Nome utente", placeholder="Inserisci il tuo nome utente")
                password_signup = gr.Textbox(label="Password", type="password", placeholder="Inserisci la tua password")
                
            
            register_button = gr.Button("Registrati")
            error_box = gr.Textbox(visible=False, interactive=False, show_label=False)
            register_button.click(
                fn=user_login_after_sign_up,
                inputs=[username_signup, password_signup, ],
                outputs=[login, signup, error_box, login_username]
            )


    return app


if __name__ == "__main__":
    if health_check():
        demo = chatbot_interface()
        demo.launch()
    else:
        print("Errore durante il controllo della salute dell'app.")
        exit(1)
