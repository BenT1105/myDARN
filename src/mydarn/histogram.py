import pydarn
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

class Histogram:
    """
    Generates one-dimensional and two-dimensional histogram plots for SuperDARN data.
    
    Methods:
    --------
        plot_vector_hist
            Plot histograms of vector field quantities.
        
        plot_scalar_hist
            Plot histograms of scalar field quantities.
        
        plot_2d_hist
            Plot 2D histograms of vector field quantities versus range gate.
        
        plot_freq_scan_hist
            Plot histograms of ionospheric scatter occurrence as a function of transmitted frequency band.
        
        plot_freq_scan_2d_hist
            Plot 2D histograms of ionospheric scatter occurrence as a function of frequency band and time.
            
    Dependencies:
    -------------
        - pyDARN
        - NumPy
        - matplotlib
        - datetime
    """
    
    @staticmethod
    def plot_vector_hist(parameter, data, groundscatter = False, normalize = True, num_bins = 'auto', boundary = None, 
                         num_bins_gs = 'auto', boundary_gs = None, beam_num = 'all', gate_num = 'all', show_txt = True):
        """
        Plots a histogram of the specified vector field quantity.
        
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
                If True, ground scatter values for the specified parameter are plotted in a separate histogram and statistics are returned separately.
                Default: False
            
            normalize: bool
                If True, the histogram is plotted as a probability density (area normalized to 1).
                Default: True
            
            num_bins: int or str
                If an int, specifies the number of equal-width bins in the histogram.
                If a str, specifies the method used to determine the number of bins.
                Default: 'auto'
            
            boundary: str or (float, float)
                The lower and upper range of the bins, values outside this range are ignored. 
                If None, uses (min(vals), max(vals)).
                If 'auto', the lowest 0.5% and highest 0.5% of the data values are excluded.
                Default: None
            
            num_bins_gs: int or str
                As 'num_bins', but applied to the ground scatter histogram.
                Default: 'auto'
            
            boundary_gs: str or (float, float)
                As 'boundary', but applied to the ground scatter histogram.
                Default: None
            
            beam_num: int or str
                If an int, selects data from a single beam number (0 to 15) to include.
                If a str, data from all beam numbers are included.
                Default: 'all'
            
            gate_num: int or str
                If an int, selects data from a single gate number (0 to 74) to include.
                If a str, data from all gate numbers are included.
                Default: 'all'
            
            show_txt: bool
                If True, the number of bins, standard deviation, mean, median, and mode are annotated on the histogram.
                Default: True
        
        Returns:
        --------
            std: float
                Standard deviation of the data in the histogram. Includes ground scatter values if 'groundscatter' is False.
            
            mean: float
                Mean of the data in the histogram. Includes ground scatter values if 'groundscatter' is False.
            
            median: float
                Median of the data in the histogram. Includes ground scatter values if 'groundscatter' is False.
            
            mode: float
                Mode of the data in the histogram. Includes ground scatter values if 'groundscatter' is False.
            
            num_pts: int
                Number of points in the dataset for the specified parameter. Includes ground scatter values if 'groundscatter' is False.
            
            std_gs: float
                Standard deviation of the ground scatter data in the histogram. Only given if 'groundscatter' is True.
            
            mean_gs: float
                Mean of the ground scatter data in the histogram. Only returned if 'groundscatter' is True.
            
            median_gs: float
                Median of the ground scatter data in the histogram. Only returned if 'groundscatter' is True.
            
            mode_gs: float
                Mode of the ground scatter data in the histogram. Only returned if 'groundscatter' is True.
            
            num_pts_gs: int
                Number of points in the ground scatter dataset for the specified parameter. Only returned if 'groundscatter' is True.
            
            pct_gs: float
                Percentage of data flagged as ground scatter by the 'gflg' parameter. Only returned if 'groundscatter' is True.
        
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
                
        ## --------------------------
        ## Check Beam and Gate Number
        ## --------------------------
        
        if (beam_num not in range(0, 16) and beam_num != 'all') or (gate_num not in range(0, 75) and gate_num != 'all'):
            raise ValueError('Beam or gate number invalid')    

        ## -----------
        ## Gather Data
        ## -----------
        
        vals, vals_gs = [], []

        for i in range(len(data)):
            try:
                if beam_num != 'all' and beam_num != data[i]['bmnum']:
                    continue

                for j in range(len(data[i][parameter])):
                    if gate_num != 'all' and gate_num != data[i]['slist'][j]:
                        continue
                    
                    value = data[i][parameter][j]
                    
                    if np.isnan(value) or np.isinf(value):
                        continue

                    if groundscatter and data[i]['gflg'][j] == 1:
                        vals_gs.append(value)
     
                    else:
                        vals.append(value)

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
        ## Generate Boundary
        ## -----------------
        
        if boundary == 'auto':
            lower, upper = np.percentile(vals, [0.5, 99.5])
            boundary = (lower, upper)
    
        if boundary_gs == 'auto':
            lower, upper = np.percentile(vals_gs, [0.5, 99.5])
            boundary_gs = (lower, upper)
            
        ## ------------------
        ## Generate Histogram
        ## ------------------
        
        hist, bin_edges = np.histogram(vals, bins = num_bins, density = normalize, range = boundary)
        
        if groundscatter:
            hist_gs, bin_edges_gs = np.histogram(vals_gs, bins = num_bins_gs, density = normalize, range = boundary_gs)
            
        ## ----------------
        ## Find Bin Centers
        ## ----------------
        
        bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
            
        if groundscatter:
            bin_centers_gs = (bin_edges_gs[:-1] + bin_edges_gs[1:]) / 2
            
        ## ------------------------------------------
        ## Standard Deviation, Mean, Median, and Mode
        ## ------------------------------------------
        
        std = np.std(vals)
        mean = np.mean(vals)
        median = np.median(vals)
        mode = bin_centers[np.argmax(hist)]
        
        if groundscatter:
            std_gs = np.std(vals_gs)
            mean_gs = np.mean(vals_gs)
            median_gs = np.median(vals_gs)
            mode_gs = bin_centers_gs[np.argmax(hist_gs)]
            
        ## ----------------------
        ## Percent Ground Scatter
        ## ----------------------
        
        if groundscatter:
            pct_gs = len(vals_gs) / (len(vals) + len(vals_gs)) * 100
        
        ## --------------
        ## Plot Histogram
        ## --------------
        
        fig1, ax1 = plt.subplots()
        ax1.bar(bin_centers, hist, width = np.diff(bin_edges), edgecolor = 'black', color = 'blue', alpha = 0.7)
        
        if groundscatter:
            fig2, ax2 = plt.subplots()
            ax2.bar(bin_centers_gs, hist_gs, width = np.diff(bin_edges_gs), edgecolor = 'black', color = 'red', alpha = 0.7)
        
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
            xlabel = '{key} {units}'.format(key = parameters[parameter][0], units = parameters[parameter][1])
            
        except KeyError:
            title = '{name} {date}\n{key}'.format(name = radar_name, date = date, key = parameter)
            xlabel = '{key}'.format(key = parameter)
            
        if beam_num != 'all' and gate_num != 'all':
            title = title + ': Beam {beam}, Gate {gate}'.format(beam = beam_num, gate = gate_num)
            
        elif beam_num != 'all':
            title = title + ': Beam {beam}'.format(beam = beam_num)
        
        elif gate_num != 'all':
            title = title + ': Gate {gate}'.format(gate = gate_num)
            
        if show_txt:
            txt = 'Number of bins = {bins}, Standard deviation = {std:.2f},\n Mean = {mean:.2f}, Median = {median:.2f}, Mode = {mode:.2f}'.format(
                bins = len(bin_centers), std = std, mean = mean, median = median, mode = mode)
        
            if groundscatter:
                txt_gs = 'Number of bins = {bins}, Standard deviation = {std:.2f},\n Mean = {mean:.2f}, Median = {median:.2f}, Mode = {mode:.2f}'.format(
                    bins = len(bin_centers_gs), std = std_gs, mean = mean_gs, median = median_gs, mode = mode_gs)
            
        ## ------------
        ## Format Plots
        ## ------------
            
        if groundscatter:
            ax1.set_xlabel(xlabel)
            ax1.set_title('{title} (Ionospheric Scatter)'.format(title = title))
            
            ax2.set_xlabel(xlabel)
            ax2.set_title('{title} (Ground Scatter)'.format(title = title))
            
            if show_txt:
                fig1.text(0.5, -0.05, txt, verticalalignment = 'top', horizontalalignment = 'center', size = 10,
                          bbox = dict(boxstyle = 'round', pad = 0.4, facecolor = 'white', edgecolor = 'black', linewidth = 0.6))
                fig2.text(0.5, -0.05, txt_gs, verticalalignment = 'top', horizontalalignment = 'center', size = 10,
                          bbox = dict(boxstyle = 'round', pad = 0.4, facecolor = 'white', edgecolor = 'black', linewidth = 0.6))

        else:    
            ax1.set_xlabel(xlabel)
            ax1.set_title(title)
            
            if show_txt:
                fig1.text(0.5, -0.05, txt, verticalalignment = 'top', horizontalalignment = 'center', size = 10,
                          bbox = dict(boxstyle = 'round', pad = 0.4, facecolor = 'white', edgecolor = 'black', linewidth = 0.6))
        
        ## -----------------
        ## Return Dictionary
        ## -----------------
        
        if groundscatter:
            return {'std': float(std), 'mean': float(mean), 'median': float(median), 'mode': float(mode), 'num_pts': len(vals),
                    'std_gs': float(std_gs), 'mean_gs': float(mean_gs), 'median_gs': float(median_gs), 'mode_gs': float(mode_gs), 'num_pts_gs': len(vals_gs),
                    'pct_gs': float(pct_gs)}
        
        else:
            return {'std': float(std), 'mean': float(mean), 'median': float(median), 'mode': float(mode), 'num_pts': len(vals)}
        
    @staticmethod
    def plot_scalar_hist(parameter, data, normalize = True, num_bins = 'auto', boundary = None, beam_num = 'all', show_txt = True):
        """ 
        Plots a histogram of the specified scalar field quantity.
        
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

            
            normalize: bool
                If True, the histogram is plotted as a probability density (area normalized to 1).
                Default: True
            
            num_bins: int or str
                If an int, specifies the number of equal-width bins in the histogram.
                If a str, specifies the method used to determine the number of bins.
                Default: 'auto'
            
            boundary: str or (float, float)
                The lower and upper range of the bins, values outside this range are ignored. 
                If None, uses (min(vals), max(vals)).
                If 'auto', the lowest 0.5% and highest 0.5% of the data values are excluded.
                Default: None
                
            beam_num: int or str
                If an int, selects data from a single beam number (0 to 15) to include.
                If a str, data from all beam numbers are included.
                Default: 'all'
            
            show_txt: bool
                If True, the number of bins, standard deviation, mean, median, and mode are annotated on the histogram.
                Default: True
                
        Returns:
        --------   
            std: float
                Standard deviation of the data in the histogram.
            
            mean: float
                Mean of the data in the histogram.
            
            median: float
                Median of the data in the histogram.
            
            mode: float
                Mode of the data in the histogram.
            
            num_pts: int
                Number of points in the dataset for the specified parameter.

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
            
        if beam_num not in range(0, 16) and beam_num != 'all':
            raise ValueError('Beam number invalid')
        
        ## -----------
        ## Gather Data
        ## -----------
        
        vals = []

        for i in range(len(data)):
            try:
                if beam_num != 'all' and beam_num != data[i]['bmnum']:
                    continue
                
                value = data[i][parameter]
                
                if np.isnan(value) or np.isinf(value):
                    continue
                
                else:
                    vals.append(value)

            except KeyError:
                continue
        
        ## ----------
        ## Check Data
        ## ----------
        
        if np.all(np.isnan(vals)) or len(vals) == 0:
            raise ValueError("No data to plot")
            
        ## -----------------
        ## Generate Boundary
        ## -----------------
        
        if boundary == 'auto':
            lower, upper = np.percentile(vals, [0.5, 99.5])
            boundary = (lower, upper)
            
        ## ------------------
        ## Generate Histogram
        ## ------------------
        
        hist, bin_edges = np.histogram(vals, bins = num_bins, density = normalize, range = boundary)
        
        ## ----------------
        ## Find Bin Centers
        ## ----------------
        
        bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
            
        ## ------------------------------------------
        ## Standard Deviation, Mean, Median, and Mode
        ## ------------------------------------------
        
        std = np.std(vals)
        mean = np.mean(vals)
        median = np.median(vals)
        mode = bin_centers[np.argmax(hist)]
        
        ## --------------
        ## Plot Histogram
        ## --------------
        
        fig, ax = plt.subplots()
        ax.bar(bin_centers, hist, width = np.diff(bin_edges), edgecolor = 'black', color = 'blue', alpha = 0.7)
        
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
            title = '{name} {date}\n{key}'.format(name = radar_name, date = date, key = parameters[parameter][0])
            xlabel = '{key} {units}'.format(key = parameters[parameter][0], units = parameters[parameter][1])
            
        except KeyError:
            title = '{name} {date}\n{key}'.format(name = radar_name, date = date, key = parameter)
            xlabel = '{key}'.format(key = parameter)
            
        if beam_num != 'all':
            title = title + ': Beam {beam}'.format(beam = beam_num)
            
        if show_txt:
            txt = 'Number of bins = {bins}, Standard deviation = {std:.2f},\n Mean = {mean:.2f}, Median = {median:.2f}, Mode = {mode:.2f}'.format(
                bins = len(bin_centers), std = std, mean = mean, median = median, mode = mode)
        
        ## ------------
        ## Format Plots
        ## ------------
        
        ax.set_xlabel(xlabel)
        ax.set_title(title)
        
        if show_txt:
            fig.text(0.5, -0.05, txt, verticalalignment = 'top', horizontalalignment = 'center', size = 10,
                     bbox = dict(boxstyle = 'round', pad = 0.4, facecolor = 'white', edgecolor = 'black', linewidth = 0.6))
        
        ## -----------------
        ## Return Dictionary
        ## -----------------
        
        return {'std': float(std), 'mean': float(mean), 'median': float(median), 'mode': float(mode), 'num_pts': len(vals)}
    
    @staticmethod
    def plot_2d_hist(parameter, data, groundscatter = False, normalize = True, num_bins = 'auto', boundary = None, 
                    num_bins_gs = 'auto', boundary_gs = None, beam_num = 'all', cmap = 'plasma'):
        """
        Plots a 2D histogram of the specified vector field quantity along the y-axis and range gate number along the x-axis.
        
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
                If True, ground scatter values for the specified parameter are plotted in a separate 2D histogram, and corresponding statistics are returned separately.
                Default: False
            
            normalize: bool
                If True, the histogram is plotted as a probability density (area normalized to 1).
                Default: True
            
            num_bins: int or str
                If an int, specifies the number of equal-width bins used along the y-axis.
                If a str, specifies the method used to determine the number of bins.
                Default: 'auto'
            
            boundary: str or (float, float)
                The lower and upper bounds of the data range along the y-axis, values outside this range are ignored.
                If None, uses (min(vals), max(vals)).
                If 'auto', the lowest 0.5% and highest 0.5% of values are excluded.
                Default: None
            
            num_bins_gs: int or str
                As 'num_bins', but applied to the ground scatter histogram.
                Default: 'auto'
            
            boundary_gs: str or (float, float)
                As 'boundary', but applied to the ground scatter histogram.
                Default: None
            
            beam_num: int or str
                If an int, selects data from a single beam number (0 to 15) to include.
                If a str, data from all beam numbers are included.
                Default: 'all'
            
            cmap: str
                Matplotlib colormap used when rendering the histogram.
                Default: 'plasma'
        
        Returns:
        --------
            num_bins: int
                Number of bins used to generate the histogram along each axis. Includes ground scatter values if 'groundscatter' is False.
            
            num_pts: int
                Number of points in the dataset for the specified parameter. Includes ground scatter values if 'groundscatter' is False.
            
            num_bins_gs: int
                Number of bins used for the ground scatter histogram along each axis. Only returned if 'groundscatter' is True.
            
            num_pts_gs: int
                Number of points in the ground scatter dataset for the specified parameter. Only returned if 'groundscatter' is True.
        
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
        ## Generate Boundary
        ## -----------------
       
        if boundary == None:
            boundary = (min(vals), max(vals))
       
        elif boundary == 'auto':
            lower, upper = np.percentile(vals, [0.5, 99.5])
            boundary = (lower, upper)
        
        if groundscatter:
            if boundary_gs == None:
                boundary_gs = (min(vals_gs), max(vals_gs))
                
            elif boundary_gs == 'auto':
                lower, upper = np.percentile(vals_gs, [0.5, 99.5])
                boundary_gs = (lower, upper)
            
        ## -------------
        ## Generate Bins
        ## -------------
        
        if num_bins == 'auto':
            num_bins = np.histogram_bin_edges(vals, bins = 'auto')
        
        if groundscatter:
            if num_bins_gs == 'auto':
                num_bins_gs = np.histogram_bin_edges(vals_gs, bins = 'auto') 
            
        ## ------------------
        ## Generate Histogram
        ## ------------------
        
        hist, x_edges, y_edges = np.histogram2d(gates, vals, bins = [data[0]['nrang'], num_bins], density = normalize, range = [(min(gates), max(gates)), boundary])
        
        if groundscatter:
            hist_gs, x_edges_gs, y_edges_gs = np.histogram2d(gates_gs, vals_gs, bins = [data[0]['nrang'], num_bins_gs], density = normalize, range = [(min(gates_gs), max(gates_gs)), boundary_gs])
           
        ## --------------
        ## Plot Histogram
        ## --------------
        
        fig1, ax1 = plt.subplots()
        im1 = ax1.imshow(hist.T, origin = 'lower', extent = [x_edges[0] - 0.5, x_edges[-1] + 0.5, y_edges[0], y_edges[-1]], aspect = 'auto', cmap = cmap)
        cb1 = fig1.colorbar(im1, ax = ax1)
        
        if groundscatter:
            fig2, ax2 = plt.subplots()
            im2 = ax2.imshow(hist_gs.T, origin = 'lower', extent = [x_edges_gs[0] - 0.5, x_edges_gs[-1] + 0.5, y_edges_gs[0], y_edges_gs[-1]], aspect = 'auto', cmap = cmap)
            cb2 = fig2.colorbar(im2, ax = ax2)
        
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
            cb1.set_label('Counts')
            
            ax2.set_xlabel('Range Gate')
            ax2.set_ylabel(ylabel)
            ax2.set_title('{title} (Ground Scatter)'.format(title = title))
            cb2.set_label('Counts')

        else:   
            ax1.set_xlabel('Range Gate')
            ax1.set_ylabel(ylabel)
            ax1.set_title(title)
            cb1.set_label('Counts')
            
        ## -----------------
        ## Return Dictionary
        ## -----------------
        
        if groundscatter:
            return {'num_bins': [len(x_edges) - 1, len(y_edges) - 1], 'num_bins_gs': [len(x_edges_gs) - 1, len(y_edges_gs) - 1], 'num_pts': len(vals), 'num_pts_gs': len(vals_gs)}
            
        else:        
            return {'num_bins': [len(x_edges) - 1, len(y_edges) - 1], 'num_pts': len(vals)}
        
    @staticmethod
    def plot_freq_scan_hist(data, freq_bands, normalize = True, boundary = None, omit_bands = None, show_txt = True):
        """
        Plots a histogram of the number of ionospheric scatter points as a function of the transmitted frequency band.
        This function is intended for plotting data from frequency sweeps and uses data from channel B only.
        
        Parameters:
        -----------
            data: list of dict
                A list of SuperDARN FITACF records.
            
            freq_bands: dict
                Dictionary specifying the frequency bands.
                Keys are band identifiers, and values are two-element lists giving the frequency range (in kHz) for each band.
            
            normalize: bool
                If True, the histogram is plotted as a probability density (area normalized to 1).
                Default: True
            
            boundary: str or (float, float)
                The lower and upper frequency limits used for binning. Values outside this range are ignored.
                If None, uses the minimum and maximum frequencies defined in 'freq_bands'.
                Default: None
            
            omit_bands: int or list of int
                Frequency band numbers to omit from the histogram and from the ordering in the returned result.
                Default: None
            
            show_txt: bool
                If True, the optimal frequency band (the band with the highest number of ionospheric scatter points) is annotated on the histogram.
                Default: True
        
        Returns:
        --------
            ordered_bands: list of dict
                Frequency bands ordered from the highest to the lowest number of ionospheric scatter points.
                Includes the band indentifier, frequency range for each band, and number of ionospheric scatter points within each band.
        
        Raises:
        -------
            TypeError
        """

        ## ---------------------
        ## Check Frequency Bands
        ## ---------------------
        
        if type(freq_bands) != dict:
            raise TypeError('Invalid frequency bands format')
            
        for band in freq_bands.values():
            if type(band) != list:
                raise TypeError('Invalid frequency band format')
                
            if len(band) != 2:
                raise TypeError('Invalid frequency band format')
        
        ## -----------------
        ## Generate Boundary
        ## -----------------
        
        if boundary == None:
            boundary = (min(min(freq_bands.values())), max(max(freq_bands.values())))
        
        ## ------------
        ## Gather Bands
        ## ------------
        
        keys = []
        bands = []
        bin_centers = []
        
        for key, value in freq_bands.items():
            center = (value[0] + value[1]) / 2
            
            if center <= boundary[0] or center >= boundary[1]:
                continue
            
            keys.append(key)
            bands.append(value)
            bin_centers.append(center)
            
        ## ------------
        ## Remove Bands
        ## ------------

        if omit_bands != None:
            if type(omit_bands) == int:
                omit_bands = [omit_bands]

            try:
                remove_bands = [freq_bands[str(band)] for band in omit_bands]
        
            except:
                raise TypeError('Invalid frequency bands to omit')

        ## ------------------
        ## Generate Histogram
        ## ------------------
        
        hist = np.zeros(len(bin_centers), dtype = int)
        
        for i in range(len(data)):
            ## Only use data from channel 2
            if data[i]['channel'] != 2:
                continue
            
            freq = data[i]['tfreq']
            
            ## Ignore NaN and inf values
            if np.isnan(freq) or np.isinf(freq):
                continue
            
            ## Ingore values out of specified range
            if freq <= boundary[0] or freq >= boundary[1]:
                continue
            
            ## Ignore values within omitted bands
            if omit_bands != None:
                if any(band[0] <= freq <= band[1] for band in remove_bands):
                    continue
            
            num_pts = 0
            
            ## Count number of ionospheric scatter points
            try:
                for j in range(len(data[i]['gflg'])):
                    if data[i]['gflg'][j] == 0:
                        num_pts += 1
                        
            except KeyError:
                continue
            
            ## Add number of points to histogram
            for i in range(len(bands)):
                    if bands[i][0] <= freq <= bands[i][1]:
                        hist[i] += num_pts
                        break
        
        ## -----------------------
        ## Ordered Frequency Bands
        ## -----------------------
        
        ordered_keys = np.argsort(hist)[::-1]
        
        ordered_bands = [{'Band': int(i), 
                          'Freq Range': bands[i],
                          'Count': int(hist[i])} for i in ordered_keys]
        
        ## ---------
        ## Normalize
        ## ---------
        
        if normalize and np.sum(hist) != 0:
            hist = hist / (np.sum(hist))
        
        ## --------------
        ## Plot Histogram
        ## --------------
        
        bar_width = max(bands)[1] - max(bands)[0]
        
        colors = ['blue'] * len(hist)
        colors[ordered_bands[0]['Band']] = 'red'
        
        fig, ax = plt.subplots()
        hist_bars = ax.bar(bin_centers, hist, width = bar_width, edgecolor = 'black', color = colors, alpha = 0.7)
        
        ## -----------
        ## Plot Titles
        ## -----------
        
        radar_name = pydarn.SuperDARNRadars.radars[pydarn.RadarID(data[0]['stid'])].name
        start_date = datetime.strftime(datetime(data[0]['time.yr'], data[0]['time.mo'], 1), '%Y %b')
        end_date = datetime.strftime(datetime(data[-1]['time.yr'], data[-1]['time.mo'], 1), '%Y %b')
        
        if start_date == end_date:
            date = '{}'.format(start_date)
        else:
            date = '{} to {}'.format(start_date, end_date)
        
        title = '{} {}'.format(radar_name, date)
        x_label = 'Transmitted Frequency [kHz]'
        y_label = 'Number of Ionospheric Scatter Points'
            
        if show_txt:
            txt = 'Optimal Frequency Band = {} - {} kHz'.format(ordered_bands[0]['Freq Range'][0], ordered_bands[0]['Freq Range'][1])

        ## ------------
        ## Format Plots
        ## ------------
        
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)
        ax.set_title(title)
            
        if show_txt:
            ax.bar_label(hist_bars, labels = np.where(hist > 0, keys, ''))
            fig.text(0.5, -0.05, txt, verticalalignment = 'top', horizontalalignment = 'center', size = 10,
                     bbox = dict(boxstyle = 'round', pad = 0.4, facecolor = 'white', edgecolor = 'black', linewidth = 0.6))
        
        ## ------------------------------
        ## Return Ordered Frequency Bands
        ## ------------------------------

        return ordered_bands
    
    @staticmethod
    def plot_freq_scan_2d_hist(data, freq_bands, date_bin = 'hour', normalize = True, boundary = None, omit_bands = None, cmap = 'plasma', show_txt = True):
        """
        Plots a 2D histogram of the number of ionospheric scatter points with frequency band along the y-axis and time (year, month, day, or hour) along the x-axis.
        This function is intended for plotting data from frequency sweeps and uses data from channel B only.
        
        Parameters:
        -----------
            data: list of dict
                A list of SuperDARN FITACF records.
            
            freq_bands: dict
                Dictionary specifying the frequency bands.
                Keys are band identifiers, and values are two-element lists giving the frequency range (in kHz) for each band.
            
            date_bin: str
                Time scale used to bin the data along the x-axis.
                Supported options include:
                    - 'year'
                    - 'month'
                    - 'day'
                    - 'hour'
            
            normalize: bool
                If True, each column of the 2D histogram is normalized such that the column sums to 1 (column-wise probability density).
                Default: True
            
            boundary: str or (float, float)
                The lower and upper frequency limits used for binning. Values outside this range are ignored.
                If None, uses the minimum and maximum frequencies defined in 'freq_bands'.
                Default: None
            
            omit_bands: int or list of int
                Frequency band numbers to omit from the histogram and from the ordering in the returned result.
                Default: None
            
            cmap: str
                Matplotlib colormap used to render the 2D histogram.
                Default: 'plasma'
            
            show_txt: bool
                If True, the optimal frequency band (the band with the highest number of ionospheric scatter points) is annotated on the histogram.
                Default: True
        
        Returns:
        --------
            ordered_bands: list of dict
                Frequency bands ordered from the highest to the lowest number of ionospheric scatter points.
                Includes the band indentifier, frequency range for each band, and number of ionospheric scatter points within each band.
        
        Raises:
        -------
            ValueError
            TypeError
        """
        
        ## ---------------------
        ## Check Frequency Bands
        ## ---------------------
        
        if type(freq_bands) != dict:
            raise TypeError('Invalid frequency bands format')
            
        for band in freq_bands.values():
            if type(band) != list:
                raise TypeError('Invalid frequency band format')
                
            if len(band) != 2:
                raise TypeError('Invalid frequency band format')
        
        ## -----------------
        ## Generate Boundary
        ## -----------------
        
        if boundary == None:
            boundary = (min(min(freq_bands.values())), max(max(freq_bands.values())))
        
        ## ------------
        ## Gather Bands
        ## ------------
        
        keys = []
        bands = []
        
        for key, value in freq_bands.items():
            ## Ingore values out of specified range
            if value[0] < boundary[0] or value[1] > boundary[1]:
                continue       
            
            keys.append(int(key))
            bands.append(value)
            
        ## ------------
        ## Remove Bands
        ## ------------
        
        if omit_bands != None:
            if type(omit_bands) == int:
                omit_bands = [omit_bands]

            try:
                remove_bands = [freq_bands[str(band)] for band in omit_bands]
            
            except:
                raise TypeError('Invalid frequency bands to omit')
            
        ## ------------
        ## Gather Dates
        ## ------------
        
        dates = []
        
        for i in range(len(data)):
            ## Only use data from channel 2
            if data[i]['channel'] != 2:
                continue
            
            if date_bin == 'year':
                date = datetime(data[i]['time.yr'], 1, 1)
                
            elif date_bin == 'month':
                date = datetime(1, data[i]['time.mo'], 1)
                
            elif date_bin == 'day':
                date = datetime(data[i]['time.yr'], data[i]['time.mo'], data[i]['time.dy'])
                
            elif date_bin == 'hour':
                if (data[i]['time.hr'] % 2) == 0:
                    date = datetime(1, 1, 1, data[i]['time.hr'])
                
            else:
                raise ValueError('Invalid date bin type: {}'.format(date_bin))
            
            if date not in dates:
                dates.append(date)

        ## ------------------
        ## Generate Histogram
        ## ------------------
        
        hist2d = np.zeros((len(bands), len(dates)), dtype = float)
        
        for i in range(len(data)):
            ## Only use data from channel 2
            if data[i]['channel'] != 2:
                continue
            
            freq = data[i]['tfreq']
            
            ## Ignore NaN and inf values
            if np.isnan(freq) or np.isinf(freq):
                continue
            
            ## Ingore values out of specified range
            if freq <= boundary[0] or freq >= boundary[1]:
                continue
            
            ## Ignore values within omitted bands
            if omit_bands != None:
                if any(band[0] <= freq <= band[1] for band in remove_bands):
                    continue

            num_pts = 0
            
            ## Count number of ionospheric scatter points
            try:
                for j in range(len(data[i]['gflg'])):
                    if data[i]['gflg'][j] == 0:
                        num_pts += 1
                        
            except KeyError:
                continue
            
            band_index = None
            
            ## Find the index of the corresponding frequency band
            for j in range(len(bands)):
                    if bands[j][0] <= freq <= bands[j][1]:
                        band_index = j
                        break
                        
            if band_index == None:
                continue
            
            ## Find the index of the corresponding date
            if date_bin == 'year':
                date = datetime(data[i]['time.yr'], 1, 1)
                
            elif date_bin == 'month':
                date = datetime(1, data[i]['time.mo'], 1)
                
            elif date_bin == 'day':
                date = datetime(data[i]['time.yr'], data[i]['time.mo'], data[i]['time.dy'])
                
            elif date_bin == 'hour':
                if (data[i]['time.hr'] % 2) == 0:
                    date = datetime(1, 1, 1, data[i]['time.hr'])
            
            date_index = dates.index(date)
            
            ## Add number of scatter points to histogram
            hist2d[band_index, date_index] += num_pts
        
        ## -----------------------
        ## Ordered Frequency Bands
        ## -----------------------
        
        band_sums = np.sum(hist2d, axis=1)
        ordered_keys = np.argsort(band_sums)[::-1]
        
        ordered_bands = [{'Band': int(i), 
                          'Freq Range': bands[i],
                          'Count': int(band_sums[i])} for i in ordered_keys]
        
        ## -----------------
        ## Normalize Columns
        ## -----------------
        
        if normalize:
            for column in range(hist2d.shape[1]):
                column_sum = np.sum(hist2d[:, column])
                
                if column_sum > 0:
                    hist2d[:, column] /= column_sum
            
        ## ---------
        ## Color Map
        ## ---------
        
        nonzero_hist2d = hist2d[hist2d > 0]
        
        if nonzero_hist2d.size > 0:
            threshold = np.percentile(nonzero_hist2d, 0.5)
            hist2d[hist2d < threshold] = np.nan
            
        else:
            hist2d[hist2d == 0.0] = np.nan
        
        try:
            cmap = plt.get_cmap(cmap)
            
        except:
            raise ValueError('Invalid matplotlib colormap: {}'.format(cmap))
        
        cmap.set_bad(color = 'white')
        
        ## ------------
        ## Format Dates
        ## ------------

        if date_bin == 'year':
            start_date = datetime.strftime(datetime(data[0]['time.yr'], 1, 1), '%Y')
            end_date = datetime.strftime(datetime(data[-1]['time.yr'], 1, 1), '%Y')
            
            x_label = 'Date [year]'
            date_labels = [date.strftime('%Y') for date in dates]
            
            size = 10
            
        elif date_bin == 'month':
            start_date = datetime.strftime(datetime(data[0]['time.yr'], data[0]['time.mo'], 1), '%Y %b')
            end_date = datetime.strftime(datetime(data[-1]['time.yr'], data[-1]['time.mo'], 1), '%Y %b')
            
            x_label = 'Date [month]'
            date_labels = [date.strftime('%b') for date in dates]
            
            size = 10
            
        elif date_bin == 'day':
            start_date = datetime.strftime(datetime(data[0]['time.yr'], data[0]['time.mo'], data[0]['time.dy']), '%Y %b %d')
            end_date = datetime.strftime(datetime(data[-1]['time.yr'], data[-1]['time.mo'], data[-1]['time.dy']), '%Y %b %d')
            
            x_label = 'Date [mm/dd]'
            date_labels = [date.strftime('%m/%d') for date in dates]
            
            size = 10
            
        elif date_bin == 'hour':
            start_date = datetime.strftime(datetime(data[0]['time.yr'], data[0]['time.mo'], 1), '%Y %b')
            end_date = datetime.strftime(datetime(data[-1]['time.yr'], data[-1]['time.mo'], 1), '%Y %b')
            
            x_label = 'Time [hour]'
            date_labels = [date.strftime('%H:00') for date in dates]
            
            size = 6
            
        ## --------------
        ## Plot Histogram
        ## --------------
        
        num_bands = len(bands)
        num_dates = len(dates)

        extent = [-0.5, num_dates - 0.5, -0.5, num_bands - 0.5]
        
        fig, ax = plt.subplots()
        im = ax.imshow(hist2d, origin = 'lower', extent = extent, aspect = 'auto', cmap = cmap)
        cb = fig.colorbar(im, ax = ax)
        
        ## -----------
        ## Plot Titles
        ## -----------
        
        radar_name = pydarn.SuperDARNRadars.radars[pydarn.RadarID(data[0]['stid'])].name
        
        if start_date == end_date:
            date = '{}'.format(start_date)
        else:
            date = '{} to {}'.format(start_date, end_date)
        
        title = '{} {}'.format(radar_name, date)
        y_label = 'Frequency Band'
        
        if show_txt:
            txt = 'Optimal Frequency Band = {} - {} kHz'.format(ordered_bands[0]['Freq Range'][0], ordered_bands[0]['Freq Range'][1])

        ## ------------
        ## Format Plots
        ## ------------
        
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)
        ax.set_title(title)
        cb.set_label('Number of Ionospheric Scatter Points')

        
        ax.set_xticks(np.arange(num_dates))
        ax.set_xticklabels(date_labels, fontsize = size)
        
        ax.set_yticks(np.arange(num_bands))
        ax.set_yticklabels([str(key) for key in keys])
        
        if show_txt:
            fig.text(0.5, -0.05, txt, verticalalignment = 'top', horizontalalignment = 'center', size = 10,
                     bbox = dict(boxstyle = 'round', pad = 0.4, facecolor = 'white', edgecolor = 'black', linewidth = 0.6))
        
        ## ------------------------------
        ## Return Ordered Frequency Bands
        ## ------------------------------

        return ordered_bands