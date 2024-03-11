def memoized(func):
    def wrapper(self, *args):
        if not hasattr(self, '_called'):
            self._called = {}
        self._called[func.__name__] = args[0] if args else True
        return func(self, *args)
    return wrapper

class UserValidator:
    
    VALIDATOR = {}
    
    def add_validator(self, validator_type, func_name, func):
        self.VALIDATOR[func_name] = func


class Validator(UserValidator):
       
    def string(self):
        return Validator.StringObject()
    
    def number(self):
        return Validator.NumberObject()
    
    def list(self):
        return Validator.ListObject()
    
    def dict(self):
        return Validator.DictObject()    
    
    
    class StringObject(UserValidator):
        
        def __init__(self):
            self.TYPE = str
            super().VALIDATOR
        
        @memoized
        def required(self):
            return self
        
        @memoized
        def contains(self, substring):
            return self
        
        @memoized
        def min_len(self, string_len:int):
            return self
        
        @memoized
        def test(self, func_name, pattern):
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
            
            if 'test' in calls:
                func_name, pattern = self._called.get('test')
                return self.VALIDATOR[func_name](string, pattern)
            
            return isinstance(string, self.TYPE)
    
        
    class NumberObject(UserValidator):
        
        def __init__(self):
            self.TYPE = int
            super().VALIDATOR
        
        @memoized
        def required(self):
            self
        
        @memoized
        def positive(self):
            return self
        
        @memoized
        def range(self, start, end):
            pass
        
        @memoized
        def test(self, func_name, threshold):
            return self
        
        def is_valid(self, number):
            try:
                calls = self._called.keys()
            except AttributeError: # type object 'NumbergObject' has no attribute '_called' - none of functions was called
                if number == None:
                    return True
                else:
                    return isinstance(number, self.TYPE)
            
            if 'required' not in calls and number==None:
                return True
            
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
            
            if 'test' in calls:
                func_name, threshold = self._called.get('test')
                return self.VALIDATOR[func_name](number, threshold)
                
            
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
        
        
    class DictObject:
        
        def __init__(self):
            self.TYPE = dict
            self.SCHEMAS = []
        
        def shape(self, d_shape:dict):
            self.SCHEMAS = d_shape.values()
            return self
        
        def is_valid(self, d):
            values = d.values()
            result = []
            for schema, value in zip(self.SCHEMAS, values):
                result.append(schema.is_valid(value))
            
            return all(result)
    
    