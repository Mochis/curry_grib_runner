# Concurrent grib commands executor
Running multiple grib bash commands in parallel using Python and writing the responses to a file. The program uses a cache for storing the responses and have not to execute again the same command with the same params, instead of that it reads and get from cache the result of any previously executed command.
