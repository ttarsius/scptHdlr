

LOG_LEVEL = {
    "ALL":0,
    "DEBUG":1,
    "DEFULT":2,
}
#全局的打印信息等级，调试时请改为 LOG_LEVEL["DEBUG"]
cur_log_level = LOG_LEVEL["DEFULT"]

def print_msg(msg, level=cur_log_level):
    print(msg)


def print_debug(msg, level=cur_log_level):
    if level <= LOG_LEVEL["DEBUG"]:
        print(msg)

def print_error(msg, level=cur_log_level):
    print(msg)

