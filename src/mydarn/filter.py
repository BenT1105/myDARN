import numpy as np
import copy

class Filter:
    """
    Provides methods to filter SuperDARN data by a chosen parameter within a specified range.
    
    Methods:
    --------
        filter_fitacf_gates
            Filter FITACF data by range gate limits.
            
    Dependencies:
    -------------
        - NumPy
        - copy
    """
    
    @staticmethod
    def filter_fitacf_gates(data, gate_min, gate_max):
        """
        Filters SuperDARN FITACF data by range gate.
        
        Parameters:
        -----------
            data: list of dict
                A list of SuperDARN FITACF records.
            
            gate_min: int
                Minimum range gate (0 to 74), inclusive.
            
            gate_max: int
                Maximum range gate (0 to 74), inclusive.
        
        Returns:
        --------
            filtered_data: list of dict
                FITACF records that fall within the specified range gate limits.
        """
        
        filtered_data = []
        
        for i in range(len(data)):
            ## Ensure slist exists and is not empty
            if 'slist' not in data[i]:
                continue
            
            slist = np.asarray(data[i]['slist'])
            if len(slist) == 0:
                continue
            
            ## Build mask for gates in requested range
            slist_mask = (slist >= gate_min) & (slist <= gate_max)
            
            if not slist_mask.any():
                continue
            
            ## Deep copy the data
            data_copy = copy.deepcopy(data[i])
            
            for key, value in data[i].items():
                ## Convery lists to arrays
                if type(value) == list or type(value) == np.ndarray:
                    vector_field = np.asarray(value)
                    
                    ## Only filter 1D arrays with the same length as slist
                    if vector_field.shape[0] == len(slist):
                        new_vector_field = vector_field[slist_mask]
                        
                        ## Preserve original type
                        if type(value) == list:
                            data_copy[key] = new_vector_field.tolist()
                        
                        else:
                            data_copy[key] = new_vector_field
                            
            ## Update nrang
            if 'nrang' in data_copy:
                data_copy['nrang'] = gate_max - gate_min + 1
                
            filtered_data.append(data_copy)
            
        return filtered_data