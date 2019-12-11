import sys
import os
from cx_Freeze import setup, Executable

import distutils
import opcode

os.environ['TCL_LIBRARY'] = "C:/Users/DGingerich2/Anaconda3/tcl/tcl8.6"
os.environ['TK_LIBRARY'] = "C:/Users/DGingerich2/Anaconda3/tcl/tk8.6"

distutils_path = os.path.join(os.path.dirname(opcode.__file__), 'distutils')
build_exe_options = {"packages": ["os", "numpy"],
                     "includes": ["tkinter", "numpy.core._methods", "numpy.lib.format", "numpy.core._dtype_ctypes"],
#                     "include_files":[
                     "include_files": [(distutils_path, 'lib/distutils'),
                                       r'C:/Users/DGingerich2/OneDrive/Research/05 Active Research Projects/Water AHEAD GUI/Water AHEAD GUI Coding/water-ahead/Code/chem_manufacturing_distribution_dictionary.py',
                                       r'C:/Users/DGingerich2/OneDrive/Research/05 Active Research Projects/Water AHEAD GUI/Water AHEAD GUI Coding/water-ahead/Code/empty_state_dictionary.py',
                                       r'C:/Users/DGingerich2/OneDrive/Research/05 Active Research Projects/Water AHEAD GUI/Water AHEAD GUI Coding/water-ahead/Code/unit_chem_consumption.py',
                                       r'C:/Users/DGingerich2/OneDrive/Research/05 Active Research Projects/Water AHEAD GUI/Water AHEAD GUI Coding/water-ahead/Code/unit_elec_consumption.py',
                                       r'C:/Users/DGingerich2/OneDrive/Research/05 Active Research Projects/Water AHEAD GUI/Water AHEAD GUI Coding/water-ahead/Code/unit_therm_consumption.py',
                                       r'C:/Users/DGingerich2/OneDrive/Research/05 Active Research Projects/Water AHEAD GUI/Water AHEAD GUI Coding/water-ahead/Data'],
                     'excludes': ['distutils']}
base = None
if sys.platform == 'win32':
    base = 'Win32GUI'

setup(name='Water AHEAD',
      version='0.1',
      description='Water Associated Health and Environmental Air Damages Tool created by the WE3 Lab',
      author='WE3 Lab',
      options={'build_exe': build_exe_options},
      executables=[Executable('water_ahead_gui.py', base=base, shortcutDir='Water AHEAD', shortcutName='Water AHEAD')])
