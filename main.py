import tkinter as tk
from tkinter import scrolledtext
import google.generativeai as genai
from tkinter import ttk

# Configure the API key for Google Generative AI
genai.configure(api_key="YOUR_API_KEY")
model = genai.GenerativeModel("gemini-1.5-flash")

# Function to get a response from the model
def get_response():
    user_input = user_entry.get()
    if user_input.lower() in ["exit", "quit"]:
        root.quit()
    elif user_input:
        # Display user's question in the chat history
        insert_chat_text(f"You: {user_input}\n", "user")
        user_entry.delete(0, tk.END)  # Clear the input box

        # Get response from the model
        try:
            response = model.generate_content(user_input)
            insert_chat_text(f"Bot: {response.text}\n\n", "bot")
        except Exception as e:
            insert_chat_text(f"Error: {e}\n\n", "error")

# Function to insert text into the chat history with custom tags
def insert_chat_text(text, tag):
    chat_history.config(state=tk.NORMAL)  # Enable text area to insert text
    chat_history.insert(tk.END, text, tag)  # Insert text with tag
    chat_history.config(state=tk.DISABLED)  # Disable text area to prevent user editing
    chat_history.yview(tk.END)  # Scroll to the end

# Setting up the GUI window
root = tk.Tk()
root.title("Chatbot")
root.geometry("500x600")
root.config(bg="#2e3440")

# Style configuration for ttk elements
style = ttk.Style()
style.configure("TFrame", background="#3b4252")
style.configure("TLabel", background="#2e3440", foreground="#eceff4", font=("Arial", 12, "bold"))
style.configure("TEntry", font=("Arial", 12))
style.configure("TButton", font=("Arial", 12, "bold"), background="#5e81ac", foreground="#eceff4")
style.map("TButton", background=[("active", "#4c566a")])

# Frame for chat history
chat_frame = ttk.Frame(root, style="TFrame")
chat_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Chat history display area with color-coded tags
chat_history = scrolledtext.ScrolledText(chat_frame, wrap=tk.WORD, width=50, height=20, bg="#eceff4", fg="#2e3440", font=("Arial", 12))
chat_history.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)
chat_history.config(state=tk.DISABLED)  # Make chat history read-only

# Adding tags for color-coded text
chat_history.tag_config("user", foreground="#81A1C1")  # Light blue for user messages
chat_history.tag_config("bot", foreground="#A3BE8C")   # Green for bot messages
chat_history.tag_config("error", foreground="red")     # Red for errors

# Frame for user input
input_frame = ttk.Frame(root, style="TFrame")
input_frame.pack(padx=10, pady=5, fill=tk.X)

user_entry = ttk.Entry(input_frame, width=40, font=("Arial", 12))
user_entry.pack(side=tk.LEFT, padx=5)
user_entry.bind("<Return>", lambda event: get_response())  # Allow pressing Enter to send message

# Send button
send_button = ttk.Button(input_frame, text="Send", command=get_response)
send_button.pack(side=tk.LEFT, padx=5)

# Run the main GUI loop
root.mainloop()