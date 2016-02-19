class LazyOperation():
    def __init__(self, function, *args, **kwargs):
        self.function = function
        self.args = args
        self.kwargs = kwargs
        
    def eval(self):
        if isinstance(self.args[0][0], LazyOperation):
            temp1 = self.args[0][0].eval()
        else:
            temp1 = self.args[0][0]
        if isinstance(self.args[0][1], LazyOperation):
            temp2 = self.args[0][1].eval()
        else:
            temp2 = self.args[0][1]

        return self.function(temp1, temp2)

def lazy(old_function):
    def wrapper(*args, **kwargs):
        return LazyOperation(old_function, args, kwargs)
    return wrapper