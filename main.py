import datetime
import os.path
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
from py_dotenv import read_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
read_dotenv(dotenv_path)
bucket = os.getenv('INFLUXDB_BUCKET')
org = os.getenv('INFLUXDB_ORG')
token = os.getenv('INFLUXDB_TOKEN')
url = os.getenv('INFLUXDB_URL')
client = influxdb_client.InfluxDBClient(
   url=url,
   token=token,
   org=org
)
write_api = client.write_api(write_options=SYNCHRONOUS)
file = open(os.getenv("LATEST_LOG"), "r")
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
                "site": os.getenv('EMULATOR_SITE'),
                "name": os.getenv('EMULATOR_NAME')
            },
            "time": time + ".000Z"
        }
        response = write_api.write(bucket=bucket, org=org, record=p1)
        print(response, f", record added for {p1['tags']['name']} at time {p1['time']}.",)

