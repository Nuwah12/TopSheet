import psutil
import socket
import time
import yaml
import gspread

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
client = gspread.oauth()
sheet = client.create("Bioinfo Job Tracker").sheet1

job_terms = ["minimap2", "bwa", "juicer", "awk", "gzip", "macs2", "STAR", "samtools", "bcftools", "java"] # list of keywords 

# Clean existing data
sheet.clear()
sheet.append_row(['Hostname', 'PID', 'Command', '%CPU', '%MEM', 'Elapsed Time', 'Last Updated'])

hostname = socket.gethostname()

def monitor():

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
