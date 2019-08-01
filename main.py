import properties
import stations
import multiprocessing
import os
from concurrent import SharedQueue, CommandExecutor, MeteoTaskData, Cache
from grib import GribCommand


def read_coords_file():
    return stations.STATIONS


def send_tasks(shared_queue: SharedQueue):
    for estacion, coords in read_coords_file().items():
        params = dict()
        params["p"] = properties.DEFAULT_PARAMS
        params["l"] = coords
        for month in range(1, 12 + 1):
            command = GribCommand(
                os.path.expanduser(properties.GRIB_BIN_RELATIVE_PATH),
                properties.GRIB_LS_COMMAND + " ",
                params,
                " " + os.path.expanduser(properties.PATH_TO_GRIB_FILE) + f"2018{month:02d}_meteo.grib"
            )
            out_filename_path = \
                os.path.expanduser(properties.RELATIVE_PATH) \
                + estacion + f"/2018{month:02d}" + f"/2018{month:02d}.csv"
            meteo_task_data = MeteoTaskData(command, out_filename_path)
            shared_queue.fill_queue(meteo_task_data)


def main():
    shared_queue = SharedQueue()
    cache = Cache()
    send_tasks(shared_queue)
    cpu_cores = multiprocessing.cpu_count()
    for core in range(cpu_cores):
        thread = CommandExecutor("T" + str(core), shared_queue, cache)
        thread.start()


if __name__ == "__main__":
    main()