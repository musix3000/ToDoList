import tkinter as tk
from tkinter import ttk
from tkinter import *
import json

def add_task():
    task = entry.get()
    category = category_var.get()
    priority = priority_var.get()

    if task:
        listbox.insert("", tk.END, values=(category, task, priority))
        entry.delete(0, tk.END)  # Очистить строку ввода
        save_tasks()

def delete_task():
    selected_item = listbox.selection()[0]
    listbox.delete(selected_item)
    save_tasks()

def edit_task():
    selected_item = listbox.selection()[0]
    item_values = listbox.item(selected_item, "values")
    task_editor(item_values, selected_item)

def task_editor(item_values, selected_item):
    task_window = tk.Toplevel(win)
    task_window.title("Edit Task")

    task_label = tk.Label(task_window, text="Task:")
    task_label.grid(row=0, column=0)

    task_entry = tk.Entry(task_window)
    task_entry.grid(row=0, column=1)
    task_entry.insert(0, item_values[1])

    priority_label = tk.Label(task_window, text="Priority:")
    priority_label.grid(row=1, column=0)

    task_priority = tk.StringVar(task_window)
    task_priority.set(item_values[2])
    priority_dropdown = tk.OptionMenu(task_window, task_priority, *priorities)
    priority_dropdown.grid(row=1, column=1)

    save_button = tk.Button(task_window, text="Save", command=lambda: save_edited_task(task_window, task_entry, task_priority, selected_item))
    save_button.grid(row=2, column=0, columnspan=2)

def save_edited_task(task_window, task_entry, task_priority, selected_item):
    edited_task = task_entry.get()
    edited_priority = task_priority.get()
    listbox.item(selected_item, values=(category_var.get(), edited_task, edited_priority))
    save_tasks()
    task_window.destroy()

def save_tasks():
    tasks = [(listbox.item(item)["values"]) for item in listbox.get_children()]
    with open("tasks.json", "w") as file:
        json.dump(tasks, file)




win = tk.Tk()
win.title('ToDoList') #название приложения
win.geometry("350x450") #размер окна
win.resizable(False, False) #запрещаем менять размер окна
photo = tk.PhotoImage(file = 'icon.png')
win.iconphoto(False, photo) #выбрали иконку
win.config(bg='#A7DBF2') #цвет фона


frame = tk.Frame(win,
                 height=350,
                 width=280)
frame.place(x=18,
            y=40)

columns = ("Категория", "Задание", "Приоритет")
listbox = ttk.Treeview(frame, columns=columns, show="headings")
for col in columns:
    listbox.heading(col, text=col)
    listbox.column(col, minwidth=0, width=100, stretch=tk.NO)
listbox.pack(side=tk.LEFT, fill=tk.BOTH)

scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL, command=listbox.yview)
scrollbar.pack(side=tk.RIGHT, fill="y")

listbox.config(yscrollcommand=scrollbar.set)


entry = tk.Entry(win, width=35)
entry.place(x=20,
            y=280)

category_label = tk.Label(win, text="Категория:")
category_label.place(x=20,
                     y=310)

categories = ["Работа", "Учеба", "Личное"]
category_var = tk.StringVar(win)
category_var.set(categories[0])
category_dropdown = tk.OptionMenu(win, category_var, *categories)
category_dropdown.place(x=20,
                        y=330)

priority_label = tk.Label(win, text="Приоритет:")
priority_label.place(x=120,
                     y=310)

priorities = ["важно", "подождет", "ваще неважно"]
priority_var = tk.StringVar(win)
priority_var.set(priorities[0])
priority_dropdown = tk.OptionMenu(win, priority_var, *priorities)
priority_dropdown.place(x=120,
                        y=330)

edit_button = tk.Button(win, text="редактировать", command=edit_task)
edit_button.place(x=20, y=370)

add_button = tk.Button(win, text="↑", command=add_task)
add_button.place(x=270, y=280)

delete_button = tk.Button(win, text="удалить", command=delete_task)
delete_button.place(x=160, y=368)


try:
    with open("tasks.json", "r") as file:
        tasks = json.load(file)
        for task in tasks:
            listbox.insert("", tk.END, values=task)
except FileNotFoundError:
    pass


win.mainloop() #открываем окно

