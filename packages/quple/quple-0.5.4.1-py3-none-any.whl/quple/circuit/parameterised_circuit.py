from abc import ABC, abstractmethod
from inspect import signature
from typing import (Any, Callable, cast, Dict, FrozenSet, Iterable, Iterator,
                    List, Optional, overload, Sequence, Set, Tuple, Type,
                    TYPE_CHECKING, TypeVar, Union)
import sympy as sp
import numpy as np

import cirq
from cirq.ops.gate_features import SingleQubitGate, TwoQubitGate

from quple.circuit.quantum_circuit import QuantumCircuit
from quple.circuit.templates.template_circuit_block import TemplateCircuitBlock
from quple.components.interaction_graphs import interaction_graph
from quple.utils.utils import merge_pqc
from pdb import set_trace
#D. Zhu, Training of quantum circuits on a hybrid quantum computer


#Devices generally operate in the Z basis, so that rotations around the Z axis will become book-keeping measures rather than physical operations on the device.

class ParameterisedCircuit(QuantumCircuit, ABC):
    def __init__(self, n_qubit:int, copies:int=1,
                rotation_blocks:Optional[Union[str, cirq.Gate, Callable, 'TemplateCircuitBlock',
                                               List[str],List[cirq.Gate],List[Callable],
                                               List['TemplateCircuitBlock']]] =None,
                entanglement_blocks:Optional[Union[str, cirq.Gate, Callable, 'TemplateCircuitBlock',
                                               List[str],List[cirq.Gate],List[Callable],
                                               List['TemplateCircuitBlock']]] =None,
                entangle_strategy:Optional[Union[str,List[str], Callable[[int,int],List[Tuple[int]]],
                                                 List[Callable[[int,int],List[Tuple[int]]]]]]=None,
                parameter_symbol:str='θ',
                final_rotation_layer:bool=False,
                auto_assemble:bool=True,
                flatten_circuit:bool=True,
                name:str=None):
        
        super().__init__(n_qubit, name=name)
        self._copies = copies
        self.rotation_blocks = rotation_blocks
        self.entanglement_blocks = entanglement_blocks
        self._entangle_strategy = entangle_strategy or 'full' 
        self._parameter_symbol = parameter_symbol
        self._final_rotation_layer = final_rotation_layer
        self._parameters = np.array([], dtype=object)
        self._readout_qubit = None
        self._flatten_circuit = flatten_circuit
        if auto_assemble:
            self.assemble()
    
    @property
    def readout_qubit(self):
        return self._readout_qubit
            
    @property
    def num_param(self):
        return len(self._parameters)

    def new_param(self, size:int=1) -> sp.Symbol:
        start = self.num_param
        params = np.array([sp.Symbol('%s_%s' % (self.parameter_symbol, i)) \
                          for i in range(start, start+size)])
        self._parameters = np.append(self._parameters, params)
        if len(params) == 1:
            return params[0]
        return params
        
    @property
    def parameters(self):
        return self._parameters
    
    @property
    def flatten_circuit(self):
        return self._flatten_circuit
    
    
    @property
    def copies(self) -> int:
        return self._copies
    
    @property
    def parameter_symbol(self) -> str:
        return self._parameter_symbol
    
    @property
    def entangle_strategy(self):
        return self._entangle_strategy
    
    @property
    def final_rotation_layer(self):
        return self._final_rotation_layer

    @property
    def rotation_blocks(self):
        '''A collection of single qubit gate operations or 
        circuit blocks consisting of multiple single qubit operations
        '''
        return self._rotation_blocks
    
    @rotation_blocks.setter
    def rotation_blocks(self, val):
        val = ParameterisedCircuit._parse_blocks(val)
        ParameterisedCircuit._validate_blocks(val, SingleQubitGate, allow_template=False)
        self._rotation_blocks = val
    
    @property
    def entanglement_blocks(self):
        '''A collection of two qubit gate operations or 
        circuit blocks consisting of multiple single/two qubit operations
        '''
        return self._entanglement_blocks
    
    @entanglement_blocks.setter
    def entanglement_blocks(self, val):
        val = ParameterisedCircuit._parse_blocks(val)
        ParameterisedCircuit._validate_blocks(val, TwoQubitGate)
        self._entanglement_blocks = val
        
    @staticmethod
    def _parse_blocks(blocks) -> List:
        if not blocks:
            return []
        blocks = [blocks] if not isinstance(blocks, list) else blocks
        blocks = [QuantumCircuit._parse_gate_operation(block) \
                  if not isinstance(block, TemplateCircuitBlock) \
                  else block for block in blocks]
        return blocks
    
    @staticmethod
    def _validate_blocks(blocks, gate_feature=None, allow_template=True) -> None:
        for block in blocks:
            if isinstance(block, TemplateCircuitBlock):
                if not allow_template:
                    raise ValueError('template circuit block is not allowed'
                                     'in rotation layer')
                else:
                    continue
            elif isinstance(block, cirq.Gate):
                if gate_feature and \
                    not isinstance(block, gate_feature):
                    raise ValueError('Gate operation {} should be a subclass of '
                                     '{}'.format(type(block), gate_feature))
            elif callable(block):
                n_param = ParameterisedCircuit._get_parameter_count(block)
                if not n_param:
                    raise ValueError('not a valid gate operation or'
                                     'circuit block: {}'.format(block))
                dummy_params = tuple(sp.symarray('x',n_param))
                ParameterisedCircuit._validate_blocks([block(*dummy_params)], gate_feature)
        
    @staticmethod
    def _get_parameter_count(gate_expr) -> int:
        '''Returns the number of parameters required for a gate operation expression
        a gate operation expression can be a cirq.Gate instance, a string that can be mapped
        to a cirq.Gate instance, a function that maps to cirq.Gate or a TemplateCircuitBlock instance
        '''
        if isinstance(gate_expr, cirq.Gate):
            if isinstance(gate_expr, (cirq.XXPowGate, cirq.YYPowGate, cirq.ZZPowGate)):
                return 1
            return 0
        elif isinstance(gate_expr, TemplateCircuitBlock):
            return gate_expr.num_params
        elif callable(gate_expr):
            return len(signature(gate_expr).parameters)
        else:
            raise ValueError('invalid gate expression {} of type {}'.format(gate_expr, type(gate_expr)))

    def get_wavefunction(self, vals:np.ndarray):
        simulator = cirq.Simulator()
        param_resolver = self.get_parameter_resolver(vals)
        return simulator.simulate(self, param_resolver=param_resolver).final_state   
     
    
    def new_layer(self, name:str=None, *args, **kwargs):
        layer = super().new_layer(name, auto_assemble=False, *args, **kwargs)
        layer._parameter_symbol = self.parameter_symbol
        return layer

    def assemble(self):
        self.clear()
        cq = cirq.Circuit()
        for _ in range(self.copies):
            # can't just multiply since parameters won't get incremented
            cq += self.get_rotation_layer()
            cq += self.get_entanglement_layer()
        if self.final_rotation_layer:
            cq += self.get_rotation_layer()
            
        self.assign(cq)
        
        if self.flatten_circuit:
            self.flatten()
    
    def add_readout(self, gate:Union[str, cirq.Gate]='XX',
                    readout_qubit:Optional['cirq.GridQubit']=None):
        parsed_gate = QuantumCircuit._parse_gate_operation(gate)
        readout_qubit = cirq.GridQubit(-1, -1) if readout_qubit is None else readout_qubit
        for qubit in self.qubits:
            final_gate = self.parameterise_gate(parsed_gate)
            self.apply_gate_operation(final_gate, (readout_qubit, qubit))
        if self.flatten_circuit:
            self.flatten()            
        self._readout_qubit = readout_qubit
    
    def readout_measurement(self):
        if self.readout_qubit is None:
            raise ValueError('no readout qubit defined in the circuit')
        return cirq.Z(self.readout_qubit)
        
    def merge(self, other):
        self._moments = merge_pqc([self, other])._moments
        self._parameters = sp.symarray(self.parameter_symbol, len(self.symbols))
        if self.flatten_circuit:
            self.flatten()
                        
    def get_interaction_graphs(self, block_index:int, num_block_qubits:int,
                               entangle_strategy:Optional[Union[str,List[str], Callable[[int,int],List[Tuple[int]]],
                                                 List[Callable[[int,int],List[Tuple[int]]]]]]=None,
                               *args, **kwargs):
        strategy = entangle_strategy if entangle_strategy is not None else self.entangle_strategy
        if isinstance(strategy, str):
            return interaction_graph[strategy](self.n_qubit, num_block_qubits)
        elif callable(strategy):
            return strategy(self.n_qubit, num_block_qubits)
        elif isinstance(strategy, list):
            if all(isinstance(strat, str) for strat in strategy):
                return interaction_graph[strategy[block_index]](self.n_qubit, num_block_qubits)
            elif all(callable(strat) for strat in strategy):
                return strategy[block_index](self.n_qubit, num_block_qubits)
        else:
            raise ValueError('invalid entangle strategy: {}'.format(strategy))
        
    # Devices are generally calibrated to circuits that alternate single-qubit gates with two-qubit gates in each layer. Staying close to this paradigm will often improve performance of circuits.

    def parameterise_gate(self, gate:Union[cirq.Gate, Callable]):
        if isinstance(gate, cirq.Gate):
            if isinstance(gate, (cirq.XXPowGate, cirq.YYPowGate, cirq.ZZPowGate)):
                param = self.new_param()
                return gate**param
            return gate
        else:
            n_param = ParameterisedCircuit._get_parameter_count(gate)
            params = self.new_param(size=n_param)
            params = tuple(params) if isinstance(params, np.ndarray) else (params,)
            return gate(*params)
        
    def add_rotation_layer(self, rotation_blocks:Optional[Union[str, cirq.Gate, Callable,
                                               List[str],List[cirq.Gate],List[Callable],
                                               List['TemplateCircuitBlock']]] =None):
        rotation_blocks = self._parse_blocks(rotation_blocks)
        self._validate_blocks(rotation_blocks, SingleQubitGate, allow_template=False)    
        for block in rotation_blocks:
            for qubit in range(self.n_qubit):
                gate = self.parameterise_gate(block)
                self.apply_gate_operation(gate, qubit)
                
    def add_entanglement_layer(self, entanglement_blocks:Optional[Union[str, cirq.Gate, Callable, 'TemplateCircuitBlock',
                                               List[str],List[cirq.Gate],List[Callable],
                                               List['TemplateCircuitBlock']]] =None,
                entangle_strategy:Optional[Union[str,List[str], Callable[[int,int],List[Tuple[int]]],
                                                 List[Callable[[int,int],List[Tuple[int]]]]]]=None):
        entanglement_blocks = self._parse_blocks(entanglement_blocks)
        self._validate_blocks(entanglement_blocks, TwoQubitGate, allow_template=True)
        for i, block in enumerate(entanglement_blocks):
            if isinstance(block, TemplateCircuitBlock):
                interaction_graphs = self.get_interaction_graphs(i, block.num_block_qubits,
                                                                entangle_strategy)
                for qubits in interaction_graphs:
                    block.build(self, qubits)
            else:
                interaction_graphs = self.get_interaction_graphs(i, 2, entangle_strategy)
                for qubits in interaction_graphs:
                    gate = self.parameterise_gate(block)
                    self.apply_gate_operation(gate, qubits)
    
    def get_rotation_layer(self):
        rotation_layer = self.new_layer('rotation_layer')
        for rotation_block in self.rotation_blocks:
            for qubit in range(self.n_qubit):
                gate = self.parameterise_gate(rotation_block)
                rotation_layer.apply_gate_operation(gate, qubit)
        return rotation_layer

    def get_entanglement_layer(self):
        entanglement_layer = self.new_layer('entanglement_layer')
        for i, entanglement_block in enumerate(self.entanglement_blocks):
            if isinstance(entanglement_block, TemplateCircuitBlock):
                interaction_graphs = self.get_interaction_graphs(i, entanglement_block.num_block_qubits)
                for qubits in interaction_graphs:
                    entanglement_block.build(entanglement_layer, qubits)
            else:
                interaction_graphs = self.get_interaction_graphs(i, 2)
                for qubits in interaction_graphs:
                    gate = self.parameterise_gate(entanglement_block)
                    entanglement_layer.apply_gate_operation(gate, qubits)
    
        return entanglement_layer


    def run_simulator(self, repetitions:int=1):
        pass
        #simulator = cirq.Simulator()
        #simulator.run(resolved_circuit, repetitions=repetitions)
        ## to get wave function:
        #simulator.simulate(resolved_circuit)
        #cirq.measure_state_vector   
        #output_state_vector = simulator.simulate(self, resolver).final_state
        #z0 = cirq.X(q0)
        #qubit_map = {q0: 0, q1: 1}
        #z0.expectation_from_wavefunction(output_state_vector, qubit_map).real