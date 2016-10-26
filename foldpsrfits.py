import numpy as np
import pyfits


class psrfits:
    def __init__(self,fname=None,fref=None,DM=None):
        self.fits = None
        self.data = None
        if fname !=None:
            self.open(fname)
            self.get_data(fref,DM)


    def open(self, filename):
        self.fits  = pyfits.open(filename)
        if self.fits['PRIMARY'].header['FITSTYPE'] != 'PSRFITS':
            raise IOError('Not a psrfits file.')
        if self.fits['HISTORY'].data[0][6] == 0:
            raise IOError('This data is in search mode. I only read psrfits files in Fold mode.  Try the pypsrfits module by Paul Demorest.')

    def get_data(self,fref,DM):
        if fref==None:
            fref = self.fits['HISTORY'].data[0][9]
        if DM==None:
            DM = self.fits['SUBINT'].header['DM']    
        print( 'freq_ref = ' + str(fref) + ' MHz')
        print( 'DM = ' + str(DM) + ' pc cm^-3')
        tbin = self.fits['HISTORY'].data[0][8]
        data = self.fits['SUBINT'].data[0][9]
        freq = self.fits['SUBINT'].data[0][5]
        I = np.zeros(data.shape,dtype=np.int)
        for i in np.arange(len(freq)):
            dt = 4.18808*10.**(3.) * DM * (1./fref**2.-1/freq[i]**2.)
            tshift = np.int(np.rint(dt/tbin))
            I[:,i,:] = np.roll(data[:,i,:],tshift,axis=1)
        self.data = I

    def close(self):
        self.fits.close()

