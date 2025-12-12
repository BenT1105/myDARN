import pydarn
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

class Scatter:
    """
    Generates scatter plots for SuperDARN data.
    
    Methods:
    --------
        plot_range_scatter
            Plot a scatter plot of a selected vector field parameter as a function of range gate number.
            
    Dependencies:
    -------------
        - pyDARN
        - NumPy
        - matplotlib
        datetime
    """
    
    @staticmethod
    def plot_range_scatter(parameter, data, groundscatter = False, beam_num = 'all'):
        """
        Plots a scatter plot of the specified vector field parameter on the y-axis and range gate number on the x-axis.
        
        Parameters:
        -----------
            parameter: str
                Key name of the vector field parameter to plot.
                Supported quantities include:
                    - Line of sight velocity ('v')
                    - Power ('p_l')
                    - Spectral width ('w_l')
                    - Elevation angle ('elv')
                    - Lag-zero power ('pwr0')
                    - Phase offset ('phi0')
            
            data: list of dict
                A list of SuperDARN FITACF or RAWACF records.
            
            groundscatter: bool
                If True, ground scatter values for the specified parameter are plotted in a separate scatter plot.
                Default: False
            
            beam_num: int or str
                If an int, selects data from a single beam number (0 to 15).
                If a str, data from all beam numbers are included.
                Default: 'all'
        
        Returns:
        --------
            None
        
        Raises:
        -------
            KeyError
            ValueError
        """
             
        ## ---------------
        ## Check Parameter
        ## ---------------
        
        key_error = True
        
        for i in range(len(data)):
            if parameter in data[i] and type(data[i][parameter]) is np.ndarray:
                key_error = False
                break

        if key_error:
            raise KeyError('Unknown vector feild parameter: {key}'.format(key = parameter))
            
        ## --------------------
        ## Check Ground Scatter
        ## --------------------   
        
        if groundscatter:
            gflg_error = True
        
            for i in range(len(data)):
                if 'gflg' in data[i]:
                    gflg_error = False
                    break
            
            if gflg_error:
                raise KeyError('Ground scatter unavailable')
            
            for i in range(len(data)):
                try:
                    if len(data[i][parameter]) != len(data[i]['gflg']):
                        raise KeyError('Ground scatter unavailable for parameter: {key}'.format(key = parameter))
                
                except KeyError:
                    continue
                
        ## ----------
        ## Check Beam
        ## ----------
        
        if (beam_num not in range(0, 16) and beam_num != 'all'):
            raise ValueError('Beam number invalid')

        ## -----------
        ## Gather Data
        ## -----------
        
        vals, vals_gs = [], []
        gates, gates_gs = [], []
        
        for i in range(len(data)):
            try:
                if beam_num != 'all' and beam_num != data[i]['bmnum']:
                    continue

                for j in range(len(data[i][parameter])):
                    value = data[i][parameter][j]
                    gate = data[i]['slist'][j]
                    
                    if np.isnan(value) or np.isinf(value):
                        continue

                    if groundscatter and data[i]['gflg'][j] == 1:
                        vals_gs.append(value)
                        gates_gs.append(gate)
                        
     
                    else:
                        vals.append(value)
                        gates.append(gate)

            except KeyError:
                continue
        
        ## ----------
        ## Check Data
        ## ----------
        
        if np.all(np.isnan(vals)) or len(vals) == 0:
            raise ValueError("No data to plot")
            
        if groundscatter:
            if np.all(np.isnan(vals_gs)) or len(vals_gs) == 0:
                raise ValueError("No data to plot")
                
        ## -----------------
        ## Plot Scatter Plot
        ## -----------------
        
        fig1, ax1 = plt.subplots()
        ax1.scatter(gates, vals, marker = '.', s = 1, color = 'blue')
        
        if groundscatter:
            fig2, ax2 = plt.subplots()
            ax2.scatter(gates_gs, vals_gs, marker = '.', s = 1, color = 'red')
        
        ## -----------
        ## Plot Titles
        ## -----------
        
        radar_name = pydarn.SuperDARNRadars.radars[pydarn.RadarID(data[0]['stid'])].name
        start_date = datetime.strftime(datetime(data[0]['time.yr'], data[0]['time.mo'], data[0]['time.dy']), '%Y %b %d')
        end_date = datetime.strftime(datetime(data[-1]['time.yr'], data[-1]['time.mo'], data[-1]['time.dy']), '%Y %b %d')
        
        if start_date == end_date:
            date = '{start}'.format(start = start_date)
        else:
            date = '{start} to {end}'.format(start = start_date, end = end_date)
        
        parameters = {'v': ('Line of Site Velocity', '[m s$^{-1}$]'),
                      'p_l': ('Power', '[dB]'),
                      'w_l': ('Spectral Width', '[m s$^{-1}$]'),
                      'elv': ('Elevation Angle', '[deg]'),
                      'pwr0': ('Lag Zero Power', '[dB]'),
                      'phi0': ('Phase Offset', '[rad]')}
        
        try:
            title = '{name} {date}\n{key}'.format(name = radar_name, date = date, key = parameters[parameter][0])
            ylabel = '{key} {units}'.format(key = parameters[parameter][0], units = parameters[parameter][1])
            
        except KeyError:
            title = '{name} {date}\n{key}'.format(name = radar_name, date = date, key = parameter)
            ylabel = '{key}'.format(key = parameter)
            
        if beam_num != 'all':
            title = title + ': Beam {beam}'.format(beam = beam_num)
            
        ## ------------
        ## Format Plots
        ## ------------
            
        if groundscatter:
            ax1.set_xlabel('Range Gate')
            ax1.set_ylabel(ylabel)
            ax1.set_title('{title} (Ionospheric Scatter)'.format(title = title))
            
            ax2.set_xlabel('Range Gate')
            ax2.set_ylabel(ylabel)
            ax2.set_title('{title} (Ground Scatter)'.format(title = title))

        else:   
            ax1.set_xlabel('Range Gate')
            ax1.set_ylabel(ylabel)
            ax1.set_title(title)
                
        return None