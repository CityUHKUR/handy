from yaml import Loader,Reader,Scanner,Parser,Composer,Constructor,Resolver
class quickLoader(Reader,Scanner,Parser,Composer,Constructor,Resolver):
    def __init__(self, stream, *args, **kwargs):
        Reader.__init__(self,stream)
        Scanner.__init__(self)



class Loader()
class Parser:
    try:
        import yaml
    except ImportError:
        from yaml import Loader as Loader, CDumper as Dumper
    import numpy as np
    """
    a class parsing file into rows of parameters and initialize functions
    """
    def __init__(self, filename, init_class, callback : callable, *args, **kwargs):
        
        self.reader = __read__(filename)
        self.dtypes = dtypes
        self.fieldnames = reader.filenames
    
    def __read__(self,filename):
        try:
            file_stream = open(filename)
            data = self.yaml.load_all(file_stream)
            return data
        except Exception as e:
            print('Seems like the file doesn\'t exist')
            print(e)
    
    def initialize(self, ):
        """
        initialize objects for key mapping, return all initialized obj afterward

        Assume key \'Key\' must be exist
        """
        obj_store = []
        for row in self.reader:

            params = zip(list(row.values()), self.dtypes)

            typed_params = map(lambda value, dtype : self.np.dtype(value,dtype), params)

            globals.update({row['KEY']:init_class(*[typed_params[i] for i in pos_index ],callback = callback)})

            obj_store.append(globals.get(row['KEY']))
        
        return obj_store
    
    def _idx(__from__ = 1, __to__ = 5):
        return [x for x in range(__from__, __to__ + 1)]


