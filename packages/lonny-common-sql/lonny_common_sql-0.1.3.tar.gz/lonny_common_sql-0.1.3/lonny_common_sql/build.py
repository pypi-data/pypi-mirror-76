from .config import Configuration

class Wrapper:
    def __init__(self):
        self.counter = 0
        self.params  = dict()
    def __call__(self, val):
        if callable(val):
            return val(self)
        self.counter += 1
        param_key = f"param_{self.counter}"
        self.params[param_key] = val
        return Configuration.format_fn(param_key)

def build(query_fn):
    wrapper = Wrapper()
    return query_fn(wrapper), wrapper.params