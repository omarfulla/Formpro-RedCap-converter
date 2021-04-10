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
    tree.delete(*tree.get_children())

def csv_frame(main, titel, data_frame, loc):
    #creat frame
    csv_frame = LabelFrame(main, text = titel)
    csv_frame.pack(side= loc, expand = "yes", padx=50, pady=50)
    # The first column of table is not displayed -> headings
    trv = ttk.Treeview(csv_frame,  show="headings")
    #Set The Header of the columns
    trv["column"] = list(data_frame.columns)
    #to remove the empty column which is the identifier
    #trv["show"] = "headings"
    for column in trv["column"]:
        trv.heading(column, text=column)
        # should be set for the x scrollbar
        trv.column(column, width=100, minwidth=100, stretch=False)
    data_frame_rows = data_frame.to_numpy().tolist()
    for row in data_frame_rows:
        trv.insert("","end",values=row)
    # Vertical Scrollbar
    yscrollbar = Scrollbar(csv_frame, orient=VERTICAL, command=trv.yview)
    yscrollbar.pack(side=RIGHT, fill=Y)
    #trv.configure(yscrollcommand=yscrollbar.set)
    # Horizontal Scrollbar
    xscrollbar = Scrollbar(csv_frame, orient=HORIZONTAL, command=trv.xview)
    xscrollbar.pack(side=BOTTOM, fill=X)
    #trv.configure(xscrollcommand=xscrollbar.set)
    trv.configure(xscrollcommand=xscrollbar.set, yscrollcommand=yscrollbar.set)
    trv.pack()
def save_as(dataframe):
    a = text.get()
    file = asksaveasfile(defaultextension=".csv")
    write_to_csv(data, r"C:\Users\Omar\Documents\New Exports\test.csv")

dictionary = pd.read_csv(r"C:\Users\Omar\Downloads\DataDictionary.csv", index_col =0, skiprows=0)
data = pd.read_csv(r"C:\Users\Omar\Documents\New Exports\test.csv", sep=';')
main = Tk()
main.title("Prince Converter")
main.geometry("1200x900")
main.resizable(False, False)
#main.getvar()
#main.iconbitmap()
code_book_tree = ttk.Treeview(main)
export_file_tree = ttk.Treeview(main)
open_bt = Button(main, text="Select Code Book.csv", padx=50, pady=20, command=open_code_book).pack()
open_bt_2 = Button(main, text="Open FormPro_export.csv", padx=50, pady=20, command=open_export_file).pack()
logo = ImageTk.PhotoImage(Image.open('logo.png'))
logo_label = Label(image=logo)
logo_label.pack()
csv_frame(main, 'dictionary', dictionary, BOTTOM)
csv_frame(main, 'Data', data, TOP)
main.mainloop()


