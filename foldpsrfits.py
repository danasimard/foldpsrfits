import numpy as np
import pyfits


class psrfits:
    def __init__(self,fname=None,fref=None,DM=None):
        self.fits = None
        self.data = None
        self.freq = None
        self.time = None
        if fname != None:
            self.open(fname)
            self.get_data(fref,DM)


    def open(self, filename):
        # Open the pyfits file and check that is is a fold mode psrfits file
        self.fits  = pyfits.open(filename)
        if self.fits['PRIMARY'].header['FITSTYPE'] != 'PSRFITS':
            raise IOError('Not a psrfits file.')
        if self.fits['HISTORY'].data[0][6] == 0:
            raise IOError('This data is in search mode. I only read psrfits files in fold mode.  Try the pypsrfits module by Paul Demorest.')

    def get_data(self,fref,DM):
        self.freq = self.fits['SUBINT'].data[0][5]
        shape = self.fits['SUBINT'].data[0][9].shape
        ntime = self.fits['SUBINT'].header['NAXIS2']
        self.time = np.array([0.])
        data = np.zeros((ntime,shape[0],shape[1],shape[2]))
        for i in np.arange(ntime):
            self.time=np.append(self.time,self.time[-1]+self.fits['SUBINT'].data[i][1])
            if np.any((self.fits['SUBINT'].data[i][5] != self.freq)):
                raise RuntimeError('Frequency channels of subint ' + str(i) + ' are not aligned with those of subint 0.')
            data[i,:,:,:] = self.fits['SUBINT'].data[i][9]
            
        # Incoherent shift of channels
        if DM != 0:
            if fref==None:
                fref = self.fits['HISTORY'].data[0][9]
            if DM==None:
                DM = self.fits['SUBINT'].header['DM']    
            print( 'freq_ref = ' + str(fref) + ' MHz')
            print( 'DM = ' + str(DM) + ' pc cm^-3')
            tbin = self.fits['HISTORY'].data[0][8]
            I = np.zeros(data.shape,dtype=np.int)
            for i in np.arange(len(self.freq)):
                dt = 4.18808*10.**(3.) * DM * (1./fref**2.-1./self.freq[i]**2.)
                tshift = np.int(np.rint(dt/tbin))
                I[:,:,i,:] = np.roll(data[:,:,i,:],tshift,axis=2)
        else:
            I = data
        self.data = I

    def close(self):
        # Close the pyfits file.  Headers will still be accessible
        self.fits.close()


