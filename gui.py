from tkinter import *
from tkinter import messagebox, filedialog, ttk
import pandas as pd
from PIL import ImageTk, Image



   #bt.add_command(label="Open",command=open_file())
   #self.close_button.pack()
def open_file():
    file_name = filedialog.askopenfilename(
        initialdir = 'C:/',
        title = 'Open A csv File',
        filetype = (('CSV File', '*.csv'),('All Files', '*.*'))
    )
    if file_name:
        try:
            file_name = r'{}'.format(file_name)
            data = pd.read_csv(file_name, sep=';')
        except ValueError:
            error_label.config(text="File Couln't be open")
        except FileNotFoundError:
            error_label.config(text="File Couln't be found")

def clear_tree(tree):
    my_tree.delete(*my_tree.get_children())

def show_tree(tree, data_frame):
    tree["column"] = list(data_frame.columns)
    tree["show"] = "headings"
    for column in tree["column"]:
        tree.heading(column, text=column)
    data_frame_rows = data_frame.to_numpy().tolist()
    for row in data_frame_rows:
        tree.insert("","end",values=row)
    tree.pack()

def csv_frame(main , txt):
    #creat frame
    frame = Frame(main, width=600, height=300)
    label = Label(frame, text=txt)
    frame.pack(side=BOTTOM)
def save_as(self, dataframe):
    a = text.get()
    file = asksaveasfile(defaultextension=".csv")
    write_to_csv(data, r"C:\Users\Omar\Documents\New Exports\test.csv")


main = Tk()
main.title("Prince Converter")
#main.iconbitmap()
open_bt = Button(main, text="Select Code Book.csv", padx=50, pady=20, command=open_file)
open_bt_2 = Button(main, text="Open FormPro_export.csv", padx=50, pady=20, command=open_file)
open_bt.pack()
open_bt_2.pack()
logo = ImageTk.PhotoImage(Image.open('logo.png'))
logo_label = Label(image=logo)
logo_label.pack()
new_frame = csv_frame(main, "old Data")
main.mainloop()


