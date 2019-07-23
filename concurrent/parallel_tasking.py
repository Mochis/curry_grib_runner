import threading
import queue
import subprocess

from grib import get_data_lines
from files import write_binary_to_file


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
        filtered_meteo_lines = get_data_lines(output)
        write_binary_to_file(meteo_task_data.get_out_filename_path(), filtered_meteo_lines)


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
