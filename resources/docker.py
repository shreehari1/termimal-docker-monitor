import docker
import subprocess
import json
from rich import box
from rich.panel import Panel
from rich.table import Table

client = docker.from_env()

def image_is_update(image_name) -> bool:
    image = client.images.get(image_name)
    imgRepoDigests = image.attrs.get("RepoDigests")[0].split('@')[1]
    registryDigest = client.images.get_registry_data(image_name).attrs.get("Descriptor").get("digest")
    return True if imgRepoDigests == registryDigest else False

def docker_container_info() -> Panel:
    table = Table(title="Docker Stats",box=box.SIMPLE_HEAD, border_style="bright_blue")
    table.add_column("Container name", justify="center", style="cyan", no_wrap=True)
    table.add_column("Status", justify="center", style="magenta")
    table.add_column("Image", justify="center", style="green")
    table.add_column("Check update", justify="center", style="yellow")

    container_list:list = client.containers.list()
    for container in container_list:
        container_name:str = container.attrs.get('Name').strip("/")
        container_status:str = container.attrs.get("State").get("Status")
        image_name:str = container.attrs.get("Config").get("Image")
        update_status:str = "Uptodate" if image_is_update(image_name) else "Need update"
        table.add_row(container_name,container_status,image_name,update_status)
    return Panel(table)

def docker_stats() -> Panel:
    table = Table(title="Docker Stats",box=box.ROUNDED, border_style="bright_blue")

    table.add_column("Container name", justify="center", style="cyan", no_wrap=True)
    table.add_column("CPU %", justify="center", style="magenta")
    table.add_column("Memory %", justify="center", style="green")
    table.add_column("Memory Usage", justify="center", style="yellow")

    stats_fil= "\"table {{json . }}\""
    result = subprocess.run(["docker", "stats","--format",stats_fil,"--no-stream"],stdout=subprocess.PIPE).stdout.decode("utf-8")
    reslines = result.splitlines()
    for l in reslines:
        line = json.loads(l[7:-1])
        table.add_row(line["Name"], line["CPUPerc"], line["MemPerc"],line["MemUsage"])

    return Panel(table)
