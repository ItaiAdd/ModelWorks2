import os 
import csv
from typing import Dict, List, Any


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
        writer = csv.DictWriter(file, fieldnames=list(trials[0].keys()))
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
    

def _callable_to_name(x: Any) -> Dict|List|str:
    if isinstance(x, list):
        return [_callable_to_name(e) for e in x]
    
    elif isinstance(x, dict):
        return {k:_callable_to_name(v) for k, v in x.items()}
    
    elif callable(x):
        return x.__name__
    
    else:
        return x
    

def _tuples_to_json_list(x:Any) -> Any:
    if isinstance(x, list):
        return [_tuples_to_json_list(e) for e in x]
    
    elif isinstance(x, dict):
        return {k:_tuples_to_json_list(v) for k, v in x.items()}
    
    elif isinstance(x, tuple):
        x_new = list(x) + ['__tuple__']
        return _tuples_to_json_list(x_new)
    
    else:
        return x


def _json_lists_to_tuple(x: Any) -> Any:
    if isinstance(x, dict):
        return {k: _json_lists_to_tuple(v) for k, v in x.items()}
    
    elif isinstance(x, list):
        if '__tuple__' in x:
            x.remove('__tuple__')
            return tuple(_json_lists_to_tuple(e) for e in x)
        else:
            return [_json_lists_to_tuple(e) for e in x]
    
    elif isinstance(x, tuple):
        return tuple(_json_lists_to_tuple(e) for e in x)
    
    else:
        return x
    

def _names_to_callables(x:Any, mapping:Dict) -> Any:
    if isinstance(x, list):
        return [_names_to_callables(e, mapping) for e in x]
    
    elif isinstance(x, dict):
        return {k:_names_to_callables(v, mapping) for k, v in x.items()}
    
    elif isinstance(x, tuple):
        x_temp = list(x)
        return tuple([_names_to_callables(e, mapping) for e in x_temp])
    
    elif x in list(mapping.keys()):
        return mapping[x]
    
    else:
        return x