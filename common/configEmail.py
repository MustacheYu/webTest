# encoding=utf-8
import os
import readConfig as readConfig
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.mime.multipart import MIMEMultipart
# from email.mime.image import MIMEImage
from Log import Log
import zipfile
import glob

log = Log(logger="Email")
logger = log.get_logger()
localReadConfig = readConfig.ReadConfig()


# noinspection PyGlobalUndefined
class Email(object):
    def __init__(self):
        global host, port, user, password, sender, receiver, subject
        host = localReadConfig.get_email("mail_host")
        port = localReadConfig.get_email("mail_port")
        user = localReadConfig.get_email("mail_user")
        password = localReadConfig.get_email("mail_pass")
        sender = localReadConfig.get_email("sender")
        receiver = localReadConfig.get_email("receiver")
        subject = localReadConfig.get_email("subject")
        self.msg = MIMEMultipart()

    def config_header(self):
        self.msg['subject'] = Header(subject, 'utf-8')
        self.msg['from'] = sender
        self.msg['to'] = receiver

    def config_content(self):
        f = open(os.path.join(readConfig.proDir, 'testFile', 'email', 'emailStyle.txt'))
        content = f.read()
        f.close()
        content_plain = MIMEText(content, 'html', 'UTF-8')
        self.msg.attach(content_plain)
        # self.config_image()

    # def config_image(self):
    #     # defined image path
    #     image1_path = os.path.join(readConfig.proDir, 'testFile', 'email', 'img', '1.png')
    #     fp1 = open(image1_path, 'rb')
    #     msgImage1 = MIMEImage(fp1.read())
    #     fp1.close()
    #
    #     # defined image id
    #     msgImage1.add_header('Content-ID', '<image1>')
    #     self.msg.attach(msgImage1)
    #
    #     image2_path = os.path.join(readConfig.proDir, 'testFile', 'email', 'img', 'logo.jpg')
    #     fp2 = open(image2_path, 'rb')
    #     msgImage2 = MIMEImage(fp2.read())
    #     fp2.close()
    #
    #     # defined image id
    #     msgImage2.add_header('Content-ID', '<image2>')
    #     self.msg.attach(msgImage2)

    @staticmethod
    def check_file():
        reportpath = log.get_report_path()
        if os.path.isfile(reportpath) and not os.stat(reportpath) == 0:
            return True
        else:
            return False

    def config_file(self):
        # if the file content is not null, then config the email file
        if self.check_file():

            reportpath = log.get_result_path()
            zippath = os.path.join(reportpath, "TestReport.zip")

            # zip file
            files = glob.glob(reportpath + '\*')
            f = zipfile.ZipFile(zippath, 'w', zipfile.ZIP_DEFLATED)
            for file_zip in files:
                # 修改压缩文件的目录结构
                f.write(file_zip, '/report/'+os.path.basename(file_zip))
            f.close()

            reportfile = open(zippath, 'rb').read()
            filehtml = MIMEText(reportfile, 'base64', 'utf-8')
            filehtml['Content-Type'] = 'application/octet-stream'
            filehtml['Content-Disposition'] = 'attachment; filename="TestReport.zip"'
            self.msg.attach(filehtml)

    def send_email(self):
        self.config_header()
        self.config_content()
        self.config_file()
        try:
            smtp = smtplib.SMTP_SSL()
            smtp.connect(host, int(port))
            smtp.login(user, password)
            smtp.sendmail(sender, receiver.split(','), self.msg.as_string())
            smtp.quit()
            logger.info("测试报告已通过电子邮件发送给开发人员")
        except Exception as ex:
            logger.error(str(ex))
