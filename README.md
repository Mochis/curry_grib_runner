# Concurrent grib commands executor
Running multiple grib bash commands in parallel using Python and writing the responses to a file. The program uses a cache for storing the responses and have not to execute again the same command with the same params, instead of that it reads and get from cache the result of any previously executed command.

GRIB (GRIdded Binary or General Regularly-distributed Information in Binary form) is a concise data format commonly used in meteorology to store historical and forecast weather data.
