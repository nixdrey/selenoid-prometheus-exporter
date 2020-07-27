from prometheus_client import start_http_server, Gauge
import requests
import time
import json

# metrics
SELENOID_TOTAL = Gauge('selenoid_total', 'Total')
SELENOID_USED = Gauge('selenoid_used', 'Used')
SELENOID_QUEUED = Gauge('selenoid_queued', 'Queued')
SELENOID_PENDING = Gauge('selenoid_pending', 'Pending')


# Host and port of your selenoid instance
# Metrics should be available here http://selenoid.local:4444/status
SELENOID_HOST = 'selenoid.local'
SELENOID_PORT = 4444


def get_status():
    r = requests.get('http://{}:{}/status'.format(SELENOID_HOST, SELENOID_PORT))
    return json.loads(r.content)


def process_request(t):
    status = get_status()

    SELENOID_TOTAL.set(status['total'])
    SELENOID_USED.set(status['used'])
    SELENOID_PENDING.set(status['pending'])
    SELENOID_QUEUED.set(status['queued'])

    time.sleep(t)


if __name__ == '__main__':
    start_http_server(8800)
    while True:
        process_request(10)
