from pytest import raises
import numpy as np
import TimeSeries as TS
from lazy import *

testSeries = TS.TimeSeries(range(0,4),range(1,5))

def test_len():
    assert len(testSeries) == 4

def test_contains():
    assert (2 in testSeries) == True

def test_getitem():
    assert testSeries[0] == 1

def test_setitem():
    tmpTestSeries = TS.TimeSeries(range(0,4),range(1,5))
    tmpTestSeries[0]=5
    assert tmpTestSeries[0] == 5

def test_equal():
    tmpTestSeries = TS.TimeSeries(range(0,4),range(1,5))
    assert tmpTestSeries == testSeries

def test_values():
    assert np.array_equal(testSeries.values(), range(1,5)) == True

def test_time():
    assert np.array_equal(testSeries.times(), range(0,4)) == True

@lazy
def check_length(a,b):
    return len(a)==len(b)

def test_check_length():
    thunk = check_length(TS.TimeSeries(range(0,4),range(1,5)).lazy, TS.TimeSeries(range(1,5),range(2,6)))
    assert thunk.eval()==True
