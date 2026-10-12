import tkinter as tk
from tkinter import messagebox
import calendar
from datetime import date


class WheelPicker(tk.Frame):

    def __init__(self, parent, values, width=100, height=170):
        super().__init__(parent, bg="white")

        self.values = values
        self.index = 0

        self.width = width
        self.height = height

        self.labels = []

        # Main canvas
        self.canvas = tk.Canvas(
            self,
            width=width,
            height=height,
            bg="white",
            highlightthickness=0
        )

        self.canvas.pack()

        # Mouse wheel
        self.canvas.bind(
    "<MouseWheel>",
    lambda event: self.change(
        -1 if event.delta > 0 else 1
    )
        )

        # Linux mouse wheel support
        self.canvas.bind(
            "<Button-4>",
            lambda event: self.change(-1)
        )

        self.canvas.bind(
            "<Button-5>",
            lambda event: self.change(1)
        )

        self.draw()

    def draw(self):

        self.canvas.delete("all")

        center_y = self.height // 2

        positions = [
            center_y - 55,
            center_y - 27,
            center_y,
            center_y + 27,
            center_y + 55
        ]

        for offset, y in zip(range(-2, 3), positions):

            index = (
                self.index + offset
            ) % len(self.values)

            value = self.values[index]

            if offset == 0:

                font = (
                    "Arial",
                    16,
                    "bold"
                )

                text_color = "#222222"

            elif abs(offset) == 1:

                font = (
                    "Arial",
                    13
                )

                text_color = "#888888"

            else:

                font = (
                    "Arial",
                    11
                )

                text_color = "#CCCCCC"

            self.canvas.create_text(
                self.width // 2,
                y,
                text=str(value),
                font=font,
                fill=text_color,
                anchor="center"
            )

        # Selection lines
        self.canvas.create_line(
            10,
            center_y - 21,
            self.width - 10,
            center_y - 21,
            fill="#E5E5E5"
        )

        self.canvas.create_line(
            10,
            center_y + 21,
            self.width - 10,
            center_y + 21,
            fill="#E5E5E5"
        )

    def change(self, amount):

        self.index = (
            self.index + amount
        ) % len(self.values)

        self.draw()

    def get_value(self):

        return self.values[self.index]


class BirthdayPicker(tk.Tk):

    def __init__(self):

        super().__init__()

        self.title("Cycora")
        self.geometry("500x520")

        self.configure(
            bg="white"
        )

        self.resizable(
            False,
            False
        )

        # TITLE

        title = tk.Label(
            self,
            text="When's your birthday?",
            font=("Arial", 24, "bold"),
            bg="white",
            fg="#222222"
        )

        title.pack(
            pady=(65, 8)
        )

        subtitle = tk.Label(
            self,
            text="This helps personalize your Cycora experience.",
            font=("Arial", 11),
            bg="white",
            fg="#888888"
        )

        subtitle.pack(
            pady=(0, 35)
        )

        # DATE VALUES

        months = [
            "January",
            "February",
            "March",
            "April",
            "May",
            "June",
            "July",
            "August",
            "September",
            "October",
            "November",
            "December"
        ]

        days = list(
            range(1, 32)
        )

        current_year = date.today().year

        years = list(
            range(
                current_year - 100,
                current_year + 1
            )
        )

        # Start with reasonable defaults
        default_month = date.today().month
        default_day = date.today().day
        default_year = current_year - 18

        # PICKER CONTAINER

        picker_frame = tk.Frame(
            self,
            bg="white"
        )

        picker_frame.pack()

        # MONTH

        month_frame = tk.Frame(
            picker_frame,
            bg="white"
        )

        month_frame.grid(
            row=0,
            column=0,
            padx=5
        )

        tk.Label(
            month_frame,
            text="",
            font=("Arial", 10),
            bg="white",
            fg="#999999"
        ).pack(
            pady=(0, 8)
        )

        self.month_picker = WheelPicker(
            month_frame,
            months,
            width=150,
            height=180
        )

        self.month_picker.pack()

        self.month_picker.index = (
            default_month - 1
        )

        self.month_picker.draw()

        # DAY

        day_frame = tk.Frame(
            picker_frame,
            bg="white"
        )

        day_frame.grid(
            row=0,
            column=1,
            padx=5
        )

        tk.Label(
            day_frame,
            text="",
            font=("Arial", 10),
            bg="white",
            fg="#999999"
        ).pack(
            pady=(0, 8)
        )

        self.day_picker = WheelPicker(
            day_frame,
            days,
            width=80,
            height=180
        )

        self.day_picker.pack()

        self.day_picker.index = (
            default_day - 1
        )

        self.day_picker.draw()

        # YEAR

        year_frame = tk.Frame(
            picker_frame,
            bg="white"
        )

        year_frame.grid(
            row=0,
            column=2,
            padx=5
        )

        tk.Label(
            year_frame,
            text="",
            font=("Arial", 10),
            bg="white",
            fg="#999999"
        ).pack(
            pady=(0, 8)
        )

        self.year_picker = WheelPicker(
            year_frame,
            years,
            width=100,
            height=180
        )

        self.year_picker.pack()

        self.year_picker.index = (
            years.index(default_year)
        )

        self.year_picker.draw()

        # SELECTED DATE

        self.selected_label = tk.Label(
            self,
            text="",
            font=("Arial", 11),
            bg="white",
            fg="#777777"
        )

        self.selected_label.pack(
            pady=(25, 20)
        )

        # CONTINUE BUTTON

        continue_button = tk.Button(
            self,
            text="Continue",
            font=("Arial", 11, "bold"),
            width=22,
            height=2,
            bg="#222222",
            fg="white",
            activebackground="#444444",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            command=self.confirm_date
        )

        continue_button.pack()

        self.update_selected_date()

    ----
    # GET SELECTED DATE
    ----

    def get_selected_date(self):

        month = (
            self.month_picker.index + 1
        )

        day = (
            self.day_picker.get_value()
        )

        year = (
            self.year_picker.get_value()
        )

        return year, month, day

    ----
    # UPDATE DATE LABEL
    ----

    def update_selected_date(self):

        year, month, day = (
            self.get_selected_date()
        )

        try:

            selected = date(
                year,
                month,
                day
            )

            formatted = selected.strftime(
                "%B %d, %Y"
            )

            self.selected_label.config(
                text=formatted
            )

        except ValueError:

            self.selected_label.config(
                text="Select a valid date"
            )

        self.after(
            100,
            self.update_selected_date
        )

    ----
    # CONFIRM DATE
    ----

    def confirm_date(self):

        year, month, day = (
            self.get_selected_date()
        )

        try:

            selected = date(
                year,
                month,
                day
            )

        except ValueError:

            messagebox.showwarning(
                "Invalid Date",
                "Please select a valid birthday."
            )

            return

        today = date.today()

        if selected > today:

            messagebox.showwarning(
                "Invalid Birthday",
                "Birthday cannot be in the future."
            )

            return

        formatted = selected.strftime(
            "%B %d, %Y"
        )

        messagebox.showinfo(
            "Birthday Selected",
            f"Birthday: {formatted}"
        )


if __name__ == "__main__":

    app = BirthdayPicker()

    app.mainloop()