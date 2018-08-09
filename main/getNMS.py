from classes.session import Session
from static.device_list import MSE_LIST


# if __name__ == '__main__':
#     usr_name = "fssgx"
#     usr_pwd  = "sgx`12345"
#     result = []
#     for m in MSE_LIST:
#         ip = m[2]
#         t = Session(ip, usr_name, usr_pwd)
#         t.login()
#         dev_nms = t.log.split('\n')[-1].strip("[").strip("]").strip("#")
#         t.close()
#         tmp = []
#         tmp.append(dev_nms)
#         for i in m:
#             tmp.append(i)
#         result.append(tmp)
#
#     print(result)