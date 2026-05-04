import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
from datetime import datetime

class TrainingPlanner:
    def __init__(self, root):
        self.root = root
        self.root.title("Training Planner")
        self.trainings = []

        # Ввод данных
        frame = ttk.Frame(root)
        frame.pack(pady=10, padx=10, fill='x')

        ttk.Label(frame, text="Дата (YYYY-MM-DD):").grid(row=0, column=0, sticky='w')
        self.date_entry = ttk.Entry(frame)
        self.date_entry.grid(row=0, column=1, sticky='ew')

        ttk.Label(frame, text="Тип тренировки:").grid(row=0, column=2, sticky='w')
        self.type_entry = ttk.Entry(frame)
        self.type_entry.grid(row=0, column=3, sticky='ew')

        ttk.Label(frame, text="Длительность (мин):").grid(row=0, column=4, sticky='w')
        self.duration_entry = ttk.Entry(frame)
        self.duration_entry.grid(row=0, column=5, sticky='ew')

        ttk.Button(frame, text="Добавить тренировку", command=self.add_training).grid(row=0, column=6, padx=5)

        # Таблица
        self.tree = ttk.Treeview(root, columns=('date', 'type', 'duration'), show='headings')
        self.tree.heading('date', text='Дата')
        self.tree.heading('type', text='Тип')
        self.tree.heading('duration', text='Длительность')
        self.tree.pack(pady=10, fill='both', expand=True)

        # Фильтры
        filter_frame = ttk.Frame(root)
        filter_frame.pack(pady=5, fill='x')

        ttk.Label(filter_frame, text="Фильтр по типу:").grid(row=0, column=0)
        self.type_filter = ttk.Entry(filter_frame)
        self.type_filter.grid(row=0, column=1)

        ttk.Label(filter_frame, text="Фильтр по дате:").grid(row=0, column=2)
        self.date_filter = ttk.Entry(filter_frame)
        self.date_filter.grid(row=0, column=3)

        ttk.Button(filter_frame, text="Применить фильтр", command=self.apply_filter).grid(row=0, column=4, padx=5)
        ttk.Button(filter_frame, text="Сбросить фильтр", command=self.reset_filter).grid(row=0, column=5)

        # Меню для сохранения/загрузки
        menubar = tk.Menu(root)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Сохранить", command=self.save_to_json)
        filemenu.add_command(label="Загрузить", command=self.load_from_json)
        menubar.add_cascade(label="Файл", menu=filemenu)

        root.config(menu=menubar)

    def add_training(self):
        date_str = self.date_entry.get()
        t_type = self.type_entry.get()
        duration_str = self.duration_entry.get()

        # Проверка даты
        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Ошибка", "Некорректный формат даты")
            return

        # Проверка длительности
        if not duration_str.isdigit() or int(duration_str) <= 0:
            messagebox.showerror("Ошибка", "Длительность должна быть положительным числом")
            return

        duration = int(duration_str)

        # Добавление записи
        self.trainings.append({
            'date': date_str,
            'type': t_type,
            'duration': duration
        })

        self.update_treeview()

        # Очистка полей
        self.date_entry.delete(0, tk.END)
        self.type_entry.delete(0, tk.END)
        self.duration_entry.delete(0, tk.END)

    def update_treeview(self, filtered=None):
        for item in self.tree.get_children():
            self.tree.delete(item)
        data = filtered if filtered is not None else self.trainings
        for t in data:
            self.tree.insert('', 'end', values=(t['date'], t['type'], t['duration']))

    def apply_filter(self):
        t_type = self.type_filter.get()
        date_filter = self.date_filter.get()

        filtered = self.trainings
        if t_type:
            filtered = [t for t in filtered if t['type'] == t_type]
        if date_filter:
            filtered = [t for t in filtered if t['date'] == date_filter]

        self.update_treeview(filtered)

    def reset_filter(self):
        self.type_filter.delete(0, tk.END)
        self.date_filter.delete(0, tk.END)
        self.update_treeview()

    def save_to_json(self):
        filename = filedialog.asksaveasfilename(defaultextension=".json")
        if filename:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.trainings, f, ensure_ascii=False, indent=4)

    def load_from_json(self):
        filename = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if filename:
            with open(filename, 'r', encoding='utf-8') as f:
                self.trainings = json.load(f)
            self.update_treeview()

if __name__ == "__main__":
    root = tk.Tk()
    app = TrainingPlanner(root)
    root.mainloop()
