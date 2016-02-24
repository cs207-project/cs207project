from pytest import raises
import TimeSeries as TS
from lazy import *

testSeries = TS.TimeSeries(range(0,4),range(1,5))

def test_len();
    assert len(testSeries) == 5

def test_contains():
    assert (2 in testSeries) == True

def test_len(

@lazy
def check_length(a,b):
    return len(a)==len(b)

def test_check_length():
    thunk = check_length(TS.TimeSeries(range(0,4),range(1,5)).lazy, TS.TimeSeries(range(1,5),range(2,6)))
    assert thunk.eval()==True
