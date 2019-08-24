class Parser:
    import csv
    import numpy as np
    """
    a class parsing file into rows of parameters and initialize functions
    """
    def __init__(self, filename, dtypes, delimiter = ' ', *args, **kwargs):
        self.reader = __read__(filename,delimiter)
        self.dtypes = dtypes
        self.fieldnames = reader.filenames
    
    def __read__(filename, delimiter = ' '):
        try:
            file = open(filename)
            reader = csv.DictReader(file, delimiter = delimiter)
            return reader
        except Exception as e:
            print('Seems like the file doesn\'t exist')
            print(e)
    
    def initialize(self, init_class, callback, pos_index = self._idx(1,5)):
        """
        initialize objects for key mapping, return all initialized obj afterward

        Assume key \'Key\' must be exist
        """
        obj_store = []
        for row in self.reader:

            params = zip(row.values(), self.dtypes)

            typed_params = map(lambda value, dtype : self.np.dtype(value,dtype), params)

            globals.update({row['KEY']:init_class(*typed_params[pos_index])})

            obj_store.append(globals.get(row['KEY'], lambda : None))
        
        return obj_store
    
    def _idx(__from__ = 1, __to__ = 5):
        return [x for x in range(__from__, __to__ + 1)]


