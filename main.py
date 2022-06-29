import datetime
import json
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS

bucket = "test"
org = "FTS"
token = "ZztbZsHLRFNu3lMuop3qAJIRq-QUTlzzMLgHZANKX3vfv836X8St2pwQFtSLiVGdPVHHnmNhhEe_T4FdmRVBhw=="
url = "http://10.253.35.154:8087"
client = influxdb_client.InfluxDBClient(
   url=url,
   token=token,
   org=org
)
write_api = client.write_api(write_options=SYNCHRONOUS)
file_name = r"\\mgc\home\asutton\emulator-data\power\PMG_monitoring.log-latest.txt"
file = open(file_name, "r")
data = []
for line in file.readlines():
    if "TX" in line:
        details = line.split(" \tTX")
        time = details[0]
        measurements = details[1]
        phases = measurements.split("A,")
        phases = [x.strip() for x in phases]
        p1 = phases[0]
        p2 = phases[1]
        p3 = phases[2]
        p1 = p1.replace('Tx1','').strip()
        p2 = p2.replace('Tx2', '').strip()
        p3 = p3.replace('Tx3', '').strip()
        p3 = p3.replace('A', '').strip()
        time = datetime.datetime.strptime(time, "%Y/%m/%d %H:%M:%S").isoformat()
        p1 = {
            "measurement": f"Emulators",
            "fields": {
                "Current A": f"{int(p1)}",
                "Current B": f"{int(p2)}",
                "Current C": f"{int(p3)}"
            },
            "tags": {
                "site": "Wilsonville",
                "name": "Demogorgon"
            },
            "time": time + ".000Z"
        }
        print(time)
        # write_api.write(bucket=bucket, org=org, record=p1)

