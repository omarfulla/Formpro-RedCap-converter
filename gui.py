from tkinter import *
from tkinter import messagebox, filedialog, ttk
import pandas as pd
from PIL import ImageTk, Image


def open_code_book():
    global code_book_df
    file_name = filedialog.askopenfilename(
        initialdir = 'C:/',
        title = 'Open A csv File',
        filetype = (('CSV File', '*.csv'),('All Files', '*.*'))
    )
    if file_name:
        try:
            file_name = r'{}'.format(file_name)
            code_book_df = pd.read_csv(file_name, sep=';')
        except ValueError:
            error_label.config(text="File Couln't be open")
        except FileNotFoundError:
            error_label.config(text="File Couln't be found")

def open_export_file():
    global export_df
    file_name = filedialog.askopenfilename(
        initialdir = 'C:/',
        title = 'Open A csv File',
        filetype = (('CSV File', '*.csv'),('All Files', '*.*'))
    )
    if file_name:
        try:
            file_name = r'{}'.format(file_name)
            export_df = pd.read_csv(file_name, sep=';')
        except ValueError:
            error_label.config(text="File Couln't be open")
        except FileNotFoundError:
            error_label.config(text="File Couln't be found")

def clear_tree(tree):
    my_tree.delete(*my_tree.get_children())

def csv_frame(main , titel, data_frame):
    #creat frame
    frame = Frame(main, width=600, height=300)
    frame_scroll = Scrollbar(frame)
    label = Label(frame, text=titel)
    tree = ttk.Treeview(main)
    tree["column"] = list(data_frame.columns)
    tree["show"] = "headings"
    for column in tree["column"]:
        tree.heading(column, text=column)
    data_frame_rows = data_frame.to_numpy().tolist()
    for row in data_frame_rows:
        tree.insert("","end",values=row)
    tree.pack()
    frame_scroll.pack(side = BOTTOM, fill = BOTH)
    frame_scroll.pack(side=BOTTOM)
def save_as(dataframe):
    a = text.get()
    file = asksaveasfile(defaultextension=".csv")
    write_to_csv(data, r"C:\Users\Omar\Documents\New Exports\test.csv")

dictionary = pd.read_csv(r"C:\Users\Omar\Downloads\DataDictionary.csv", index_col =0, skiprows=0)
data = pd.read_csv(r"C:\Users\Omar\Documents\New Exports\Z2_V_042017_DataBase.csv", sep=';')
main = Tk()
main.title("Prince Converter")
#main.iconbitmap()
code_book_tree = ttk.Treeview(main)
export_file_tree = ttk.Treeview(main)
open_bt = Button(main, text="Select Code Book.csv", padx=50, pady=20, command=open_code_book).pack()
open_bt_2 = Button(main, text="Open FormPro_export.csv", padx=50, pady=20, command=open_export_file).pack()
logo = ImageTk.PhotoImage(Image.open('logo.png'))
logo_label = Label(image=logo)
logo_label.pack()
csv_frame(main, 'Dictionary', dictionary)
csv_frame(main, 'Data', dictionary)
main.mainloop()


