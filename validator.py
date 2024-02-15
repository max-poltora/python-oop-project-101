
def memoized(func):
    def wrapper(self, *args):
        if not hasattr(self, '_called'):
            self._called = {}
        self._called[func.__name__] = args
        return func(self, *args)
    return wrapper

class Validator:
    
    def string(self):
        return Validator.StringObject()
    
    def number(self):
        return Validator.NumberObject()
    
    def list(self):
        return Validator.ListObject()
    
    
    class StringObject:
        
        def __init__(self):
            self.TYPE = str
        
        @memoized
        def required(self):
            pass
        
        @memoized
        def contains(self, substring):
            return self
        
        @memoized
        def min_len(self, string_len:int):
            return self
        
        def is_valid(self, string):
            try:
                calls = self._called.keys()
            except AttributeError: # type object 'StringObject' has no attribute '_called' - none of functions was called
                if string == None:
                    return True
                else:
                    return isinstance(string, self.TYPE)
            
            if 'required' in calls and string=='' or string==None:
                return False
            
            if 'contains' in calls:
                return self._called.get('contains') in string
            
            if 'min_len' in calls:
                return len(string) >= self._called.get('min_len')
            
            return isinstance(string, self.TYPE)
    
        
    class NumberObject:
        
        def __init__(self):
            self.TYPE = int
        
        @memoized
        def required(self):
            pass
        
        @memoized
        def positive(self):
            return self
        
        @memoized
        def range(self, start, end):
            pass
        
        def is_valid(self, number):
            try:
                calls = self._called.keys()
            except AttributeError: # type object 'NumbergObject' has no attribute '_called' - none of functions was called
                if number == None:
                    return True
                else:
                    return isinstance(number, self.TYPE)
            
            if 'required' in calls and number==None:
                return False
            
            if 'positive' in calls:
                return number>=0
            
            if 'range' in calls:
                start, end = self._called.get('range')
                if 'positive' in calls:
                    return number>=0 and number in range(start, end+1)
                else:
                    return number in range(start, end+1)
            
            return isinstance(number, self.TYPE)
    
    
    class ListObject:
        
        def __init__(self):
            self.TYPE = list
            
        @memoized
        def required(self):
            return self
        
        @memoized
        def sizeof(self, size):
            print(isinstance(size, int))
            return self
        
        def is_valid(self, lst):
            try:
                calls = self._called.keys()
            except AttributeError: # type object 'ListObject' has no attribute '_called' - none of functions was called
                if lst == None:
                    return True
                else:
                    return isinstance(lst, self.TYPE)
            
            if 'required' in calls and lst==None:
                return False
            
            if 'sizeof' in calls:
                return len(lst) == self._called.get('sizeof')[0]
            
            return isinstance(lst, self.TYPE)