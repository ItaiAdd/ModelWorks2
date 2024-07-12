import pytest
import os
import sys

parent = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent)

from modelworks2.spec import Spec


test_input_csv = os.path.join(parent, 'tests/test-input.csv')


def _mock_fit_pred():
    pass


def test_trials_from_csv():
    test_spec = Spec('test_spec', _mock_fit_pred, _mock_fit_pred)
    test_spec.trials_from_csv(test_input_csv)

    assert test_spec.trials == [{'param1_str':'str_p1', 'param2_int':1, 'param3_flt':0.1 ,'metric_1':0.01, 'metric_2':0.001},
                                {'param1_str':'str_p2', 'param2_int':2, 'param3_flt':0.2 ,'metric_1':0.02, 'metric_2':0.002}]
    
    test_spec.trials_from_csv(test_input_csv)

    assert test_spec.trials == [{'param1_str':'str_p1', 'param2_int':1, 'param3_flt':0.1 ,'metric_1':0.01, 'metric_2':0.001},
                                {'param1_str':'str_p2', 'param2_int':2, 'param3_flt':0.2 ,'metric_1':0.02, 'metric_2':0.002},
                                {'param1_str':'str_p1', 'param2_int':1, 'param3_flt':0.1 ,'metric_1':0.01, 'metric_2':0.001},
                                {'param1_str':'str_p2', 'param2_int':2, 'param3_flt':0.2 ,'metric_1':0.02, 'metric_2':0.002}]
    

def test_trials_from_csv_append():
    test_spec = Spec('test_spec', _mock_fit_pred, _mock_fit_pred)
    test_spec.add_trial({'param1_str':'str_p1', 'param2_int':1, 'param3_flt':0.1 ,'metric_1':0.01, 'metric_2':0.001})

    test_spec.trials_from_csv(test_input_csv)

    assert test_spec.trials == [{'param1_str':'str_p1', 'param2_int':1, 'param3_flt':0.1 ,'metric_1':0.01, 'metric_2':0.001},
                                {'param1_str':'str_p1', 'param2_int':1, 'param3_flt':0.1 ,'metric_1':0.01, 'metric_2':0.001},
                                {'param1_str':'str_p2', 'param2_int':2, 'param3_flt':0.2 ,'metric_1':0.02, 'metric_2':0.002}]
    

def test_trials_from_csv_replace():
    test_spec = Spec('test_spec', _mock_fit_pred, _mock_fit_pred)
    test_spec.add_trial({'param1_str':'str_p1', 'param2_int':1, 'param3_flt':0.1 ,'metric_1':0.01, 'metric_2':0.001})

    test_spec.trials_from_csv(test_input_csv, replace=True)

    assert test_spec.trials == [{'param1_str':'str_p1', 'param2_int':1, 'param3_flt':0.1 ,'metric_1':0.01, 'metric_2':0.001},
                                {'param1_str':'str_p2', 'param2_int':2, 'param3_flt':0.2 ,'metric_1':0.02, 'metric_2':0.002}]


