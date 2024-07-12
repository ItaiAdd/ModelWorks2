from dataclasses import dataclass
from typing import Dict, Callable, Union, Any, Optional
import os

from .utils import (_is_file,
                   _is_dir,
                   _parent_dir_exists,
                   _ends_in_file,
                   _write_csv,
                   _append_csv,
                   _read_csv)


@dataclass
class Spec:
    spec_name: str
    fit: Callable
    pred: Callable
    metrics: Dict[str,Callable] = None
    params: Optional[Dict[str,Any]] = None
    fit_params: Optional[Dict[str,Any]] = None
    pred_params: Optional[Dict[str,Any]] = None
    preprocessing: Optional[Dict[str,Callable]] = None


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