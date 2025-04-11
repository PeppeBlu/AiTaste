import gradio as gr

# Funzione per mostrare il messaggio
def mostra_messaggio():
    return gr.update(visible=True), gr.update(visible=False)

# Funzione per nascondere il messaggio
def nascondi_messaggio():
    return gr.update(visible=False), gr.update(visible=True)

# Interfaccia Gradio
with gr.Blocks() as app:
    # Riquadro nascosto inizialmente
    messaggio = gr.Row(visible=False)
    with messaggio:
        gr.Markdown("### Questo è un messaggio visibile solo quando richiesto!")
        gr.Textbox(label="Inserisci qualcosa qui")

    # Riquadro alternativo nascosto inizialmente
    altro_messaggio = gr.Row(visible=True)
    with altro_messaggio:
        gr.Markdown("### Questo è un altro messaggio visibile quando il primo è nascosto!")
        gr.Textbox(label="Inserisci qualcosa qui")

    # Pulsanti per mostrare e nascondere il messaggio
    mostra_button = gr.Button("Mostra Messaggio")
    nascondi_button = gr.Button("Nascondi Messaggio")

    # Collegamento dei pulsanti alle funzioni
    mostra_button.click(fn=mostra_messaggio, inputs=[], outputs=[messaggio, altro_messaggio])
    nascondi_button.click(fn=nascondi_messaggio, inputs=[], outputs=[messaggio, altro_messaggio])

# Avvia l'app
app.launch()