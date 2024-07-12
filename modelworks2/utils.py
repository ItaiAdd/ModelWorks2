import os 
import csv
from typing import Dict, List


def _is_file(p) -> bool:
    return os.path.isfile(p)


def _is_dir(p) -> bool:
    return os.path.isdir(p)


def _parent_dir_exists(p) -> bool:
    return os.path.exists(os.path.dirname(p))


def _ends_in_file(p) -> bool:
    dirname = os.path.dirname(p)
    end = p.strip().replace(dirname, "")
    if len(end) > 0:
        result = True
    else:
        result = False
    return result


def _write_csv(p, trials) -> None:
    with open(p, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=list(trials[0]).keys())
        writer.writeheader()
        writer.writerows(trials)


def _append_csv(p, trials) -> None:
    with open(p, "a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=list(trials[0].keys()))
        writer.writerows(trials)


def _restore_dtype_csv(row) -> Dict:
    restored_row = {}
    for key, val in row.items():
        try:
            val_lower = val.lower()
            if "." in val or "e" in val_lower:
                restored_row[key] = float(val)
            else:
                restored_row[key] = int(val)
        except ValueError:
            if val_lower == "true":
                restored_row[key] = True
            elif val_lower == "false":
                restored_row[key] = False
            else:
                restored_row[key] = val
    return restored_row


def _read_csv(p) -> List[Dict]:
    with open(p, "r", newline="") as file:
        reader = csv.DictReader(file)
        rows = [_restore_dtype_csv(row) for row in reader]
        return rows