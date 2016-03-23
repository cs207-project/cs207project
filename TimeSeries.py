import numpy as np
from lazy import *
import numbers

class TimeSeries():
    '''
    """
Help on package TimeSeries:

NAME
    TimeSeries

DESCRIPTION
    TimeSeries
    =====
    
    Provides
      1. An sequence or any iterable objects
    
    How to use the documentation
    ----------------------------
    Documentation is available in two forms: docstrings provided
    with the code, and a loose standing reference guide, available from
    `the TimeSeries homepage <https://github.com/cs207-project>`_.
    
    We recommend exploring the docstrings using
    `IPython <http://ipython.scipy.org>`_, an advanced Python shell with
    TAB-completion and introspection capabilities.  See below for further
    instructions.
    
    The docstring examples assume that `numpy` has been imported as `np`::  

    
     |  Methods inherited from builtins.RuntimeWarning:
     |  
     |  __init__(self, *args, **kwargs)
     |      Initialize self.  See help(type(self)) for accurate signature.
     |      Stors a TimeSeries in self.TimeSeries_
     |    
     |  __repr__(self, /)
     |      Return a printable sequence shown in python list format containing all values in [self].
     |  
     |  __str__(self, /)
     |      Return a printable abbreviated sequence of maximum first 100 entrees.
     |  
     |  __getitem__(self, index)
     |      Return self[index]
     |
     |  __setitem__(self, index, values)
     |      Set self[index] = values
     |
     |  __len__(self)
     |      Return len(self.TimeSeries_)
     '''
    def __init__(self, times, values):
        """

        This initialise the Time Series Class by passing into the "times" and "values" lists

        Note
        ----
        The times and values must be of the same in length, and they can both be empty.

        Parameters
        ----------
        times : list of floats
            sequence of time values represented as float
        values : list of floats
            sequence of values corresponding to each time value

        """
        if (iter(times) and iter(values)):
            # reorder according to Time step
            idx = np.argsort(times)
            times = np.array(times)[idx]
            values = np.array(values)[idx]

            self._TimeSeries=np.vstack((times,values))
            self._vindex = 0
            self._values = self._TimeSeries[1]
            self._times = self._TimeSeries[0]
    
    @property
    @lazy

    def lazy(self):

        return self

    def itervalues(self):
        for v in self._values:
            yield v

    def itertimes(self):
        for t in self._times:
            yield t

    def iteritems(self):
        for t,v in zip(self._times,self._values):
            yield (t,v)
            
    def __len__(self):
        return len(self._TimeSeries[0])
    
    def __contains__(self, time):
        index = np.where(self._TimeSeries[0]==time)
        return index[0].size>0
            
    
    def __getitem__(self,time):
        if (time in self):
            index = np.where(self._TimeSeries[0]==time)
            return self._TimeSeries[1][index]
        else:
            print ("no time point at t={0}".format(time))

    def __setitem__(self,time,value):
        if (time in self):
            index = np.where(self._TimeSeries[0]==time)
            self._TimeSeries[1][index]=value
        else:
            print ("no time point at t={0}".format(time))
            
    def __iter__(self):
        return iter(self._TimeSeries[1])
    
    def __repr__(self):
        return "%r"%(self._TimeSeries)
    
    def __str__(self):
        className = type(self).__name__
        if len(self)>100:
            return "%s" %('['+(str(self._values[:99]))[1:-1]+'...'+']')
        else:
            return "%s" %(self._TimeSeries)
        
    def __eq__(self, other):
        return np.array_equal(self._TimeSeries, other._TimeSeries)
        
    def values(self):
        return self._values
    
    def times(self):
        return self._times
    
    def mean(self):        
        if(len(self._values) == 0):
            raise ValueError("cant calculate mean of length 0 list")
        return np.mean(self._values)
    
    def median(self):
        '''
        Getting the median of self.values

        Returns
        -------
        float
            the median of self.values

        Raises
        ------
        ValueError
            If self.values is empty
        '''
        if(len(self._values) == 0):
            raise ValueError("cant calculate median of length 0 list")
        return np.median(self._values)
    
    def interpolate(self, times):
        '''
        Filling the TimeSeries class with a given list of times using linear interpolation

        Parameters
        ----------
        times: list of float
            a list of times to be added to self

        Returns
        -------
        TimeSeries
             New TimeSeries instance with parameter 'times' and interpolated 'values' added

        '''
        new_values = []
        for time in times:
            if time > self._times[-1]: # over the rightest boundary
                new_values.append(self._values[-1])
            elif time < self._times[0]: # over the leftest boundary
                new_values.append(self._values[0])
            elif time in self._times:
                new_values.append(self.__getitem__(time))
            else : #within boundary
                for i in range(len(self._times)):
                    if self._times[i] > time:
                        left_value = self._values[i-1]
                        right_value = self._values[i]
                        left_time = self._times[i-1]
                        right_time = self._times[i]
                        #interpolate
                        new_values.append(left_value + (right_value - left_value)/(right_time - left_time)*(time - left_time))
                        break
        return TimeSeries(times, new_values)
        
    def checkTime(self,rhs):
        '''
        Tool function checking wether the given parameter 'rhs' and self have the same time points

        Parameters
        ----------
        rhs: TimeSeries
            TimeSeries instance to be compared with self on 'times' list

        Returns
        -------
        bool
             True if rhs and self have the same 'times' list, False otherwise

        '''
        return np.array_equal(self._times, rhs._times)

    def __add__(self, rhs):
        '''
        Elementwise add operation

        Parameters
        ----------
        rhs: TimeSeries
            TimeSeries instance with the same 'times' points for TimeSeries addition, applied only on 'values' list

        Returns
        -------
        TimeSeries
             result of TimeSeries Class added by parameter 'rhs'

        Raises
        ------
        TypeError
            If values in rhs are not real number
        ValueError
            If time points in self and rhs do not match

        '''
        try:
            
            if isinstance(rhs, numbers.Real):

                return TimeSeries(self._times, rhs + self._values)

            elif self.checkTime(rhs) == True:

                return TimeSeries(self._times, rhs._values + self._values)
            
            else:
                
                raise ValueError(str(self)+' and '+str(rhs)+' must have the same time points')
        except TypeError:
            
            raise NotImplemented


    def __radd__(self, other):
        '''
        other + self delegates to __add__

        Parameters
        ----------
        other : TimeSeries
            TimeSeries instance for TimeSeries addition

        Returns
        -------
        TimeSeries
             result of self added by parameter 'other', 'values' of which are the sum of two 'values' lists
        '''
        return self + other

    def __sub__(self, rhs):

        '''
        Elementwise subtract operation

        Parameters
        ----------
        rhs: TimeSeries
            TimeSeries instance with the same 'times' points for TimeSeries subtraction, applied only on 'values' list

        Returns
        -------
        TimeSeries
             result of TimeSeries Class subtracted by parameter 'rhs'

        Raises
        ------
        TypeError
            If values in rhs are not real number
        ValueError
            If time points in self and rhs do not match

        '''

        try:
            if isinstance(rhs, numbers.Real):
                return TimeSeries(self._times, self._values - rhs)
            elif self.checkTime(rhs) == True:
                return TimeSeries(self._times, self._values - rhs._values )
            else:
                
                raise ValueError(str(self)+' and '+str(rhs)+' must have the same time points')
        except TypeError:
            raise NotImplemented

    def __mul__(self, rhs):
        '''
        Elementwise multiply operations

        Parameters
        ----------
        rhs: TimeSeries
            TimeSeries instance with the same 'times' points for multiplication, applied only on 'values' list

        Returns
        -------
        TimeSeries
             result of TimeSeries Class multiplied by parameter 'rhs'

        Raises
        ------
        TypeError
            If values in rhs are not real number
        ValueError
            If time points in self and rhs do not match
        '''
        try: 
            if isinstance(rhs, numbers.Real):
                return TimeSeries(self._times, self._values * rhs)
            
            elif self.checkTime(rhs)==True: # same length
                return TimeSeries(self._times, self._values * rhs._values)
                
            else:
                raise ValueError(str(self)+' and '+str(rhs)+' must have the same time points')
        
        except TypeError:
            raise NotImplemented


    def __rmul__(self, other):
        '''
        other * self delegates to __mul__
        Parameters
        ----------
        other : TimeSeries
            TimeSeries instance for TimeSeries multiplication

        Returns
        -------
        TimeSeries
             result of TimeSeries Class multiplied by parameter 'other'
        '''

        return self * other

    def __abs__(self):
        '''
        Returns
        -------
        float
            The square root of the sum of all squared values in TimeSeries values list
        '''

        return np.sqrt(np.sum(np.power(self._values,2)))

    def __bool__(self):
        '''
        Returns
        -------
        bool
            True if the abs value of TimeSeries is greater than zero, False otherwise
        '''
        return bool(abs(self))

    def __neg__(self):
        '''
        Returns
        -------
        TimeSeries
            the TimeSeries instance with the same 'times' list but negative (opposite sign) 'values' list
        '''
        return TimeSeries(self._times,-1*self._values)
        
    def __pos__(self):
        '''
        Returns
        -------
        TimeSeries
            the TimeSeries instance itself
        '''
        return (self)
