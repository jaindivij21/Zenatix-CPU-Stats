from abc import abstractproperty
import psutil
import time
from datetime import datetime


# function to return processes and their corresponding information
def listOfProcesses():
    processDatabase = []
    # run a loop for maxCount minutes
    maxCount = 10
    count = 0

    while True:
        time.sleep(60 - time.time() % 60)
        count += 1
        # get current time
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")

        # iterate over the pid list
        tempList = []
        for proc in psutil.process_iter(attrs=("name", "pid", "cpu_percent", "memory_percent")):
            info = {
                "PID": proc.info["pid"],
                "Name": proc.info["name"],
                "CPU in Use": psutil.Process(proc.info["pid"]).cpu_percent(interval=0.1) / psutil.cpu_count(),
                # percentage
                "Memory in Use": (mem := proc.info['memory_percent']),
                # In GB
                "Memory Usage": (psutil.virtual_memory().total * (mem / 100) / (1024 ** 3)),
                "Time": current_time
            }
            tempList.append(info)

        # insert into the process database
        processDatabase.append(tempList)
        if count == maxCount:
            break

    return processDatabase


# function to get 10 pids and their info from the first minute
# Memory Usage in GB
def getExcerpt(proc):
    excerpt = []

    i = 0
    for pro in proc:
        if i == 10:
            break
        excerpt.append(pro)
        i += 1
    return excerpt


# function that prints the high memory using processes (threshold set = 1.5% memory)
def highMemUsage(proc):
    highMem = []    # result

    for pro in proc:
        if float(pro['Memory in Use']) > 2.0:
            highMem.append(pro)
        else:
            continue
    highMem.sort(key=lambda i: i['Memory Usage'], reverse=True)
    return highMem
