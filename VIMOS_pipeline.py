



# -*- coding: utf-8 -*-
"""
Created on Thu May 23 10:50:27 2013

@author: jselsing
"""

import pidly
import glob
import commands
import numpy as np

#Global parameters
idl = pidly.IDL()
idl('parfile="nvimos_mr.prm"')
commands.getoutput('mkdir Output')
idl('opath="Output"')


#Set the target-specific parameter file
userparfile='user_p3d.prm'



###############################################################################
#Bias
MasterBias = []
for n in np.arange(0,4):
    n = str(n+1)    
#    BiasFiles = str(glob.glob('BIAS/Quadrant'+n+'/*.fits'))
#    detector=str(int(n)-1) 
#    idl('p3d_cmbias,'+BiasFiles+',parfile,userparfile="'+userparfile+'",opath=opath,detector='+detector+',logfile=opath+"/biasred'+n+'.log",/verbose,ofilename=ofilename')
#    MasterBias.append("'"+str(idl.ofilename)+"'")
    MasterBias.append(str(glob.glob('Output/*mbias'+n+'.fits')))


###############################################################################
#Trace
TraceMask =[]
for n in np.arange(0,4):
    n = str(n+1)
#    TraceFiles = str(glob.glob('FLAT,LAMP/Quadrant'+n+'/*.fits'))
#    detector=str(int(n)-1) 
#    idl('p3d_ctrace,'+TraceFiles+',parfile,masterbias='+MasterBias[int(n)-1]+',userparfile="'+userparfile+'",opath=opath,detector='+detector+',logfile=opath+"/tracemask'+n+'.log",/verbose,ofilename=ofilename')
#    TraceMask.append("'"+str(idl.ofilename)+"'")
#    x = raw_input()
    TraceMask.append(str(glob.glob('Output/*trace'+n+'.fits')))

###############################################################################
##Dispersion solution
DispMaskIn = []
for n in np.arange(0,4):
    n = str(n+1)
    DispMaskIn.append(str(glob.glob('/Users/jselsing/Work/VIMOS/GRB_counterparts/dispmaskin/*dmask'+n+'.fits')))


DispersionMask = []
for n in np.arange(0,4):
    n = str(n+1)
    DispersionFiles = str(glob.glob('WAVE,LAMP/Quadrant'+n+'/*.fits'))  
    detector=str(int(n)-1) 
    idl('p3d_cdmask,'+DispersionFiles+',parfile,masterbias='+MasterBias[int(n)-1]+',tracemask='+TraceMask[int(n)-1]+',dispmaskin='+DispMaskIn[int(n)-1]+',userparfile="'+userparfile+'",opath=opath,detector='+detector+',logfile=opath+"/dispersionmask'+n+'.log",/verbose,ofilename=ofilename')
    DispersionMask.append("'"+str(idl.ofilename)+"'")
#    DispersionMask.append(str(glob.glob('Output/*dmask'+n+'.fits')))
#        dispmaskin='+DispMaskIn[int(n)-1]+',
    
###############################################################################
#Flat Field
FlatField = []
for n in np.arange(0,4):
    n = str(n+1)
    FlatFieldFiles = str(glob.glob('FLAT,LAMP/Quadrant'+n+'/*.fits'))
    detector=str(int(n)-1) 
    idl('p3d_cflatf,'+FlatFieldFiles+',parfile,masterbias='+MasterBias[int(n)-1]+',tracemask='+TraceMask[int(n)-1]+',dispmask='+DispersionMask[int(n)-1]+',userparfile="'+userparfile+'",opath=opath,detector='+detector+',logfile=opath+"/flatfield'+n+'.log",/verbose,ofilename=ofilename')
    FlatField.append("'"+str(idl.ofilename)+"'")
#    FlatField.append(str(glob.glob('Output/*flatf'+n+'.fits')))   



###############################################################################
#Science Reduction
Science = []
for n in np.arange(0,4):
    n = str(n+1)
    ScienceFiles = str(glob.glob('OBJECT/Quadrant'+n+'/*.fits'))   
    detector=str(int(n)-1) 
    idl('p3d_cobjex,'+ScienceFiles+',parfile,masterbias='+MasterBias[int(n)-1]+',tracemask='+TraceMask[int(n)-1]+',dispmask='+DispersionMask[int(n)-1]+',flatfield='+FlatField[int(n)-1]+',userparfile="'+userparfile+'",opath=opath,detector='+detector+',/crclean,logfile=opath+"/sciencered'+n+'.log",/verbose,ofilename=ofilename')
    Science.append("'"+str(idl.ofilename)+"'")
#    Science.append(glob.glob('Output/*crcl_oextr'+n+'.fits'))

##################################################################################
#Science Flux Calibration
    
SensitivityFunction = []
for n in np.arange(0,4):
    n = str(n+1)    
    SensitivityFunction.append(str('stdspec'+n+'_fluxsens.fits')) 
    
    
ScienceCal = []
for n in np.arange(0,4):
    n = str(n+1)
    extinctionfile = "'/Users/jselsing/Work/VIMOS/GRB_counterparts/Calibration_Files/Atmospheric_Extinction/M.VIMOS.2011-06-28T15:33:40.456.fits'" 
    detector=str(int(n)-1) 
    idl('p3d_fluxcal,'+str(Science[int(n)-1])+',parfile,sensfunc="'+str(SensitivityFunction[int(n)-1])+'",extinctionfile='+extinctionfile+',userparfile="'+userparfile+'",opath=opath,logfile=opath+"/fluxcal'+n+'.log",/verbose,ofilename=ofilefluxcal')
    ScienceCal.append(str(idl.ofilefluxcal))


###############################################################################
#Combination of Images         
idl('p3d_cvimos_combine,'+str(ScienceCal)+',parfile,userparfile="'+userparfile+'",opath=opath,logfile=opath+"/scicombred.log",/verbose,ofilename=ofilecomb')
idl('file = ofilecomb')
idl('p3d_darc,file,parfile,userparfile="'+userparfile+'",method=0,opath=opath,logfile=opath+"/darccorr.log",/verbose,ofilename=ofilename')
#print idl.ofilename
################################################################################
#Plot the resulting combined image
idl('image=readfits(ofilename,header,EXTEN_NO = 1)')
idl('p3d_rss,image,parfile=parfile,hdr=header,colortable=-1,/verbose')
x = raw_input()
    
    
    