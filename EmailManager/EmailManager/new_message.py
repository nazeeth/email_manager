# new_message.py
import tkinter as tk
from tkinter import messagebox
import message_manager as messages
import font_manager as fonts

class NewMessageGUI:
    def __init__(self, master):
        self.master = master
        master.title("New Message")
        master.geometry("500x400")
        fonts.configure()

        # Sender field
        tk.Label(master, text="Sender:").grid(row=0, column=0, padx=10, pady=5, sticky="E")
        self.sender_entry = tk.Entry(master, width=40)
        self.sender_entry.grid(row=0, column=1, padx=10, pady=5)

        # Recipient field
        tk.Label(master, text="Recipient:").grid(row=1, column=0, padx=10, pady=5, sticky="E")
        self.recipient_entry = tk.Entry(master, width=40)
        self.recipient_entry.grid(row=1, column=1, padx=10, pady=5)

        # Subject field
        tk.Label(master, text="Subject:").grid(row=2, column=0, padx=10, pady=5, sticky="E")
        self.subject_entry = tk.Entry(master, width=40)
        self.subject_entry.grid(row=2, column=1, padx=10, pady=5)

        # Message content field (using a Text widget)
        tk.Label(master, text="Content:").grid(row=3, column=0, padx=10, pady=5, sticky="NE")
        self.content_text = tk.Text(master, width=40, height=10)
        self.content_text.grid(row=3, column=1, padx=10, pady=5)

        # Send and Cancel buttons
        send_btn = tk.Button(master, text="Send", command=self.send_message)
        send_btn.grid(row=4, column=0, padx=10, pady=10)
        cancel_btn = tk.Button(master, text="Cancel", command=master.destroy)
        cancel_btn.grid(row=4, column=1, padx=10, pady=10, sticky="E")

    def send_message(self):
        # Retrieve the user inputs from each field
        sender = self.sender_entry.get().strip()
        recipient = self.recipient_entry.get().strip()
        subject = self.subject_entry.get().strip()
        content = self.content_text.get("1.0", tk.END).strip()

        # Check that all fields have been filled in
        if not sender or not recipient or not subject or not content:
            messagebox.showerror("Input Error", "All fields must be filled in.")
            return

        # Add the new message using the message manager
        messages.new_message(sender, recipient, subject, content)
        messagebox.showinfo("Success", "Message sent successfully!")
        self.master.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    NewMessageGUI(root)
    root.mainloop()
