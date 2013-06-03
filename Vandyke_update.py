#/usr/bin/python
#coding=utf-8

import os,sys
import urllib
import urllib2
import getpass
import cookielib

##################################################################################
#                                Conf
##################################################################################
# 脚本日志路径
logpath = '/home/'+getpass.getuser()+'/.Vandyke_update.log'
# vandyke 试用版本记录文件,未到期重新安装scrt,需要删除这个文件.到期则不需要
Vandykecnf_path = '/home/'+getpass.getuser()+'/.vandyke/Config/SecureCRT_eval.lic'
# 文件保存位置, 默认为脚本当前位置
Save_path = os.path.abspath('.')
# 需要下载的文件名称,在help()中选择其他的文件 默认为ubuntu 11.x and 12.x 64bit
File_Name = 'SecureCRT_ubuntu1164_deb'
# 当前用户密码
pass_wd = '********'
# dpkg 或者rpm 路径(这里自动输出了当前用户的密码,ubuntu 默认)
bin_path = '/bin/echo %s|/usr/bin/sudo -S dpkg -i' %(pass_wd)
##################################################################################
def help():
    usage =\
    """
    ###########################################################################
    #                       下载文件                                          #
    #Vandyke 支持Win/Mac/Linux发行版本,本脚本支持rh系和debian系               #
    #默认下载Ubuntu 11.x and 12.x 的64bit 版本                                #
    #需要下载符合自己系统的版本只需要在Conf中更改File_Name的对应值            #
    #修改bin_path的对应值                                                     #
    ###########################################################################
    #File_Name = "SecureCRT_ubuntu1132_deb" # Ubuntu 11.x and 12.x 32bit      #
    #File_Name = "SecureCRT_ubuntu1164_deb" # Ubuntu 11.x and 12.x 64bit      #
    #File_Name = "SecureCRT_ubuntu_deb" # Ubuntu 10.x 32bit                   #
    #File_Name = "SecureCRT_ubuntu64_deb" # Ubuntu 10.x 64bit                 #
    #File_Name = "SecureCRT_rh6_rpm" # Red Hat Enterprise Linux 6.0 32-bit    #
    #File_Name = "SecureCRT_rh6_64_rpm" # Red Hat Enterprise Linux 6.0 64-bit #
    #File_Name = "SecureCRT_rh55_rpm" # Red Hat Enterprise Linux 5.5 32-bit   #
    #File_Name = "SecureCRT_rh55_64_rpm" # Red Hat Enterprise Linux 5.5 64-bit#
    ###########################################################################
    """
    print usage

cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
urllib2.install_opener(opener)

def main():
    import time
    DateNow = time.mktime(time.strptime(time.strftime("%Y-%m-%d",time.localtime()),"%Y-%m-%d")) # 获取当前时间
    if os.path.exists(logpath): # 存在本脚本的日志文件
        fp = open(logpath,'r').read()
        date = fp.split('\t')[-1].strip() # 读取脚本日志中的时间
        Date = time.strftime("%Y-%m-%d",time.strptime(date,"%Y-%m-%d")) # 格式化日志中时间,转换成日期格式(默认是字符型)
        Date = time.mktime(time.strptime(Date,"%Y-%m-%d")) # 格式化当前时间
        if int(DateNow - Date) >= 2419200: # 2419200 单位是s 等于28天
            download(File_Name,Save_path) # 重新下载
        else:sys.exit(0)
    else:download(File_Name,Save_path) # 不存在脚本的日志文件, 重新下载

def Install(file):
    if os.path.exists(Vandykecnf_path):os.remove(Vandykecnf_path) # 删掉原来的scrt的日期文件
    cmd = bin_path+' '+file # 类似dpkg -i xxx.deb
    result = os.popen(cmd) # 执行
    print result.read()

def log(content):
    """用于记录脚本第一次运行时间"""
    import time
    Date = time.strftime("%Y-%m-%d",time.localtime())
    fp = open(logpath,'w')
    fp.write(content+'\t'+Date+'\n')
    fp.close()


def download(file_name,path):
    """下载scrt"""
    save_path = path # scrt保存位置
    head = {}
    loglist = []
    # 填充post数据
    post_denglu = urllib.urlencode({'pid':File_Name,\
                          'username':'eleven.i386@gmail.com',\
                          'password':'12ae75',\
                          'status':'4'})

    post_ziyuan = urllib.urlencode({'pid':File_Name,\
                          'status':'self'})
    req_denglu = urllib2.urlopen('https://secure.vandyke.com/cgi-bin/account_verify.php', post_denglu)
    req_ziyuan = urllib2.urlopen('https://secure.vandyke.com/cgi-bin/download.php', post_ziyuan)
    # 格式化返回头信息
    for i in req_ziyuan.info().headers:
        header = i.replace('\n','').split(':')
        head[header[0]] = header[1].strip()
        # 文件名称
    savename = head['Content-Disposition'].split(';')[1].split('=')[1]
    # 文件大小
    filesize = head['Content-Length']
    # 流式写入下载文件数据
    fp = open(os.path.join(save_path,savename),'wb')
    """以下用作进度条显示"""
    file_size = 0
    while 1:
        # 每次读取8192字节,
        Buffer = req_ziyuan.read(8192)
        if not Buffer:
            break
        file_size += len(Buffer)
        fp.write(Buffer)
        status = r'Downloading %10d [%3.2f%%]' %(file_size,file_size * 100. / int(filesize))
        status = status + chr(8)*(len(status)+1)
        print status, # 终端显示进度条
    fp.close()
    # 将这次下载时间记录到日志
    log('Download %s Bytes FileName: %s' %(filesize,savename))
    # 调用系统命令安装scrt包
    Install(os.path.join(save_path,savename))
    # 收尾
    os.remove(os.path.join(save_path,savename))


if __name__ == '__main__':main()
