import os
import subprocess
from glob import glob

class RST:
    """
    Processes SuperDARN data using RST subprocesses. Requires a working local installation of the Radar Software Toolkit (RST) version 5.1 or later.
    
    Methods:
    --------
        rawacf_to_fitacf
            Convert RAWACF files to FITACF using the RST 'make_fit' subprocess.
        
        fitacf_to_grid
            Convert FITACF files to GRID using the RST 'make_grid' subprocess.
        
        fit_speck_removal
            Remove isolated noise points from FITACF data using the RST 'fit_speck_removal' subprocess.
    
    Dependencies:
    -------------
        - os
        - subprocess
        - glob
    """
    
    @staticmethod
    def rawacf_to_fitacf(rawacf_filepath, fitacf_filepath, version = 3):
        """
        Converts SuperDARN RAWACF files to FITACF files using the RST 'make_fit' subprocess.
        
        Parameters:
        -----------
            rawacf_filepath: str
                File path pattern to RAWACF file(s) containing '*' wildcard characters.
            
            fitacf_filepath: str
                File path to the output FITACF file to be created.
            
            version: float
                The fitting algorithm version to use (2.5 or 3).
                Default: 3
        
        Returns:
        --------
            None
        
        Raises:
        -------
            ValueError
            FileNotFoundError
            OSError
        """

        
        ## ---------------------
        ## Ensure RST is in PATH
        ## ---------------------
        
        rst_bin = os.path.join(os.environ["RSTPATH"], "bin")
        if rst_bin not in os.environ["PATH"]:
            os.environ["PATH"] += os.pathsep + rst_bin
        
        ## ------------------------
        ## Determine FITACF Version
        ## ------------------------
        
        if version == 2.5:
            fit_version = '-fitacf2'
        elif version == 3:
            fit_version = '-fitacf3'
        else:
            raise ValueError('FITACF version unavailable: {}'.format(version))
            
        ## ------------------------
        ## Find and Sort Data Files
        ## ------------------------
        
        rawacf_files = glob(rawacf_filepath)
        rawacf_files.sort()
        
        ## ----------------------
        ## Check RAWACF Filepaths
        ## ----------------------
        
        if len(rawacf_files) == 0:
            raise FileNotFoundError('File not found: {}'.format(rawacf_filepath))
            
        ## ---------------------
        ## Check FITACF Filepath
        ## ---------------------
        
        if not os.path.isdir(fitacf_filepath):
            raise FileNotFoundError('Directory not found: {}'.format(fitacf_filepath))
        
        ### -----------
        ### Run Command
        ### -----------
        
        for rawacf_file in rawacf_files:
            fitacf_file = os.path.join(fitacf_filepath, os.path.basename(rawacf_file).replace('.rawacf', '.fitacf'))
            
            print('Converting to FITACF file: {}'.format(rawacf_file))
            
            try:
                command = 'make_fit {version} {rawacf} > {fitacf}'.format(version = fit_version, rawacf = rawacf_file, fitacf = fitacf_file)
                subprocess.run(command, text = True, check = True, shell = True)
                
            except subprocess.CalledProcessError:
                print('Unable to convert file: {}'.format(rawacf_file))
                continue
                
        print('Files converted')
        
        return None
    
    @staticmethod
    def fitacf_to_grid(fitacf_filepath, grid_filepath):
        """
        Converts SuperDARN FITACF files to GRID files using the RST 'make_grid' subprocess.

        Parameters:
        -----------
            fitacf_filepath: str
                File path pattern to FITACF file(s) containing '*' wildcard characters.
            
            grid_filepath: str
                File path to the output GRID file to be created.

        Returns:
        --------
            None
            
        Raises:
        -------
            ValueError
            FileNotFoundError
            OSError
        """
        
        ## ---------------------
        ## Ensure RST is in PATH
        ## ---------------------
        
        rst_bin = os.path.join(os.environ["RSTPATH"], "bin")
        if rst_bin not in os.environ["PATH"]:
            os.environ["PATH"] += os.pathsep + rst_bin
            
        ## ------------------------
        ## Find and Sort Data Files
        ## ------------------------
        
        fitacf_files = glob(fitacf_filepath)
        fitacf_files.sort()
        
        ## ----------------------
        ## Check FITACF Filepaths
        ## ----------------------
        
        if len(fitacf_files) == 0:
            raise FileNotFoundError('File not found: {}'.format(fitacf_filepath))
            
        ## -------------------
        ## Check GRID Filepath
        ## -------------------
        
        if not os.path.isdir(grid_filepath):
            raise FileNotFoundError('Directory not found: {}'.format(grid_filepath))
        
        ### -----------
        ### Run Command
        ### -----------
        
        for fitacf_file in fitacf_files:
            grid_file = os.path.join(grid_filepath, os.path.basename(fitacf_file).replace('.fitacf', '.grid'))
            
            print('Converting to GRID file: {}'.format(fitacf_file))
            
            try:
                command = 'make_grid {fitacf} > {grid}'.format(fitacf = fitacf_file, grid = grid_file)
                subprocess.run(command, text = True, check = True, shell = True)
                
            except subprocess.CalledProcessError:
                print('Unable to convert file: {}'.format(fitacf_file))
                continue
                
        print('Files converted')
        
        return None
    
    @staticmethod
    def fit_speck_removal(fitacf_filepath, despeck_filepath):
        """
        Removes isolated noise points from SuperDARN FITACF data using the RST 'fit_speck_removal' subprocess.

        Parameters:
        -----------
            fitacf_filepath: str
                File path pattern to FITACF file(s) containing '*' wildcard characters.
            
            despeck_file: str
                File path to the output despecked FITACF file to be created.

        Returns:
        --------
            pct_removed: list of float
                Percentage of noise points removed from the data by the 'fit_speck_removal' subprocess.
            
        Raises:
        -------
            ValueError
            FileNotFoundError
            OSError
        """
        
        ## ---------------------
        ## Ensure RST is in PATH
        ## ---------------------
        
        rst_bin = os.path.join(os.environ["RSTPATH"], "bin")
        if rst_bin not in os.environ["PATH"]:
            os.environ["PATH"] += os.pathsep + rst_bin
            
        ## ------------------------
        ## Find and Sort Data Files
        ## ------------------------
        
        fitacf_files = glob(fitacf_filepath)
        fitacf_files.sort()
        
        ## ----------------------
        ## Check FITACF Filepaths
        ## ----------------------
        
        if len(fitacf_files) == 0:
            raise FileNotFoundError('File not found: {}'.format(fitacf_filepath))
            
        ## ----------------------
        ## Check despeck Filepath
        ## ----------------------
        
        if not os.path.isdir(despeck_filepath):
            raise FileNotFoundError('Directory not found: {}'.format(despeck_filepath))
        
        ### -----------
        ### Run Command
        ### -----------
        
        pct_removed = []
        
        for fitacf_file in fitacf_files:
            despeck_file = os.path.join(despeck_filepath, os.path.basename(fitacf_file).replace('.fitacf', '.despeck.fitacf'))
            
            print('Despecking file: {}'.format(fitacf_file))
            
            try:
                command = 'fit_speck_removal {fitacf} > {despeck}'.format(fitacf = fitacf_file, despeck = despeck_file)
                result = subprocess.run(command, text = True, check = True, shell = True, stderr = subprocess.PIPE)
                
                output = result.stderr
                print(output.strip())
                print()
                
                if '(' in output and '%' in output:
                    start = output.find('(')
                    end = output.find('%')
                    pct_removed.append(float(output[start + 1: end]))
                
            except subprocess.CalledProcessError:
                print('Unable to despeck file: {}'.format(fitacf_file))
                continue
                
        print('Files despecked')
        
        return pct_removed