from dataclasses import dataclass
from typing import Dict, Callable, Union, Any, Optional
import csv
import os


@dataclass
class Spec:
    spec_name: str
    fit: Callable
    pred: Callable
    metrics: Dict[str,Callable]
    params: Optional[Dict[str:Any]] = None
    fit_params: Optional[Dict[str,Any]] = None
    pred_params: Optional[Dict[str,Any]] = None
    preprocessing: Optional[Dict[str,Callable]] = None

    def __post_init__(self) -> None:
        self.trials = {key:[] for key in {**self.params, **self.metrics}.keys()}
    

    def add_trial(self, trial) -> None:
        for key in self.trials.keys():
            if callable(trial[key]):
                self.trials[key].append(trial[key].__name__)
            else:
                self.trials[key].append(trial[key])
    

    def trials_to_csv(self, path) -> None:
        if not path:
            print("Save path not specified.")
        elif not os.path.exists(os.path.dirname(path)):
            print(f"{os.path.dirname(path)} does not exist.")
        else:
            with open(path, "w") as file:
                writer = csv.writer(file)
                writer.writerow(self.trials.keys())
                writer.writerows(zip(*self.trials.values()))
    

    def trials_from_csv(self, path) -> None:
        with open(path, "r") as file:
            reader = csv.DictReader(file, quoting=csv.QUOTE_NONNUMERIC)
            self.trials = {key:[val] for key, val in next(reader).items()}
            for row in reader:
                for key, val in row.items():
                    self.trials[key].append(val)
