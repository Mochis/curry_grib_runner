import os


def write_binary_to_file(output_filename_path, binary_data_lines):
    path = _get_path(output_filename_path)
    if not os.path.exists(path):
        os.makedirs(path)
    with open(output_filename_path, "wb") as file:
        for line in binary_data_lines:
            file.write(line + b"\n")


def _get_path(output_path):
    return os.path.dirname(output_path)


def _get_filename(output_path):
    return os.path.basename(output_path)