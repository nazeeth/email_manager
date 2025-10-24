# label_messages.py
import tkinter as tk
import tkinter.scrolledtext as tkst
from tkinter import messagebox
import message_manager as messages
import font_manager as fonts

class LabelMessagesGUI:
    def __init__(self, master):
        self.master = master
        master.title("Label Messages")
        master.geometry("600x400")
        fonts.configure()

        # Label field for entering a label (e.g., ToDo, Done)
        tk.Label(master, text="Label:").grid(row=0, column=0, padx=10, pady=5, sticky="E")
        self.label_entry = tk.Entry(master, width=20)
        self.label_entry.grid(row=0, column=1, padx=10, pady=5)

        # Button to list all messages with the given label
        list_btn = tk.Button(master, text="List All Messages Labelled", command=self.list_labelled)
        list_btn.grid(row=0, column=2, padx=10, pady=5)

        # ScrolledText area to display the filtered messages
        self.result_text = tkst.ScrolledText(master, width=70, height=10, wrap="none")
        self.result_text.grid(row=1, column=0, columnspan=3, padx=10, pady=5)

        # Field for entering a message ID for which to add the label
        tk.Label(master, text="Message ID:").grid(row=2, column=0, padx=10, pady=5, sticky="E")
        self.msg_id_entry = tk.Entry(master, width=5)
        self.msg_id_entry.grid(row=2, column=1, padx=10, pady=5, sticky="W")

        # Button to add the label to the specified message
        add_label_btn = tk.Button(master, text="Add Label to Message", command=self.add_label)
        add_label_btn.grid(row=2, column=2, padx=10, pady=5)

        # Close button to exit the GUI
        close_btn = tk.Button(master, text="Close", command=master.destroy)
        close_btn.grid(row=3, column=2, padx=10, pady=10, sticky="E")

    def list_labelled(self):
        # Retrieve the label from the entry field
        label = self.label_entry.get().strip()
        # Get the list of messages with that label using list_all() from message_manager
        message_list = messages.list_all(label)
        self.result_text.config(state="normal")
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert(tk.END, message_list)
        self.result_text.config(state="disabled")

    def add_label(self):
        # Get label and message ID from user inputs
        label = self.label_entry.get().strip()
        msg_id_str = self.msg_id_entry.get().strip()

        # Validate that the message ID is a number
        try:
            msg_id = int(msg_id_str)
        except ValueError:
            messagebox.showerror("Error", "Message ID must be a number.")
            return

        # Check if a message with the given ID exists
        if messages.get_sender(msg_id) is None:
            messagebox.showerror("Error", "No message found with that ID.")
            return

        # Set the label for the message and show a success message
        messages.set_label(msg_id, label)
        messagebox.showinfo("Success", f"Label '{label}' added to message {msg_id}.")

if __name__ == "__main__":
    root = tk.Tk()
    LabelMessagesGUI(root)
    root.mainloop()
