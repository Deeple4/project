import tkinter as tk
from tkinter import simpledialog, messagebox, scrolledtext, ttk
from datetime import datetime


BACKGROUND_COLOR = "#2D2D30"
TEXT_COLOR = "#CCCCCC"
BUTTON_COLOR = "#3C3F41"
BUTTON_TEXT_COLOR = "#FFFFFF"
ENTRY_BACKGROUND = "#333337"
ENTRY_FOREGROUND = "#CCCCCC"
HEADING_FONT = ("Verdana", 12, "bold")
BUTTON_FONT = ("Verdana", 10, "bold")
TEXT_FONT = ("Verdana", 10)

class Notebook:
    def init(self):
        self.notes = {}
        self.next_id = 1

    def add_note(self, title, content):
        if title and content:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.notes[self.next_id] = {
                "title": title,
                "content": content,
                "created_at": timestamp,
                "last_modified": timestamp
            }
            self.next_id += 1
            return self.next_id - 1
        else:
            return None

    def edit_note(self, note_id, title, content):
        if note_id in self.notes and title and content:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.notes[note_id]["title"] = title
            self.notes[note_id]["content"] = content
            self.notes[note_id]["last_modified"] = timestamp
            return True
        return False

    def delete_note(self, note_id):
        return self.notes.pop(note_id, None) is not None

    def list_notes(self):
        return self.notes

    def search_notes(self, search_query):
        search_terms = search_query.lower().split()
        return {id_: note for id_, note in self.notes.items() if all(term in note["title"].lower() or term in note["content"].lower() for term in search_terms)}


def open_note_dialog(note_id=None):
    dialog = tk.Toplevel(application_window)
    dialog.title("Add Note" if note_id is None else "Edit Note")
    dialog.geometry("400x300")
    dialog.configure(bg=BACKGROUND_COLOR)

    tk.Label(dialog, text="Title:", bg=BACKGROUND_COLOR, fg=TEXT_COLOR, font=TEXT_FONT).pack(pady=(10, 0))
    title_entry = tk.Entry(dialog, font=TEXT_FONT, bg=ENTRY_BACKGROUND, fg=ENTRY_FOREGROUND)
    title_entry.pack(fill='x', padx=20, pady=5)

    tk.Label(dialog, text="Content:", bg=BACKGROUND_COLOR, fg=TEXT_COLOR, font=TEXT_FONT).pack()
    content_text = tk.Text(dialog, height=10, bg=ENTRY_BACKGROUND, fg=ENTRY_FOREGROUND)
    content_text.pack(fill='both', expand=True, padx=20, pady=5)

    if note_id is not None:
        note = notebook.notes.get(note_id, {})
        title_entry.insert(0, note.get('title', ''))
        content_text.insert('1.0', note.get('content', ''))

    def save_note():
        title = title_entry.get()
        content = content_text.get('1.0', 'end-1c')
        if note_id is None:
            notebook.add_note(title, content)
        else:
            notebook.edit_note(note_id, title, content)
        update_listbox()
        dialog.destroy()

    save_button = tk.Button(dialog, text="Save", command=save_note, bg=BUTTON_COLOR, fg=BUTTON_TEXT_COLOR, font=BUTTON_FONT)
    save_button.pack(pady=10)

def gui_add_note():
    open_note_dialog()

def gui_edit_note():
    try:
        note_id = int(simpledialog.askstring("Input", "Enter note ID to edit:", parent=application_window))
        if note_id in notebook.notes:
            open_note_dialog(note_id)
        else:
            messagebox.showerror("Error", "Invalid note ID.")
    except ValueError:
        messagebox.showerror("Error", "Invalid note ID.")

def gui_delete_note():
    try:
        note_id = int(simpledialog.askstring("Input", "Enter note ID to delete:", parent=application_window))
        if notebook.delete_note(note_id):
            update_listbox()
        else:
            messagebox.showerror("Error", "Note ID does not exist.")
    except ValueError:
        messagebox.showerror("Error", "Invalid note ID.")

def gui_search_notes():
    search_query = search_entry.get()
    filtered_notes = notebook.search_notes(search_query)
    update_listbox(filtered_notes)

def update_listbox(notes=None):
    if notes is None:
        notes = notebook.list_notes()
    listbox.delete('1.0', tk.END)
    for note_id, note_info in notes.items():
        note_title = note_info["title"]
        created_at = note_info.get("created_at", "N/A")
        last_modified = note_info.get("last_modified", "N/A")
        listbox_entry = f"Note {note_id}: {note_title} (Created: {created_at}, Last Modified: {last_modified})\n"
        listbox.insert(tk.END, listbox_entry)


notebook = Notebook()
application_window = tk.Tk()
application_window.title("Notebook Application")
application_window.geometry("600x500")
application_window.configure(bg=BACKGROUND_COLOR)

frame = tk.Frame(application_window, bg=BACKGROUND_COLOR)
frame.pack(pady=20)

search_frame = tk.Frame(application_window, bg=BACKGROUND_COLOR)
search_frame.pack(pady=10)

search_entry = tk.Entry(search_frame, font=TEXT_FONT, bg=ENTRY_BACKGROUND, fg=ENTRY_FOREGROUND)
search_entry.pack(side=tk.LEFT, fill='x', expand=True, padx=10)
search_button = tk.Button(search_frame, text="Search", command=gui_search_notes, bg=BUTTON_COLOR, fg=BUTTON_TEXT_COLOR, font=BUTTON_FONT)
search_button.pack(side=tk.LEFT, padx=10)

btn_add = tk.Button(frame, text="Add Note", command=gui_add_note, bg=BUTTON_COLOR, fg=BUTTON_TEXT_COLOR, font=BUTTON_FONT)
btn_edit = tk.Button(frame, text="Edit Note", command=gui_edit_note, bg=BUTTON_COLOR, fg=BUTTON_TEXT_COLOR, font=BUTTON_FONT)
btn_delete = tk.Button(frame, text="Delete Note", command=gui_delete_note, bg=BUTTON_COLOR, fg=BUTTON_TEXT_COLOR, font=BUTTON_FONT)

btn_add.grid(row=0, column=0, padx=5, pady=5)
btn_edit.grid(row=0, column=1, padx=5, pady=5)
btn_delete.grid(row=0, column=2, padx=5, pady=5)

listbox = scrolledtext.ScrolledText(application_window, font=TEXT_FONT, bg=ENTRY_BACKGROUND, fg=ENTRY_FOREGROUND)
listbox.pack(fill='both', expand=True, padx=20, pady=10)

application_window.mainloop()