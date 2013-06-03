一个用于自动下载安装SecureCRT的脚本

每隔28天自动重新下载安装SecureCRT, 避免手工重复工作.

第一次使用, 请先用任何你熟悉的编辑器,编辑Vandeky_update.py脚本,修改其中的
Conf部分的pass_wd部分, 这个是用于记录你当前用户密码的变量, 用于sudo安装SecureCRT
第一次使用会在当前用户的家目录下保存一个.Vandyke_update.log的文件, 用于记录该次安装的时间

请使用cron来做计划任务,在cron中加入任意一个时间,比如上午10

0 10 * * * python Vandyke_update.py

让每天上午10点运行一遍这个脚本. 脚本会检测当天时间于上次安装时间相差多少天, 如果大于等于28天, 则会开始下载SecureCRT并且
给你安装好, 让你不间断无限使用Vandyke的SecureCRT工具,而不用付出任何费用
