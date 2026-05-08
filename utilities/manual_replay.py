# manual_replay.py
# Temporary utility to replay quarantined events back into the Bronze layer
# Note: This uses standard os/shutil for local or FUSE-enabled DBFS.
# For standard DBFS, use dbutils.fs.mv.

import os
import shutil

QUARANTINE_DIR = "/mnt/datalake/quarantine/failed_events/"
LANDING_ZONE = "/mnt/datalake/raw/ecommerce_events/"

def replay_events(event_id=None):
    """Moves files from quarantine back to landing zone for reprocessing."""
    if not os.path.exists(QUARANTINE_DIR):
        print("Quarantine directory not found.")
        return

    files = os.listdir(QUARANTINE_DIR)
    count = 0
    for f in files:
        if event_id and event_id not in f:
            continue
        shutil.move(os.path.join(QUARANTINE_DIR, f), os.path.join(LANDING_ZONE, f))
        count += 1
    print(f"Replayed {count} files.")

if __name__ == "__main__":
    # replay_events()
    pass
