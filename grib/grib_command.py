
class GribCommand:

    def __init__(self, relative_path, command, coords, params, where, grib_file):
        self.relative_path = relative_path
        self.command = command
        self.coords = coords
        self.params = params
        self.where = where
        self.grib_file = grib_file

    def to_string(self):
        return "%s -l %.2f,%.2f,1 -p %s -w %s %s" % \
               (self.relative_path + self.command, self.coords[0], self.coords[1], self.params,
                self.where, self.grib_file)
