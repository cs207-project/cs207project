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

def test_mean_empty():
    with raises(ValueError):
         TS.TimeSeries([],[]).mean() 

def test_median_empty():
    with raises(ValueError):
         TS.TimeSeries([],[]).median()

def test_mean():
    assert testSeries.mean() == 2.5

def test_median():
    assert testSeries.median() == 2.5

def test_interpolation():
    a = TS.TimeSeries([0,5,10], [1,2,3])
    b = TS.TimeSeries([2.5,7.5], [100, -100])
    # Simple cases
    assert a.interpolate([1]) == TS.TimeSeries([1],[1.2])
    assert a.interpolate(b.times()) == TS.TimeSeries([2.5,7.5], [1.5, 2.5])
    # Boundary conditions
    assert a.interpolate([-100,100]) == TS.TimeSeries([-100,100],[1,3])

@lazy
def check_length(a,b):
    return len(a)==len(b)

def test_check_length():
    thunk = check_length(TS.TimeSeries(range(0,4),range(1,5)).lazy, TS.TimeSeries(range(1,5),range(2,6)))
    assert thunk.eval()==True
