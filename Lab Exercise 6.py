import paramiko


class Connector:
    def __init__(self, host, user, pwd, port=22):
        self._host = host
        self.__user = user
        self.__pwd = pwd
        self.__port = port

        self.__ssh_client = paramiko.SSHClient()
        self.__ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.__ssh_client.connect(hostname=self._host, username=self.__user, password=self.__pwd, port=self.__port)

        self.__shell = self.__ssh_client.invoke_shell()

    def __del__(self):
        self.__ssh_client.close()

    def send_shell_command(self, command, user_input=None):
        self.__shell.send(command + "\n")
        time.sleep(2)

        response = self.__shell.recv(10000)

        output = response.decode()

        if user_input and len(user_input) > 0:
            self.__shell.send(user_input + "\n")
            time.sleep(2)
            response = self.__shell.recv(10000)
            output += response.decode()

        return output

    def send_exec_command(self, command, save_to_file=False):
        stdin, stdout, stderr = self.__ssh_client.exec_command(command + "\n")
        time.sleep(2)

        output = stdout.read().decode()

