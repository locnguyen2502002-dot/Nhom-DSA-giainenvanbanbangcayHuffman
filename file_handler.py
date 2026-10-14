import json
import struct

from huffman import (
    count_frequency,
    build_huffman_tree,
    generate_codes,
    encode,
    decode
)


# 1. Doc file van ban
def read_file(path):
    with open(path, "r", encoding="utf-8") as file:
        return file.read()


# 2. Ghi file van ban
def write_file(path, data):
    with open(path, "w", encoding="utf-8") as file:
        file.write(data)


# 3. Dong goi chuoi bit thanh bytes
def bits_to_bytes(bits):
    if not bits:
        return b""

    # Them bit 0 vao cuoi neu chua du 8 bit
    padding = (8 - len(bits) % 8) % 8
    bits += "0" * padding

    data = bytearray()

    for i in range(0, len(bits), 8):
        byte = bits[i:i + 8]
        data.append(int(byte, 2))

    return bytes(data)


# 4. Chuyen bytes thanh chuoi bit
def bytes_to_bits(data, bit_length):
    bits = "".join(format(byte, "08b") for byte in data)
    return bits[:bit_length]


# 5. Nen file van ban
def compress_file(input_path, output_path):
    text = read_file(input_path)

    # Dem tan suat va tao cay Huffman
    freq_table = count_frequency(text)
    root = build_huffman_tree(freq_table)
    codes = generate_codes(root)

    # Ma hoa va dong goi du lieu
    bits = encode(text, codes)
    binary_data = bits_to_bytes(bits)

    # Luu thong tin de dung lai cay khi giai nen
    metadata = {
        "frequencies": dict(freq_table),
        "bit_length": len(bits)
    }

    header = json.dumps(
        metadata,
        ensure_ascii=False
    ).encode("utf-8")

    # Cau truc file:
    # 4 bytes do dai header
    # header JSON
    # du lieu nhi phan da nen
    with open(output_path, "wb") as file:
        file.write(struct.pack(">I", len(header)))
        file.write(header)
        file.write(binary_data)

    return codes, len(text), len(bits)


# 6. Giai nen file Huffman
def decompress_file(input_path, output_path):
    with open(input_path, "rb") as file:
        # Doc 4 bytes dau de biet do dai header
        raw_length = file.read(4)

        if len(raw_length) != 4:
            raise ValueError("File nen khong hop le")

        header_length = struct.unpack(">I", raw_length)[0]

        # Doc metadata
        header = file.read(header_length)

        if len(header) != header_length:
            raise ValueError("Header bi thieu du lieu")

        metadata = json.loads(header.decode("utf-8"))

        freq_table = metadata["frequencies"]
        bit_length = metadata["bit_length"]

        # Doc phan du lieu nhi phan
        binary_data = file.read()

    # Khoi phuc chuoi bit
    bits = bytes_to_bits(binary_data, bit_length)

    if len(bits) != bit_length:
        raise ValueError("Du lieu nen bi thieu")

    # Tao lai cay Huffman
    root = build_huffman_tree(freq_table)

    # Giai ma va ghi ket qua
    text = decode(bits, root)
    write_file(output_path, text)

    return text