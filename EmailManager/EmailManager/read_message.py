import tkinter as tk
import tkinter.scrolledtext as tkst

import message_manager as messages  # Import module to handle message operations (retrieve, update, delete, etc.)
import font_manager as fonts          # Import module to configure fonts for the GUI


class ReadMessage():
    def __init__(self, window, message_id):
        """
        Initialize the ReadMessage GUI.

        Parameters:
        - window: The parent Tkinter window or Toplevel widget where this GUI is displayed.
        - message_id: The ID of the message to be displayed. If None, no message details are loaded.
        """
        self.message_id = message_id

        # Set the parent window reference and configure its basic properties.
        self.window = window
        self.window.geometry("500x320")  # Set the window size to 500x320 pixels
        self.window.title(f"Read Message {message_id}")  # Set the window title including the message ID

        # Create and place a label for the sender's email.
        sender_lbl = tk.Label(window, text="From:")
        sender_lbl.grid(row=0, column=0, sticky="E", padx=10, pady=10)

        # Create an entry widget to display the sender. It will be set to read-only after populating.
        self.sender_txt = tk.Entry(window, width=40)
        self.sender_txt.grid(row=0, column=1, columnspan=5, sticky="W", padx=10, pady=10)

        # Create and place a label for the recipient's email.
        recipient_lbl = tk.Label(window, text="To:")
        recipient_lbl.grid(row=1, column=0, sticky="E", padx=10, pady=10)

        # Create an entry widget to display the recipient.
        self.recipient_txt = tk.Entry(window, width=40)
        self.recipient_txt.grid(row=1, column=1, columnspan=5, sticky="W", padx=10, pady=10)

        # Create and place a label for the subject.
        subject_lbl = tk.Label(window, text="Subject:")
        subject_lbl.grid(row=2, column=0, sticky="E", padx=10, pady=10)

        # Create an entry widget to display the subject of the message.
        self.subject_txt = tk.Entry(window, width=40)
        self.subject_txt.grid(row=2, column=1, columnspan=5, sticky="W", padx=10, pady=10)

        # Create a ScrolledText widget to display the message content.
        self.content_txt = tkst.ScrolledText(window, width=48, height=6, wrap="word")
        self.content_txt.grid(row=3, column=0, columnspan=6, sticky="W", padx=10, pady=10)

        # Create a label for entering a new priority value (between 1 and 5).
        # Note: We reuse the variable name subject_lbl here for the new label.
        subject_lbl = tk.Label(window, text="New priority (1-5):")
        subject_lbl.grid(row=4, column=0, columnspan=2, sticky="E", padx=10, pady=10)

        # Create an entry widget for the user to input the new priority value.
        self.priority_txt = tk.Entry(window, width=3)
        self.priority_txt.grid(row=4, column=2, sticky="W", padx=10, pady=10)

        # Create a button to update the message priority.
        # When clicked, it will call the update_priority() method.
        update_btn = tk.Button(window, text="Update", command=self.update_priority)
        update_btn.grid(row=4, column=3, sticky="W", padx=10, pady=10)

        # Create a button to delete the message.
        # When clicked, it will call the delete_message() method.
        delete_btn = tk.Button(window, text="Delete", command=self.delete_message)
        delete_btn.grid(row=4, column=4, padx=10, pady=10)

        # Create a button to close the window.
        # When clicked, it will call the close() method.
        close_btn = tk.Button(window, text="Close", command=self.close)
        close_btn.grid(row=4, column=5, padx=10, pady=10)

        # If a valid message_id is provided, attempt to load and display the message details.
        if message_id is not None:
            sender = messages.get_sender(message_id)
            if sender is not None:
                # Insert the sender's email into the sender entry and set it to read-only.
                self.sender_txt.insert(tk.END, sender)
                self.sender_txt.configure(state='readonly')
                # Insert the recipient's email into the recipient entry and set it to read-only.
                self.recipient_txt.insert(tk.END, messages.get_recipient(message_id))
                self.recipient_txt.configure(state='readonly')
                # Insert the subject into the subject entry and set it to read-only.
                self.subject_txt.insert(tk.END, messages.get_subject(message_id))
                self.subject_txt.configure(state='readonly')
                # Insert the message content into the scrolled text widget.
                self.content_txt.insert(tk.END, messages.get_content(message_id))
            else:
                # If no message exists with the provided ID, display an error message in the content area.
                self.content_txt.insert(tk.END, 'No such message')
        # Disable editing of the content text area so that users cannot change the message content.
        self.content_txt["state"] = "disabled"

    def delete_message(self):
        """
        Delete the message with the current message_id and close the window.
        """
        if self.message_id is not None:
            messages.delete_message(self.message_id)
        self.close()

    def update_priority(self):
        """
        Update the message's priority.
        Reads the new priority value from the priority_txt entry, converts it to an integer,
        and then updates the message using the message manager.
        """
        if self.message_id is not None:
            messages.set_priority(self.message_id, int(self.priority_txt.get()))

    def close(self):
        """
        Close the current GUI window.
        """
        self.window.destroy()


if __name__ == "__main__":
    # This block runs only if this file is executed as a standalone script.
    # Create a new Tkinter main window.
    window = tk.Tk()  # create a TK object
    fonts.configure()  # configure the fonts for the GUI using the font manager
    ReadMessage(window, None)  # open the ReadMessage GUI (with no specific message loaded)
    window.mainloop()  # run the window main loop, reacting to button presses, etc.
