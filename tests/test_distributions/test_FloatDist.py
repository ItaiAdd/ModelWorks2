import pytest
import numpy as np
import decimal

from modelworks2.distributions import FloatDist

STANDARD_SAMPLE_SIZE = 50
STANDARD_LOG_MIN = 0.01
STANDARD_MIN = -100.0
STANDARD_MAX = 100.0
STANDARD_STEP = 2.5

# computing rounding precisions to mitigate floating point errors.
STANDARD_LOG_MIN_PRECISION = abs(decimal.Decimal(STANDARD_LOG_MIN).as_tuple().exponent)
STANDARD_MIN_PRECISION = abs(decimal.Decimal(STANDARD_MIN).as_tuple().exponent)
STANDARD_MAX_PRECISION = abs(decimal.Decimal(STANDARD_MAX).as_tuple().exponent)
STANDARD_STEP_PRECISION = abs(decimal.Decimal(STANDARD_STEP).as_tuple().exponent)


def test_sample_no_step():
    test_dist = FloatDist('test', STANDARD_MIN, STANDARD_MAX)
    samples = test_dist.sample(STANDARD_SAMPLE_SIZE)
    assert np.round(min(samples), STANDARD_MIN_PRECISION) >= STANDARD_MIN
    assert np.round(max(samples), STANDARD_MAX_PRECISION) <= STANDARD_MAX

def test_sample_with_step():
    test_dist = FloatDist('test', STANDARD_MIN, STANDARD_MAX, step=STANDARD_STEP)
    samples = test_dist.sample(STANDARD_SAMPLE_SIZE)
    assert np.round(min(samples), STANDARD_MIN_PRECISION) >= STANDARD_MIN
    assert np.round(max(samples), STANDARD_MAX_PRECISION) <= STANDARD_MAX
    assert np.round(min(np.diff(sorted(np.unique(samples)))), STANDARD_STEP_PRECISION) >= STANDARD_STEP


def test_log_sample_no_step():
    test_dist = FloatDist('test', STANDARD_LOG_MIN, STANDARD_MAX, log=True)
    samples = test_dist.sample(STANDARD_SAMPLE_SIZE)
    assert np.round(min(samples), STANDARD_MIN_PRECISION) >= STANDARD_MIN
    assert np.round(max(samples), STANDARD_MAX_PRECISION) <= STANDARD_MAX


def test_log_sample_with_step():
    test_dist = FloatDist('test', STANDARD_LOG_MIN, STANDARD_MAX, step=STANDARD_STEP, log=True)
    samples = test_dist.sample(STANDARD_SAMPLE_SIZE)
    assert np.round(min(samples), STANDARD_LOG_MIN_PRECISION) >= STANDARD_LOG_MIN
    assert np.round(max(samples), STANDARD_MAX_PRECISION) <= STANDARD_MAX
    assert np.round(min(np.diff(sorted(np.unique(samples)))), STANDARD_STEP_PRECISION) >= STANDARD_STEP


def test_unique_sample_no_step():
    test_dist = FloatDist('test', STANDARD_MIN, STANDARD_MAX)
    samples = test_dist.sample_unique(STANDARD_SAMPLE_SIZE)
    assert np.round(min(samples), STANDARD_MIN_PRECISION) >= STANDARD_MIN
    assert np.round(max(samples), STANDARD_MAX_PRECISION) <= STANDARD_MAX
    assert len(samples) == len(np.unique(samples))


def test_unique_sample_with_step():
    test_dist = FloatDist('test', STANDARD_MIN, STANDARD_MAX, step=STANDARD_STEP)
    samples = test_dist.sample_unique(STANDARD_SAMPLE_SIZE)
    assert np.round(min(samples), STANDARD_MIN_PRECISION) >= STANDARD_MIN
    assert np.round(max(samples), STANDARD_MAX_PRECISION) <= STANDARD_MAX
    assert len(samples) == len(np.unique(samples))
    assert np.round(min(np.diff(sorted(np.unique(samples)))), STANDARD_STEP_PRECISION) >= STANDARD_STEP


def test_log_unique_sample_no_step():
    test_dist = FloatDist('test', STANDARD_LOG_MIN, STANDARD_MAX, log=True)
    samples = test_dist.sample_unique(STANDARD_SAMPLE_SIZE)
    assert np.round(min(samples), STANDARD_LOG_MIN_PRECISION) >= STANDARD_LOG_MIN
    assert np.round(max(samples), STANDARD_MAX_PRECISION) <= STANDARD_MAX
    assert len(samples) == len(np.unique(samples))


def test_log_unique_sample_with_step():
    test_dist = FloatDist('test', STANDARD_LOG_MIN, STANDARD_MAX, log=True, step=STANDARD_STEP)
    samples = test_dist.sample_unique(STANDARD_SAMPLE_SIZE)
    assert np.round(min(samples), STANDARD_LOG_MIN_PRECISION) >= STANDARD_LOG_MIN
    assert np.round(max(samples), STANDARD_MAX_PRECISION) <= STANDARD_MAX
    assert len(samples) == len(np.unique(samples))
    assert np.round(min(np.diff(sorted(np.unique(samples)))), STANDARD_STEP_PRECISION) >= STANDARD_STEP