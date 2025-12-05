import psutil,platform,datetime,pymysql

from config.settings import MYSQL_CONFIG

# 监控代码逻辑
def collect_system_data():
    users = psutil.users()
    hostnames = [user.host for user in users if user.host]

    kernel_version = platform.release()
    boot_time = datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cpu_count = psutil.cpu_count()
    cpu_percent = psutil.cpu_percent(interval=1)
    cpu_load = [x/cpu_count*100 for x in psutil.getloadavg()]

    mem = psutil.virtual_memory()
    total_mem = mem.total/1024**3
    available_mem = mem.available/1024**3
    mem_percent = (mem.total-mem.available)/mem.total*100

    disk = psutil.disk_usage('/')
    total_disk = disk.total/1024**3
    free_disk = disk.free/1024**3
    disk_percent = disk.used/disk.total*100

    #准备保存mysql数据
    monitor_data={
              'timestamp':current_time,
              'cpu_percent':cpu_percent,
              'disk_percent':disk_percent,
              'memory_percent':mem_percent,
              'cpu_count':psutil.cpu_count(),
              'hostname':hostnames[0] if hostnames else 'unknown',
              'mem_total_gb': round(mem.total/1024**3,2),
              'mem_available_gb': round(available_mem, 2),
              'disk_total_gb': round(total_disk, 2),
              'disk_free_gb': round(free_disk, 2),
              'kernel_version': kernel_version,
              'boot_time': boot_time
             }
            
    return monitor_data
def save_to_db(data):
        #保存数据到数据库中
        conn=None
        cursor=None
        try:
            #链接
            conn=pymysql.connect(**MYSQL_CONFIG)
            cursor = conn.cursor()

            #检查其是否存在表，不存在则新创立表
            cursor.execute("show tables like 'monitor_log'")
            if not cursor.fetchone():
                cursor.execute("""
                    create table monitor_log (
                    id int auto_increment primary key,
                    timestamp datetime,
                    cpu_percent float,
                    memory_percent float,
                    disk_percent float,
                    hostname varchar(100)
                )
            """)
            #插入数据进入表内
            cursor.execute("""
            insert into monitor_log
            (timestamp,cpu_percent,memory_percent,disk_percent,hostname)
            values (%s,%s,%s,%s,%s)
            """,(
            data['timestamp'],
            data['cpu_percent'],
            data['memory_percent'],
            data['disk_percent'],
            data['hostname']
            ))

            conn.commit()

            print(f"👍数据已保存mysql(Time:{data['timestamp']})")
            return True

        except Exception as e:
            print(f"👎 mysql保存失败{e}")
            return False
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()


