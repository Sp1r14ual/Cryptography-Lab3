from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showerror, showwarning, showinfo

import shannon


def click_button():
    alphabet_filename = alphabet_entry.get()
    probabilities_filename = probabilities_entry.get()
    text_filename = text_entry.get()

    alphabet_file = None
    probabilities_file = None
    text_file = None

    alphabet = None
    probabilities = None
    text = None

    try:
        if not (".txt" in alphabet_filename or ".txt" in probabilities_filename or ".txt" in text_filename):
            raise FileExistsError("Некорректное имя файла")

        try:
            alphabet_file = open(alphabet_filename, "r")
            probabilities_file = open(probabilities_filename, "r")
            text_file = open(text_filename, "r")
        except:
            raise FileNotFoundError("Не удалось открыть файл")

        try:
            alphabet = tuple(map(str, alphabet_file.read().split()))
            probabilities = tuple(
                map(float, probabilities_file.read().split()))
            text = tuple(map(str, text_file.read().split()))
        except:
            raise ValueError("Некорректные данные")

    except Exception as E:
        showerror("Ошибка", str(E))
        return

    mode = cryptMode.get()
    try:
        shannon.start(alphabet, probabilities, text, mode)
    except:
        showerror("Ошибка", "В ходе исполнения алгоритма произошла ошибка")
        return

    showinfo("Выполнено", "Результат работы программы записан в файл output.txt")

    return


root = Tk()
root.title("Shannon Codes")
root.geometry("400x400+200+150")

root.resizable(False, False)

alphabet_label = ttk.Label(text="Файл с алфавитом", font=("Arial", 14))
alphabet_label.pack(pady=10)

alphabet_entry = ttk.Entry(justify=CENTER)
alphabet_entry.pack()

probabilities_label = ttk.Label(
    text="Файл с вероятностями", font=("Arial", 14))
probabilities_label.pack(padx=8, pady=10)

probabilities_entry = ttk.Entry(justify=CENTER)
probabilities_entry.pack()

text_label = ttk.Label(
    text="Файл с последовательностью символов", font=("Arial", 14))
text_label.pack(padx=8, pady=10)

text_entry = ttk.Entry(justify=CENTER)
text_entry.pack()

cryptMode = StringVar(value="E")

encodeOption = ttk.Radiobutton(
    text="Закодировать", value="E", variable=cryptMode)
encodeOption.pack(ipady=5)

decodeOption = ttk.Radiobutton(
    text="Декодировать", value="D", variable=cryptMode)
decodeOption.pack()

btn = ttk.Button(text="Пуск", command=click_button)
btn.pack(pady=10)

root.mainloop()
