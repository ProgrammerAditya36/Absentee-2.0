import tkinter as tk
from tkinter import filedialog
import pandas as pd
import xlwt
import datetime
import os
import subprocess

folder = str(os.getcwd())
main_list = []
absent_check_dictionary = {}
absentee_dictionary = {}
time_of_class = 60
font = ("Gadugi", 20)
today = datetime.datetime.now().strftime("%d-%m-%Y")


def time_calculate(time_string):
    time_string = time_string[:-2]
    time_list = str(time_string).split(":")
    time = int(time_list[0]) * 3600 + int(time_list[1]) * 60 + int("00" + time_list[2])
    return time


def print_to_excel(data):
    workbook = xlwt.Workbook()
    worksheet = workbook.add_sheet("Absentees")
    column = 0
    for date in data:
        worksheet.write(0, column, date)
        row = 1
        for student in data[date]:
            worksheet.write(row, column, student)
            row += 1
        column += 1
    workbook.save(f"{today}_absentees.xls")
    label_success.grid(row=13, column=0, columnspan=2, sticky="nsew")
    file_output.grid(row=14, column=0, sticky="nsew", columnspan=3)


def open_file(file_path):
    subprocess.call(f"explorer {file_path}", shell=True)


def entry():
    main_dictionary = absent_check_dictionary
    for d in main_dictionary:
        absentees = []
        date = main_dictionary[d]['date']
        joined_list = main_dictionary[d]['joined_list']
        left_list = main_dictionary[d]['left_list']
        absentee_check_list = main_dictionary[d]['absentee_check_list']
        for i in range(0, len(joined_list)):
            join_time = time_calculate(joined_list[i])
            leave_time = time_calculate(left_list[i])
            if leave_time - join_time < time_of_class / 2:
                absentees.append(absentee_check_list[i])
        for student in main_list:
            if student not in absentee_check_list:
                absentees.append(student)
        absentee_dictionary.update({date: absentees})
    print_to_excel(absentee_dictionary)


def file_open(query, row, column, column_span=1):
    global main_list
    file = str(filedialog.askopenfilename(title="Select File", filetypes=(("csv", "*.csv"), ("All Files", "*.*"))))
    text = file.split("/")[-1]
    label = tk.Label(text=text, height=2, relief=tk.GROOVE, font=font)
    label.grid(sticky="nsew", row=row, column=column, columnspan=column_span)
    try:
        csv_extract = pd.read_csv(file)
        data_names = list(csv_extract['Full Name'])
    except KeyError:
        csv_extract = pd.read_csv(file, encoding="utf-16", sep="\t")
        data_names = list(csv_extract['Full Name'])
    if "main" not in str(query).lower():
        joined_list = []
        left_list = []
        absentee_check_list = []
        data_user_action = list(csv_extract['User Action'])
        data_time = list(csv_extract['Timestamp'])
        for i in range(len(data_names)):
            s = i
            if s + 1 > len(data_names) - 1:
                s = -1
            student = data_names
            student_time_stamp = str(data_time[i])
            student_time = student_time_stamp[student_time_stamp.find(",") + 2:]
            if data_user_action[i] != "Left" and student[i] != student[i - 1]:
                joined_list.append(student_time)
            if data_user_action[s] != "Left" and student[i] != student[s + 1] and data_user_action[s + 1] != "Left":
                left_list.append("100:100:100")
            elif data_user_action[i] == "Left" and data_user_action[i - 1] != "Left" and student[s] != student[s + 1]:
                left_list.append(student_time)
            if student[i] != student[i - 1]:
                absentee_check_list.append(student[i])
        date_time = str(csv_extract["Timestamp"][0])
        date = date_time[:date_time.find(",")]
        absent_check_dictionary.update(
            {date: {
                "date": date,
                "absentee_check_list": absentee_check_list,
                "joined_list": joined_list,
                "left_list": left_list}}
        )
    elif "main" in str(query).lower():
        data_names = list(set(data_names))
        main_list = data_names
    else:
        print("Error In Recognizing the File Please Try Again")


class Body:
    def __init__(self):
        self.button = None

    def button_create(self, text, row, column, column_span=1, enter=False):
        if enter:
            self.button = tk.Button(text=text, command=lambda: entry(), font=font)
        else:
            self.button = tk.Button(text=text, font=font, command=lambda: file_open(text, row, column, column_span))
            if self.button['state'] == tk.ACTIVE:
                self.button['relief'] = tk.FLAT
        self.button.grid(sticky="nsew", row=row, column=column, columnspan=column_span)


body = Body()
root = tk.Tk()
root.title("Detailed Absentee Generator")


def number_of_files_entry():
    row = 2
    enter_number_of_files.destroy()
    for file in range(int(number_of_files.get())):
        body.button_create(f"Choose File {file + 1}", row, 0, 3)
        row += 1
    body.button_create("Enter", row + 1, 0, 3, True)


body.button_create("Choose Main File", 0, 0, 3)
label_number_of_files = tk.Label(text="Choose The Number Of Files:- ", font=font)
number_of_files = tk.StringVar()
number_of_files.set(1)
number_of_files_option_menu = tk.OptionMenu(root, number_of_files, *range(1, 11))
number_of_files_option_menu.config(font=font)

label_number_of_files.grid(sticky="nsew", row=1, column=0)
number_of_files_option_menu.grid(sticky="nsew", row=1, column=1)
enter_number_of_files = tk.Button(text="Enter", command=number_of_files_entry, font=font)
enter_number_of_files.grid(sticky="nsew", row=1, column=2)
label_success = tk.Label(text="Absentee File Generated Successfully", font=font)
files = folder + f"\\{today}_absentees.xls"
file_output = tk.Button(text="Open The Absentee File", command=lambda: open_file(files), font=font)
root.mainloop()
