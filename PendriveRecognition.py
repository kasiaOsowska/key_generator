import psutil

def find_pendrive_path_windows():
    for device in psutil.disk_partitions():
        if 'removable' in device.opts:
            return device.mountpoint
    return None

def pendrive_detection():
    print("Oczekiwanie na pendrive...")
    while True:
        pendrive_path = find_pendrive_path_windows()
        if pendrive_path:
            print(f"Pendrive znaleziony w ścieżce: {pendrive_path}")
            return pendrive_path
