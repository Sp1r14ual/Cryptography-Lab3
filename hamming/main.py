from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showerror, showwarning, showinfo

import hamming


def click_button():
    text_filename = text_entry.get()
    text_file = None
    text = None

    try:
        if not (".txt" in text_filename):
            raise FileExistsError("Некорректное имя файла")

        try:
            text_file = open(text_filename, "r")
        except:
            raise FileNotFoundError("Не удалось открыть файл")

        try:
            text = text_file.read().split()
        except:
            raise ValueError("Некорректные входные данные")

    except Exception as E:
        showerror("Ошибка", str(E))
        return

    mode = CryptMode.get()

    try:
        hamming.start(text, mode)
    except Exception as E:
        showerror("Ошибка", "В ходе исполнения алгоритма произошла ошибка")
        print(str(E))
        return

    showinfo("Выполнено", "Результат работы программы записан в файл output.txt")

    return


root = Tk()
root.title("Hamming Codes")
root.geometry("400x400+200+150")

root.resizable(False, False)

text_label = ttk.Label(text="Файл с последовательностью", font=("Arial", 14))
text_label.pack(pady=10)

text_entry = ttk.Entry(justify=CENTER)
text_entry.pack()

CryptMode = StringVar(value="E")

EncodeOption = ttk.Radiobutton(
    text="Закодировать", value="E", variable=CryptMode)
EncodeOption.pack(ipady=5)

DecodeOption = ttk.Radiobutton(
    text="Декодировать", value="D", variable=CryptMode)
DecodeOption.pack()

btn = ttk.Button(text="Пуск", command=click_button)
btn.pack(pady=10)

root.mainloop()
