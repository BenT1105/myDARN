import pydarn
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

class Fan:
    """
    Generates fan plots for SuperDARN data.
    
    Methods:
    --------
        plot_fan_plots
            Create a sequence of fan plots for a specified parameter over a given time range.
            
    Dependencies:
    -------------
        - pyDARN
        - matplotlib
        - datetime
    """
    
    @staticmethod
    def plot_fan_plots(data, parameter, start_time, end_time, tolerance = 60, interval = 60, fig_path = None, groundscatter = False, coastline = True, grid = True, boundary = True, lowlat = 0):
        """
        Plots a sequence of fan plots for a specified parameter from 'start_time' to 'end_time', generating plots at intervals defined by 'interval'.
        Each plot includes data within the specified time 'tolerance' around the scan time.
        
        Parameters:
        -----------
            data: list of dict
                A list of SuperDARN FITACF records.
            
            parameter: str
                Key name of the vector field parameter to plot.
                Supported quantities include:
                    - Line of sight velocity ('v')
                    - Power ('p_l')
                    - Spectral width ('w_l')
                    - Elevation angle ('elv')
            
            fig_path: str
                File path to save each generated plot. If None, plots are not saved.
                Default: None
            
            start_time: datetime.datetime
                Datetime object marking the start of the plotting interval.
            
            end_time: datetime.datetime
                Datetime object marking the end of the plotting interval.
            
            tolerance: int
                Time window (in seconds) around each scan during which data is included.
                Default: 60
            
            interval: int
                Number of minutes between each generated plot.
                Default: 60
            
            groundscatter: bool
                If True, ground scatter points are shown in grey.
                Default: False
            
            coastline: bool
                If True, coastlines are drawn on the plot.
                Default: True
            
            grid: bool
                If True, overlays the radar field-of-view grid.
                Default: True
            
            boundary: bool
                If True, draws the outline of the radar field of view.
                Default: True
            
            lowlat: int
                Minimum latitude threshold. Only data above this latitude is plotted.
                Default: 0
        
        Returns:
        --------
            None
        
        Raises:
        -------
            TypeError
            ValueError
        """
        
        ## ------------------------
        ## Check Start and End Time
        ## ------------------------
        
        if type(start_time) != datetime:
            raise TypeError('Invalid start date and time')
        
        if type(end_time) != datetime:
            raise TypeError('Invalid end date and time')
        
        ## ---------------
        ## Check Parameter
        ## ---------------
        
        parameters = {'v': ('Line of Site Velocity', '[m s$^{-1}$]'),
                      'p_l': ('Power', '[dB]'),
                      'w_l': ('Spectral Width', '[m s$^{-1}$]'),
                      'elv': ('Elevation Angle', '[deg]')}
        
        if parameter not in parameters.keys():
            raise ValueError('Invalid parameter')
            
        ## ----------------------
        ## Generate List of Times
        ## ----------------------

        interval = timedelta(minutes = interval)
        
        times = [start_time]

        while times[-1] + interval <= end_time:
            times.append(times[-1] + interval)
            
        ## --------------
        ## Generate Plots
        ## --------------
        
        for time in times:
            fig_title = '{}.{}.{}.fan.png'.format(datetime.strftime(time, '%Y%m%d'), datetime.strftime(time, '%H%M'), parameter)
                
            try:
                pydarn.Fan.plot_fan(data, parameter = parameter, groundscatter = groundscatter, coastline = coastline, grid = grid, boundary = boundary, lowlat = lowlat,
                                    colorbar_label = f'{parameters[parameter][0]} {parameters[parameter][1]}',
                                    scan_time = time, scan_time_tolerance = timedelta(seconds = tolerance))
                
                print(f'Successfully plotted: {fig_title}')
            
                if fig_path != None:
                    try:
                        plt.savefig(fig_path + fig_title, format = 'png')
                    
                    except:
                        print(f'File not found: {fig_path}')
                        continue
                
                plt.show()
                
            except:
                print(f'Error plotting: {fig_title}')
                continue
                
        return None