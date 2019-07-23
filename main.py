import constans, stations
import multiprocessing
import os
from concurrent import SharedQueue, CommandExecutor, MeteoTaskData
from grib import GribCommand


def read_coords_file():
    return stations.STATIONS


def send_tasks(shared_queue: SharedQueue):
    for estacion, coords in read_coords_file().items():
        for month in range(1, 12 + 1):
            for meteo_var in constans.METEO_VARS:
                command = GribCommand(
                    os.path.expanduser(constans.GRIB_BIN_RELATIVE_PATH),
                    constans.GRIB_LS_COMMAND,
                    coords,
                    ",".join(constans.DEFAULT_PARAMS),
                    "shortName=" + meteo_var,
                    os.path.expanduser(constans.PATH_TO_GRIB_FILE) + f"2018{month:02d}_meteo.grib"
                )
                out_filename_path = \
                    os.path.expanduser(constans.RELATIVE_PATH) \
                    + estacion + f"/2018{month:02d}" + f"/2018{month:02d}_" + meteo_var + ".csv"
                meteo_task_data = MeteoTaskData(command, out_filename_path)
                shared_queue.fill_queue(meteo_task_data)


def main():
    shared_queue = SharedQueue()
    send_tasks(shared_queue)
    cpu_cores = multiprocessing.cpu_count()
    for core in range(cpu_cores):
        thread = CommandExecutor("T" + str(core), shared_queue)
        thread.start()


if __name__ == "__main__":
    main()