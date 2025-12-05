底层使用了python的一个库，名字叫做psutil 这是一个很强大的库，可以查看很多的系统数据以及硬件数据 这是psutil的官方网站 https://psutil.readthedocs.io/en/latest/# 然后使用了flask框架建立网站，再使用了nginx反向代理网络 再使用pymysql库连接mysql数据库，储存数据 使用crontab -e 定时运行curl命令
