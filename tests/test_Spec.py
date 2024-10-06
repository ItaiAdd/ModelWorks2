import pytest
import os
import sys
import csv
import json

parent = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent)

from modelworks2.spec import Spec


test_input_csv = os.path.join(parent, 'tests/test-input.csv')
test_write_path = os.path.join(parent, 'tests/test-output.csv')
test_spec_read_path = os.path.join(parent, 'tests/test_spec_read.json')
test_spec_write_path = os.path.join(parent, 'tests/test_spec_write.json')



def _mock_fit_pred():
    pass


def _mock_metric():
    pass


def _mock_tran():
    pass


@pytest.fixture(scope="module")
def test_input_file():
    data = [
        {'param1_str': 'str_p1', 'param2_int': 1, 'param3_flt': 0.1, 'metric_1': 0.01, 'metric_2': 0.001},
        {'param1_str': 'str_p2', 'param2_int': 2, 'param3_flt': 0.2, 'metric_1': 0.02, 'metric_2': 0.002}
    ]
    with open(test_input_csv, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

    yield test_input_csv

    os.remove(test_input_csv)
    if os.path.exists(test_write_path):
        os.remove(test_write_path)


@pytest.fixture(scope="module")
def test_spec_fixture():
    data = {'spec_name':'test_spec',
                'fit':'_mock_fit_pred',
                'pred':'_mock_fit_pred',
                'metrics':{'m1':'_mock_metric', 'm2':'_mock_metric'},
                'params':{'param1':[1,2,3], 'param2':[0,1,'__tuple__'], 'param3':['p1', 'p2']},
                'fit_params':{'param1':1, 'param2':'a'},
                'pred_params':{'param1':2, 'param2':'b'},
                'preprocessing':{'pp1':'_mock_tran', 'pp2':'_mock_tran'},
                'trials':[{'param1':1, 'param2':0.01, 'param3':'p1', 'm1':0.1, 'm2':0.2},
                          {'param1':2, 'param2':0.02, 'param3':'p2', 'm1':0.2, 'm2':0.3}]
            }
    with open(test_spec_read_path, "w") as file:
        json.dump(data, file)

    yield test_spec_read_path

    os.remove(test_spec_read_path)
    if os.path.exists(test_spec_write_path):
        os.remove(test_spec_write_path)


def test_trials_from_csv(test_input_file):
    test_spec = Spec('test_spec', _mock_fit_pred, _mock_fit_pred)
    test_spec.trials_from_csv(test_input_csv)

    assert test_spec.trials == [{'param1_str':'str_p1', 'param2_int':1, 'param3_flt':0.1 ,'metric_1':0.01, 'metric_2':0.001},
                                {'param1_str':'str_p2', 'param2_int':2, 'param3_flt':0.2 ,'metric_1':0.02, 'metric_2':0.002}]
    
    test_spec.trials_from_csv(test_input_file)

    assert test_spec.trials == [{'param1_str':'str_p1', 'param2_int':1, 'param3_flt':0.1 ,'metric_1':0.01, 'metric_2':0.001},
                                {'param1_str':'str_p2', 'param2_int':2, 'param3_flt':0.2 ,'metric_1':0.02, 'metric_2':0.002},
                                {'param1_str':'str_p1', 'param2_int':1, 'param3_flt':0.1 ,'metric_1':0.01, 'metric_2':0.001},
                                {'param1_str':'str_p2', 'param2_int':2, 'param3_flt':0.2 ,'metric_1':0.02, 'metric_2':0.002}]
    

def test_trials_from_csv_append(test_input_file):
    test_spec = Spec('test_spec', _mock_fit_pred, _mock_fit_pred)
    test_spec.add_trial({'param1_str':'str_p1', 'param2_int':1, 'param3_flt':0.1 ,'metric_1':0.01, 'metric_2':0.001})

    test_spec.trials_from_csv(test_input_file)

    assert test_spec.trials == [{'param1_str':'str_p1', 'param2_int':1, 'param3_flt':0.1 ,'metric_1':0.01, 'metric_2':0.001},
                                {'param1_str':'str_p1', 'param2_int':1, 'param3_flt':0.1 ,'metric_1':0.01, 'metric_2':0.001},
                                {'param1_str':'str_p2', 'param2_int':2, 'param3_flt':0.2 ,'metric_1':0.02, 'metric_2':0.002}]
    

def test_trials_from_csv_replace(test_input_file):
    test_spec = Spec('test_spec', _mock_fit_pred, _mock_fit_pred)
    test_spec.add_trial({'param1_str':'str_p1', 'param2_int':1, 'param3_flt':0.1 ,'metric_1':0.01, 'metric_2':0.001})

    test_spec.trials_from_csv(test_input_file, replace=True)

    assert test_spec.trials == [{'param1_str':'str_p1', 'param2_int':1, 'param3_flt':0.1 ,'metric_1':0.01, 'metric_2':0.001},
                                {'param1_str':'str_p2', 'param2_int':2, 'param3_flt':0.2 ,'metric_1':0.02, 'metric_2':0.002}]


def test_trials_to_csv_create():
    test_spec = Spec('test_spec', _mock_fit_pred, _mock_fit_pred)
    test_spec.add_trial({'param1_str':'str_p1', 'param2_int':1, 'param3_flt':0.1 ,'metric_1':0.01, 'metric_2':0.001})

    test_spec.trials_to_csv(test_write_path)    
    test_spec.trials_from_csv(test_write_path, replace=True)

    assert test_spec.trials == [{'param1_str':'str_p1', 'param2_int':1, 'param3_flt':0.1 ,'metric_1':0.01, 'metric_2':0.001}]


def test_trials_to_csv_overwrite(test_input_file):
    test_spec = Spec('test_spec', _mock_fit_pred, _mock_fit_pred)
    test_spec.add_trial({'param1_str':'str_p2', 'param2_int':2, 'param3_flt':0.2 ,'metric_1':0.02, 'metric_2':0.002})

    test_spec.trials_to_csv(test_write_path, overwrite=True)
    test_spec.trials_from_csv(test_write_path, replace=True)

    assert test_spec.trials == [{'param1_str':'str_p2', 'param2_int':2, 'param3_flt':0.2 ,'metric_1':0.02, 'metric_2':0.002}]


def test_trials_to_csv_append(test_input_file):
    test_spec = Spec('test_spec', _mock_fit_pred, _mock_fit_pred)
    test_spec.add_trial({'param1_str':'str_p1', 'param2_int':1, 'param3_flt':0.1 ,'metric_1':0.01, 'metric_2':0.001})

    test_spec.trials_to_csv(test_write_path, append=True)
    test_spec.trials_from_csv(test_write_path, replace=True)

    assert test_spec.trials == [{'param1_str':'str_p2', 'param2_int':2, 'param3_flt':0.2 ,'metric_1':0.02, 'metric_2':0.002},
                                {'param1_str':'str_p1', 'param2_int':1, 'param3_flt':0.1 ,'metric_1':0.01, 'metric_2':0.001}]


def test_save_and_load_spec(test_spec_fixture):
    test_spec = Spec('test_spec', _mock_fit_pred, _mock_fit_pred, {'m1':_mock_metric, 'm2':_mock_metric},
                     {'param1':[1,2,3], 'param2':(0,1), 'param3':['p1', 'p2']}, {'param1':1, 'param2':'a'},
                     {'param1':2, 'param2':'b'}, {'pp1':_mock_tran, 'pp2':_mock_tran})
    
    test_spec.add_trial({'param1':1, 'param2':0.01, 'param3':'p1', 'm1':0.1, 'm2':0.2})
    test_spec.add_trial({'param1':2, 'param2':0.02, 'param3':'p2', 'm1':0.2, 'm2':0.3})

    test_spec.save_spec(test_spec_write_path)

    test_spec = Spec()

    test_spec.load_spec(test_spec_write_path)

    assert test_spec.to_dict() == {'spec_name':'test_spec',
                                   'fit':'_mock_fit_pred',
                                   'pred':'_mock_fit_pred',
                                   'metrics':{'m1':'_mock_metric', 'm2':'_mock_metric'},
                                   'params':{'param1':[1,2,3], 'param2':(0,1), 'param3':['p1', 'p2']},
                                   'fit_params':{'param1':1, 'param2':'a'},
                                   'pred_params':{'param1':2, 'param2':'b'},
                                   'preprocessing':{'pp1':'_mock_tran', 'pp2':'_mock_tran'},
                                   'trials':[{'param1':1, 'param2':0.01, 'param3':'p1', 'm1':0.1, 'm2':0.2},
                                             {'param1':2, 'param2':0.02, 'param3':'p2', 'm1':0.2, 'm2':0.3}]
                                  }


def test_trials_from_spec(test_spec_fixture):
    test_spec = Spec('test_spec', _mock_fit_pred, _mock_fit_pred, {'m1':_mock_metric, 'm2':_mock_metric},
                     {'param1':[1,2,3], 'param2':(0,1), 'param3':['p1', 'p2']}, {'param1':1, 'param2':'a'},
                     {'param1':2, 'param2':'b'}, {'pp1':_mock_tran, 'pp2':_mock_tran})
    
    test_spec.trials_from_spec(test_spec_fixture)

    assert test_spec.trials == [{'param1':1, 'param2':0.01, 'param3':'p1', 'm1':0.1, 'm2':0.2},
                                             {'param1':2, 'param2':0.02, 'param3':'p2', 'm1':0.2, 'm2':0.3}]
    
    test_spec.trials_from_spec(test_spec_fixture)

    assert test_spec.trials == [{'param1':1, 'param2':0.01, 'param3':'p1', 'm1':0.1, 'm2':0.2},
                                             {'param1':2, 'param2':0.02, 'param3':'p2', 'm1':0.2, 'm2':0.3},
                                             {'param1':1, 'param2':0.01, 'param3':'p1', 'm1':0.1, 'm2':0.2},
                                             {'param1':2, 'param2':0.02, 'param3':'p2', 'm1':0.2, 'm2':0.3}]
    
    test_spec.trials_from_spec(test_spec_fixture, replace=True)

    assert test_spec.trials == [{'param1':1, 'param2':0.01, 'param3':'p1', 'm1':0.1, 'm2':0.2},
                                             {'param1':2, 'param2':0.02, 'param3':'p2', 'm1':0.2, 'm2':0.3}]


def test_names_to_callables(test_spec_fixture):
    test_spec = Spec()

    mapping = [_mock_fit_pred, _mock_metric, _mock_tran]

    test_spec.load_spec(test_spec_fixture)

    test_spec.names_to_callables(mapping)

    assert test_spec.to_dict() == {'spec_name':'test_spec',
                                   'fit':_mock_fit_pred,
                                   'pred':_mock_fit_pred,
                                   'metrics':{'m1':_mock_metric, 'm2':_mock_metric},
                                   'params':{'param1':[1,2,3], 'param2':(0,1), 'param3':['p1', 'p2']},
                                   'fit_params':{'param1':1, 'param2':'a'},
                                   'pred_params':{'param1':2, 'param2':'b'},
                                   'preprocessing':{'pp1':_mock_tran, 'pp2':_mock_tran},
                                   'trials':[{'param1':1, 'param2':0.01, 'param3':'p1', 'm1':0.1, 'm2':0.2},
                                             {'param1':2, 'param2':0.02, 'param3':'p2', 'm1':0.2, 'm2':0.3}]
                                  }