import os
import speech_recognition as sr
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

class FileManagerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("File Manager App")
        
        self.create_widgets()
        
    def create_widgets(self):
        # Create command label and entry
        self.command_label = tk.Label(self.master, text="Enter Command:")
        self.command_label.grid(row=0, column=0, padx=5, pady=5)

        self.command_entry = tk.Entry(self.master, width=50)
        self.command_entry.grid(row=0, column=1, padx=5, pady=5)

        # Create buttons for actions
        self.open_button = tk.Button(self.master, text="Open File", command=self.open_file)
        self.open_button.grid(row=1, column=0, padx=5, pady=5)

        self.create_button = tk.Button(self.master, text="Create File", command=self.create_file)
        self.create_button.grid(row=1, column=1, padx=5, pady=5)

        self.delete_button = tk.Button(self.master, text="Delete File", command=self.delete_file)
        self.delete_button.grid(row=1, column=2, padx=5, pady=5)

        self.rename_button = tk.Button(self.master, text="Rename File", command=self.rename_file)
        self.rename_button.grid(row=1, column=3, padx=5, pady=5)

        # Create status label
        self.status_label = tk.Label(self.master, text="")
        self.status_label.grid(row=2, column=0, columnspan=4, padx=5, pady=5)

    def recognize_speech(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            self.status_label.config(text="Speak...")
            self.master.update()
            audio = r.listen(source)

        try:
            command = r.recognize_google(audio)
            self.status_label.config(text="You said: " + command)
            self.master.update()
            return command
        except sr.UnknownValueError:
            self.status_label.config(text="Google Speech Recognition could not understand audio")
            self.master.update()
        except sr.RequestError as e:
            self.status_label.config(text="Could not request results from Google Speech Recognition service; {0}".format(e))
            self.master.update()        

    def open_file(self):
        filename = filedialog.askopenfilename(title="Select File", filetypes=(("All files", "*.*"),))
        if filename:
            try:
                os.startfile(filename)
                self.status_label.config(text="File opened successfully")
                self.master.update()
            except FileNotFoundError:
                self.status_label.config(text="File not found")
                self.master.update()
                
    def create_file(self):
        filename = filedialog.asksaveasfilename(title="Create File", defaultextension=".txt")
        if filename:
            try:
                with open(filename, 'w'):
                    self.status_label.config(text="File created successfully")
                    self.master.update()
                    file_ext = os.path.splitext(filename)[1].lower()
                    self.move_file_to_folder(filename, file_ext)
            except FileExistsError:
                self.status_label.config(text="File already exists")
                self.master.update()
                
    def delete_file(self):
        filename = filedialog.askopenfilename(title="Select File to Delete", filetypes=(("All files", "*.*"),))
        if filename:
            confirm = messagebox.askyesno(title="Confirm Deletion", message=f"Are you sure you want to delete {os.path.basename(filename)}?")
            if confirm:
                try:
                    os.remove(filename)
                    self.status_label.config(text="File deleted successfully")
                    self.master.update()
                except FileNotFoundError:
                    self.status_label.config(text="File not found")
                    self.master.update()
    def rename_file(self):
        filename = filedialog.askopenfilename(title="Select File to Rename", filetypes=(("All files", "*.*"),))
        if filename:
            new_filename = filedialog.asksaveasfilename(title="Rename File", defaultextension=os.path.splitext(filename)[1])
            if new_filename:
                try:
                    os.rename(filename, new_filename)
                    self.status_label.config(text="File renamed successfully")
                    self.master.update()
                except FileExistsError:
                    self.status_label.config(text="File already exists with that name")
                    self.master.update()

    def move_file_to_folder(self, filename, file_ext):
        folder_path = os.path.join(os.getcwd(), file_ext[1:].upper() + "_Files")
        if not os.path.exists(folder_path):
            os.mkdir(folder_path)
        new_file_path = os.path.join(folder_path, os.path.basename(filename))
        os.replace(filename, new_file_path)
    
    def move_file_to_location(self):
        filename = filedialog.askopenfilename(title="Select File to Move", filetypes=(("All files", "*.*"),))
        if filename:
            new_location = filedialog.askdirectory(title="Select Destination Folder")
            if new_location:
                try:
                    _, file_ext = os.path.splitext(filename)
                    new_file_path = os.path.join(new_location, os.path.basename(filename)) 
                    os.replace(filename, new_file_path)
                    self.status_label.config(text="File moved successfully")
                    self.master.update()
                except FileNotFoundError:
                    self.status_label.config(text="File not found")
                    self.master.update()

    def execute_command(self):
        command = self.command_entry.get().lower()
        if command == "open":
            self.open_file()
        elif command == "create":
            self.create_file()
        elif command == "delete":
            self.delete_file()
        elif command == "rename":
            self.rename_file()
        elif command == "move":
            self.move_file_to_location()
        elif command == "speech":
            recognized_command = self.recognize_speech()
            if recognized_command:
                self.command_entry.delete(0, tk.END)
                self.command_entry.insert(0, recognized_command)
                self.execute_command()
        else:
            self.status_label.config(text="Invalid command entered")
            self.master.update()

    def on_key_press(self, event):
        if event.keysym == "Return":
            self.execute_command()

def main():
    root = tk.Tk()
    app = FileManagerApp(root)
    root.bind('<Key>', app.on_key_press)
    root.mainloop()
    
if __name__ == '__main__':
    main()    