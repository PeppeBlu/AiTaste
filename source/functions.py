

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
def send_message(history):
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
    else:
        # Mostra un messaggio di errore
        return gr.update(visible=False), gr.update(visible=True), "Errore durante la registrazione", ""