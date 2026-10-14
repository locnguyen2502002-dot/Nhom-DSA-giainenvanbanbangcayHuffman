import json
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from huffman import (
    count_frequency,
    build_huffman_tree,
    generate_codes,
    encode,
    decode
)


class HuffmanApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Huffman Compression")
        self.root.geometry("900x650")

        # Lưu dữ liệu đang xử lý
        self.text = ""
        self.freq_table = {}
        self.root_node = None
        self.codes = {}
        self.encoded_text = ""

        # Tiêu đề
        tk.Label(
            root,
            text="HUFFMAN COMPRESSION",
            font=("Arial", 18, "bold")
        ).pack(pady=10)

        # Các nút chức năng
        button_frame = tk.Frame(root)
        button_frame.pack(pady=5)

        tk.Button(
            button_frame,
            text="Mở file TXT",
            command=self.open_file
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            button_frame,
            text="Mã hóa",
            command=self.encode_text
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            button_frame,
            text="Lưu file nén",
            command=self.save_compressed
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            button_frame,
            text="Mở file nén",
            command=self.open_compressed
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            button_frame,
            text="Giải mã",
            command=self.decode_text
        ).pack(side=tk.LEFT, padx=5)

        # Khu vực văn bản gốc
        tk.Label(root, text="Văn bản gốc").pack()

        self.input_box = tk.Text(root, height=6, width=100)
        self.input_box.pack(padx=10, pady=5)

        # Bảng tần suất và mã Huffman
        tk.Label(root, text="Bảng tần suất và mã Huffman").pack()

        columns = ("character", "frequency", "code")
        self.table = ttk.Treeview(
            root,
            columns=columns,
            show="headings",
            height=7
        )

        self.table.heading("character", text="Ký tự")
        self.table.heading("frequency", text="Tần suất")
        self.table.heading("code", text="Mã Huffman")

        self.table.column("character", width=150)
        self.table.column("frequency", width=150)
        self.table.column("code", width=300)

        self.table.pack(padx=10, pady=5, fill=tk.X)

        # Khu vực dữ liệu đã mã hóa
        tk.Label(root, text="Dữ liệu sau mã hóa").pack()

        self.encoded_box = tk.Text(root, height=5, width=100)
        self.encoded_box.pack(padx=10, pady=5)

        # Khu vực kết quả giải mã
        tk.Label(root, text="Kết quả giải mã").pack()

        self.decoded_box = tk.Text(root, height=5, width=100)
        self.decoded_box.pack(padx=10, pady=5)

        # Hiển thị tỷ lệ nén
        self.ratio_label = tk.Label(
            root,
            text="Tỷ lệ nén: chưa có dữ liệu"
        )
        self.ratio_label.pack(pady=5)

    # 1. Mở file văn bản
    def open_file(self):
        path = filedialog.askopenfilename(
            filetypes=[("Text files", "*.txt")]
        )

        if not path:
            return

        try:
            with open(path, "r", encoding="utf-8") as file:
                self.text = file.read()

            self.input_box.delete("1.0", tk.END)
            self.input_box.insert("1.0", self.text)

            # Xóa khung kết quả giải mã cũ
            self.decoded_box.delete("1.0", tk.END)

            messagebox.showinfo("Thông báo", "Đã mở file thành công!")

        except Exception as error:
            messagebox.showerror("Lỗi", str(error))

    # 2. Mã hóa văn bản
    def encode_text(self):
        self.text = self.input_box.get("1.0", "end-1c")

        if not self.text:
            messagebox.showwarning(
                "Cảnh báo", "Vui lòng nhập hoặc mở văn bản!"
            )
            return

        self.freq_table = count_frequency(self.text)
        self.root_node = build_huffman_tree(self.freq_table)
        self.codes = generate_codes(self.root_node)
        self.encoded_text = encode(self.text, self.codes)

        # Hiển thị bảng tần suất và mã
        for item in self.table.get_children():
            self.table.delete(item)

        for char, frequency in self.freq_table.items():
            display_char = repr(char)

            self.table.insert(
                "",
                tk.END,
                values=(
                    display_char,
                    frequency,
                    self.codes[char]
                )
            )

        # Hiển thị chuỗi bit
        self.encoded_box.delete("1.0", tk.END)
        self.encoded_box.insert("1.0", self.encoded_text)

        # Xóa khung kết quả giải mã cũ
        self.decoded_box.delete("1.0", tk.END)

        # Tính tỷ lệ nén theo số bit
        original_bits = len(self.text.encode("utf-8")) * 8
        encoded_bits = len(self.encoded_text)

        if original_bits > 0:
            ratio = encoded_bits / original_bits * 100

            self.ratio_label.config(
                text=(
                    f"Số bit gốc: {original_bits} | "
                    f"Số bit mã hóa: {encoded_bits} | "
                    f"Tỷ lệ: {ratio:.2f}%"
                )
            )

    # 3. Lưu dữ liệu đã mã hóa
    def save_compressed(self):
        if not self.encoded_text:
            messagebox.showwarning(
                "Cảnh báo", "Hãy mã hóa văn bản trước!"
            )
            return

        path = filedialog.asksaveasfilename(
            defaultextension=".huff",
            filetypes=[("Huffman files", "*.huff")]
        )

        if not path:
            return

        try:
            data = {
                "frequency": self.freq_table,
                "encoded": self.encoded_text
            }

            with open(path, "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=True)

            messagebox.showinfo(
                "Thông báo", "Đã lưu file nén thành công!"
            )

        except Exception as error:
            messagebox.showerror("Lỗi", str(error))

    # 3.5. Mở file nén
    def open_compressed(self):
        path = filedialog.askopenfilename(
            filetypes=[("Huffman files", "*.huff")]
        )

        if not path:
            return

        try:
            with open(path, "r", encoding="utf-8") as file:
                data = json.load(file)

            self.freq_table = data["frequency"]
            self.encoded_text = data["encoded"]

            # Xây lại cây Huffman từ bảng tần suất
            self.root_node = build_huffman_tree(self.freq_table)
            self.codes = generate_codes(self.root_node)

            # Hiển thị bảng tần suất
            for item in self.table.get_children():
                self.table.delete(item)

            for char, frequency in self.freq_table.items():
                display_char = repr(char)

                self.table.insert(
                    "",
                    tk.END,
                    values=(
                        display_char,
                        frequency,
                        self.codes[char]
                    )
                )

            # Hiển thị chuỗi bit
            self.encoded_box.delete("1.0", tk.END)
            self.encoded_box.insert("1.0", self.encoded_text)

            # Xóa khung kết quả giải mã cũ
            self.decoded_box.delete("1.0", tk.END)

            messagebox.showinfo("Thông báo", "Đã mở file nén thành công!")

        except Exception as error:
            messagebox.showerror("Lỗi", str(error))

    # 4. Giải mã dữ liệu hiện tại
    def decode_text(self):
        if self.root_node is None or not self.encoded_text:
            messagebox.showwarning(
                "Cảnh báo", "Hãy mã hóa văn bản trước!"
            )
            return

        try:
            decoded = decode(self.encoded_text, self.root_node)

            self.decoded_box.delete("1.0", tk.END)
            self.decoded_box.insert("1.0", decoded)

        except Exception as error:
            messagebox.showerror("Lỗi giải mã", str(error))


# Hàm để main.py gọi
def run_app():
    root = tk.Tk()
    app = HuffmanApp(root)
    root.mainloop()


if __name__ == "__main__":
    run_app()