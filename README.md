# foldpsrfits
Python module for reading in fold-psrfits files

Requires pyfits

To use:

<pre>import foldpsrfits as pf</pre>

To open the file and read in the data:

<pre>
fh = pf.psrfits(fname='path_to_file',DM=dispersion_measure,fref=reference_freq)
fh.fits.close() # Close the fits file to save memory
</pre>

DM and fref are optional arguments, if they are not included but a filename is, then they will be determined from the headers.  DM is in pc/cm^3 and fref in MHz.  If you don't want incoherent dedisperion to be done when the file is read in, give DM=0

Now you can see the data, original fits file, etc:
<pre>
fh.data # the data (after incoherent dedispersion), 4-dimensional array (time,pol,freq,phase)
fh.fits # equivalent to pyfits.open(fname='filename')
fh.freq # the freq axis
fh.time # the time axis
</pre>
