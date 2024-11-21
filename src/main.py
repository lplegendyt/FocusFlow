import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import ttk  # Hinzufügen des Imports für ttk
import time
import winsound

# Hauptfenster erstellen
root = tk.Tk()
root.title("FocusFlow - Task Manager")
root.geometry("1000x750")  # Größeres Fenster für bessere Bedienbarkeit
root.minsize(1000, 1000)  # Minimale Fenstergröße für Flexibilität
root.config(bg="#E8F5E9")

# Timer-Variablen
timer_running = False
time_left = 0

# Funktionen
def add_task():
    """Neue Aufgabe zur Liste hinzufügen."""
    task = task_input.get()
    if task:
        task_listbox.insert(tk.END, task)
        task_input.delete(0, tk.END)
    else:
        messagebox.showwarning("Input Error", "Please enter a task.")

def delete_task():
    """Ausgewählte Aufgabe löschen."""
    selected_task = task_listbox.curselection()
    if selected_task:
        task_listbox.delete(selected_task)
    else:
        messagebox.showwarning("Selection Error", "Please select a task to delete.")

def mark_done():
    """Markiert die ausgewählte Aufgabe als erledigt."""
    selected_task = task_listbox.curselection()
    if selected_task:
        task = task_listbox.get(selected_task)
        task_listbox.delete(selected_task)
        task_listbox.insert(tk.END, f"[Done] {task}")
        task_listbox.itemconfig(tk.END, {'fg': 'green'})
        messagebox.showinfo("Task Completed", f"'{task}' marked as done!")
    else:
        messagebox.showwarning("Selection Error", "Please select a task to mark as done.")

def prioritize_task():
    """Setzt die ausgewählte Aufgabe als Priorität an den Anfang der Liste."""
    selected_task = task_listbox.curselection()
    if selected_task:
        task = task_listbox.get(selected_task)
        task_listbox.delete(selected_task)
        task_listbox.insert(0, f"[Priority] {task}")
        task_listbox.itemconfig(0, {'fg': 'red'})
        messagebox.showinfo("Task Prioritized", f"'{task}' set as a priority!")
    else:
        messagebox.showwarning("Selection Error", "Please select a task to prioritize.")

def save_tasks():
    """Speichert Aufgaben in einer Datei."""
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", 
                                             filetypes=[("Text Files", "*.txt")])
    if file_path:
        with open(file_path, "w") as file:
            tasks = task_listbox.get(0, tk.END)
            for task in tasks:
                file.write(task + "\n")
        messagebox.showinfo("Save Successful", "Tasks saved successfully!")

def load_tasks():
    """Lädt Aufgaben aus einer Datei."""
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if file_path:
        with open(file_path, "r") as file:
            tasks = file.readlines()
            for task in tasks:
                task_listbox.insert(tk.END, task.strip())
        messagebox.showinfo("Load Successful", "Tasks loaded successfully!")

def search_task():
    """Sucht nach einer Aufgabe in der Liste."""
    search_query = search_input.get()
    if search_query:
        for idx, task in enumerate(task_listbox.get(0, tk.END)):
            if search_query.lower() in task.lower():
                task_listbox.selection_clear(0, tk.END)
                task_listbox.selection_set(idx)
                task_listbox.see(idx)
                return
        messagebox.showinfo("Search Result", "No matching task found.")
    else:
        messagebox.showwarning("Input Error", "Please enter a search term.")

def start_timer():
    """Startet einen 25-Minuten-Timer."""
    global timer_running, time_left
    if not timer_running:
        time_left = 25 * 60  # 25 Minuten in Sekunden
        timer_running = True
        countdown()

def stop_timer():
    """Stoppt den Timer."""
    global timer_running
    timer_running = False

def countdown():
    """Handle the timer countdown."""
    global timer_running, time_left
    if timer_running and time_left > 0:
        mins, secs = divmod(time_left, 60)
        timer_label.config(text=f"Time Left: {mins:02}:{secs:02}")
        progress_bar['value'] = (1 - (time_left / (25 * 60))) * 100  # Timer-Prozessbalken
        time_left -= 1
        root.after(1000, countdown)
    else:
        timer_running = False
        timer_label.config(text="Time Left: 25:00")
        progress_bar['value'] = 0
        if time_left == 0:
            winsound.Beep(1000, 1000)  # Benachrichtigung bei Timer-Ende
            messagebox.showinfo("Timer Finished", "Focus time is over!")

# Benutzeroberfläche
header_frame = tk.Frame(root, bg="#388E3C")
header_frame.pack(fill=tk.X, pady=20)

header_label = tk.Label(header_frame, text="FocusFlow - Your Task Manager", font=("Helvetica", 20), bg="#388E3C", fg="white")
header_label.pack()

# Aufgabenrahmen
task_frame = tk.Frame(root, bg="#E8F5E9")
task_frame.pack(pady=25)

task_input = tk.Entry(task_frame, width=50, font=("Helvetica", 14), bd=2, relief="solid", fg="#388E3C")
task_input.grid(row=0, column=0, padx=15)

add_button = tk.Button(task_frame, text="Add Task", font=("Helvetica", 14), command=add_task, bg="#388E3C", fg="white", width=12, relief="flat")
add_button.grid(row=0, column=1, padx=15)

# Aufgabenliste
task_listbox = tk.Listbox(root, width=60, height=20, font=("Helvetica", 12), selectmode=tk.SINGLE, bg="#ffffff", bd=2, relief="solid")
task_listbox.pack(pady=10)

scrollbar = tk.Scrollbar(root, orient=tk.VERTICAL, command=task_listbox.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
task_listbox.config(yscrollcommand=scrollbar.set)

# Aktionsbuttons für Aufgaben
action_buttons_frame = tk.Frame(root, bg="#E8F5E9")
action_buttons_frame.pack(pady=20)

delete_button = tk.Button(action_buttons_frame, text="Delete Task", font=("Helvetica", 14), command=delete_task, bg="#FF5722", fg="white", width=12, relief="flat")
delete_button.pack(side=tk.LEFT, padx=10)

done_button = tk.Button(action_buttons_frame, text="Mark as Done", font=("Helvetica", 14), command=mark_done, bg="#4CAF50", fg="white", width=12, relief="flat")
done_button.pack(side=tk.LEFT, padx=10)

priority_button = tk.Button(action_buttons_frame, text="Prioritize", font=("Helvetica", 14), command=prioritize_task, bg="#FFEB3B", fg="black", width=12, relief="flat")
priority_button.pack(side=tk.LEFT, padx=10)

# Speichern/Loaden Buttons
save_load_buttons_frame = tk.Frame(root, bg="#E8F5E9")
save_load_buttons_frame.pack(pady=20)

save_button = tk.Button(save_load_buttons_frame, text="Save Tasks", font=("Helvetica", 14), command=save_tasks, bg="#4CAF50", fg="white", width=12, relief="flat")
save_button.pack(side=tk.LEFT, padx=10)

load_button = tk.Button(save_load_buttons_frame, text="Load Tasks", font=("Helvetica", 14), command=load_tasks, bg="#FFC107", fg="black", width=12, relief="flat")
load_button.pack(side=tk.LEFT, padx=10)

# Suchfeld
search_frame = tk.Frame(root, bg="#E8F5E9")
search_frame.pack(pady=20)

search_input = tk.Entry(search_frame, width=30, font=("Helvetica", 14), bd=2, relief="solid", fg="#388E3C")
search_input.pack(side=tk.LEFT, padx=15)

search_button = tk.Button(search_frame, text="Search Task", font=("Helvetica", 14), command=search_task, bg="#FF9800", fg="white", width=12, relief="flat")
search_button.pack(side=tk.LEFT, padx=10)

# Timerbereich
timer_frame = tk.Frame(root, bg="#E8F5E9")
timer_frame.pack(pady=20)

timer_label = tk.Label(timer_frame, text="Time Left: 25:00", font=("Helvetica", 16), bg="#E8F5E9", fg="black")
timer_label.pack()

progress_bar = ttk.Progressbar(timer_frame, length=300, mode="determinate", maximum=100)  # Verwende ttk.Progressbar
progress_bar.pack(pady=15)

timer_buttons_frame = tk.Frame(root, bg="#E8F5E9")
timer_buttons_frame.pack(pady=10)

start_timer_button = tk.Button(timer_buttons_frame, text="Start Timer", font=("Helvetica", 14), command=start_timer, bg="#4CAF50", fg="white", width=12, relief="flat")
start_timer_button.pack(side=tk.LEFT, padx=10)

stop_timer_button = tk.Button(timer_buttons_frame, text="Stop Timer", font=("Helvetica", 14), command=stop_timer, bg="#FF6347", fg="white", width=12, relief="flat")
stop_timer_button.pack(side=tk.LEFT, padx=10)

root.mainloop()
