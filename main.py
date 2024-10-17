import subprocess
from flask import Flask
from markupsafe import escape

app = Flask(__name__)


def stat_server_uptime():
    with open('/proc/uptime') as f:
        t = float(f.readline().split()[0])
        seconds = int(t % 60)
        minutes = int((t // 60) % 60)
        hours = int((t // (60 * 60)) % 24)
        days = int(t // (24 * 60 * 60))

        return (days, hours, minutes, seconds)


def stat_cpu_core_utilization():
    pass


def stat_ssd_utilization():

    # df | grep -i '/home' | awk {'print $5'}
    df = subprocess.Popen(["df"], stdout=subprocess.PIPE)
    home_partition = subprocess.Popen(['grep', '-i', '/home'], 
                                      stdin=df.stdout, stdout=subprocess.PIPE)
    output = subprocess.Popen(['awk', '{print $5}'], 
                              stdin=home_partition.stdout, 
                              stdout=subprocess.PIPE)
    return output.communicate()[0].decode()


def stat_ram_utilization():
    with open('/proc/meminfo', 'r') as f:
        data = f.readlines()

    mem_dict = {}
    for line in data:
        if "MemTotal" in line:
            mem_dict['MemTotal'] = line.split()[1]
        if "MemFree" in line:
            mem_dict['MemFree'] = line.split()[1]
        if len(mem_dict) == 2:
            return mem_dict


def stat_cpu_temp():
    pass


def stat_fan_speeds():
    pass


def generate_content():
    t = stat_server_uptime()
    mem_d = stat_ram_utilization()


    html_header = """
        <head>
            <title>Linuxbox Status</title>
            <link rel="icon" href="linux_.png" type="image/x-icon">
        </head>
    """
    css_preamble = """
    <style>
        table, th, td {
            border: 1px solid black;
            background-color: #f7dc6f;
            width: 50%
        }
        h1 {
            font-weight: bold;
            font-family: monospace;
            color: #6ff792;
            background-color: black
        }
    </style>
    """
    html_body = f"""
    <body>
    <h1>tharindu@linuxbox></h1>
    <table>
        <tr>
            <td>Uptime</td> <td>{escape(t[0])}d {escape(t[1])}h
                {escape(t[2])}m {escape(t[3])}s</td>
        </tr>
        <tr>
            <td>RAM</td> <td> Total: {escape(mem_d['MemTotal'])} kB | Free: {escape(mem_d["MemFree"])} kB</td>
        </tr>
        <tr>
            <td>SSD</td> <td> {escape(stat_ssd_utilization())}</td>
        </tr>
    </table>
    </body>
    """
    return f"""
    <!DOCTYPE html>
    <html>
    {html_header}
    {css_preamble}
    {html_body}
    </html>
"""


@app.route("/")
def landing_page():
    return generate_content()


if __name__ == '__main__':
    app.run()