import tkinter as tk
from tkinter import ttk, messagebox
import tkinter.scrolledtext as tkst

import message_manager as messages
import font_manager as fonts


def set_text(text_area, content):
    text_area.config(state="normal")
    text_area.delete("1.0", tk.END)
    text_area.insert("1.0", content)
    text_area.config(state="disabled")


class EmailManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Unified Email Manager")
        self.root.geometry("800x600")
        fonts.configure()

        # Create a Notebook widget for the tabbed interface
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True)

        # Create tabs for Inbox, Compose, Read/Update, and Label Messages
        self.tab_inbox = ttk.Frame(self.notebook)
        self.tab_compose = ttk.Frame(self.notebook)
        self.tab_read = ttk.Frame(self.notebook)
        self.tab_label = ttk.Frame(self.notebook)

        self.notebook.add(self.tab_inbox, text="Inbox")
        self.notebook.add(self.tab_compose, text="Compose")
        self.notebook.add(self.tab_read, text="Read/Update")
        self.notebook.add(self.tab_label, text="Label Messages")

        # Setup each tab's widgets
        self.setup_inbox_tab()
        self.setup_compose_tab()
        self.setup_read_tab()
        self.setup_label_tab()

    def setup_inbox_tab(self):
        # Create a frame for search and refresh controls
        top_frame = tk.Frame(self.tab_inbox, bg="#d9e1f2")
        top_frame.pack(pady=5, padx=10, anchor="w", fill="x")

        # Search label and entry
        tk.Label(top_frame, text="Search:", bg="#d9e1f2").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.search_entry = tk.Entry(top_frame, width=30)
        self.search_entry.grid(row=0, column=1, padx=5, pady=5)

        # Search button
        tk.Button(
            top_frame,
            text="Search",
            command=self.search_messages,
            bg="#4a90e2",
            fg="white",
            activebackground="#357ABD"
        ).grid(row=0, column=2, padx=5, pady=5)

        # Refresh button
        tk.Button(
            top_frame,
            text="Refresh",
            command=self.list_messages,
            bg="#4a90e2",
            fg="white",
            activebackground="#357ABD"
        ).grid(row=0, column=3, padx=5, pady=5)

        # Scrolled text widget to display messages
        self.inbox_text = tkst.ScrolledText(self.tab_inbox, width=80, height=25, wrap="none")
        self.inbox_text.pack(padx=10, pady=10, fill="both", expand=True)

        # Initially list messages
        self.list_messages()

    def search_messages(self):
        search_str = self.search_entry.get().strip().lower()
        results = "ID Priority From                      Label Subject\n"
        results += "== ======== ====                      ===== =======\n"
        for msg_id, msg in messages.messages.items():
            if (search_str in msg.subject.lower() or
                search_str in msg.content.lower() or
                search_str in msg.sender.lower()):
                results += f"{msg_id:2d} {msg.info()}\n"
        set_text(self.inbox_text, results)

    def list_messages(self):
        message_list = messages.list_all()
        set_text(self.inbox_text, message_list)

    def setup_compose_tab(self):
        frame = self.tab_compose
        tk.Label(frame, text="Sender:").grid(row=0, column=0, padx=10, pady=5, sticky="E")
        self.sender_entry = tk.Entry(frame, width=40)
        self.sender_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(frame, text="Recipient:").grid(row=1, column=0, padx=10, pady=5, sticky="E")
        self.recipient_entry = tk.Entry(frame, width=40)
        self.recipient_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(frame, text="Subject:").grid(row=2, column=0, padx=10, pady=5, sticky="E")
        self.subject_entry = tk.Entry(frame, width=40)
        self.subject_entry.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(frame, text="Content:").grid(row=3, column=0, padx=10, pady=5, sticky="NE")
        self.content_text = tk.Text(frame, width=40, height=10)
        self.content_text.grid(row=3, column=1, padx=10, pady=5)

        send_btn = tk.Button(frame, text="Send", command=self.send_message,
                             bg="#4a90e2", fg="white", activebackground="#357ABD")
        send_btn.grid(row=4, column=0, padx=10, pady=10)
        cancel_btn = tk.Button(frame, text="Cancel", command=self.clear_compose,
                               bg="#4a90e2", fg="white", activebackground="#357ABD")
        cancel_btn.grid(row=4, column=1, padx=10, pady=10, sticky="E")

    def send_message(self):
        sender = self.sender_entry.get().strip()
        recipient = self.recipient_entry.get().strip()
        subject = self.subject_entry.get().strip()
        content = self.content_text.get("1.0", tk.END).strip()
        if not sender or not recipient or not subject or not content:
            messagebox.showerror("Error", "All fields must be filled in.")
            return
        messages.new_message(sender, recipient, subject, content)
        messagebox.showinfo("Success", "Message sent!")
        self.clear_compose()
        self.list_messages()

    def clear_compose(self):
        self.sender_entry.delete(0, tk.END)
        self.recipient_entry.delete(0, tk.END)
        self.subject_entry.delete(0, tk.END)
        self.content_text.delete("1.0", tk.END)

    def setup_read_tab(self):
        frame = self.tab_read
        tk.Label(frame, text="Message ID:").grid(row=0, column=0, padx=10, pady=5, sticky="E")
        self.msg_id_entry = tk.Entry(frame, width=5)
        self.msg_id_entry.grid(row=0, column=1, padx=10, pady=5, sticky="W")
        load_btn = tk.Button(frame, text="Load Message", command=self.load_message,
                             bg="#4a90e2", fg="white", activebackground="#357ABD")
        load_btn.grid(row=0, column=2, padx=10, pady=5)

        tk.Label(frame, text="From:").grid(row=1, column=0, padx=10, pady=5, sticky="E")
        self.read_sender = tk.Entry(frame, width=40)
        self.read_sender.grid(row=1, column=1, columnspan=2, padx=10, pady=5)
        self.read_sender.config(state="readonly")

        tk.Label(frame, text="To:").grid(row=2, column=0, padx=10, pady=5, sticky="E")
        self.read_recipient = tk.Entry(frame, width=40)
        self.read_recipient.grid(row=2, column=1, columnspan=2, padx=10, pady=5)
        self.read_recipient.config(state="readonly")

        tk.Label(frame, text="Subject:").grid(row=3, column=0, padx=10, pady=5, sticky="E")
        self.read_subject = tk.Entry(frame, width=40)
        self.read_subject.grid(row=3, column=1, columnspan=2, padx=10, pady=5)
        self.read_subject.config(state="readonly")

        tk.Label(frame, text="Content:").grid(row=4, column=0, padx=10, pady=5, sticky="NE")
        self.read_content = tk.Text(frame, width=40, height=10)
        self.read_content.grid(row=4, column=1, columnspan=2, padx=10, pady=5)
        self.read_content.config(state="disabled")

        tk.Label(frame, text="New Priority (1-5):").grid(row=5, column=0, padx=10, pady=5, sticky="E")
        self.new_priority_entry = tk.Entry(frame, width=3)
        self.new_priority_entry.grid(row=5, column=1, padx=10, pady=5, sticky="W")

        update_btn = tk.Button(frame, text="Update", command=self.update_priority,
                               bg="#4a90e2", fg="white", activebackground="#357ABD")
        update_btn.grid(row=5, column=2, padx=10, pady=5)
        delete_btn = tk.Button(frame, text="Delete", command=self.delete_message,
                               bg="#4a90e2", fg="white", activebackground="#357ABD")
        delete_btn.grid(row=6, column=1, padx=10, pady=5)
        clear_btn = tk.Button(frame, text="Clear", command=self.clear_read_tab,
                              bg="#4a90e2", fg="white", activebackground="#357ABD")
        clear_btn.grid(row=6, column=2, padx=10, pady=5)

    def load_message(self):
        msg_id_str = self.msg_id_entry.get().strip()
        if not msg_id_str:
            messagebox.showerror("Error", "Please enter a message ID.")
            return
        try:
            msg_id = int(msg_id_str)
        except ValueError:
            messagebox.showerror("Error", "Message ID must be a number.")
            return
        if msg_id not in messages.messages:
            messagebox.showerror("Error", "Message not found.")
            return
        msg = messages.messages[msg_id]
        self.read_sender.config(state="normal")
        self.read_recipient.config(state="normal")
        self.read_subject.config(state="normal")
        self.read_content.config(state="normal")
        self.read_sender.delete(0, tk.END)
        self.read_recipient.delete(0, tk.END)
        self.read_subject.delete(0, tk.END)
        self.read_content.delete("1.0", tk.END)
        self.read_sender.insert(tk.END, msg.sender)
        self.read_recipient.insert(tk.END, msg.recipient)
        self.read_subject.insert(tk.END, msg.subject)
        self.read_content.insert(tk.END, msg.content)
        self.read_sender.config(state="readonly")
        self.read_recipient.config(state="readonly")
        self.read_subject.config(state="readonly")
        self.read_content.config(state="disabled")

    def update_priority(self):
        msg_id_str = self.msg_id_entry.get().strip()
        if not msg_id_str:
            messagebox.showerror("Error", "Please load a message first.")
            return
        try:
            msg_id = int(msg_id_str)
        except ValueError:
            messagebox.showerror("Error", "Message ID must be a number.")
            return
        try:
            new_priority = int(self.new_priority_entry.get().strip())
        except ValueError:
            messagebox.showerror("Error", "Priority must be a number.")
            return
        messages.set_priority(msg_id, new_priority)
        messagebox.showinfo("Success", "Priority updated.")
        self.list_messages()

    def delete_message(self):
        msg_id_str = self.msg_id_entry.get().strip()
        if not msg_id_str:
            messagebox.showerror("Error", "Please load a message first.")
            return
        try:
            msg_id = int(msg_id_str)
        except ValueError:
            messagebox.showerror("Error", "Message ID must be a number.")
            return
        messages.delete_message(msg_id)
        messagebox.showinfo("Success", "Message deleted.")
        self.clear_read_tab()
        self.list_messages()

    def clear_read_tab(self):
        self.msg_id_entry.delete(0, tk.END)
        self.read_sender.config(state="normal")
        self.read_recipient.config(state="normal")
        self.read_subject.config(state="normal")
        self.read_content.config(state="normal")
        self.read_sender.delete(0, tk.END)
        self.read_recipient.delete(0, tk.END)
        self.read_subject.delete(0, tk.END)
        self.read_content.delete("1.0", tk.END)
        self.read_sender.config(state="readonly")
        self.read_recipient.config(state="readonly")
        self.read_subject.config(state="readonly")
        self.read_content.config(state="disabled")
        self.new_priority_entry.delete(0, tk.END)

    # ------------------ Label Messages Tab ------------------
    def setup_label_tab(self):
        frame = self.tab_label
        # Label field for entering a label (e.g., ToDo, Done)
        tk.Label(frame, text="Label:", bg="#d9e1f2").grid(row=0, column=0, padx=10, pady=5, sticky="E")
        self.label_entry_label = tk.Entry(frame, width=20)
        self.label_entry_label.grid(row=0, column=1, padx=10, pady=5)

        # Button to list all messages with the given label
        tk.Button(
            frame,
            text="List All Messages Labelled",
            command=self.list_labelled,
            bg="#4a90e2", fg="white", activebackground="#357ABD"
        ).grid(row=0, column=2, padx=10, pady=5)

        # ScrolledText area to display the filtered messages
        self.result_text = tkst.ScrolledText(frame, width=70, height=10, wrap="none")
        self.result_text.grid(row=1, column=0, columnspan=3, padx=10, pady=5)

        # Field for entering a message ID for which to add the label
        tk.Label(frame, text="Message ID:", bg="#d9e1f2").grid(row=2, column=0, padx=10, pady=5, sticky="E")
        self.msg_id_entry_label = tk.Entry(frame, width=5)
        self.msg_id_entry_label.grid(row=2, column=1, padx=10, pady=5, sticky="W")

        # Button to add the label to the specified message
        tk.Button(
            frame,
            text="Add Label to Message",
            command=self.add_label,
            bg="#4a90e2", fg="white", activebackground="#357ABD"
        ).grid(row=2, column=2, padx=10, pady=5)

    def list_labelled(self):
        label = self.label_entry_label.get().strip()
        message_list = messages.list_all(label)
        self.result_text.config(state="normal")
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert(tk.END, message_list)
        self.result_text.config(state="disabled")

    def add_label(self):
        label = self.label_entry_label.get().strip()
        msg_id_str = self.msg_id_entry_label.get().strip()
        try:
            msg_id = int(msg_id_str)
        except ValueError:
            messagebox.showerror("Error", "Message ID must be a number.")
            return
        if messages.get_sender(msg_id) is None:
            messagebox.showerror("Error", "No message found with that ID.")
            return
        messages.set_label(msg_id, label)
        messagebox.showinfo("Success", f"Label '{label}' added to message {msg_id}.")

if __name__ == "__main__":
    root = tk.Tk()
    fonts.configure()
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TNotebook", background="#d9e1f2", borderwidth=0)
    style.configure("TFrame", background="#d9e1f2")
    style.configure("TButton", background="#4a90e2", foreground="white")
    style.configure("TLabel", background="#d9e1f2", foreground="#333333")

    EmailManagerApp(root)
    root.mainloop()
