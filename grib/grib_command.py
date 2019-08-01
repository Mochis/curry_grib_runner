import os


class GribCommand:

    def __init__(self, relative_path, command, params, grib_file):
        self.relative_path = relative_path
        self.command = command
        self.params = params
        self.grib_file = grib_file

    def to_string(self):
        string_command = self.relative_path + self.command
        if self.params is not None:
            all_params = list()
            for param, values in self.params.items():
                all_params.append("-%s %s" % (param, ",".join(str(el) for el in values)))
            string_command = string_command + " ".join(all_params)

        string_command = string_command + self.grib_file

        return string_command

    def get_params(self):
        return self.params

    def get_param(self, param):
        return self.params.get(param, None)

    def get_filename(self):
        return os.path.basename(self.grib_file)


