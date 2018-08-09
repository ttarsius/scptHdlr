import telnetlib

class Session:
    host_name = ""
    host_ip = ""
    user_name = ""
    user_pwd = ""
    log = ""
    #tn = telnetlib.Telnet()

    def __init__(self, ip, usr, pwd):
        self.host_ip = ip
        self.user_name = usr
        self.user_pwd = pwd

    def read_until(self, expected_word):
        self.log += self.tn.read_until(expected_word.encode('utf-8')).decode('utf-8')

    def write(self, cmd_line):
        self.tn.write(cmd_line.encode('utf-8')+b'\n')

    def read_all(self):
        self.log += self.tn.read_all().decode('utf-8')

    def expect(self, expected_list):
        """
        一直从session读取，直到正则列表其中一个值匹配时返回
        :param expected_list: 匹配值的正则列表
        :return: 含有3个值的tuple，[0]为匹配到的正则列表的index，[1]为匹配到的值，[2]为从session读到的文本
        """
        exp_list = []
        for i in expected_list:
            exp_list.append(i.encode('utf-8'))
        result = self.tn.expect(exp_list)
        self.log += result[2].decode('utf-8')
        return result

    def login(self):
        try:
            self.tn = telnetlib.Telnet(host=self.host_ip)
        except:
            print("Cannot open host")
            return

        self.expect(["Username:","Login:"])
        self.write(self.user_name)
        self.read_until("Password:")
        self.write(self.user_pwd)
        mark = self.expect([">", "#"])
        if mark[0] == 0:
            self.write("sy")
            self.read_until("]")

        return


    def close(self):
        self.tn.close()


    def save_log_to_file(self, filename):
        f = open(filename, "w")
        f.write(self.log)
        f.close()


    def clear_log(self):
        self.log = ""


    def exec_command(self, cmd_line, continue_word, finish_word):
        self.write(cmd_line)
        i = 0
        while i==0:
            i = self.expect([continue_word, finish_word])[0]
            if i==0:
                self.write(" ")

        return

    def logout(self):
        pass

