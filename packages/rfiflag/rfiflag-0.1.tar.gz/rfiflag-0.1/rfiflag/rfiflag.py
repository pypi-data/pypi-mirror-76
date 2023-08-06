import os
import numpy as np
import pandas as pd
import datetime
import casatools as cts
from casatasks import flagdata


def rfi_per_antenna(dataframe, datasetid):
  '''This creates a file of RFI in each antenna'''

  # Getting a list of unique antennas in the dataframe:
  antennas = pd.unique(dataframe.antenna)

  # Sub-select the dataframe on antenna and extract the matching RFI info:
  for antenna in antennas:
    ant_df = dataframe[(dataframe.datasetid==datasetid) & (dataframe.antenna==antenna)]

    # Extracting antenna info to ant file to check for flags (kept for troubleshooting)
    ant_rfi = ant_df.loc[:,['fc','width','at', 'scanno']]
    ant_rfi.to_csv('%s_rfi.txt' % antenna, sep=' ', index=False, header=False)


def rfi_to_flagfile(dataframe, datasetid, remove_intermediate=False):
  '''This creates a flagfile for the MS based on RFI per antenna files'''

  # Initializing CASA tools
  msmd = cts.msmetadata()
  qt = cts.quanta()

  # Open a flagfile to write flags into:
  if os.path.exists('%s_rfidb_flags.txt' % datasetid):
    os.system('rm %s_rfidb_flags.txt' % datasetid) # safety check
  f = open('%s_rfidb_flags.txt' % datasetid, 'a')

  # Getting the range of frequencies from the MS; flags outside will not be written to the file (used in loop below)
  msname = datasetid + '.ms'
  msmd.open(msname)
  nspw = msmd.nspw()
  min_freq = msmd.chanfreqs(spw=0, unit='MHz')[0]   
  max_freq = msmd.chanfreqs(spw=nspw-1, unit='MHz')[-1]  

  # Go through each antenna (file) and extract RFI that is within bounds of the MS
  antennas = pd.unique(dataframe.antenna)
  for antenna in antennas:

    # Reading antenna flag file, read each line, adjust format, and write flags within bounds
    ant_rfi = open('%s_rfi.txt' % antenna, 'r').readlines()
    flags = []
    for line in ant_rfi:
      
      # unloading RFI line into each part
      fc, width, date, time, scan = line.split()
      width = 128 # hardcoding width for troubleshooting (too wide falls outside range and no flags added)
  
      # Getting the RFI frequency peak and width; getting start and end frequency based on width
      fc = float(fc.strip()) # strip whitespaces
      fc_start = fc - (0.5 * float(width))
      fc_end = fc + (0.5 * float(width))

      # If RFI frequency outside the MS frequency range skip adding it to the flagfile and go to next RFI entry
      # If the width is large enough to go out of bounds, it will not write to flagfile
      if fc_end < min_freq or fc_start > max_freq:
        print(f"Antenna {antenna} RFI frequency {fc_start, fc_end} outside range {min_freq, max_freq} in MS")
        continue

      # Get scan's time range from MS; convert from MJD to H/M/S and compare to RFI observed time
      try:
        scan_times = msmd.timesforscans(scans=int(scan))
      except:
        print(f"Scan {scan} (from DB) doesn't exist for {antenna} antenna (in MS); observation issue?")
        # break here to go to next antenna file entirely ; 
        break
        
      scan_start = scan_times[0]
      scan_end = scan_times[-1]
      qss = qt.quantity(scan_start, 's')
      qse = qt.quantity(scan_end, 's')
      scan_start = qt.formxxx(qss, 'hms')
      scan_end = qt.formxxx(qse, 'hms')

      # RFI observed time; Pandas handled timezone correction; reconstruct datetime string
      rfi_date = date.replace('-','/').strip('"')
      rfi_time = time.strip('"')[:-6] 
      start_datetime = '%s/%s' % (rfi_date, rfi_time)

      # flagdata list mode needs a range, create the end-time for the range 
      # THIS IS CRUDE, DOES NOT ACCOUNT FOR ROLLOVER TO MINUTES HOURS OR DATES
      hr = rfi_time.split(':')[0]
      min = rfi_time.split(':')[1]
      sec = str(float(rfi_time.split(':')[-1]) + 1.0)
      end_time = '%s:%s:%s' % (hr, min, sec)
      end_datetime = '%s/%s' % (rfi_date, end_time)

      # If RFI was observed outside of the MS scan times skip adding it to flagfile
      if rfi_time < scan_start or end_time > scan_end:
        print(f"Antenna {antenna} RFI time {rfi_time, end_time} outside range {scan_start, scan_end} in MS")
        continue

      # Putting together the whole flag command in CASA format and writing to file
      # As per CAS 13091 ticket, add a range to timerange if using in list mode when running flag file
      flag = "antenna='%s&&*' scan='%s' spw='*:%s~%sMHz' timerange='%s~%s' reason='RFI_DB'\n" % (antenna, scan, fc_start, fc_end, start_datetime, end_datetime)
      f.write(flag)

    # Removing individual antenna RFI file now that it's written
    if remove_intermediate == True:
      os.system('rm %s_rfi.txt' % antenna)

  # Close the flagging file:
  f.close()

  # Closing the CASA tools
  qt.done()
  msmd.done()
  msmd.close() # redundancy 
  print('Flag file complete')


def run_flag_commands(ms, flagfile, tbuff=0.0):
	'''Run CASAs flagdata with the input flagfile and optional tbuff parameter'''

	# Run flagdata in list mode with flagfile
	# tbuff parameter extends flags in time across the duration of our stacker integration set in agrab.py 
	print('Running flagdata')
	flagdata(vis=ms, mode='list', tbuff=tbuff, inpfile=flagfile)
	return


def simple_flag(dataframe, datasetid):
	''' A simple one-method-does-all function for extracting and applying flags'''
	rfi_per_antenna(dataframe, datasetid)
	rfi_to_flagfile(dataframe, datasetid, remove_intermediate=True)
	run_flag_commands(datasetid+'.ms', datasetid+'_rfidb_flags.txt', tbuff=0.0)
	return


