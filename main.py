#from classes.session import Session
from static import device_list
from static.AAA import AAA_USR_PWD, AAA_USR_NAME
from main import gen_MSE_report

if __name__ == '__main__':
    #t = Session("113.98.172.179", "fssgx", "sgx`12345")

    #t.login()

    #t.write("disp cur")

    # lines = t.log.split("\n")
    # print(lines[-1].strip("[").strip("]"))


    # t.write("disp cur")
    # i = 0
    # while i == 0:
    #     i = t.expect(["----", "]"])[0]
    #     if i== 0:
    #         t.write(" ")
    #
    # fname = "tests/dis_cur_log.txt"
    # t.save_log_to_file(fname)


    # f = open("tests\hw_MSE_POOL.txt", "w")
    # text = []
    # pools = ["163.gd", "e8manage", "iptv.gd", "pub.163.gd"]
    # labels = ["poolLen", "used", "used_rate"]
    # for dev in MSE_LIST:
    #     usage = {}
    #     if "huawei" in dev[4]:
    #         print("analyzing "+dev[0]+" ......")
    #         usage = ip_pool.analyze_hw_log(ip_pool.get_ip_pool_data(dev))
    #         text.append("///////  " + dev[0] + " " + dev[1] + "  ///////")
    #         for pool in pools:
    #             text.append(pool+":")
    #             for l in labels:
    #                 text.append("    "+l+":"+usage[pool][l])
    #
    # for line in text:
    #     f.write(line+'\n')
    #
    # f.close()


    # tn = Session(dev[2], AAA_USR_NAME, AAA_USR_PWD)
    # tn.login()
    # tn.clear_log()
    # tn.exec_command("show submanage ip-pool used-rate domain iptv.gd", "--More--", "#")
    # tn.close()
    #
    # print(tn.log)

    # usage = {}
    # for dev in MSE_LIST:
    #     print("analyzing " + dev[0] + " ......")
    #     if "huawei" in dev[4]:
    #         usage[dev[0]] = ip_pool.analyze_nat_log(ip_pool.get_hw_nat_data(dev))
    # print(usage)
    gen_MSE_report.generate_xl_usage_report(device_list.MSE_LIST, AAA_USR_NAME, AAA_USR_PWD)

    gen_MSE_report.generate_xl_nat_report(device_list.MSE_LIST, AAA_USR_NAME, AAA_USR_PWD)
