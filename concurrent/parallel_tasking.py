import threading
import queue
import subprocess
import os


class CommandExecutor(threading.Thread):
    def __init__(self, tname, shared_queue):
        threading.Thread.__init__(self)
        self.shared_queue = shared_queue
        self.tname = tname

    def run(self):
        print("Starting Executor Thread " + self.tname)
        while True:
            meteo_task_data = self.shared_queue.consume_item_queue()
            if meteo_task_data is not None:
                print("Executing command: " + meteo_task_data.get_grib_command().to_string())
                self.run_bash_command(meteo_task_data)
            else:
                break
        print("Finishing Executor " + self.tname)

    def run_bash_command(self, meteo_task_data):
        process = subprocess.Popen(meteo_task_data.get_grib_command().to_string().split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
        binary_lines = output.split(b"\n")
        filtered_meteo_lines = binary_lines[1:len(binary_lines) - 11]
        paths = meteo_task_data.get_out_filename_path().split("/")
        path = "/" + "/".join(paths[1:len(paths)-1])
        if not os.path.exists(path):
            os.makedirs(path)
        with open(meteo_task_data.get_out_filename_path(), "wb") as file:
            for meteo_line_data in filtered_meteo_lines:
                file.write(meteo_line_data + b"\n")


class SharedQueue:
    def __init__(self):
        self.queue = queue.Queue()
        self.queue_lock = threading.Lock()

    def fill_queue(self, meteo_task_data):
        self.queue.put(meteo_task_data)

    def consume_item_queue(self):
        self.queue_lock.acquire()
        if self.queue.empty():
            command = None
        else:
            command = self.queue.get()
        self.queue_lock.release()
        return command


class MeteoTaskData:
    def __init__(self, grib_command, out_filename_path):
        self.grib_command = grib_command
        self.out_filename_path = out_filename_path

    def get_grib_command(self):
        return self.grib_command

    def get_out_filename_path(self):
        return self.out_filename_path
