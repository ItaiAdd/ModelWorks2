import os 
import csv
from inspect import isclass
from typing import Dict, List, Any, Tuple, Callable

from .distributions import BaseDistribution


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


def _spec_to_json_dict(x:Any) -> Any:
    if isinstance(x, BaseDistribution):
        return {'BaseDistribution':{'name':x.__class__.__name__, 'params':_spec_to_json_dict(x.__dict__)}}
    
    elif isinstance(x, list):
        return [_spec_to_json_dict(e) for e in x]
    
    elif isinstance(x, dict):
        return {k:_spec_to_json_dict(v) for k, v in x.items()}
    
    elif callable(x):
        return {'__callable__':x.__name__}
    
    else:
        return x


def _json_to_spec(x:Any, mapping:Dict) -> Any:
    if isinstance(x, dict):
        if 'BaseDistribution' in x:
            name = x['BaseDistribution']['name']
            params = x['BaseDistribution']['params']
            return mapping[name](**_json_to_spec(params, mapping))
    
        elif '__callable__' in x:
            return mapping[x['__callable__']]
        
        else:
            return {k:_json_to_spec(v, mapping) for k, v in x.items()}
        
    elif isinstance(x, list):
        return [_json_to_spec(e, mapping) for e in x]
    
    else:
        return x
    

def _callables_mapping(callables:List[Callable]) -> Dict[str, Callable]:
    return {c.__name__ :c for c in callables}