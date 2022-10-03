import os
import random
import datetime
from sys import getsizeof

from newrelic_telemetry_sdk import MetricClient, GaugeMetric, CountMetric, SummaryMetric
from newrelic_telemetry_sdk import EventClient, Event

metric_client = MetricClient(os.environ["NEW_RELIC_LICENSE_KEY"])
event_client = EventClient(os.environ["NEW_RELIC_LICENSE_KEY"])

db = {}
stats = {
    "read_response_times": [],
    "read_errors": 0,
    "read_count": 0,
    "create_response_times": [],
    "create_errors": 0,
    "create_count": 0,
    "update_response_times": [],
    "update_errors": 0,
    "update_count": 0,
    "delete_response_times": [],
    "delete_errors": 0,
    "delete_count": 0,
    "cache_hit": 0,
}
last_push = {
    "read": datetime.datetime.now(),
    "create": datetime.datetime.now(),
    "update": datetime.datetime.now(),
    "delete": datetime.datetime.now(),
}

def read(key):

    print(f"Reading...")

    if random.randint(0, 30) > 10:
        stats["cache_hit"] += 1

    stats["read_response_times"].append(random.uniform(0.5, 1.0))
    if random.choice([True, False]):
        stats["read_errors"] += 1
    stats["read_count"] += 1
    try_send("read")

def create(key, value):

    print(f"Writing...")

    db[key] = value
    stats["create_response_times"].append(random.uniform(0.5, 1.0))
    if random.choice([True, False]):
        stats["create_errors"] += 1
    stats["create_count"] += 1
    try_send("create")

def update(key, value):

    print(f"Updating...")

    db[key] = value
    stats["update_response_times"].append(random.uniform(0.5, 1.0))
    if random.choice([True, False]):
        stats["update_errors"] += 1
    stats["update_count"] += 1
    try_send("update")

def delete(key):

    print(f"Deleting...")

    db.pop(key, None)
    stats["delete_response_times"].append(random.uniform(0.5, 1.0))
    if random.choice([True, False]):
        stats["delete_errors"] += 1
    stats["delete_count"] += 1
    try_send("delete")

def try_send(type_):

    print("try_send")

    now = datetime.datetime.now()
    interval_ms = (now - last_push[type_]).total_seconds() * 1000
    if interval_ms >= 2000:
        send_metrics(type_, interval_ms)
        send_event(type_)

def send_metrics(type_, interval_ms):
    
    print("sending metrics...")

    keys = GaugeMetric("fdb_keys", len(db))
    db_size = GaugeMetric("fdb_size", getsizeof(db))

    errors = CountMetric(
        name=f"fdb_{type_}_errors",
        value=stats[f"{type_}_errors"],
        interval_ms=interval_ms
    )

    cache_hits = CountMetric(
        name=f"fdb_cache_hits",
        value=stats["cache_hit"],
        interval_ms=interval_ms
    )

    response_times = stats[f"{type_}_response_times"]
    response_time_summary = SummaryMetric(
        f"fdb_{type_}_responses",
        count=len(response_times),
        min=min(response_times),
        max=max(response_times),
        sum=sum(response_times),
        interval_ms=interval_ms,
    )

    batch = [keys, db_size, errors, cache_hits, response_time_summary]
    response = metric_client.send_batch(batch)
    response.raise_for_status()
    print("Sent metrics successfully!")
    clear(type_)

def send_event(type_):

    print("sending event...")

    count = Event(
        "fdb_method", {"method": type_}
    )

    response = event_client.send_batch(count)
    response.raise_for_status()
    print("Event sent successfully!")

def clear(type_):
    stats[f"{type_}_response_times"] = []
    stats[f"{type_}_errors"] = 0
    stats["cache_hit"] = 0
    stats[f"{type_}_count"] = 0
    last_push[type_] = datetime.datetime.now()
