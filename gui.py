import tkinter as tk
from tkinter import ttk, messagebox
import sv_ttk
import MainTwoGis

class MainApplication(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.parent.title("TwoGisParser")
        self.parent.geometry("1000x700")
        
        try:
            icon = tk.PhotoImage(file="static/mappin.png")
            self.parent.iconphoto(True, icon)
        except Exception:
            pass
            
        self.interface_style()
        self.pack(fill=tk.BOTH, expand=True)
        self.create_widgets()
        
        self.toggle_parser_mode()
        
    def interface_style(self):
        sv_ttk.set_theme("light")
        
    def create_widgets(self):
        """Создание всех виджетов интерфейса"""
        self.top_level_menu()
        self.create_parser_controls()
        self.create_status_bar()
        
    def top_level_menu(self):
        """Верхнее меню"""
        menubar = tk.Menu(self.parent)
        self.parent.config(menu=menubar)

        parse_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Парсинг", menu=parse_menu)
        parse_menu.add_command(label="Запустить парсинг", command=self.run_parsing)
        parse_menu.add_separator()
        parse_menu.add_command(label="Выход", command=self.btn_exit)

        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Справка", menu=help_menu)
        help_menu.add_command(label="Руководство пользователя", command=self.user_manual)
        help_menu.add_command(label="О программе", command=self.btn_about)

    def create_parser_controls(self):
        """Создание элементов управления для парсера"""
        # Основной фрейм
        main_frame = ttk.Frame(self, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Фрейм для выбора режима парсинга
        mode_frame = ttk.LabelFrame(main_frame, text="Режим парсинга", padding=10)
        mode_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.parser_mode = tk.StringVar(value="keyword")  # По умолчанию парсер по ключу
        
        # Радио-кнопки для выбора режима
        ttk.Radiobutton(mode_frame, text="Парсер по ключу", 
                       variable=self.parser_mode, 
                       value="keyword",
                       command=self.toggle_parser_mode).grid(row=0, column=0, sticky=tk.W, padx=20, pady=5)
        
        ttk.Radiobutton(mode_frame, text="Парсер по URL", 
                       variable=self.parser_mode, 
                       value="url",
                       command=self.toggle_parser_mode).grid(row=0, column=1, sticky=tk.W, padx=20, pady=5)
        
        # Фрейм для параметров парсинга (будет меняться в зависимости от режима)
        self.params_frame = ttk.LabelFrame(main_frame, text="Параметры парсинга", padding=10)
        self.params_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Создаем оба варианта параметров, но показываем только один
        self.create_keyword_params()
        self.create_url_params()
        
        # Дополнительные параметры (общие для обоих режимов)
        self.create_common_params()
        self.create_control_buttons()  # Кнопки управления
        self.create_log_area()  # Лог выполнения
        
    def create_keyword_params(self):
        """Создание элементов для парсера по ключу"""
        self.keyword_frame = ttk.Frame(self.params_frame)
        
        # Ключевое слово
        ttk.Label(self.keyword_frame, text="Ключевое слово:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.keyword_var = tk.StringVar(value="Мойка")
        self.keyword_entry = ttk.Entry(self.keyword_frame, textvariable=self.keyword_var, width=25)
        self.keyword_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        
        # Город
        ttk.Label(self.keyword_frame, text="Город:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.city_var = tk.StringVar(value="Челябинск")
        self.city_entry = ttk.Entry(self.keyword_frame, textvariable=self.city_var, width=25)
        self.city_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
        
    def create_url_params(self):
        """Создание элементов для парсера по URL"""
        self.url_frame = ttk.Frame(self.params_frame)
        
        # URL для парсинга
        ttk.Label(self.url_frame, text="URL страницы 2ГИС:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.url_var = tk.StringVar(value="https://2gis.ru/chelyabinsk/search/Мойка")
        self.url_entry = ttk.Entry(self.url_frame, textvariable=self.url_var, width=50)
        self.url_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        
        # Привязываем нажатие Ctrl+V для удобной вставки URL
        self.url_entry.bind("<Control-v>", lambda e: self.url_entry.event_generate('<<Paste>>'))
        
    def create_common_params(self):
        """Создание общих параметров для обоих режимов"""
        common_frame = ttk.LabelFrame(self, text="Дополнительные параметры", padding=10)
        common_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Количество фирм
        ttk.Label(common_frame, text="Количество фирм:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.firm_count_var = tk.IntVar(value=50)
        self.firm_count_spinbox = ttk.Spinbox(common_frame, from_=1, to=1000, 
                                              textvariable=self.firm_count_var, width=20)
        self.firm_count_spinbox.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        
        
        # Кнопка для генерации URL (только для режима по ключу)
        self.generate_url_btn = ttk.Button(common_frame, text="Сгенерировать URL", 
                                          command=self.generate_url, width=20)
        self.generate_url_btn.grid(row=1, column=2, columnspan=2, padx=5, pady=5)
        
    def create_control_buttons(self):
        """Создание кнопок управления"""
        button_frame = ttk.Frame(self, padding=10)
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="Запустить парсинг", 
                  command=self.run_parsing, width=25).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Остановить парсинг", 
                  command=self.stop_parsing, width=25).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Очистить лог", 
                  command=self.clear_log, width=25).pack(side=tk.LEFT, padx=5)
        
    def create_log_area(self):
        """Создание области для логов"""
        log_frame = ttk.LabelFrame(self, text="Лог выполнения", padding=10)
        log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Создаем текстовое поле для логов
        self.log_text = tk.Text(log_frame, height=20, wrap=tk.WORD)
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # Добавляем скроллбар
        scrollbar = ttk.Scrollbar(self.log_text)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.log_text.yview)
        
    def create_status_bar(self):
        """Создание строки состояния"""
        self.status_var = tk.StringVar()
        self.status_var.set("Готов к работе")
        self.status_bar = ttk.Label(self, textvariable=self.status_var, 
                                   relief=tk.SUNKEN, padding=(10, 5))
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
    def toggle_parser_mode(self):
        """Переключение между режимами парсинга"""
        if self.parser_mode.get() == "keyword":
            # Показываем параметры для парсера по ключу
            for widget in self.params_frame.winfo_children():
                widget.pack_forget()
            self.keyword_frame.pack(fill=tk.X, pady=5)
            self.generate_url_btn.config(state=tk.NORMAL)
            self.status_var.set("Режим: Парсер по ключу")
        else:
            # Показываем параметры для парсера по URL
            for widget in self.params_frame.winfo_children():
                widget.pack_forget()
            self.url_frame.pack(fill=tk.X, pady=5)
            self.generate_url_btn.config(state=tk.DISABLED)
            self.status_var.set("Режим: Парсер по URL")
            
    def generate_url(self):
        """Генерация URL на основе ключевого слова и города"""
        keyword = self.keyword_var.get().strip()
        city = self.city_var.get().strip()
        
        if not keyword or not city:
            messagebox.showwarning("Предупреждение", "Введите ключевое слово и город!")
            return
            
        # Преобразуем кириллицу в латиницу для URL (упрощенный вариант)
        city_lower = city.lower()
        keyword_encoded = keyword.replace(" ", "%20")
        
        # Простое преобразование для русских городов
        city_mapping = {
            "Белая Калитва": "belaya-kalitva",
            "Санкт-Петербург": "spb",
            "Белая Холуница": "belaya-holunica",
            "Большой Камень": "bolshoj-kamen",
            "Великие Луки": "velikie-luki",
            "Великий Новгород": "v_novgorod",
            "Великий Устюг": "velikij-ustyug",
            "Верхний Тагил": "verhnij-tagil",
            "Нижний Новгород": "n_novgorod",
        }
        
        city_code = city_mapping.get(city_lower, city_lower)
        generated_url = f"https://2gis.ru/{city_code}/search/{keyword_encoded}"
        
        self.url_var.set(generated_url)
        
        # Предлагаем переключиться на режим по URL
        if messagebox.askyesno("URL сгенерирован", 
                              f"URL успешно сгенерирован:\n{generated_url}\n\n"
                              f"Хотите переключиться на парсер по URL?"):
            self.parser_mode.set("url")
            self.toggle_parser_mode()
            
    def run_parsing(self):
        """Запуск парсинга в зависимости от выбранного режима"""
        if self.parser_mode.get() == "keyword":
            self.run_keyword_parsing()
        else:
            self.run_url_parsing()
            
    def run_keyword_parsing(self):
        """Запуск парсинга по ключу"""
        keyword = self.keyword_var.get()
        city = self.city_var.get()
        firm_count = self.firm_count_var.get()
        
        if not keyword or not city:
            messagebox.showwarning("Предупреждение", "Заполните все поля!")
            return
            
        self.log_message(f"Начало парсинга по ключу: '{keyword}' в {city}, количество: {firm_count}")
        self.status_var.set(f"Парсинг по ключу: {keyword} в {city}")
        
        # Здесь будет вызов реального парсера
        self.simulate_parsing("keyword", keyword, city, firm_count)
        
    def run_url_parsing(self):
        """Запуск парсинга по URL"""
        url = self.url_var.get()
        firm_count = self.firm_count_var.get()
        
        if not url:
            messagebox.showwarning("Предупреждение", "Введите URL для парсинга!")
            return
            
        if not url.startswith(('https://2gis.ru/', 'http://2gis.ru/')):
            messagebox.showwarning("Предупреждение", "Введите корректный URL 2ГИС!")
            return
            
        self.log_message(f"Начало парсинга по URL: {url}")
        self.status_var.set(f"Парсинг по URL: {url[:50]}...")
        
        # Здесь будет вызов реального парсера
        self.simulate_parsing("url", url, firm_count)

    def simulate_parsing(self, mode, *args):
        """Имитация работы парсера"""
        import threading
        import time
        import random
        
        def parsing_thread():
            try:
                if mode == "keyword":
                    keyword, city, firm_count = args
                    for i in range(1, min(firm_count, 15) + 1):
                        time.sleep(0.5 + random.random() * 0.5)
                        message = f"Найдена фирма {i}: {keyword} #{i} в {city}"
                        self.after(0, self.log_message, message)
                    
                    self.after(0, lambda: self.status_var.set("Парсинг по ключу завершен"))
                    self.after(0, lambda: self.log_message(f"Найдено {min(firm_count, 15)} организаций"))
                else:
                    url, firm_count = args
                    
                    self.after(0, self.log_message, f"Анализ URL: {url}")
                    
                    self.after(0, lambda: self.status_var.set("Парсинг по URL завершен"))
                    self.after(0, lambda: self.log_message(f"Обработано {min(firm_count, 20)} записей"))
                
                self.after(0, lambda: self.log_message("Парсинг успешно завершен!"))
            except Exception as e:
                self.after(0, lambda: self.log_message(f"Ошибка: {str(e)}"))
        
        thread = threading.Thread(target=parsing_thread)
        thread.daemon = True
        thread.start()

    def stop_parsing(self):
        """Остановка парсинга"""
        self.status_var.set("Парсинг остановлен")
        self.log_message("Парсинг остановлен пользователем")
        
    def clear_log(self):
        """Очистка лога"""
        self.log_text.delete(1.0, tk.END)
        self.log_message("Лог очищен")
        
    def log_message(self, message):
        """Добавление сообщения в лог"""
        import datetime
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)


    def user_manual(self):
        """Обработчик кнопки 'Руководство пользователя'"""
        about_text = """
        Руководство пользователя
        
        1. Выберите режим парсинга:
           • Парсер по ключу - поиск по ключевому слову и городу
           • Парсер по URL - парсинг конкретной страницы 2ГИС
        
        2. Заполните параметры:
           • Для парсера по ключу: ключевое слово и город
           • Для парсера по URL: вставьте URL страницы
           • Укажите количество фирм для парсинга
        
        3. Дополнительные параметры:
           • Для парсера по ключу: кнопка "Сгенерировать URL"
        
        4. Нажмите "Запустить парсинг"
        
        Примечания:
        • Для работы парсера требуется стабильное интернет-соединение
        • Можно переключаться между режимами в процессе работы
        """
        messagebox.showinfo("Руководство пользователя", about_text, icon="question")

    def btn_about(self):
        """Обработчик кнопки 'О программе'"""
        about_text = """
        Парсер данных 2ГИС
        Версия 2.0.0
        
        Два режима работы в одном интерфейсе:
        1. Парсер по ключу - поиск организаций по ключевому слову и городу
        2. Парсер по URL - парсинг конкретной страницы поиска 2ГИС
        
        https://github.com/itgeroy/TwoGisParser
        
        Используемые технологии:
        • Python 3.11+
        • playwright для веб-скрапинга
        • tkinter для графического интерфейса
        • sv_ttk для современных стилей
        """
        messagebox.showinfo("О программе", about_text)

    def btn_exit(self):
        """Выход из приложения"""
        if messagebox.askyesno("Выход", "Вы уверены, что хотите выйти?"):
            self.parent.quit()

def main():
    """Точка входа в приложение"""
    root = tk.Tk()
    app = MainApplication(root)
    root.mainloop()

if __name__ == "__main__":
    main()