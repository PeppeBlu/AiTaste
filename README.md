
---
# 🍽️ AiTaste – AI Assistant for Gourmet Flavor Pairing

**AiTaste** is a web app powered by AI that helps you create innovative and scientifically grounded ingredient combinations. With a clean and interactive interface, you can select ingredients, add custom ones, and get suggestions from an **AI chef specialized in food chemistry and molecular gastronomy**.

---

## 🚀 Features

- ✅ Interactive web interface built with **Gradio**
- ✅ Choose from common or custom ingredients
- ✅ AI suggestions based on molecular affinity and taste synergy
- ✅ Cooking technique recommendations and creative dish naming
- ✅ Chat interface with conversation history

---

## 🧠 Under the Hood

- **AI Model**: `deepseek-r1-distill-llama-70b` via [Groq API](https://groq.com/)
- **Interface**: Built with [Gradio](https://www.gradio.app/)
- **Environment Variables**: Handled using `python-dotenv`

---

## 🔧 Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/PeppeBlu/aitaste.git
   cd aitaste


2.	**Create a virtual environment (optional but recommended):**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate


3.	**Install dependencies:**

    ```bash
    pip install -r requirements.txt


4.	Create a .env file named config.env and add your Groq API key:

    GROQ_API_KEY=your_api_key_here


⸻

**▶️ Run the App**

Start the app with:

    python source/aitaste.py

The app will launch locally, and a shareable public link will be available via Gradio.

⸻

**💡 How It Works**
1.	Select or add ingredients using the right-hand panel.
2.	Click Set Ingredients to send them to the AI.
3.	The AI replies with:
    - Key affinities between ingredients
    - Suggested cooking technique
    - A creative dish composition based on food chemistry
**-** You can also interact directly from chatbox on the left

⸻

📷 UI Preview (Optional)

Add a screenshot here to show off the interface.


⸻

🛠️ To Do
	•	Add multi-language support
	•	Improve ingredient compatibility logic
	•	Save ingredient profiles across sessions

⸻

🧑‍🍳 Created With Passion

Built by a food lover combining tech and taste. Feedback and contributions are welcome!

---
