
from groq import Groq
import os
from dotenv import load_dotenv
import gradio as gr
from functions import (
    health_check,
    toggle_ingrediente,
    aggiungi_personalizzato,
    rimuovi_personalizzato,
    svuota_casella,
    show_user_input,
    show_ingredient_input,
    send_message,
    invia_ingredienti,
    from_to_interface,
    user_login,
    user_login_after_sign_up
)

from utils import (
    ingredienti_comuni,
    client,
    prompt_setting
)  

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
                    fn=svuota_casella,
                    inputs=[],
                    outputs=[input_textbox]
                ).then(
                    send_message,
                    inputs=[history],
                    outputs=[chatbot_interface, history]
                )
                
                submit_button = gr.Button("Invia Messaggio")
                submit_button.click(
                    fn=show_user_input,
                    inputs=[history, input_textbox],
                    outputs=[history, chatbot_interface]
                ).then(
                    fn=svuota_casella,
                    inputs=[],
                    outputs=[input_textbox]
                ).then(
                    send_message,
                    inputs=[history],
                    outputs=[chatbot_interface, history]
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
    if health_check(prompt_setting, client):
        demo = chatbot_interface()
        demo.launch()
    else:
        print("Errore durante il controllo della salute dell'app.")
        exit(1)
