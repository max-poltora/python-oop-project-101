def memoized(func):
    def wrapper(*args):
        wrapper.arg = args[1] if len(args)>1 else None
        wrapper.called = True
        return func(*args)
    wrapper.called = False
    return wrapper

class Validator:
    
    def __init__(self):
        self.Object = None
    
    def string(self):
        self.Object = type(self.__class__.__name__, (), {'required': self.required,
                                                         'contains': self.contains,
                                                         'is_valid': self.is_valid,
                                                         'TYPE': str})
        return self.Object
    
    @memoized
    def required(self):
        pass
    
    @memoized
    def contains(self, substring):
        return self.Object
    
    def is_valid(self, string):
        if not self.required.called:
            return True
        if self.required.called: 
            check = string=='' or string==None
            if check:
                return False
            if self.contains.called:
                return self.contains.arg in string
        return isinstance(string, self.Object.TYPE)
    
    
