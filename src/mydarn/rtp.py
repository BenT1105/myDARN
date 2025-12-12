import pydarn
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

class RTP:
    """
    Generates time series plots of vector and scalar fiel parameters for SuperDARN data.
    
    Methods:
    --------
        plot_vector_time_series
            Plot the time series of a selected vector field parameter for a given range gate and beam number.
        
        plot_scalar_time_series
            Plot the time series of a selected scalar field parameter for a given beam number.
    
    Dependencies:
    -------------
        - pyDARN
        - NumPy
        - matplotlib
        - datetime
    """
    
    @staticmethod
    def plot_vector_time_series(parameter, data, beam_num, gate_num, groundscatter = False):
        """
        Plots a time series of the specified vector field parameter for a given range gate and beam number.
            
        Future Work:
        ------------
            - Plot the time series of the specified vector field parameter across all range gates for a given beam number, or across all beam numbers for a given range gate.
            - Plot the time series of the specified vector field parameter averaged across a specified range gate or beam number.
            
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
                
            beam_num: int
                Beam number (0 to 15) of the data to plot.
                
            gate_num: int
                Range gate number (0 to 74) of the data to plot.
                
            groundscatter: bool
                If True, ground scatter values for the specified parameter are plotted separately from ionospheric scatter.
                Default: False
            
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
                        raise ValueError('Ground scatter plot unavailable')
                    
                except KeyError:
                    continue
                
        ## --------------------------
        ## Check Beam and Gate Number
        ## --------------------------
            
        if beam_num not in range(0, 16) or gate_num not in range(0, 75):
            raise ValueError('Beam or gate number invalid')  
        
        ## -----------
        ## Gather Data
        ## -----------

        x, y = [], []
        x_gs, y_gs = [],  []

        for i in range(len(data)):
            try:
                if beam_num != data[i]['bmnum']:
                    continue

                for j in range(len(data[i]['slist'])):
                    if gate_num != data[i]['slist'][j]:
                        continue
                    
                    value = data[i][parameter][j]
                    time = datetime(data[i]['time.yr'], data[i]['time.mo'], data[i]['time.dy'], data[i]['time.hr'], data[i]['time.mt'], data[i]['time.sc'])
                    
                    if np.isnan(value) or np.isinf(value):
                        continue

                    if groundscatter and data[i]['gflg'][j] == 1:
                        x_gs.append(time)
                        y_gs.append(value)
     
                    else:
                        x.append(time)
                        y.append(value)

            except KeyError:
                continue

        ## ----------
        ## Check Data
        ## ----------
        
        if (np.all(np.isnan(y)) or len(y) == 0) and (np.all(np.isnan(y_gs)) or len(y_gs) == 0):
          raise ValueError("No data to plot")
                
        ## ---------       
        ## Plot Data
        ## ---------
        
        fig, ax = plt.subplots()
        ax.plot(x, y, color = 'blue', marker = '.', linestyle = '-', label = 'Ionospheric Scatter')
        
        if groundscatter:
            ax.plot(x_gs, y_gs, color = 'red', marker = '.', linestyle = '-', label = 'Ground Scatter')
        
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
            title = '{name} {date}\n{key}: Beam {beam}, Gate {gate}'.format(name = radar_name, date = date, key = parameters[parameter][0], beam = beam_num, gate = gate_num)
            ylabel = '{key} {units}'.format(key = parameters[parameter][0], units = parameters[parameter][1])
            
        except KeyError:
            title = '{name} {date}\n{key}: Beam {beam}, Gate {gate}'.format(name = radar_name, date = date, key = parameter, beam = beam_num, gate = gate_num)
            ylabel = '{key}'.format(key = parameter)
        
        ## -----------
        ## Format Plot
        ## -----------
        
        ax.xaxis.set_major_locator(mdates.MinuteLocator(interval = 15))
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
        ax.xaxis.set_minor_locator(mdates.MinuteLocator(interval = 3))
        
        ax.set_xlabel('Time [UTC]')
        ax.set_ylabel(ylabel)
        ax.set_title(title)
        
        if groundscatter:
            ax.legend(loc = 'upper center', bbox_to_anchor = (0.5, -0.15), ncol = 2)
        
        return None
    
    @staticmethod
    def plot_scalar_time_series(parameter, data, beam_num):
        """
        Plots a time series of the specified scalar field parameter for a given beam number.
        
        Future Work:
        ------------
            - Plot the time series of the specified scalar field parameter across all beam numbers.
            - Plot the time series of the specified scalar field parameter averaged across a specified beam number.
        
        Parameters:
        -----------
            parameter: str
                Key name of the scalar field parameter to plot.
                Supported quantities include:
                    - Sky noise ('noise.sky')
                    - Transmitted frequency ('tfreq')
                    - Lag to first range ('lagfr')
                    - Sample separation ('smsep')
                    - Number of pulse sequences transmitted ('nave')
        
            data: list of dict
                A list of SuperDARN FITACF or RAWACF records.
            
            beam_num: int
                Beam number (0 to 15) of the data to plot.
        
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
            if parameter in data[i] and type(data[i][parameter]) is not np.ndarray:
                key_error = False
                break
            
        if key_error:
            raise KeyError('Unknown scalar feild parameter: {key}'.format(key = parameter))
                
        ## -----------------
        ## Check Beam Number
        ## -----------------
            
        if beam_num not in range(0, 16):
            raise ValueError('Beam number invalid')  
        
        ## -----------
        ## Gather Data
        ## -----------

        x, y = [], []

        for i in range(len(data)):
            try:
                if beam_num != data[i]['bmnum']:
                    continue
                
                value = data[i][parameter]
                time = datetime(data[i]['time.yr'], data[i]['time.mo'], data[i]['time.dy'], data[i]['time.hr'], data[i]['time.mt'], data[i]['time.sc'])
    
                if np.isnan(value) or np.isinf(value):
                    continue
                
                x.append(time)
                y.append(value)

            except KeyError:
                continue

        ## ----------
        ## Check Data
        ## ----------
        
        if np.all(np.isnan(y)) or len(y) == 0:
          raise ValueError("No data to plot")
                
        ## ---------       
        ## Plot Data
        ## ---------
        
        fig, ax = plt.subplots()
        ax.plot(x, y, color = 'blue', marker = '.', linestyle = '-')
        
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
        
        parameters = {'noise.sky': ['Sky Noise', ''],
                      'tfreq': ['Transmitted Frequency', '[kHz]'],
                      'lagfr': ['Lag to First Range', '[μs]'],
                      'smsep': ['Sample Seperation', '[μs]'],
                      'nave': ['Number of Pulse Sequences Transmitted', '']}
        
        try:
            title = '{name} {date}\n{key}: Beam {beam}'.format(name = radar_name, date = date, key = parameters[parameter][0], beam = beam_num)
            ylabel = '{key} {units}'.format(key = parameters[parameter][0], units = parameters[parameter][1])
            
        except KeyError:
            title = '{name} {date}\n{key}: Beam {beam}'.format(name = radar_name, date = date, key = parameter, beam = beam_num)
            ylabel = '{key}'.format(key = parameter)
        
        ## -----------
        ## Format Plot
        ## -----------
        
        ax.xaxis.set_major_locator(mdates.MinuteLocator(interval = 15))
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
        ax.xaxis.set_minor_locator(mdates.MinuteLocator(interval = 3))
        
        ax.set_xlabel('Time [UTC]')
        ax.set_ylabel(ylabel)
        ax.set_title(title)
        
        return None