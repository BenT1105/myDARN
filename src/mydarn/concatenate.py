import pydarn
import pydarnio
from glob import glob
import collections
import os

class Concatenate:
    """
    Provides methods for reading, writing, and grouping SuperDARN DMAP-based data formats, including FITACF, RAWACF, and GRID files.
    
    Methods:
    --------
        read_fitacf
            Read and concatenate SuperDARN FITACF data files.
        
        read_rawacf
            Read and concatenate SuperDARN RAWACF data files.
        
        read_grid
            Read and concatenate SuperDARN GRID files.
        
        read_dmap
            Generic DMAP file reader.
        
        write_fitacf
            Write SuperDARN FITACF data to file.
        
        write_rawacf
            Write SuperDARN RAWACF data to file.
        
        write_grid
            Write SuperDARN GRID data to file.
        
        write_dmap
            Generic DMAP file writer.
        
        group_files
            Group SuperDARN data files by day, month, or year.
            
    Dependencies:
    -------------
        - pyDARN
        - pyDARNio
        - glob
        - collections
        - os
    """
    
    @staticmethod
    def read_fitacf(filepath, print_console = True):
        """
        Reads and concatenates SuperDARN FITACF data from one or more files.
        
        Parameters:
        -----------
            filepath: str or list of str
                If provided as a string, it is interpreted as a file path pattern to FITACF SuperDARN data files containing '*' wildcard characters.
                If provided as a list, it must contain explicit file paths to the SuperDARN FITACF files to be processed.
        
            print_console: bool
                If True, progress and status messages are printed to the console.
                Default: True
        
        Returns:
        --------
            data: list of dict
                A list of FITACF records concatenated from the provided files.
        
        Raises:
        -------
            FileNotFoundError
            TypeError
        """
        
        ## ------------------------
        ## Find and Sort Data Files
        ## ------------------------
        
        if type(filepath) == str:
            fitacf_files = glob(filepath)
            fitacf_files.sort()
            
        elif type(filepath) == list:
            fitacf_files = filepath
            fitacf_files.sort()
        
        else:
            raise TypeError('Invalid file path type')
        
        ## ---------------
        ## Check Filepaths
        ## ---------------
        
        if len(fitacf_files) == 0:
            raise FileNotFoundError('Files not found: {}'.format(filepath))
        
        ## -------------------
        ## Read in FITACF Data
        ## -------------------
        
        if print_console:
            print('Reading in FITACF files...')

        data = []
        for fitacf_file in fitacf_files:
            SDarn_read = pydarnio.SDarnRead(fitacf_file)
            data.extend(SDarn_read.read_fitacf())
        
        if print_console:
            print('Reading complete')
        
        return data
    
    @staticmethod
    def read_rawacf(filepath, print_console = True):
        """
        Reads and concatenates SuperDARN RAWACF data from one or more files.
        
        Parameters:
        -----------
            filepath: str or list of str
                If provided as a string, it is interpreted as a file path pattern to RAWACF SuperDARN data files containing '*' wildcard characters.
                If provided as a list, it must contain explicit file paths to the SuperDARN RAWACF files to be processed.
        
            print_console: bool
                If True, progress and status messages are printed to the console.
                Default: True
        
        Returns:
        --------
            data: list of dict
                A list of RAWACF records concatenated from the provided files.
        
        Raises:
        -------
            FileNotFoundError
            TypeError
        """
        
        ## ------------------------
        ## Find and Sort Data Files
        ## ------------------------
        
        if type(filepath) == str:
            rawacf_files = glob(filepath)
            rawacf_files.sort()
            
        elif type(filepath) == list:
            rawacf_files = filepath
            rawacf_files.sort()
        
        else:
            raise TypeError('Invalid file path type')
        
        ## ---------------
        ## Check Filepaths
        ## ---------------
        
        if len(rawacf_files) == 0:
            raise FileNotFoundError('Files not found: {}'.format(filepath))
        
        ## -------------------
        ## Read in RAWACF Data
        ## -------------------
        
        if print_console:
            print('Reading in RAWACF files...')

        data = []
        for rawacf_file in rawacf_files:
            SDarn_read = pydarnio.SDarnRead(rawacf_file)
            data.extend(SDarn_read.read_rawacf())
        
        if print_console:
            print('Reading complete')
        
        return data
    
    @staticmethod
    def read_grid(filepath, print_console = True):
        """
        Reads and concatenates SuperDARN GRID data from one or more files.
        
        Parameters:
        -----------
            filepath: str or list of str
                If provided as a string, it is interpreted as a file path pattern to GRID SuperDARN data files containing '*' wildcard characters.
                If provided as a list, it must contain explicit file paths to the SuperDARN GRID files to be processed.
        
            print_console: bool
                If True, progress and status messages are printed to the console.
                Default: True
        
        Returns:
        --------
            data: list of dict
                A list of GRID records concatenated from the provided files.
        
        Raises:
        -------
            FileNotFoundError
            TypeError
        """
        
        ## ------------------------
        ## Find and Sort Data Files
        ## ------------------------
        
        if type(filepath) == str:
            grid_files = glob(filepath)
            grid_files.sort()
            
        elif type(filepath) == list:
            grid_files = filepath
            grid_files.sort()
        
        else:
            raise TypeError('Invalid file path type')
        
        ## ---------------
        ## Check Filepaths
        ## ---------------
        
        if len(grid_files) == 0:
            raise FileNotFoundError('Files not found: {}'.format(filepath))
        
        ## -----------------
        ## Read in GRID Data
        ## -----------------
        
        if print_console:
            print('Reading in GRID files...')

        data = []
        for grid_file in grid_files:
            SDarn_read = pydarnio.SDarnRead(grid_file)
            data.extend(SDarn_read.read_grid())
        
        if print_console:
            print('Reading complete')
        
        return data
    
    @staticmethod
    def read_dmap(filepath, print_console = True):
        """
        Reads and concatenates generic SuperDARN DMAP data from one or more files.
        
        Parameters:
        -----------
            filepath: str or list of str
                If provided as a string, it is interpreted as a file path pattern to DMAP SuperDARN data files containing '*' wildcard characters.
                If provided as a list, it must contain explicit file paths to the SuperDARN DMAP files to be processed.
        
            print_console: bool
                If True, progress and status messages are printed to the console.
                Default: True
        
        Returns:
        --------
            data: list of dict
                A list of DMAP records concatenated from the provided files.
        
        Raises:
        -------
            FileNotFoundError
            TypeError
        """
        
        ## ------------------------
        ## Find and Sort Data Files
        ## ------------------------
        
        if type(filepath) == str:
            dmap_files = glob(filepath)
            dmap_files.sort()
            
        elif type(filepath) == list:
            dmap_files = filepath
            dmap_files.sort()
        
        else:
            raise TypeError('Invalid file path type')
        
        ## ---------------
        ## Check Filepaths
        ## ---------------
        
        if len(dmap_files) == 0:
            raise FileNotFoundError('Files not found: {}'.format(filepath))
        
        ## -----------------
        ## Read in DMap Data
        ## -----------------
        
        if print_console:
            print('Reading in DMap files...')

        data = []
        for dmap_file in dmap_files:
            data.extend(pydarn.SuperDARNRead().read_dmap(dmap_file))
        
        if print_console:
            print('Reading complete')
        
        return data

    @staticmethod
    def write_fitacf(data, filepath, print_console = True):
        """
        Writes SuperDARN FITACF data to a FITACF file.
        
        Parameters:
        -----------
            data: list of dict
                A list of SuperDARN FITACF records to be written.
        
            filepath: str
                The output file path, including the desired filename.
        
            print_console: bool, optional
                If True, progress and status messages are printed to the console.
                Default: True
        
        Returns:
        --------
            None
        
        Raises:
        -------
            TypeError
        """
        
        ## ----------
        ## Check Data
        ## ----------
        
        if type(data) != list or len(data) == 0:
            raise TypeError('Invalid data type')
                
        if type(data[0]) != collections.OrderedDict:
            raise TypeError('Invalid data type')
            
        ## -----------------
        ## Write FITACF file
        ## -----------------
        
        if print_console:
            print('Writing FITACF file...')
        
        SDarn_write = pydarnio.SDarnWrite(data)
        SDarn_write.write_fitacf(filepath)
        
        if print_console:
            print('Writing complete')
        
        return None
    
    @staticmethod
    def write_rawacf(data, filepath, print_console = True):
        """
        Writes SuperDARN RAWACF data to a RAWACF file.
        
        Parameters:
        -----------
            data: list of dict
                A list of SuperDARN RAWACF records to be written.
        
            filepath: str
                The output file path, including the desired filename.
        
            print_console: bool, optional
                If True, progress and status messages are printed to the console.
                Default: True
        
        Returns:
        --------
            None
        
        Raises:
        -------
            TypeError
        """
        
        ## ----------
        ## Check Data
        ## ----------
        
        if type(data) != list or len(data) == 0:
            raise TypeError('Invalid data type')
                
        if type(data[0]) != collections.OrderedDict:
            raise TypeError('Invalid data type')
            
        ## -----------------
        ## Write RAWACF file
        ## -----------------
        
        if print_console:
            print('Writing RAWACF file...')
        
        SDarn_write = pydarnio.SDarnWrite(data)
        SDarn_write.write_rawacf(filepath)
        
        if print_console:
            print('Writing complete')
        
        return None
    
    @staticmethod
    def write_grid(data, filepath, print_console = True):
        """
        Writes SuperDARN GRID data to a GRID file.
        
        Parameters:
        -----------
            data: list of dict
                A list of SuperDARN GRID records to be written.
        
            filepath: str
                The output file path, including the desired filename.
        
            print_console: bool, optional
                If True, progress and status messages are printed to the console.
                Default: True
        
        Returns:
        --------
            None
        
        Raises:
        -------
            TypeError
        """
        
        ## ----------
        ## Check Data
        ## ----------
        
        if type(data) != list or len(data) == 0:
            raise TypeError('Invalid data type')
                
        if type(data[0]) != collections.OrderedDict:
            raise TypeError('Invalid data type')
            
        ## ---------------
        ## Write GRID file
        ## ---------------
        
        if print_console:
            print('Writing GRID file...')
        
        SDarn_write = pydarnio.SDarnWrite(data)
        SDarn_write.write_grid(filepath)
        
        if print_console:
            print('Writing complete')
        
        return None
    
    @staticmethod
    def write_dmap(data, filepath, print_console = True):
        """
        Writes generic SuperDARN DMAP data to a DMAP file.
        
        Parameters:
        -----------
            data: list of dict
                A list of SuperDARN DMAP records to be written.
        
            filepath: str
                The output file path, including the desired filename.
        
            print_console: bool, optional
                If True, progress and status messages are printed to the console.
                Default: True
        
        Returns:
        --------
            None
        
        Raises:
        -------
            TypeError
        """
        
        ## ----------
        ## Check Data
        ## ----------
        
        if type(data) != list or len(data) == 0:
            raise TypeError('Invalid data type')
                
        if type(data[0]) != collections.OrderedDict:
            raise TypeError('Invalid data type')
            
        ## ---------------
        ## Write DMap file
        ## ---------------
        
        if print_console:
            print('Writing DMap file...')
        
        SDarn_write = pydarnio.SDarnWrite(data)
        SDarn_write.write_dmap(filepath)
        
        if print_console:
            print('Writing complete')
        
        return None
    
    @staticmethod
    def group_files(filepath, group_by = 'day'):
        """
        Groups SuperDARN data files based on date information.
        
        Parameters:
        -----------
            filepath: str or list of str
                If provided as a string, it is interpreted as a file path pattern to SuperDARN data files containing '*' wildcard characters.
                If provided as a list, it must contain explicit file paths to the SuperDARN files to be processed.
        
            group_by: str, optional
                Specifies how the files should be grouped: 'day', 'month', or 'year'.
                Default: 'day'
        
        Returns:
        --------
            groups: dict
                A dictionary where each key is a date (formatted according to the grouping method), and each value is a list of file paths corresponding to that date.
        
        Raises:
        -------
            FileNotFoundError
            NameError
            TypeError
        """
        
        ## ------------------------
        ## Find and Sort Data Files
        ## ------------------------
        
        if type(filepath) == str:
            files = glob(filepath)
            files.sort()
            
        elif type(filepath) == list:
            files = filepath
            files.sort()
        
        else:
            raise TypeError('Invalid file path type')
        
        ## ---------------
        ## Check Filepaths
        ## ---------------
        
        if len(files) == 0:
            raise FileNotFoundError('Files not found: {}'.format(filepath))
            
        ## -----------
        ## Group Files
        ## -----------
        
        groups = {}
        
        try:
            date_len = {'year': 4, 'month': 6, 'day': 8}[group_by]
            
        except:
            raise NameError('Invalid grouping method: {}'.format(group_by))

        for file in files:
            basename = os.path.basename(file)
            
            date = ''
            
            for char in basename:
                if char.isdigit():
                    date += char
                    
                    if len(date) == date_len:
                        break
                    
            if len(date) != date_len:
                raise NameError('No date found in file: {}'.format(basename))
            
            if group_by == 'year':
                key = date[:4]
                
            elif group_by == 'month':
                key = (date[:4], date[4:6])
                
            elif group_by == 'day':
                key = (date[:4], date[4:6], date[6:8])
            
            if key not in groups:
                groups[key] = []
                
            groups[key].append(file)
        
        return groups