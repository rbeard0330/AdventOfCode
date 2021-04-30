import dataclasses




def build_vector_class(n, frozen=True):
    methods = {__add__, vect_addition}
    
    def vect_addition(self, other):
        
        result_attrs = {}
        return self.__class__()