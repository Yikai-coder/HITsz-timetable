# iOS的HIT助手！

该项目目前正在维护+上新之中。

自动爬取由`jw.hitsz.edu.cn`导出的Excel课表文件，并生成**iCal**\(iCalendar, a.k.a. Webcal
[Wiki](https://en.wikipedia.org/wiki/ICalendar)
[百度百科](https://baike.baidu.com/item/iCal)\)格式的日历信息。

虽然iCalendar格式由Apple首先发布，但是该格式目前已经成为事实上的标准。Microsoft Outlook、Google Calendar等带有
日历功能的软件或服务均支持iCal格式的日历信息。

## 已经实现的功能

* 可以选择输出到`stdout`或者是指定文件。控制方法参见下一条"CLI".

* CLI。用法如下：
  
  * 必需参数：
    * `-u [Username]` 指定用户名
    * `-y [Year]`     指定本学期第一周星期一的日期（年）
    * `-m [Month]`    指定本学期第一周星期一的日期（月）
    * `-d [Day]`      指定本学期第一周星期一的日期（日）
      **例子**：我的学号是123456789，2021年春季学期第一周星期一的日期为2021.2.22（**日期是真的**），命令行参数就设置为：
      `-u 123456789 -y 2021 -m 2 -d 22`
  * 可选参数：
    * `-p [Password]` 指定密码。如果不想在shell中留下痕迹可以不填，在运行时会要求输入。
    * `-f [FilePath]` 指定输出ics文件的路径
    * `--stdout`      将ics文件内容写到标准输出，优先级比`-f`选项高。就是说，指定`--stdout`之后，`-f`就没用了。

## 第三方库依赖（通过脚本源码运行时需要）

* `click`
* `requests`
* `bs4`
* `openpyxl`
* `icalendar`
* `pyinstaller`（打包用）

## 玩法

* 可以用这个工具生成ics，同步到iOS设备上。方法如下：
  
  * 方法1：借助Microsoft Outlook、Apple Calendar或Google Calendar（如果可以）进行云同步。
  * 方法2：发一封邮件到自己的QQ邮箱，把ics文件作为附件。然后在手机上**用Safari浏览器登录邮箱**，下载附件，点击**全部加入**即可。

* 可以部署到有**CGI**功能的服务器上。
  
  * **CGI**是**通用网关接口**的英文简称，它可以扩充Web服务器的功能，是一个古老而有效的工具。Apache httpd支持这项功能。
  
  * 此处我们可以利用Python+CGI来提供iCalendar服务。这样的好处是**可以随时更新，不用担心哪天忽然多出一节课没显示**
  
  * 入口文件可以像下面这么写（未验证）。然后就可以通过URL：`webcal://Server-Address/CGI-Program-Path`来订阅日历了。
    
    ```python
    #! C:/Python/Python39/python.exe
    # coding=utf-8
    
    import os
    import subprocess
    import sys, codecs
    
    # 这里是防止Python+CGI出现中文乱码现象
    sys.stdout = codecs.getwriter('utf8')(sys.stdout.buffer)
    
    # 回应头，声明提供iCalendar协议的服务
    print("content-type: text/calendar\n")
    
    # 调起timetable，从标准输出取得webcal payload
    retval, output = subprocess.getstatusoutput("C:/.../timetable.exe -u 123456789 -p ********* -y 2021 -m 2 -d 22 --stdout")
    if retval==0:
      for i in output.split('\n'):
          print(i)
    ```

## 目标

* 通过教务系统爬取校历，这样就不用手动输入本学期第一周星期一的日期了！
