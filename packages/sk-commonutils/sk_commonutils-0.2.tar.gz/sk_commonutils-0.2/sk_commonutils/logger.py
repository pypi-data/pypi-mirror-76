from datetime import datetime

def logConsole(logType, *msg):
    timeStamp = datetime.now().strftime("%d.%m.%Y_%H:%M:%S")
    print("[{0}] [{1:^7s}] - {2:s}".format(timeStamp, logType, ''.join([str(x) for x in msg])))

SUCCESS="SUCCESS"
INFO="INFO"
DEBUG="DEBUG"
WARN="WARN"
ERROR="ERROR"
FATAL="FATAL"

# logConsole("INFO", "Executed Successfully")
# logConsole("WARN", "Your brain may be malfunctioning.")
# logConsole("ERROR", "Your existance is PAIN")
# logConsole("SUCCESS", "You've made it.... somehow....")
# logConsole("FATAL", "Get lost!")
