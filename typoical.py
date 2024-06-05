from tkinter import *
from tkinter import ttk
from tkinter import simpledialog

class UserInterface:
    def __init__(self, menu_win):
        self.tab_counter = 1
        self.tabs_list = []
        self.tab_contents = {}  # Словник для зберігання вмісту вкладок

        win_size = '450x400'
        bg_color = '#ffe0ca'

        self.menu_gui(menu_win, win_size, bg_color)

    def menu_gui(self, window, size, bg_color):
        window.title('Obichniy calculator')
        window.geometry(size)

        self.tabs = ttk.Notebook(window)
        self.tabs.pack(anchor=N, fill=X)
        self.tabs.bind("<<NotebookTabChanged>>", self.update_button)

        # Initial tabs
        tab1 = Frame(self.tabs)
        self.tabs.add(tab1, text='0')
        self.tabs.bind("<3>", self.show_context_menu)

        self.tabs_list.append(tab1)
        self.tab_contents['0'] = ""  # Ініціалізуйте вміст початкової вкладки

        self.cont_menu = Menu(window, tearoff=0)
        self.cont_menu.add_command(label='Rename')

        enter_frame = Frame(window)
        enter_frame.place(relheight=0.15, relwidth=0.67, rely=0.1)

        self.enter_field = Entry(enter_frame, font=10)
        self.enter_field.pack(fill='both', expand=True)
        self.enter_field.bind("<KeyRelease>", self.update_tab_content)  # Зв'язок з подією <KeyRelease>

        output_screen = Frame(window, bg=bg_color)
        output_screen.place(relheight=0.57, relwidth=0.67, rely=0.25)

        func_label_frame = Frame(window)
        func_label_frame.place(relheight=0.18, relwidth=0.67, rely=0.82)

        func_label = Label(func_label_frame, font=10, bg='red')
        func_label.pack(fill='both', expand=True)

        brackets_label_frame = Frame(window)
        brackets_label_frame.place(relheight=0.72, relwidth=0.33, relx=0.67, rely=0.1)

        brackets_label = Label(brackets_label_frame, font=10, bg='blue')
        brackets_label.pack(fill='both', expand=True)

        button_frame = Frame(window)
        button_frame.place(relheight=0.18, relwidth=0.33, rely=0.82, relx=0.67)

        self.Brackets_button = Button(button_frame, text='Br_culc[0]')
        self.Brackets_button.pack(fill='both', expand=True)

        self.Culc_button = Button(button_frame, text='Culc[0]')
        self.Culc_button.pack(fill='both', expand=True)

        # Add and Remove buttons
        add_tab_button = Button(self.tabs, text="+", command=self.add_tab)
        add_tab_button.pack(side=RIGHT)

        # remove_tab_button = Button(self.tabs, text="-", command=self.remove_tab)
        # remove_tab_button.pack(side=RIGHT)

    def add_tab(self):
        new_tab = Frame(self.tabs)
        tab_text = str(self.tab_counter)
        self.tabs.add(new_tab, text=tab_text)
        new_tab.bind('<3>', self.show_context_menu)
        
        self.tabs.bind("<Double-Button-1>", self.double_create)

        self.tabs_list.append(new_tab)
        self.tab_contents[tab_text] = ""  # Додайте порожній рядок для нової вкладки
        self.tab_counter += 1

    def remove_tab(self):
        if len(self.tabs_list) > 1:
            selected_tab = self.tabs.select()
            if selected_tab:
                tab_text = self.tabs.tab(selected_tab, "text")
                self.tabs.forget(selected_tab)
                self.tabs_list = [tab for tab in self.tabs_list if str(tab) != selected_tab]
                del self.tab_contents[tab_text]  # Видаліть вміст вкладки зі словника
                self.tab_counter -= 1

    def update_button(self, event):
        selected_tab = self.tabs.tab(self.tabs.select(), "text")
        self.Brackets_button.config(text=f'Br_culc[{selected_tab}]')
        self.Culc_button.config(text=f'Culc[{selected_tab}]')
        self.enter_field.delete(0, END)  # Очистіть поле введення
        self.enter_field.insert(0, self.tab_contents[selected_tab])  # Завантажте вміст вкладки

    def update_tab_content(self, event):
        selected_tab = self.tabs.tab(self.tabs.select(), "text")
        self.tab_contents[selected_tab] = self.enter_field.get()
    
    def double_create(self, event):
        tab_index = event.widget.index("@%d,%d" % (event.x, event.y))
        if tab_index >= 0:
            self.tabs.select(tab_index)
            self.remove_tab()


    def show_context_menu(self, event):
        tab_index = event.widget.index("@%d,%d" % (event.x, event.y))
        if tab_index >= 0:
            self.tabs.select(tab_index)
            context_menu = Menu(self.tabs, tearoff=0)
            context_menu.add_command(label="rename", command=lambda: self.rename_tab(tab_index))
            context_menu.add_command(label="delete", command=self.remove_tab)
            context_menu.add_command(label='new', command=lambda: self.add_tab())
            context_menu.post(event.x_root, event.y_root)

    def rename_tab(self, tab_index):
        current_name = self.tabs.tab(tab_index, "text")
        new_name = simpledialog.askstring("Перейменувати вкладку", "Введіть нову назву вкладки:", initialvalue=current_name)
        if new_name:
            self.tabs.tab(tab_index, text=new_name)
            old_content = self.tab_contents.pop(current_name)
            self.tab_contents[new_name] = old_content

if __name__ == '__main__':
    root = Tk()
    main_menu = UserInterface(root)
    root.mainloop()
