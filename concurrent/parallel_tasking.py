import threading
import queue
import subprocess
import constants

from grib import get_data_lines
from files import write_binary_to_file


class CommandExecutor(threading.Thread):
    def __init__(self, tname, shared_queue, cache):
        threading.Thread.__init__(self)
        self.shared_queue = shared_queue
        self.tname = tname
        self.cache = cache

    def run(self):
        meteo_task_data = None
        try:
            print("Starting Executor Thread " + self.tname)
            while True:
                meteo_task_data = self.shared_queue.consume_item_queue()
                if meteo_task_data is not None:
                    self.run_bash_command(meteo_task_data)
                else:
                    break
            print("Finishing Executor " + self.tname)
        except Exception as e:
            print("Error with Thread:%s in command %s. The error: %s" % (self.tname,
                                                          meteo_task_data.get_grib_command().to_string(), e))

    def run_bash_command(self, meteo_task_data):
        command = meteo_task_data.get_grib_command()
        print("Executing command: " + command.to_string())
        coords_param = command.get_param("l")
        if coords_param is not None:
            cache_key = "%s,%s,%s" % (coords_param[0], coords_param[1], command.get_filename())
            cache_value = self.cache.get_value(cache_key)
            if cache_value is not None:
                print("Thread:%s Getting value %s from cache" % (self.tname, coords_param))
                output = cache_value
            else:
                print("Thread:%s Running command %s" % (self.tname, command.to_string()))
                process = subprocess.Popen(command.to_string().split(), stdout=subprocess.PIPE)
                output, error = process.communicate()
                self.cache.put_value(cache_key, output)
        else:
            print("Thread:%s Running command %s" % (self.tname, command.to_string()))
            process = subprocess.Popen(command.to_string().split(), stdout=subprocess.PIPE)
            output, error = process.communicate()

        filtered_meteo_lines = get_data_lines(output, constants.HEADER_LINES_SKIP, constants.TAIL_LINES_SKIP)
        write_binary_to_file(meteo_task_data.get_out_filename_path(), filtered_meteo_lines)


class SharedQueue:
    def __init__(self):
        self.queue = queue.Queue()
        self.queue_lock = threading.Lock()

    def fill_queue(self, meteo_task_data):
        self.queue.put(meteo_task_data)  # Queue is "thread-safe" https://docs.python.org/3/library/queue.html

    def consume_item_queue(self):
        self.queue_lock.acquire()
        if self.queue.empty(): # empty method does not guarantee that subsequent call to get() will not block
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

    def to_string(self):
        return self.grib_command.to_string() + " " + self.out_filename_path
