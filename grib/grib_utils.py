
def get_data_lines(binary_data):
    binary_lines = binary_data.split(b"\n")
    # removing the summary
    return binary_lines[1:len(binary_lines) - 11]