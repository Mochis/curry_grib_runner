
def get_data_lines(binary_data, start_at, finish_offset):
    binary_lines = binary_data.split(b"\n")
    # discard x first lines and removing the summary
    return binary_lines[start_at:len(binary_lines) - finish_offset]