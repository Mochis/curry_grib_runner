
def get_data_lines(binary_data, start_at, finish_offset):
    binary_lines = binary_data.split(b"\n")
    # discarding x first lines and removing last y lines with the summary
    return binary_lines[start_at:len(binary_lines) - finish_offset]