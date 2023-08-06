# rfiflagger

RFI Flagger allows CASA users to generate a flag-file for calibration based off entries in the RFI database.

# Dependencies

1. This will need to be run on a NRAO-networked  machine. 
2. Psycopg2, a PostgreSQL adapter for the Python programming language.
3. Python 3.6 (or later) to install CASA 6
4. Numpy
5. Pandas
6. datetime

# Installation

Clone the package to your machine and install

```bash
cd rfiflag_package/
```

```bash
pip install .
```

Installation of CASA into python3.6
```python
import os
os.system("apt-get install libgfortran3")
os.system("pip install --extra-index-url https://casa-pip.nrao.edu/repository/pypi-group/simple casatools")
os.system("pip install --extra-index-url https://casa-pip.nrao.edu/repository/pypi-group/simple casatasks")
os.system("mkdir ~/.casa")
!echo home, datapath = \'/content/\', [\'/content/\'] > ~/.casa/toolrc.py
!more /root/.casa/toolrc.py
```


# Example 1
This is the simplest method to create and apply flags to your measurement-set

```python
import rfiflag as rf

# Extract the RFI database into a dataframe
df = rf.extractDB(password='12345', output='db.csv')

# Match flags to observation and apply via flagdata
datasetid = '2016A-12345'
simple_flag(df, datasetid)
```

# Example 2
This example uses the underlying methods for added flexibility

```python
import rfiflag as rf

# Extract the RFI database into a dataframe
df = rf.extractDB(password='12345', output='db.csv')

datasetid = '20A-156.sb38236874.eb38553221.59061.04613805556'
msname = datasetid + '.ms'
flagfile = datasetid + '_rfidb_flags.txt'

rfi_per_antenna(df, datasetid)
rfi_to_flagfile(df, datasetid, remove_intermediate=False)
run_flag_commands(msname, flagfile, tbuff=10.0)
```