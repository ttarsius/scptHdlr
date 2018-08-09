from classes.session import Session
from logics.logger import *

DOMAIN_NAMES = ["163.gd", "e8manage", "pub.163.gd", "iptv.gd"]

NE40E_POOL_CMD = "display ip-pool pool-usage"
NE40E_NAT_CMD = [
    "disp nat address-usage instance instance_NAT444-1 address-group pool_163_NAT01",
    "disp nat address-usage instance instance_NAT444-2 address-group pool_163_NAT02"
]

M6000_POOL_CMD = [
    "show submanage ip-pool used-rate domain 163.gd",
    "show submanage ip-pool used-rate domain iptv.gd",
    "show submanage ip-pool used-rate domain pub.163.gd",
    "show submanage ip-pool used-rate domain e8manage",
]

NE40E_CONTINUE_WORD = "---- More ----"
NE40E_FINISH_WORD = "]"
M6000_CONTINUE_WORD = "--More--"
M6000_FINISH_WORD ="#"


#telnet到设备，执行查询地址池的命令，返回查询的结果
def get_ip_pool_data(MSE_DEVICE, AAA_USR_NAME, AAA_USR_PWD):
    msg = []
    #Telnet设备
    tn = Session(MSE_DEVICE[2], AAA_USR_NAME, AAA_USR_PWD)
    tn.login()
    tn.clear_log()

    if MSE_DEVICE[5] == 'NE40E-X16':
        tn.exec_command(NE40E_POOL_CMD,NE40E_CONTINUE_WORD, NE40E_FINISH_WORD)
        msg = tn.log

    elif MSE_DEVICE[5] == 'M6000':
        for cmd in M6000_POOL_CMD:
            tn.exec_command(cmd, M6000_CONTINUE_WORD, M6000_FINISH_WORD)
        msg = tn.log

    tn.close()
    return msg


def get_hw_nat_data(MSE_DEVICE, AAA_USR_NAME, AAA_USR_PWD):
    msg = []
    tn = Session(MSE_DEVICE[2], AAA_USR_NAME, AAA_USR_PWD)
    tn.login()
    tn.clear_log()

    for cmd in NE40E_NAT_CMD:
        tn.exec_command(cmd, NE40E_CONTINUE_WORD, NE40E_FINISH_WORD)
    msg = tn.log

    tn.close()
    return msg


def get_clean_logs(log_data):
    '''
    清除日志中由于continue_word引起的无效信息，如：
    “---- More ----\x1b[42D  ”
    返回按行分割的日志
    :param log_data:"display ip-pool pool-usage" 返回的原始输出结果
    :return:
    '''
    msg = log_data.split("\r\n")
    for i in range(0, len(msg)):
        if "42D" in msg[i]:
            msg[i] = msg[i].split("42D")[-1]

    return msg


def analyze_nat_log(log_data):
    '''

    :param log_data:
    :return:
    '''
    logs = get_clean_logs(log_data)
    usage = {}
    for index, value in enumerate(logs):
        if "-group" in value:
            print_debug("matched: " + value)
            pool_name = value.split("-group")[-1].strip(" ")
            usage[pool_name]= []
            print_debug(pool_name)
            if "Error" in logs[index+1]:
                continue
            i = index+1
            while (i < len(logs)):
                if "Slot" in logs[i]:
                    print_debug("slot line matched: " + logs[i])
                    first_line_words = [i for i in logs[i].split(" ") if i]
                    second_line_words = logs[i+2].split(":")
                    third_line_words = logs[i+3].split(":")
                    usage[pool_name].append([
                        first_line_words[1],  #slot
                        first_line_words[-1],  #engine
                        second_line_words[-1].strip(" "),  #poolID
                        third_line_words[-1].strip(" "),   #Usage
                    ])
                if "]" in logs[i]:
                    break
                i += 1

    print_debug(usage)

    return usage


def analyze_hw_log(log_data):
    '''
    返回华为MSE的地址池使用状况，数据格式如下：
    usage = {
        "pool_001":{
            "poolLen":123, "used":12, "used_rate":10%,},
        "pool_002":{
            ... },
        ...
        "Total":{
            ... },
    }
    :param log_data: "display ip-pool pool-usage" 返回的原始输出结果
    :return: usage：地址池使用情况的字典
    '''
    logs = get_clean_logs(log_data)
    usage = {}
    for line in logs:
        tmp = [i for i in line.split(" ") if i]
        if tmp[0] in DOMAIN_NAMES:
            usage[tmp[0]]={"poolLen":tmp[1], "used":tmp[2], "used_rate":tmp[3]}
        # if "Total" in tmp:
        #     usage["Total"] = {"poolLen":tmp[-3], "used":tmp[-2], "used_rate":tmp[-1]}

    return usage


def analyze_zte_log(log_data):
    '''
    与analyze_hw_log类似，返回usage字典，各个地址池包含poolLen、used、used_rate 3个字段
    :param log_data:
    :return:
    '''
    logs = get_clean_logs(log_data)
    usage = {}
    for index, value in enumerate(logs):
        if "submanage" in value:
            pool_name = value.split(" ")[-1]
            first_line_words = [i for i in logs[index+2].split(" ") if i]
            second_line_words = [i for i in logs[index+3].split(" ") if i]
            usage[pool_name]={
                "poolLen":first_line_words[0].split(":")[-1],
                "used": first_line_words[1].split(":")[-1],
                "used_rate": second_line_words[0].split(":")[-1],
            }

    return usage

