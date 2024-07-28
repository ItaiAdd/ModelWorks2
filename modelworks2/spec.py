from dataclasses import dataclass
from typing import Dict, Callable, Union, Any, Optional, Tuple, Generator
import os
import json

from .utils import (_is_file,
                   _is_dir,
                   _parent_dir_exists,
                   _ends_in_file,
                   _write_csv,
                   _append_csv,
                   _read_csv,
                   _callable_to_name,
                   _tuples_to_json_list,
                   _json_lists_to_tuple,
                   _names_to_callables)


@dataclass
class Spec:
    spec_name: str = None
    fit: Callable|str = None
    pred: Callable|str = None
    metrics: Dict[str,Callable|str] = None
    params: Optional[Dict[str,Any]] = None
    fit_params: Optional[Dict[str,Any]] = None
    pred_params: Optional[Dict[str,Any]] = None
    preprocessing: Optional[Dict[str,Callable|str]] = None


    def __post_init__(self) -> None:
        self.trials = []
        

    def add_trial(self, trial) -> None:
        self.trials.append(trial)

    
    def trials_to_csv(self, path, overwrite=False, append=False) -> None:
        if not path:
            raise ValueError("Path not provided. You must provide a path to write to.")
        
        elif not _parent_dir_exists(path):
            raise ValueError(f"{os.path.dirname(path)} does not exist.")

        elif _is_dir(path):
            raise ValueError(f"Supplied {path} is a directory. You must provide a filename.")
        
        elif not _ends_in_file(path):
            raise ValueError("Path should end in the filename to write to.")
        
        elif not _is_file(path) or overwrite:
            _write_csv(path, self.trials)
        
        elif append:
            _append_csv(path, self.trials)
        
        else:
            print(f"""Trials not saved. {path} already exists. Either:
                  1. Change overwright to True to overwrite the file.
                  2. Change append to True to append trials to the file.
                  3. Provide a different file. """)
            
    
    def trials_from_csv(self, path, replace=False) -> None:
        if not path:
            raise ValueError("Path not provided. You must provide a path to read from.")
        
        elif not _is_file(path):
            raise ValueError(f"{path} is not a file.")
        
        elif replace:
            self.trials = []
            self.trials.extend(_read_csv(path))

        else:
            self.trials.extend(_read_csv(path))


    def to_dict(self) -> Dict:
        return {'spec_name':self.spec_name,
                'fit':self.fit,
                'pred':self.pred,
                'metrics':self.metrics,
                'params':self.params,
                'fit_params':self.fit_params,
                'pred_params':self.pred_params,
                'preprocessing':self.preprocessing,
                'trials':self.trials}
    

    def __iter__(self) -> Generator[Tuple[str, Any], None, None]:
        for attr, val in self.to_dict().items():
            yield attr, val


    def save_spec(self, path, overwrite=False) -> None:
        if not path:
            raise ValueError("Path not provided. You must provide a path to write to.")
        
        elif not _parent_dir_exists(path):
            raise ValueError(f"{os.path.dirname(path)} does not exist.")

        elif _is_dir(path):
            raise ValueError(f"Supplied {path} is a directory. You must provide a filename.")
        
        elif not _ends_in_file(path):
            raise ValueError("Path should end in the filename to write to.")

        elif not _is_file(path) or overwrite:
            spec_dict = {}

            for attr, val in self:
                spec_dict[attr] = _tuples_to_json_list(_callable_to_name(val))

            with open(path, 'w') as file:
                json.dump(spec_dict, file)


    def load_spec(self, path) -> None:
        with open(path, "r") as file:
            spec_data = json.load(file)
            for attr, _ in self:
                setattr(self, attr, _json_lists_to_tuple(spec_data[attr]))


    def trials_from_spec(self, path, replace=False) -> None:
        if not path:
            raise ValueError("Path not provided.You must provide the path to the saved Spec.")
        
        with open(path, "r") as file:
            spec_data = json.load(file)

            if replace:
                self.trials = spec_data['trials']

            else:
                self.trials.extend(spec_data['trials'])


    def names_to_callables(self, callables:list) -> None:
        mapping = {e.__name__:e for e in callables}

        for attr, val in self:
            if attr in ['spec_name', 'trials']:
                continue

            else:
                setattr(self, attr, _names_to_callables(val, mapping))
