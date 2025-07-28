import psutil
import socket
import time
import yaml
import gspread

#### TODO:
# TopSheetParams.yml for parameters

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
client = gspread.oauth()
# make the sheet name customizable
sheet = client.create("Bioinfo Job Tracker").sheet1

# TODO: Make this a user parameter
job_terms = ["minimap2", "bwa", "juicer", "awk", "gzip", "macs2", "STAR", "samtools", "bcftools", "java"] # list of keywords 

# Clean existing data
sheet.clear()
## move this as it will be determined by user params
sheet.append_row(['Hostname', 'PID', 'Command', '%CPU', '%MEM', 'Elapsed Time', 'Last Updated'])

hostname = socket.gethostname()

def monitor():
"""
Function to stream process information.

TODO:
    - Add usability parameters (refresh interval, process info fields, portion of command string to parse)
    - Add endpoint parameter (i.e. what machine to monitor)
"""
    while True:
        now = time.strftime('%Y-%m-%d %H:%M:%S')
        rows = []

        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'create_time', 'cmdline']):
            try:
                cmd = ' '.join(proc.info['cmdline']) if proc.info['cmdline'] else proc.info['name']
                if any(term in cmd for term in job_terms):
                    elapsed = int(time.time() - proc.info['create_time'])
                    rows.append([
                        hostname,
                        proc.info['pid'],
                        cmd[:50],
                        round(proc.info['cpu_percent'], 2),
                        round(proc.info['memory_percent'], 2),
                        f"{elapsed//3600}h {(elapsed%3600)//60}m",
                        now
                    ])
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        # Refresh sheet
        sheet.resize(rows=len(rows)+1)
        sheet.update('A2', rows)

        time.sleep(60)  # check every minute

if __name__ == "__main__":
    monitor()
