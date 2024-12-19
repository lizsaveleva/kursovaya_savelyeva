from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, messagebox, filedialog, Listbox, Variable
from PIL import Image
from tkinter import ttk
import sqlite3
import datetime
from tkcalendar import Calendar
from werkzeug.security import generate_password_hash, check_password_hash



connection = sqlite3.connect('db/Booking.db')
cursor = connection.cursor()


def create_tables():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            login TEXT NOT NULL UNIQUE,
            hashed_password TEXT NOT NULL,
            name TEXT NOT NULL,
            surname TEXT NOT NULL,
            patronymic TEXT NOT NULL,
            number TEXT NOT NULL,
            date_b TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS hotels (
            hotel_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            png TEXT NOT NULL,
            price INTEGER NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bron (
            bron_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            hotel_id INTEGER,
            date_in TEXT,
            date_out TEXT,
            price TEXT,
            type TEXT,
            FOREIGN KEY (user_id) REFERENCES users (user_id),
            FOREIGN KEY (hotel_id) REFERENCES hotels (hotel_id)
        )
    ''')

    connection.commit()


def add_bd_user(login, hashed_password, name, surname, patronymic, number, date_b):
    cursor.execute('''
        INSERT INTO users (login, hashed_password, name, surname, patronymic, number, date_b) 
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (login, hashed_password, name, surname, patronymic, number, date_b))

    connection.commit()


def add_bd_user(login, hashed_password, name, surname, patronymic, number, date_b):
    cursor.execute(f'INSERT INTO users (login, hashed_password, name, surname, patronymic, number, date_b) '
                   f'VALUES (?, ?, ?, ?, ?, ?, ?)',
                   (login, hashed_password, name, surname, patronymic, number, date_b,))
    connection.commit()


def add_bd_hotels(name, png, price):
    cursor.execute(f'INSERT INTO hotels (name, png, price) '
                   f'VALUES (?, ?, ?)',
                   (name, png, price,))
    connection.commit()


def add_bd_bron(name):
    cursor.execute(f'INSERT INTO bron (user_id) '
                   f'VALUES (?)',
                   (name,))
    connection.commit()


def main_page(name):
    spis = [n[0] for n in cursor.execute('SELECT name FROM hotels').fetchall()]

    def back():
        window.destroy()
        sign_in_form()
    window = Tk()

    def hotel_page_click():
        a = listbox.get(listbox.curselection())
        window.destroy()
        hotel_page(cursor.execute('SELECT user_id FROM users WHERE login=?', (name,)).fetchall()[0][0],
                   a, 1, cursor.execute(
            'SELECT price FROM hotels WHERE name=?', (a,)).fetchall()[0][0])

    def click():
        window.destroy()
        us_page(cursor.execute('SELECT user_id FROM users WHERE login=?', (name,)).fetchall()[0][0])
    window.geometry("575x600")
    window.configure(bg="#000000")

    canvas = Canvas(
        window,
        bg="#000000",
        height=600,
        width=575,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )

    canvas.place(x=0, y=0)
    canvas.create_rectangle(
        0.0,
        0.0,
        575.0,
        80.0,
        fill="#425E4A",
        outline="")

    canvas.create_rectangle(
        10,
        24.0,
        159.0,
        62.0,
        fill="#D9D9D9",
        outline="")

    canvas.create_rectangle(
        0.0,
        532.0,
        575.0,
        600.0,
        fill="#D9D9D9",
        outline="")

    button_1 = Button(
        borderwidth=0,
        highlightthickness=0,
        command=click,
        relief="flat",
        text=name
    )
    button_1.place(
        x=10,
        y=26.0,
        width=145.0,
        height=34.0
    )

    button_image_2 = PhotoImage(
        file="./assets/frame3/button_2.png")
    button_2 = Button(
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=hotel_page_click,
        relief="flat"
    )
    button_2.place(
        x=5.0,
        y=537.0,
        width=564.0,
        height=58.0
    )
    button_image_3 = PhotoImage(
        file="./assets/frame3/button_3.png")
    button_3 = Button(
        image=button_image_3,
        borderwidth=0,
        highlightthickness=0,
        command=back,
        relief="flat"
    )
    canvas.create_rectangle(
        520.0,
        14.0,
        600.0,
        69.0,
        fill="#FFFFFF",
        outline="")
    button_3.place(
        x=525.0,
        y=19.0,
        width=44.99998474121094,
        height=44.0
    )
    listbox = Listbox(
        bg='#729D7F',
        listvariable=Variable(value=spis)
    )
    listbox.place(
        x=0,
        y=80,
        width=575,
        height=452
    )
    window.resizable(False, False)
    window.mainloop()


def sign_in_form():
    def clicked_sign_in():
        if entry_1.get() and entry_2.get():
            ne = cursor.execute(
                'SELECT hashed_password FROM users WHERE login=?', (entry_1.get(),)).fetchall()
            if ne:
                if check_password_hash(ne[0][0], entry_2.get()):
                    if entry_1.get() == "admin":
                        window.destroy()
                        hotels_form()
                    else:
                        a = entry_1.get()
                        window.destroy()
                        main_page(a)
                else:
                    messagebox.showerror("Ошибка", "Неверный пароль")
            else:
                messagebox.showerror("Ошибка", "Такого пользователя нет, попробуйте зарегистрироваться")
        else:
            messagebox.showerror("Ошибка", "Поля не могу быть пустыми")

    def clicked_sign_up():
        window.destroy()
        sign_up_form()

    window = Tk()

    window.geometry("900x600")
    window.configure(bg="#FFFFFF")

    canvas = Canvas(
        window,
        bg="#FFFFFF",
        height=600,
        width=900,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )

    canvas.place(x=0, y=0)
    image_image_1 = PhotoImage(
        file="./assets/frame0/image_1.png")
    image_1 = canvas.create_image(
        450.0,
        300.0,
        image=image_image_1
    )

    canvas.create_rectangle(
        419.0,
        25.0,
        881.0,
        576.0,
        fill="#EBFFF1",
        outline="")

    canvas.create_text(
        522.0,
        259.0,
        anchor="nw",
        text="Пароль",
        fill="#000000",
        font=("Inter Light", 16 * -1)
    )

    canvas.create_text(
        522.0,
        128.0,
        anchor="nw",
        text="Логин",
        fill="#000000",
        font=("Inter Light", 16 * -1)
    )

    canvas.create_rectangle(
        0.0,
        0.0,
        392.0,
        600.0,
        fill="#425E4A",
        outline="")

    canvas.create_text(
        35.0,
        90.0,
        anchor="nw",
        text="Отелей",
        fill="#D0D0D0",
        font=("Inter Medium", 40 * -1)
    )
    canvas.create_text(
        35.0,
        177.0,
        anchor="nw",
        text="Вход в аккаунт",
        fill="#D0D0D0",
        font=("Inter Medium", 40 * -1)
    )
    canvas.create_text(
        35.0,
        42.0,
        anchor="nw",
        text="Бронирование",
        fill="#D0D0D0",
        font=("Inter Medium", 40 * -1)
    )
    canvas.create_rectangle(
        -3.0,
        156.0,
        391.9995822189594,
        161.0795733911242,
        fill="#FFFFFF",
        outline="")
    button_image_1 = PhotoImage(
        file="./assets/frame0/button_1.png")
    button_1 = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=clicked_sign_up,
        relief="flat"
    )
    button_1.place(
        x=507.0,
        y=453.0,
        width=281.0,
        height=40.0
    )

    button_image_2 = PhotoImage(
        file="./assets/frame0/button_2.png")
    button_2 = Button(
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=clicked_sign_in,
        relief="flat"
    )
    button_2.place(
        x=507.0,
        y=396.0,
        width=281.0,
        height=40.0
    )

    entry_image_1 = PhotoImage(
        file="./assets/frame0/entry_1.png")
    entry_bg_1 = canvas.create_image(
        647.5,
        175.5,
        image=entry_image_1
    )
    entry_1 = Entry(
        bd=0,
        bg="#D9D9D9",
        fg="#000716",
        highlightthickness=0
    )
    entry_1.place(
        x=529.0,
        y=155.0,
        width=237.0,
        height=39.0
    )

    entry_image_2 = PhotoImage(
        file="./assets/frame0/entry_2.png")
    entry_bg_2 = canvas.create_image(
        647.5,
        306.5,
        image=entry_image_2
    )
    entry_2 = Entry(
        bd=0,
        bg="#D9D9D9",
        fg="#000716",
        highlightthickness=0
    )
    entry_2.place(
        x=529.0,
        y=286.0,
        width=237.0,
        height=39.0
    )
    window.resizable(False, False)
    window.mainloop()


def hotels_form():
    def file_choice():
        global name_image
        name = filedialog.askopenfilename()
        img = Image.open(name)
        img = img.resize((275, 375))
        img.save(f"./assets/hotels/{name.split('/')[-1].split('.')[0] + '.png'}", "PNG")
        name_image = f"./assets/hotels/{name.split('/')[-1].split('.')[0] + '.png'}"


    def add():
        if bool(entry_1.get()) and bool(entry_2.get()):
            if entry_2.get().isdigit():
                if ((entry_1.get().capitalize(),) not in cursor.execute('SELECT name FROM hotels', ).fetchall()):
                    try:
                        add_bd_hotels(entry_1.get().capitalize(), name_image,entry_2.get())
                        messagebox.showinfo('Успех', 'Отель создан')
                    except Exception:
                        messagebox.showerror('Ошибка заполнения', 'Выберите изображение')
                else:
                    messagebox.showerror('Ошибка заполнения', 'Такой отель уже есть')
            else:
                messagebox.showerror('Ошибка заполнения', 'Цена не может быть такой')
        else:
            messagebox.showerror('Ошибка заполнения', 'Поля не могут быть пустыми')

    def delete_hotel():
        if bool(cursor.execute('SELECT name FROM hotels WHERE name=?',
                               (entry_1.get().capitalize(),)).fetchall()):
            cursor.execute('DELETE FROM hotels WHERE name = ?', (entry_1.get().capitalize(),))
            connection.commit()
            messagebox.showinfo('Успех', f"Отель {entry_1.get()} успешно удален")
        else:
            messagebox.showerror('Ошибка', 'Такого отеля нет')

    def back():
        window.destroy()
        sign_in_form()

    def inf():
        window.destroy()
        info()

    window = Tk()
    window.geometry("900x600")
    window.configure(bg="#FFFFFF")

    canvas = Canvas(
        window,
        bg="#FFFFFF",
        height=600,
        width=900,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )

    canvas.place(x=0, y=0)
    image_image_1 = PhotoImage(
        file="./assets/frame1/image_1.png")
    image_1 = canvas.create_image(
        450.0,
        300.0,
        image=image_image_1
    )

    canvas.create_rectangle(
        29.0,
        28.0,
        338.0,
        429.0,
        fill="#FFFFFF",
        outline="")

    canvas.create_rectangle(
        25.0,
        469.0,
        334.0,
        538.0,
        fill="#FFFFFF",
        outline="")

    canvas.create_rectangle(
        828.0,
        14.0,
        885.0,
        69.0,
        fill="#FFFFFF",
        outline="")

    button_image_1 = PhotoImage(
        file="./assets/frame1/button_1.png")
    button_1 = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=back,
        relief="flat"
    )
    button_1.place(
        x=835.0,
        y=19.0,
        width=44.99998474121094,
        height=44.0
    )

    canvas.create_rectangle(
        784.0,
        452.0,
        871.0,
        558.0,
        fill="#47624F",
        outline="")

    button_image_2 = PhotoImage(
        file="./assets/frame1/button_2.png")
    button_2 = Button(
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=delete_hotel,
        relief="flat"
    )
    button_2.place(
        x=790.0,
        y=460.0,
        width=76.0,
        height=88.83334350585938
    )
    canvas.create_rectangle(
        784.0,
        332.0,
        871.0,
        438.0,
        fill="#47624F",
        outline="")
    button_image_5 = PhotoImage(
        file="./assets/frame1/button_5.png")
    button_5 = Button(
        image=button_image_5,
        borderwidth=0,
        highlightthickness=0,
        command=inf,
        relief="flat"
    )
    button_5.place(
        x=790.0,
        y=340.0,
        width=76.0,
        height=88.83334350585938
    )
    button_image_3 = PhotoImage(
        file="./assets/frame1/button_3.png")
    button_3 = Button(
        image=button_image_3,
        borderwidth=0,
        highlightthickness=0,
        command=file_choice,
        relief="flat"
    )
    button_3.place(
        x=48.0,
        y=41.0,
        width=275.0,
        height=375.0
    )

    button_image_4 = PhotoImage(
        file="./assets/frame1/button_4.png")
    button_4 = Button(
        image=button_image_4,
        borderwidth=0,
        highlightthickness=0,
        command=add,
        relief="flat"
    )
    button_4.place(
        x=42.0,
        y=477.0,
        width=275.0,
        height=54.0
    )

    entry_image_1 = PhotoImage(
        file="./assets/frame1/entry_1.png")
    entry_bg_1 = canvas.create_image(
        567.0,
        122.0,
        image=entry_image_1
    )
    entry_1 = Entry(
        bd=0,
        bg="#D9D9D9",
        fg="#000716",
        highlightthickness=0
    )
    entry_1.place(
        x=388.0,
        y=95.0,
        width=358.0,
        height=52.0
    )

    entry_image_2 = PhotoImage(
        file="./assets/frame1/entry_2.png")
    entry_bg_2 = canvas.create_image(
        567.0,
        232.0,
        image=entry_image_2
    )
    entry_2 = Entry(
        bd=0,
        bg="#D9D9D9",
        fg="#000716",
        highlightthickness=0
    )
    entry_2.place(
        x=388.0,
        y=205.0,
        width=358.0,
        height=52.0
    )

    canvas.create_text(
        372.0,
        52.0,
        anchor="nw",
        text="Название отеля",
        fill="#213126",
        font=("Inter", 24 * -1)
    )

    canvas.create_text(
        372.0,
        169.0,
        anchor="nw",
        text="Цена",
        fill="#213126",
        font=("Inter", 24 * -1)
    )

    window.resizable(False, False)
    window.mainloop()


def sign_up_form():
    def back():
        window.destroy()
        sign_in_form()

    def click_sign_up():
        r_pass = entry_7.get()
        if not bool(cursor.execute('SELECT * FROM users WHERE login=?', (entry_2.get(),)).fetchall()):
            if (bool(entry_1.get()) and bool(entry_1.get()) and bool(entry_1.get()) and bool(entry_1.get())
                and bool(entry_1.get()) and bool(entry_1.get()) and bool(entry_1.get()) and bool(entry_1.get())):
                if entry_7.get() == entry_3.get():
                    if (entry_8.get()[:2] == '+7'
                            and len(entry_8.get()[2:]) == 10 and entry_8.get()[2:].isdigit()):
                            if (entry_1.get().replace('.', '').isdigit() and len(entry_1.get().split('.')[0]) == 2
                                    and len(entry_1.get().split('.')[1]) == 2 and len(entry_1.get().split('.')[2]) == 4):
                                n = entry_1.get().split('.')
                                add_bd_user(entry_2.get(), generate_password_hash(entry_3.get()), entry_4.get(),
                                            entry_5.get(), entry_6.get(), entry_8.get(), '.'.join([n[0], n[1], n[2]]))
                                add_bd_bron(cursor.execute('SELECT user_id FROM users WHERE login=?',
                                                           (entry_2.get(),)).fetchall()[0][0])
                                messagebox.showinfo('Успех', 'Аккаунт создан')
                            else:
                                messagebox.showerror('Ошибка', 'Некорректная дата рождения')
                    else:
                        messagebox.showerror('Ошибка', 'Некорректный номер телефона')
                else:
                    messagebox.showerror('Ошибка', 'Пароли не совпадают')
            else:
                messagebox.showerror('Ошибка', 'Поля не могут быть пустыми')
        else:
            messagebox.showerror('Ошибка', 'Такой пользователь уже есть попробуйте войти')
    window = Tk()


    window.geometry("900x600")
    window.configure(bg="#FFFFFF")

    canvas = Canvas(
        window,
        bg="#FFFFFF",
        height=600,
        width=900,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )

    canvas.place(x=0, y=0)
    image_image_1 = PhotoImage(
        file="./assets/frame2/image_1.png")
    image_1 = canvas.create_image(
        450.0,
        300.0,
        image=image_image_1
    )

    canvas.create_rectangle(
        419.0,
        18.0,
        881.0,
        569.0,
        fill="#EBFFF1",
        outline="")

    canvas.create_text(
        646.0,
        303.0,
        anchor="nw",
        text="Дата рождения (дд.мм.гггг)",
        fill="#000000",
        font=("Inter Light", 16 * -1)
    )
    button_image_2 = PhotoImage(
        file="./assets/frame2/button_2.png")
    button_2 = Button(
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=back,
        relief="flat"
    )
    button_2.place(
        x=835.0,
        y=19.0,
        width=44.99998474121094,
        height=44.0
    )
    entry_image_1 = PhotoImage(
        file="./assets/frame2/entry_1.png")
    entry_bg_1 = canvas.create_image(
        751.0,
        350.5,
        image=entry_image_1
    )
    entry_1 = Entry(
        bd=0,
        bg="#D9D9D9",
        fg="#000716",
        highlightthickness=0
    )
    entry_1.place(
        x=665.0,
        y=330.0,
        width=172.0,
        height=39.0
    )

    canvas.create_text(
        504.0,
        138.0,
        anchor="nw",
        text="Пароль",
        fill="#000000",
        font=("Inter Light", 16 * -1)
    )

    canvas.create_text(
        513.0,
        60.0,
        anchor="nw",
        text="Логин",
        fill="#000000",
        font=("Inter Light", 16 * -1)
    )

    canvas.create_rectangle(
        0.0,
        0.0,
        392.0,
        600.0,
        fill="#425E4A",
        outline="")

    canvas.create_text(
        35.0,
        90.0,
        anchor="nw",
        text="Отелей",
        fill="#D0D0D0",
        font=("Inter Medium", 40 * -1)
    )

    canvas.create_text(
        35.0,
        42.0,
        anchor="nw",
        text="Бронирование",
        fill="#D0D0D0",
        font=("Inter Medium", 40 * -1)
    )
    canvas.create_text(
        35.0,
        177.0,
        anchor="nw",
        text="Регистрация",
        fill="#D0D0D0",
        font=("Inter Medium", 40 * -1)
    )
    canvas.create_rectangle(
        -3.0,
        156.0,
        391.9995822189594,
        161.0795733911242,
        fill="#FFFFFF",
        outline="")
    canvas.create_text(
        35.0,
        177.0,
        anchor="nw",
        text="Регистрация",
        fill="#D0D0D0",
        font=("Inter Medium", 40 * -1)
    )

    button_image_1 = PhotoImage(
        file="./assets/frame2/button_1.png")
    button_1 = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=click_sign_up,
        relief="flat"
    )
    button_1.place(
        x=505.0,
        y=435.0,
        width=281.0,
        height=40.0
    )

    entry_image_2 = PhotoImage(
        file="./assets/frame2/entry_2.png")
    entry_bg_2 = canvas.create_image(
        540.0,
        106.5,
        image=entry_image_2
    )
    entry_2 = Entry(
        bd=0,
        bg="#D9D9D9",
        fg="#000716",
        highlightthickness=0
    )
    entry_2.place(
        x=454.0,
        y=86.0,
        width=172.0,
        height=39.0
    )

    entry_image_3 = PhotoImage(
        file="./assets/frame2/entry_3.png")
    entry_bg_3 = canvas.create_image(
        539.5,
        184.5,
        image=entry_image_3
    )
    entry_3 = Entry(
        bd=0,
        bg="#D9D9D9",
        fg="#000716",
        highlightthickness=0
    )
    entry_3.place(
        x=456.0,
        y=164.0,
        width=167.0,
        height=39.0
    )

    canvas.create_text(
        708.0,
        140.0,
        anchor="nw",
        text="Фамилия",
        fill="#000000",
        font=("Inter Light", 16 * -1)
    )

    canvas.create_text(
        727.0,
        67.0,
        anchor="nw",
        text="Имя",
        fill="#000000",
        font=("Inter Light", 16 * -1)
    )

    entry_image_4 = PhotoImage(
        file="./assets/frame2/entry_4.png")
    entry_bg_4 = canvas.create_image(
        746.0,
        106.5,
        image=entry_image_4
    )
    entry_4 = Entry(
        bd=0,
        bg="#D9D9D9",
        fg="#000716",
        highlightthickness=0
    )
    entry_4.place(
        x=660.0,
        y=86.0,
        width=172.0,
        height=39.0
    )

    entry_image_5 = PhotoImage(
        file="./assets/frame2/entry_5.png")
    entry_bg_5 = canvas.create_image(
        745.5,
        184.5,
        image=entry_image_5
    )
    entry_5 = Entry(
        bd=0,
        bg="#D9D9D9",
        fg="#000716",
        highlightthickness=0
    )
    entry_5.place(
        x=662.0,
        y=164.0,
        width=167.0,
        height=39.0
    )

    canvas.create_text(
        706.0,
        216.0,
        anchor="nw",
        text="Отчество",
        fill="#000000",
        font=("Inter Light", 16 * -1)
    )

    entry_image_6 = PhotoImage(
        file="./assets/frame2/entry_6.png")
    entry_bg_6 = canvas.create_image(
        743.5,
        260.5,
        image=entry_image_6
    )
    entry_6 = Entry(
        bd=0,
        bg="#D9D9D9",
        fg="#000716",
        highlightthickness=0
    )
    entry_6.place(
        x=660.0,
        y=240.0,
        width=167.0,
        height=39.0
    )

    canvas.create_text(
        465.0,
        216.0,
        anchor="nw",
        text="Повторите пароль",
        fill="#000000",
        font=("Inter Light", 16 * -1)
    )

    entry_image_7 = PhotoImage(
        file="./assets/frame2/entry_7.png")
    entry_bg_7 = canvas.create_image(
        537.5,
        261.5,
        image=entry_image_7
    )
    entry_7 = Entry(
        bd=0,
        bg="#D9D9D9",
        fg="#000716",
        highlightthickness=0
    )
    entry_7.place(
        x=454.0,
        y=241.0,
        width=167.0,
        height=39.0
    )

    canvas.create_text(
        476.0,
        299.0,
        anchor="nw",
        text="Номер телефона",
        fill="#000000",
        font=("Inter Light", 16 * -1)
    )

    entry_image_8 = PhotoImage(
        file="./assets/frame2/entry_8.png")
    entry_bg_8 = canvas.create_image(
        540.0,
        350.5,
        image=entry_image_8
    )
    entry_8 = Entry(
        bd=0,
        bg="#D9D9D9",
        fg="#000716",
        highlightthickness=0
    )
    entry_8.place(
        x=454.0,
        y=330.0,
        width=172.0,
        height=39.0
    )

    canvas.create_rectangle(
        -3.0,
        156.0,
        391.9995822189594,
        161.0795733911242,
        fill="#FFFFFF",
        outline="")
    window.resizable(False, False)
    window.mainloop()


def hotel_page(name, name_hotel, ind, price, data_in='111', data_out='111'):
    def price_cahge_stand():
        ind = 1
        window.destroy()
        hotel_page(name, name_hotel, ind, price, data_in, data_out)

    def price_cahge_prem():
        ind = 1.4
        window.destroy()
        hotel_page(name, name_hotel, ind, price, data_in, data_out)

    def price_cahge_luks():
        ind = 1.8
        window.destroy()
        hotel_page(name, name_hotel, ind, price, data_in, data_out)

    def mat():
        c_1 = calend_v.get_date().split('/')
        c_2 = calend_vi.get_date().split('/')
        d = (datetime.datetime(int('20' + c_2[2]), int(c_2[0]), int(c_2[1]))
             - datetime.datetime(int('20' + c_1[2]), int(c_1[0]), int(c_1[1]))).days
        if d == abs(d):
            colvo_days = d
            window.destroy()
            hotel_page(name, name_hotel, ind,
                       int(cursor.execute("SELECT price FROM hotels WHERE name=?",
                                          (name_hotel,)).fetchall()[0][0]) * colvo_days,
                       '.'.join(c_1), '.'.join(c_2))
        else:
            messagebox.showerror('Ошибка', 'Некоректная дата')

    def back():
        window.destroy()
        main_page(cursor.execute("SELECT login FROM users WHERE user_id=?", (name,)).fetchall()[0][0])

    def bron():
        if (cursor.execute("SELECT hotel_id FROM bron WHERE user_id=?",
            (name,)).fetchall()[0][0] == None or
                cursor.execute("SELECT hotel_id FROM bron WHERE user_id=?",
            (name,)).fetchall()[0][0] == ''):
            if data_in != '111':
                if ind == 1:
                    s = 'Стандарт'
                elif ind == 1.4:
                    s = 'Премиум'
                elif ind == 1.8:
                    s = 'Люкс'
                cursor.execute('UPDATE bron SET hotel_id=?,'
                               ' date_in=?, price=?, date_out=?, type=? WHERE user_id=?',
                                   (cursor.execute("SELECT hotel_id FROM hotels WHERE name=?",
                                                   (name_hotel,)).fetchall()[0][0], data_in,
                                    str(round(int(price) * ind)), data_out, s, name,)).fetchall()
                connection.commit()
                messagebox.showinfo('Успех', 'Отель забронирован')
            else:
                messagebox.showerror('Ошибка', 'Даты не выбраны и не подсчитаны')
        else:
            messagebox.showerror('Ошибка', 'Вы уже забронировали отель')



    window = Tk()
    window.geometry("900x600")
    window.configure(bg="#FFFFFF")

    canvas = Canvas(
        window,
        bg="#FFFFFF",
        height=600,
        width=900,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )

    canvas.place(x=0, y=0)
    canvas.create_rectangle(
        0.0,
        0.0,
        900.0,
        600.0,
        fill="#729D7F",
        outline="")
    try:
        image_image_1 = PhotoImage(
            file=cursor.execute("SELECT png FROM hotels WHERE name=?", (name_hotel,)).fetchall()[0])
        image_1 = canvas.create_image(
            179.0,
            220.0,
            image=image_image_1
        )

    except Exception:
        image_image_1 = PhotoImage(
            file="./assets/frame4/image_1.png")
        image_1 = canvas.create_image(
            179.0,
            220.0,
            image=image_image_1
        )

    canvas.create_text(
        360.0,
        33.0,
        anchor="nw",
        text=cursor.execute("SELECT name FROM hotels WHERE name=?", (name_hotel,)).fetchall()[0][0],
        fill="#213126",
        font=("Inter", 40 * -1)
    )

    canvas.create_text(
        358.0,
        158.0,
        anchor="nw",
        text=(str(round(int(cursor.execute("SELECT price FROM hotels WHERE name=?",
                                           (name_hotel,)).fetchall()[0][0]) * ind))) + "₽ в день",
        fill="#213126",
        font=("Inter", 40 * -1)
    )
    calend_v = Calendar(window, selectmode='day')
    calend_v.place(
        width=240,
        height=230,
        x=360,
        y=270
    )
    calend_vi = Calendar(window, selectmode='day')
    calend_vi.place(
        width=240,
        height=230,
        x=620,
        y=270
    )
    canvas.create_text(
        358.0,
        234.0,
        anchor="nw",
        text="Дата въезда",
        fill="#213126",
        font=("Inter", 24 * -1)
    )

    canvas.create_text(
        621.0,
        234.0,
        anchor="nw",
        text="Дата выезда",
        fill="#213126",
        font=("Inter", 24 * -1)
    )

    canvas.create_rectangle(
        358.0,
        96.0,
        527.0,
        141.0,
        fill="#FFFFFF",
        outline="")

    button_image_1 = PhotoImage(
        file="./assets/frame4/button_1.png")
    button_1 = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=price_cahge_stand,
        relief="flat"
    )
    button_1.place(
        x=360.0,
        y=98.0,
        width=165.0,
        height=41.0
    )

    canvas.create_rectangle(
        536.0,
        96.0,
        705.0,
        141.0,
        fill="#FFFFFF",
        outline="")

    button_image_2 = PhotoImage(
        file="./assets/frame4/button_2.png")
    button_2 = Button(
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=price_cahge_prem,
        relief="flat"
    )
    button_2.place(
        x=538.0,
        y=98.0,
        width=165.0,
        height=41.0
    )

    canvas.create_rectangle(
        714.0,
        96.0,
        883.0,
        141.0,
        fill="#FFFFFF",
        outline="")

    button_image_3 = PhotoImage(
        file="./assets/frame4/button_3.png")
    button_3 = Button(
        image=button_image_3,
        borderwidth=0,
        highlightthickness=0,
        command=price_cahge_luks,
        relief="flat"
    )
    button_3.place(
        x=716.0,
        y=98.0,
        width=165.0,
        height=41.0
    )

    canvas.create_text(
        360.0,
        520.0,
        anchor="nw",
        text="Итого:",
        fill="#213126",
        font=("Inter", 40 * -1)
    )

    canvas.create_rectangle(
        40.0,
        499.0,
        313.0,
        544.0,
        fill="#FFFFFF",
        outline="")

    button_image_4 = PhotoImage(
        file="./assets/frame4/button_4.png")
    button_4 = Button(
        image=button_image_4,
        borderwidth=0,
        highlightthickness=0,
        command=bron,
        relief="flat"
    )
    button_4.place(
        x=43.23077392578125,
        y=501.0,
        width=266.5384826660156,
        height=41.0
    )
    canvas.create_text(
        509.0,
        520.0,
        anchor="nw",
        text=str(round(int(price) * ind)),
        fill="#213126",
        font=("Inter", 40 * -1)
    )

    canvas.create_rectangle(
        43.0,
        434.0,
        316.0,
        479.0,
        fill="#FFFFFF",
        outline="")

    button_image_5 = PhotoImage(
        file="./assets/frame4/button_5.png")
    button_5 = Button(
        image=button_image_5,
        borderwidth=0,
        highlightthickness=0,
        command=mat,
        relief="flat"
    )
    button_5.place(
        x=46.23077392578125,
        y=436.0,
        width=266.5384826660156,
        height=41.0
    )

    canvas.create_rectangle(
        835.0,
        27.0,
        877.0,
        69.0,
        fill="#FFFFFF",
        outline="")

    button_image_6 = PhotoImage(
        file="./assets/frame4/button_6.png")
    button_6 = Button(
        image=button_image_6,
        borderwidth=0,
        highlightthickness=0,
        command=back,
        relief="flat"
    )
    button_6.place(
        x=836.0,
        y=28.0,
        width=40.40826416015625,
        height=40.0
    )

    canvas.create_rectangle(
        334.0,
        225.0,
        900.0,
        228.0,
        fill="#FFFFFF",
        outline="")

    canvas.create_rectangle(
        333.0,
        -3.0,
        337.00000005138224,
        600.0000319469182,
        fill="#FFFFFF",
        outline="")
    window.resizable(False, False)
    window.mainloop()


def us_page(id):
    def delit():
        cursor.execute('UPDATE bron SET hotel_id=?,'
                       ' date_in=?, price=?, date_out=?, type=? WHERE user_id=?',
                       ('', '', '', '', '', id,)).fetchall()
        connection.commit()
        messagebox.showinfo('Успех', 'бронь отменена')
        window.destroy()
        us_page(id)
    def back():
        window.destroy()
        main_page(cursor.execute('SELECT login FROM users WHERE user_id=?', (id,)).fetchall()[0][0])
    window = Tk()

    window.geometry("900x600")
    window.configure(bg="#FFFFFF")

    canvas = Canvas(
        window,
        bg="#FFFFFF",
        height=600,
        width=900,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )

    canvas.place(x=0, y=0)
    canvas.create_rectangle(
        0.0,
        0.0,
        900.0,
        600.0,
        fill="#729D7F",
        outline="")

    canvas.create_text(
        437.0,
        209.0,
        anchor="nw",
        text="Номер",
        fill="#FFFFFF",
        font=("Inter", 30 * -1)
    )
    canvas.create_text(
        435.0,
        41.0,
        anchor="nw",
        text="Имя:",
        fill="#FFFFFF",
        font=("Inter", 30 * -1)
    )
    canvas.create_rectangle(
        835.0,
        27.0,
        877.0,
        69.0,
        fill="#FFFFFF",
        outline="")

    button_image_2 = PhotoImage(
        file="./assets/frame5/button_2.png")
    button_2 = Button(
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=back,
        relief="flat"
    )
    button_2.place(
        x=836.0,
        y=28.0,
        width=40.40826416015625,
        height=40.0
    )
    canvas.create_text(
        518.0,
        41.0,
        anchor="nw",
        text=cursor.execute("SELECT name FROM users WHERE user_id=?", (id,)).fetchall()[0],
        fill="#FFFFFF",
        font=("Inter", 30 * -1)
    )

    canvas.create_text(
        437.0,
        239.0,
        anchor="nw",
        text="телефона:",
        fill="#FFFFFF",
        font=("Inter", 30 * -1)
    )

    canvas.create_rectangle(
        0.0,
        0.0,
        400.0,
        600.0,
        fill="#47624F",
        outline="")

    canvas.create_text(
        26.0,
        80.0,
        anchor="nw",
        text=cursor.execute('SELECT login FROM users WHERE user_id=?', (id,)).fetchall()[0][0],
        fill="#FFFFFF",
        font=("Inter", 40 * -1)
    )

    canvas.create_text(
        26.0,
        227.0,
        anchor="nw",
        text="Страница",
        fill="#FFFFFF",
        font=("Inter", 40 * -1)
    )

    canvas.create_text(
        26.0,
        276.0,
        anchor="nw",
        text="Пользователя",
        fill="#FFFFFF",
        font=("Inter", 40 * -1)
    )

    canvas.create_rectangle(
        -3.0,
        191.0,
        400.0000114402137,
        195.00000003232583,
        fill="#FFFFFF",
        outline="")

    canvas.create_text(
        435.0,
        99.0,
        anchor="nw",
        text="Фамилия:",
        fill="#FFFFFF",
        font=("Inter", 30 * -1)
    )

    canvas.create_text(
        586.0,
        99.0,
        anchor="nw",
        text=cursor.execute("SELECT surname FROM users WHERE user_id=?", (id,)).fetchall()[0],
        fill="#FFFFFF",
        font=("Inter", 30 * -1)
    )

    canvas.create_text(
        436.0,
        159.0,
        anchor="nw",
        text="Отчество:",
        fill="#FFFFFF",
        font=("Inter", 30 * -1)
    )

    canvas.create_text(
        591.0,
        159.0,
        anchor="nw",
        text=cursor.execute("SELECT patronymic FROM users WHERE user_id=?", (id,)).fetchall()[0],
        fill="#FFFFFF",
        font=("Inter", 30 * -1)
    )

    canvas.create_text(
        604.0,
        240.0,
        anchor="nw",
        text=cursor.execute("SELECT number FROM users WHERE user_id=?", (id,)).fetchall()[0],
        fill="#FFFFFF",
        font=("Inter", 30 * -1)
    )
    if cursor.execute("SELECT hotel_id FROM bron WHERE user_id=?",(id,)).fetchall()[0][0] != None\
    and cursor.execute("SELECT hotel_id FROM bron WHERE user_id=?",(id,)).fetchall()[0][0] != '':
        canvas.create_text(
            435.0,
            397.0,
            anchor="nw",
            text="Дата въезда:",
            fill="#FFFFFF",
            font=("Inter", 30 * -1)
        )

        canvas.create_text(
            436.0,
            433.0,
            anchor="nw",
            text=cursor.execute("SELECT date_in FROM bron WHERE user_id=?", (id,)).fetchall()[0],
            fill="#FFFFFF",
            font=("Inter", 30 * -1)
        )

        canvas.create_text(
            646.0,
            397.0,
            anchor="nw",
            text="Дата выезда:",
            fill="#FFFFFF",
            font=("Inter", 30 * -1)
        )

        canvas.create_text(
            651.0,
            433.0,
            anchor="nw",
            text=cursor.execute("SELECT date_out FROM bron WHERE user_id=?", (id,)).fetchall()[0],
            fill="#FFFFFF",
            font=("Inter", 30 * -1)
        )

        canvas.create_text(
            437.0,
            300.0,
            anchor="nw",
            text="Забронированный",
            fill="#FFFFFF",
            font=("Inter", 30 * -1)
        )

        canvas.create_text(
            440.0,
            336.0,
            anchor="nw",
            text="отель:",
            fill="#FFFFFF",
            font=("Inter", 30 * -1)
        )
        s = cursor.execute("SELECT hotel_id FROM bron WHERE user_id=?", (id,)).fetchall()[0][0]
        canvas.create_text(
            548.0,
            336.0,
            anchor="nw",
            text=cursor.execute("SELECT name FROM hotels WHERE hotel_id=?", (s,)).fetchall()[0][0],
            fill="#FFFFFF",
            font=("Inter", 30 * -1)
        )
        canvas.create_rectangle(
            401.0,
            559.0,
            900.0,
            600.0,
            fill="#D9D9D9",
            outline="")

        button_image_1 = PhotoImage(
            file="./assets/frame5/button_1.png")
        button_1 = Button(
            image=button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=delit,
            relief="flat"
        )
        button_1.place(
            x=403.0,
            y=561.0,
            width=495.0,
            height=37.0
        )
    else:
        canvas.create_text(
            437.0,
            300.0,
            anchor="nw",
            text="Отель не забронирован",
            fill="#FFFFFF",
            font=("Inter", 30 * -1)
        )
    window.resizable(False, False)
    window.mainloop()


def info():
    window = Tk()
    window.geometry("900x600")
    window.configure(bg="#FFFFFF")

    def back():
        window.destroy()
        hotels_form()

    canvas = Canvas(
        window,
        bg="#FFFFFF",
        height=600,
        width=900,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )

    canvas.place(x=0, y=0)
    canvas.create_rectangle(
        0.0,
        0.0,
        900.0,
        600.0,
        fill="#729D7F",
        outline="")

    canvas.create_rectangle(
        0.0,
        0.0,
        900.0,
        80.0,
        fill="#47624F",
        outline="")

    canvas.create_rectangle(
        842.0,
        19.0,
        884.0,
        61.0,
        fill="#FFFFFF",
        outline="")

    button_image_1 = PhotoImage(
        file="./assets/frame6/button_1.png")
    button_1 = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=back,
        relief="flat"
    )
    button_1.place(
        x=843.0,
        y=20.0,
        width=40.40826416015625,
        height=40.0
    )

    canvas.create_text(
        46.0,
        20.0,
        anchor="nw",
        text="Информация",
        fill="#FFFFFF",
        font=("Inter", 30 * -1)
    )

    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()

    columns = ('Логин', 'Имя', 'Фамилия', 'Отчество', 'Номер', 'Дата рождения')
    tree = ttk.Treeview(window, columns=columns, show='headings')

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=150, anchor='center')

    for row in rows:
        tree.insert('', 'end', values=(row[1], row[3], row[4], row[5], row[6], row[7]))

    tree.place(x=0, y=80, width=900, height=520)

    window.resizable(False, False)
    window.mainloop()

def main():
    sign_in_form()


if __name__ == '__main__':
    create_tables()
    main()
