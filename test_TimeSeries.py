from pytest import raises
import TimeSeries as TS
from lazy import *

@lazy
def check_length(a,b):
    return len(a)==len(b)
thunk = check_length(TS.TimeSeries(range(0,4),range(1,5)).lazy, TS.TimeSeries(range(1,5),range(2,6)))
assert thunk.eval()==True
