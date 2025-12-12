import os
from glob import glob
import bz2
import gzip

class Convert:
    """
    Provides methods for compressing and uncompressing .gz and .bz2 files.
    
    Methods:
    --------
        unzip_bz2
            Uncompress .bz2 files and remove the original archives.
        
        zip_bz2
            Compress files into .bz2 format and remove the original files.
        
        unzip_gz
            Uncompress .gz files and remove the original archives.
        
        zip_gz
            Compress files into .gz format and remove the original files.
            
    Dependencies:
    -------------
        - os
        - glob
        - bz2
        - gzip
    """
    
    @staticmethod
    def unzip_bz2(filepath):
        """
        Uncompresses .bz2 files and removes the original compressed file.
        
        Parameters:
        -----------
            filepath: str
                File path pattern to compressed .bz2 files, using '*' wildcard characters.
        
        Returns:
        --------
            None
        
        Raises:
        -------
            FileNotFoundError
        """
        
        ## ------------------------
        ## Find and Sort Data Files
        ## ------------------------
        
        input_files = glob(filepath)
        input_files.sort()
        
        ## -----------
        ## Check Files
        ## -----------
        
        if len(input_files) == 0:
            raise FileNotFoundError('File not found: {}'.format(filepath))
        
        ## --------------------------------------
        ## Uncompress Files and Remove Origionals
        ## --------------------------------------
        
        for input_file in input_files:
            if input_file.endswith('.bz2'):
                output_file = input_file.replace('.bz2', '')
                
                print('Uncompressing: {}'.format(input_file))
            
                with bz2.BZ2File(input_file, 'rb') as infile, open(output_file, 'wb') as outfile:
                    outfile.write(infile.read())
                
                os.remove(input_file)
            
            else:
                print('File not .bz2 format: {}'.format(input_file))
                continue
        
        print('Files uncompressed')
        
        return None
    
    @staticmethod
    def zip_bz2(filepath):
        """
        Compresses files into .bz2 format and removes the original uncompressed files.
        
        Parameters:
        -----------
            filepath: str
                File path pattern to uncompressed files, using '*' wildcard characters.
        
        Returns:
        --------
            None
        
        Raises:
        -------
            FileNotFoundError
        """
        
        ## ------------------------
        ## Find and Sort Data Files
        ## ------------------------
        
        input_files = glob(filepath)
        input_files.sort()
        
        ## -----------
        ## Check Files
        ## -----------
        
        if len(input_files) == 0:
            raise FileNotFoundError('File not found: {}'.format(filepath))
            
        ## ----------------------------------
        ## Compress Files and Remove Originals
        ## ----------------------------------
        
        for input_file in input_files:
            if not input_file.endswith('.bz2'):
                output_file = input_file + '.bz2'
                
                print('Compressing: {}'.format(input_file))
                
                with open(input_file, 'rb') as infile, bz2.BZ2File(output_file, 'wb') as outfile:
                    outfile.write(infile.read())
            
                os.remove(input_file)
                
            else:
                print('File already .bz2 format: {}'.format(input_file))
                continue
            
        print('Files compressed')
        
        return None
    
    @staticmethod
    def unzip_gz(filepath):
        """
        Uncompresses .gz files and removes the original compressed file.
        
        Parameters:
        -----------
            filepath: str
                File path pattern to compressed .gz files, using '*' wildcard characters.
        
        Returns:
        --------
            None
        
        Raises:
        -------
            FileNotFoundError
        """
        
        ## ------------------------
        ## Find and Sort Data Files
        ## ------------------------
        
        input_files = glob(filepath)
        input_files.sort()
        
        ## -----------
        ## Check Files
        ## -----------
        
        if len(input_files) == 0:
            raise FileNotFoundError('File not found: {}'.format(filepath))
        
        ## --------------------------------------
        ## Uncompress Files and Remove Origionals
        ## --------------------------------------
        
        for input_file in input_files:
            if input_file.endswith('.gz'):
                output_file = input_file.replace('.gz', '')
                
                print('Uncompressing: {}'.format(input_file))
            
                with gzip.GzipFile(input_file, 'rb') as infile, open(output_file, 'wb') as outfile:
                    outfile.write(infile.read())
                
                os.remove(input_file)
            
            else:
                print('File not .bz2 format: {}'.format(input_file))
                continue
        
        print('Files uncompressed')
        
        return None
    
    @staticmethod
    def zip_gz(filepath):
        """
        Compresses files into .gz format and removes the original uncompressed files.
        
        Parameters:
        -----------
            filepath: str
                File path pattern to uncompressed files, using '*' wildcard characters.
        
        Returns:
        --------
            None
        
        Raises:
        -------
            FileNotFoundError
        """
        
        ## ------------------------
        ## Find and Sort Data Files
        ## ------------------------
        
        input_files = glob(filepath)
        input_files.sort()
        
        ## -----------
        ## Check Files
        ## -----------
        
        if len(input_files) == 0:
            raise FileNotFoundError('File not found: {}'.format(filepath))
            
        ## ----------------------------------
        ## Compress Files and Remove Originals
        ## ----------------------------------
        
        for input_file in input_files:
            if not input_file.endswith('.gz'):
                output_file = input_file + '.gz'
                
                print('Compressing: {}'.format(input_file))
                
                with open(input_file, 'rb') as infile, gzip.GzipFile(output_file, 'wb') as outfile:
                    outfile.write(infile.read())
            
                os.remove(input_file)
                
            else:
                print('File already .gz format: {}'.format(input_file))
                continue
            
        print('Files compressed')
        
        return None