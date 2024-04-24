import psutil
from rich import box
from rich.bar import Bar
from rich.console import Group
from rich.panel import Panel
from rich.table import Table

def updateStats() -> Table:

    # CPU related information
    cpu_freq = str(round(psutil.cpu_freq().current)/1000)
    cpu_freq_max = str(round(psutil.cpu_freq().max)/1000)
    cpu_temp = str(round(psutil.sensors_temperatures().get("cpu_thermal")[0].current))
    cpu_percentage = psutil.cpu_percent()
    fan_speed = " RPM" #str(psutil.sensors_fans())

    # Calculate memory information
    memory = psutil.virtual_memory()
    # Convert Bytes to MB (Bytes -> KB -> MB)
    memory_available = round(memory.available/1024.0/1024.0/1024.0,1)
    memory_used = round(memory.used/1024.0/1024.0/1024.0,1)
    memory_total = round(memory.total/1024.0/1024.0/1024.0,1)
    memory_info = 'Used:' + str(memory_used) + '/' + str(memory_total) + 'GB | ' + 'Free:' + str(memory_available) + 'GB'
    
    # Calculate disk information
    disk = psutil.disk_usage('/')
    # Convert Bytes to GB (Bytes -> KB -> MB -> GB)
    disk_free = round(disk.free/1024.0/1024.0/1024.0,1)
    disk_used = round(disk.used/1024.0/1024.0/1024.0,1)
    disk_total = round(disk.total/1024.0/1024.0/1024.0,1)
    disk_info = 'Used:' + str(disk_used) + '/' + str(disk_total) + 'GB | ' + 'Free:' + str(disk_free) + 'GB'

    cpu_group = Group(
            "CPU usage: "+str(cpu_percentage)+str("%"),
            "Cores: " + str(psutil.cpu_count()) + " | Clock:" + cpu_freq + "/" + cpu_freq_max + "GHz",
            Bar(100, width=40, begin=0, end=cpu_percentage, color="dark_green",bgcolor="black"),
            "Temp:"+ cpu_temp + "'C" + " | Fan:" + fan_speed,
        )
    mem_group = Group(
            "Memory usage: "+str(memory.percent)+str("%"),
            memory_info,
            Bar(100, width=40, begin=0, end=memory.percent, color="bright_yellow",bgcolor="black"),
            ""
        )
    disk_group = Group(
            "Disk usage: "+ str(disk.percent)+str("%"),
            disk_info,
            Bar(100, width=40, begin=0, end=disk.percent, color="dark_blue",bgcolor="black"),
            ""
        )
    battey_group = Group(
        "Battery usage: 100%",
        "Battery state: Charging",
        Bar(100, width=40, begin=0, end=100, color="dark_blue",bgcolor="black"),
        ""
    )

    stats_table = Table.grid(expand=True)
    stats_table.add_row(
    Panel(cpu_group, title="[b]CPU",box=box.ROUNDED, border_style="bright_blue", padding=(1, 1)),
    Panel(mem_group, title="[b]Memory", border_style="bright_blue", padding=(1, 1)),
    Panel(disk_group, title="[b]Disk", border_style="bright_blue", padding=(1, 1)),
    Panel(battey_group, title="[b]Battery", border_style="bright_blue", padding=(1, 1)),
    )
    return stats_table

