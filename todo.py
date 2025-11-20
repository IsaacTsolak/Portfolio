import tkinter as tk
from tkinter import messagebox
from tkinter import font as tkFont

class TodoApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Fancy To-Do List")
        self.geometry("1200x1200")
        self.config(bg="#f4f4f9")

        # Load tasks from file
        self.tasks = self.load_tasks()

        # Custom font styles
        self.title_font = tkFont.Font(family="Helvetica", size=20, weight="bold")
        self.button_font = tkFont.Font(family="Helvetica", size=14)
        self.task_font = tkFont.Font(family="Arial", size=16)

        # Title Label
        self.title_label = tk.Label(self, text="To-Do List", font=self.title_font, bg="#f4f4f9", fg="#4f4f4f")
        self.title_label.pack(pady=20)

        # Create the task Listbox
        self.task_listbox = tk.Listbox(self, height=15, width=50, font=self.task_font, bd=5, relief="flat", bg="#ffffff", fg="#4f4f4f", selectbackground="#d1e0e0")
        self.task_listbox.pack(pady=20)
        self.update_task_listbox()

        # Task entry widget
        self.task_entry = tk.Entry(self, width=40, font=self.task_font, bd=5, relief="flat", fg="#555", bg="#ffffff")
        self.task_entry.pack(pady=10)

        # Buttons
        self.add_task_button = tk.Button(self, text="Add Task", width=20, font=self.button_font, command=self.add_task, bg="#28a745", fg="white", relief="raised", bd=5)
        self.add_task_button.pack(pady=10)

        self.delete_task_button = tk.Button(self, text="Remove Task", width=20, font=self.button_font, command=self.delete_task, bg="#dc3545", fg="white", relief="raised", bd=5)
        self.delete_task_button.pack(pady=10)

        self.mark_done_button = tk.Button(self, text="Mark as Done", width=20, font=self.button_font, command=self.mark_done, bg="#007bff", fg="white", relief="raised", bd=5)
        self.mark_done_button.pack(pady=10)

    # Load tasks from file
    def load_tasks(self):
        try:
            with open("tasks.txt", "r") as file:
                tasks = [line.strip() for line in file.readlines()]
        except FileNotFoundError:
            tasks = []
        return tasks

    # Save tasks to file
    def save_tasks(self):
        with open("tasks.txt", "w") as file:
            for task in self.tasks:
                file.write(f"{task}\n")

    # Update Listbox
    def update_task_listbox(self):
        self.task_listbox.delete(0, tk.END)
        for task in self.tasks:
            self.task_listbox.insert(tk.END, task)

    # Add new task
    def add_task(self):
        task = self.task_entry.get()
        if task != "":
            self.tasks.append(task)
            self.save_tasks()
            self.update_task_listbox()
            self.task_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Input Error", "Please enter a task.")

    # Delete a selected task
    def delete_task(self):
        try:
            task_index = self.task_listbox.curselection()[0]
            del self.tasks[task_index]
            self.save_tasks()
            self.update_task_listbox()
        except IndexError:
            messagebox.showwarning("Selection Error", "Please select a task to remove.")

    # Mark a task as done
    def mark_done(self):
        try:
            task_index = self.task_listbox.curselection()[0]
            task = self.tasks[task_index]
            self.tasks[task_index] = f"[Done] {task}"
            self.save_tasks()
            self.update_task_listbox()
        except IndexError:
            messagebox.showwarning("Selection Error", "Please select a task to mark as done.")

# Create and run the app
app = TodoApp()
app.mainloop()
