from typing import Callable, Optional
import numpy as np

from quple.data_encoding.pauli_z_expansion import PauliZExpansion

class FirstOrderExpansion(PauliZExpansion):
    def __init__(self, feature_dimension: int,
                 copies:int=2, 
                 encoding_map:Optional[Callable[[np.ndarray], float]] = None,
                 name:str='FirstOrderExpansion', *args, **kwargs):
        '''Create First Order Expansion feature map
        Args:
            feature_dimension: dimension of data to be encoded (=number of qubits in the circuit)
            depth: the number of repetition of the encoding circuit
            encoding_map: data mapping function from R^(feature_dimension) to R
            name: name of circuit
        '''        
        super().__init__(feature_dimension, copies=copies, z_order=1,
                         encoding_map=encoding_map, name=name,
                         *args, **kwargs)