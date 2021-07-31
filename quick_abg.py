import tkinter as tk
from tkinter import filedialog
import pandas as pd


main_list = []
absent_check_dictionary = {}
absentee_list = []
time_of_class = 60
font = ("Gadugi", 20)
output_font = ("Gadugi", 14)


def time_calculate(time_string):
    time_string = time_string[:-2]
    time_list = str(time_string).split(":")
    time = int(time_list[0]) * 3600 + int(time_list[1]) * 60 + int("00" + time_list[2])
    return time


def print_to_window(data):
    print(data)
    body.button_destroy()
    column = 0
    row = 5
    total_absentees = tk.Label(text=f"Total Absentees :- {len(data)}", font=font)
    total_absentees.grid(row=row, column=column)
    for student in data:
        student_label = tk.Label(text=student, font=output_font)
        row += 1
        if row >= 20:
            row = 6
            column += 1
        student_label.grid(row=row, column=column)


def entry():
    main_dictionary = absent_check_dictionary
    absentees = []
    for d in main_dictionary:
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
    print_to_window(absentees)


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

    def button_destroy(self):
        self.button.destroy()


if __name__ == '__main__':
    body = Body()
    root = tk.Tk()
    root.title("Quick Absentee Generator")

    def number_of_files_entry():
        body.button_create(f"Choose The Absentee File", 1, 0, 3)
        body.button_create("Enter", 2 + 1, 0, 3, True)


    body.button_create("Choose Main File", 0, 0, 3)
    number_of_files_entry()
    root.mainloop()
