from functions.transform_to_binary import transform_to_binary
import functions.binary_to_hex as binary_to_hex
from opcode_dict import opcode_dict
from functions.format_input import get_format_lines
from functions.get_information import (
    get_instructions,
    get_operation,
    get_mode_and_literal,
    get_data_lines,
    get_code_lines,
    get_labels_dict
)
from iic2343 import Basys3
import sys
from tkinter import *
from tkinter import filedialog
import tkinter.scrolledtext as scrolledtext
import threading
import pyperclip


class Assembler:
    def __init__(self):
        self.root = Tk()
        self.root.title("Assembler")
        self.basys_is_connected = False
        self.switch_basys_is_connected = BooleanVar()
        self.file_path = ""
        self.create_gui()

    def create_gui(self):
        # Get screen width and height
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Calculate x and y coordinates for the Tk root window
        x = (screen_width - 600) // 2
        y = (screen_height - 450) // 2

        # Set the dimensions of the screen
        self.root.geometry("600x450+{}+{}".format(x, y))

        frame = Frame(self.root, padx=10, pady=10)
        frame.pack(expand=True, fill="both")

        title_label = Label(
            frame, text="Bienvenido al Ensamblador", font=("Arial", 17))
        title_label.pack(pady=(0, 20))

        self.switch_basys_is_connected = BooleanVar()
        self.switch_button = Checkbutton(frame, text="¿La Placa Basys está conectada?", font=(
            "Arial", 14), variable=self.switch_basys_is_connected, command=self.update_switch_button_text)
        self.switch_button.pack(pady=20)

        select_button = Button(frame, text="Seleccionar archivo", font=(
            "Arial", 10), command=self.open_file)
        select_button.pack()

        self.path_label = Label(frame, text="", font=(
            "Arial", 10), wraplength=350, justify="left")
        self.path_label.pack(pady=20)

        self.assembler_button = Button(frame, text="Ensamblar", font=("Arial", 14), command=lambda: threading.Thread(
            target=self.assemble_code()).start(), state='disabled')
        self.assembler_button.pack(pady=20)

        self.status_label = Label(frame, text="", font=(
            "Arial", 14), wraplength=350, justify="left")
        self.status_label.pack(pady=20)

        self.root.mainloop()

    def update_switch_button_text(self):
        self.basys_is_connected = self.switch_basys_is_connected.get()
        if self.switch_basys_is_connected.get():
            self.switch_button.config(
                text="¿La Placa Basys está conectada?: Sí 😎", fg="green")
        else:
            self.switch_button.config(
                text="¿La Placa Basys está conectada?: No 😞", fg="#0071bc")

    def open_file(self):
        self.file_path = filedialog.askopenfilename(
            title="Seleccionar archivo")
        if self.file_path:
            self.path_label.config(
                text=f"Ruta del archivo seleccionado:\n{self.file_path}")
            self.assembler_button.config(state='normal')

    def show_instructions(self, instructions_as_string):
        new_window = Toplevel(self.root)
        file_name = self.file_path.split('/')[-1]
        new_window.title(f"Instrucciones Generadas - {file_name}")

        instructions_text = scrolledtext.ScrolledText(
            new_window, wrap=WORD, width=60, height=15)
        instructions_text.pack(pady=10)
        instructions_text.insert(INSERT, instructions_as_string)

        copy_button = Button(new_window, text="Copiar al portapapeles",
                             command=lambda: self.copy_to_clipboard(instructions_as_string))
        copy_button.pack(pady=10)

    def copy_to_clipboard(self, text):
        pyperclip.copy(text)

    def assemble_code(self):
        print("Basys connected:", self.basys_is_connected)
        # Clear de instructions list
        self.instructions = []

        try:
            if self.basys_is_connected:
                self.rom_programmer = Basys3()
                self.rom_programmer.begin()

            self.lines = get_format_lines(self.file_path)

            # Dictionary to store the labels and their memory direction
            self.labels_dict = get_labels_dict(self.lines)

            self.data_logic()
            self.code_logic()

            self.rom_programming()

        except Exception as e:
            self.status_label.config(text=f"Error: {e}", fg="red")
            print(e)

    def data_logic(self):
        data_lines = get_data_lines(self.lines)
        print(f"Data lines: {data_lines}")

        # Dictionary to store the variables and their memory direction
        self.data_dict = dict()

        memory_direction = 0
        for line in data_lines:
            if len(line) == 2:                                  # Ej: arr 7
                variable = line[0]
                # Save the variable and its memory direction (Ej: 'arr': 0)
                self.data_dict[variable] = str(memory_direction)
                self.instructions.append(get_instructions(
                    operation='MOV', mode='A_LIT', literal=line[1])[0])
            else:                                               # Ej:     9
                self.instructions.append(get_instructions(
                    operation='MOV', mode='A_LIT', literal=line[0])[0])

            self.instructions.append(get_instructions(
                operation='MOV', mode='(DIR)_A', literal=str(memory_direction))[0])
            memory_direction += 1

    def code_logic(self):
        code_lines = get_code_lines(self.lines)
        print(f"Code lines:")

        for line in code_lines:
            operation = get_operation(line)
            mode, literal = get_mode_and_literal(
                line, self.data_dict, self.labels_dict)
            print(f"Line: {line}")
            print(f"Operation: {operation}")
            print(f"Mode: {mode}")
            print(f"Literal: {literal}")
            instruction_1, instruction_2 = get_instructions(
                operation=operation, mode=mode, literal=literal)

            # instruction_1, instruction_2 = get_instructions(operation=operation, mode=mode, literal=literal)
            if instruction_1 is not None:
                print(f"Instruction 1: {instruction_1}")
                self.instructions.append(instruction_1)
            if instruction_2 is not None:
                print(f"Instruction 2: {instruction_2}\n")
                self.instructions.append(instruction_2)
            print()

    def clear_rom(self):
        n_lines = 4096
        for i in range(n_lines):
            if self.basys_is_connected:
                self.rom_programmer.write(
                    i, bytearray([0x00, 0x00, 0x00, 0x00, 0x00]))
            i += 1

    def rom_programming(self):
        i = 0
        self.clear_rom()
        for instruction in self.instructions:
            hexadecimal_instruction = binary_to_hex.binary_to_hex(instruction)
            if self.basys_is_connected:
                self.rom_programmer.write(
                    i, bytearray.fromhex(hexadecimal_instruction))
            i += 1

        if self.basys_is_connected:
            self.rom_programmer.end()

        self.status_label.config(text="Ensamblado exitoso ✔️", fg="green")
        self.show_instructions('\n'.join(self.instructions))


if __name__ == "__main__":
    assembler = Assembler()
