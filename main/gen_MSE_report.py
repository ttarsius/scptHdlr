from logics import ip_pool
from excel import xl_hdlr
import datetime
from logics.logger import *

OUTPUT_DIR = "Outputs"

def get_MSE_pool_usage(DEV_LIST, AAA_USR, AAA_PWD):
    usage = {}
    for dev in DEV_LIST:
        print_msg("正在获取 "+dev[0] + " 地址池信息 ...", cur_log_level)
        if "huawei" in dev[4]:
            usage[dev[0]] = ip_pool.analyze_hw_log(
                ip_pool.get_ip_pool_data(dev, AAA_USR, AAA_PWD)
            )
            print_msg(dev[0] + " 获取完毕。")
        elif "zte" in dev[4]:
            usage[dev[0]] = ip_pool.analyze_zte_log(
                ip_pool.get_ip_pool_data(dev, AAA_USR, AAA_PWD)
            )
            print_msg(dev[0] + " 获取完毕。")
        else:
            print_error("未知设备类型， 获取失败。")

    return usage


def get_MSE_nat_usage(DEV_LIST, AAA_USR, AAA_PWD):
    usage = {}
    for dev in DEV_LIST:
        if "huawei" in dev[4]:
            print_msg("正在获取 " + dev[0] + " NAT信息 ...", cur_log_level)
            usage[dev[0]] = ip_pool.analyze_nat_log(
                ip_pool.get_hw_nat_data(dev, AAA_USR, AAA_PWD)
            )
            print_msg(dev[0] + " 获取完毕。")
        else:
            print_error("仅支持获取huawei设备的NAT占用率。")

    return usage

def generate_xl_usage_report(DEV_LIST, AAA_USR, AAA_PWD):
    pool_usage = get_MSE_pool_usage(DEV_LIST, AAA_USR, AAA_PWD)

    fname = OUTPUT_DIR+'\\'+str(datetime.date.today())+"_MSE地址池占用率.xls"
    print_msg("正在写入地址池占用率EXCEL表 ...")
    lines = [["设备名称","别名", "地址池","大小","已使用数","占用率"]]
    for device in DEV_LIST:
        for index, key in enumerate(pool_usage[device[0]]):
            vals = pool_usage[device[0]][key]
            lines.append([device[0], device[1], key, vals["poolLen"], vals["used"], vals["used_rate"]])

    xl_hdlr.write_lines(lines, fname)

    return


def generate_xl_nat_report(DEV_LIST, AAA_USR, AAA_PWD):
    nat_usage = get_MSE_nat_usage(DEV_LIST, AAA_USR, AAA_PWD)

    fname = OUTPUT_DIR+'\\'+str(datetime.date.today())+"_MSE_NAT占用率.xls"
    print_msg("正在写入NAT占用率EXCEL表 ...")
    lines = [["设备名称","别名", "地址池","slot","engine","poolID","占用率"]]
    for device in DEV_LIST:
        if "huawei" in device[4]:
            for index, key in enumerate(nat_usage[device[0]]):
                vals = nat_usage[device[0]][key]
                print_debug(vals)
                for i in vals:
                    lines.append(([device[0], device[1], key, i[0], i[1], i[2], i[3]]))

    xl_hdlr.write_lines(lines, fname)

    return