from pytest import raises
import TimeSeries as TS


@lazy
def check_length(a,b):
    return len(a)==len(b)
thunk = check_length(TimeSeries(range(0,4),range(1,5)).lazy, TimeSeries(range(1,5),range(2,6)))
assert thunk.eval()==True
