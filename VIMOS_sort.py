# -*- coding: utf-8 -*-
"""
Created on Tue Apr 30 11:15:39 2013

@author: jselsing
"""
import commands
import os.path
import pyfits
import numpy as np
import glob

#Getting relavant header keywords for sorting


class ReadHeader:
    def __init__(self, FitsName):
        if os.path.isfile(FitsName) != True:
            print 'File:\t'+FitsName+'\tdoes not exist'

        self.FitsName = FitsName

        ThisHeader =  pyfits.getheader(FitsName)
#        print ThisHeader.keys()
#        print ThisHeader
        #Quadrant Number
        if 'ESO OCS CON QUAD' in ThisHeader.keys():
            self.QuadrantNumber = str(ThisHeader['ESO OCS CON QUAD'])
        else:
            #print "Warning: HIERARCH ESO OCS CON QUAD not in header"
            self.QuadrantNumber = ""

        #Observation Date
        if 'DATE-OBS' in ThisHeader.keys():
            self.DateObs = str(ThisHeader['DATE-OBS'])
        else:
            #print "Warning: DATE-OBS not in header"
            self.DateObs = ""

        #Observation Date
        if 'MJD-OBS' in ThisHeader.keys():
            self.DateObsJulian = str(ThisHeader['MJD-OBS'])
        else:
            #print "Warning: MJD-OBS not in header"
            self.DateObsJulian = ""

        #Observation Type
        if 'ESO DPR TYPE' in ThisHeader.keys():
            self.ObsType = str(ThisHeader['ESO DPR TYPE'])
        else:
            #print "Warning: ESO DPR TYPE not in header"
            self.ObsType = ""
         #Observation Target
        if 'ESO OBS TARG NAME' in ThisHeader.keys():
            self.ObsTarget = str(ThisHeader['ESO OBS TARG NAME'])
        else:
            #print "Warning: ESO OBS TARG NAME not in header"
            self.ObsTarget = ""

        #Short file name
        if 'ARCFILE' in ThisHeader.keys():
            self.ShortName = str(ThisHeader['ARCFILE'])
        else:
            #print "Warning: ARCFILE not in header"
            self.ShortName = ""

        # Obs Id
        if 'ESO OBS ID' in ThisHeader.keys():
            self.ObsId = str(ThisHeader['ESO OBS ID'])
        else:
            #print "Warning: HIERARCH ESO OBS ID not in header"
            self.ObsId = ""

        # Obs RA
        if 'RA' in ThisHeader.keys():
            self.RA = str(ThisHeader['RA'])
        else:
            #print "Warning: RA not in header"
            self.RA = ""

        # Obs DEC
        if 'DEC' in ThisHeader.keys():
            self.DEC = str(ThisHeader['DEC'])
        else:
            #print "Warning: DEC not in header"
            self.DEC = ""

    def GetFitsName(self):
        return self.FitsName

    def GetQuadrantNumber(self):
        return self.QuadrantNumber

    def GetDateObsJulian(self):
        return self.DateObsJulian

    def GetDateObs(self):
        return self.DateObs

    def GetObsType(self):
        return self.ObsType

    def GetObsTarget(self):
        return "".join(self.ObsTarget.split())

    def GetShortName(self):
        return self.ShortName

    def GetObsId(self):
        return self.ObsId

    def GetRA(self):
        return self.RA

    def GetDEC(self):
        return self.DEC


class VISMOS_sort:
    """
    Python class for sorting VIMOS IFU data.\n
    Required inputs: Listoffiles \n
    Listoffiles can be supplied with the following commands: \n
        Listoffiles = glob.glob('*.fits') \n
        sort = VISMOS_sort() \n
        sort.InputFiles(Listoffiles) \n
    The sorting is then done by running: \n
        sort.RunSort()
    """
    def __init__(self):
        self.files = {}
        self.OutputDir = 'Sorted_Data'
        self.OutputSubDir = 'Object'
        self.OutputSubSubDir = 'Obs-full-name'
        self.OutputSubSubSubDir = 'Data_type'
        self.OutputSubSubSubSubDir = 'Quadrant_Number'

    def InputFiles(self, files):
        List = []
        for i in files:
            List.append(ReadHeader(i))
        self.files = List

    def Printer(self):
        for f in self.files:
#            print '\t',f.GetQuadrantNumber(),f.GetObsId(),f.GetObsType(),f.GetObsTarget()
            print '\t',f.GetQuadrantNumber(),f.GetDateObs(),f.GetObsId(),f.GetRA(),f.GetDEC(),f.GetObsType(),f.GetObsTarget()

    def RunSort(self):
        print 'VIMOS fits sorting tool, by Jonatan Selsing, Dark Cosmology Centre, 2013. -still a work in progress \n'

        if os.path.exists(self.OutputDir) == False:
            print 'Directory with name '+self.OutputDir+' does not exist.'
            commands.getoutput('mkdir '+self.OutputDir)
            print 'Directory with name '+ self.OutputDir +' has now been created.\n'

        # Making name lists for Bias sorting
        ListDates = []
        ListTargetNames = []
        ListTargetNamesFull = []
        for f in self.files:
            if f.GetObsType() == 'OBJECT' or f.GetObsType() == 'STD':
                ListDates.append(f.GetDateObsJulian())
                ListTargetNames.append(f.GetObsTarget())
                ListTargetNamesFull.append(f.GetObsTarget()+'-'+f.GetObsId()+'-'+f.GetRA()+'-'+f.GetDEC())

        # Making list for STD sorting
        ListDatesSCI = []
        ListTargetNamesSCI = []

        for f in self.files:
            if f.GetObsType() == 'OBJECT':
                ListDatesSCI.append(f.GetDateObsJulian())
                ListTargetNamesSCI.append(f.GetObsTarget()+'-'+f.GetObsId()+'-'+f.GetRA()+'-'+f.GetDEC())

        for f in self.files:
                    if f.GetObsType() == 'OBJECT' or f.GetObsType() == 'STD':
                        OutputSubDir = f.GetObsTarget()
                        self.OutputSubDir = OutputSubDir
                        OutputSubSubDir = f.GetObsTarget()+'-'+f.GetObsId()+'-'+f.GetRA()+'-'+f.GetDEC()
                        self.OutputSubSubDir = OutputSubSubDir

                    # Making exeption for Bias,Flat,Wave
                    for n in range(0,len(ListDates)):
                        if f.GetObsType() == 'BIAS' and abs(float(f.GetDateObsJulian()) - float(ListDates[n])) < 0.5:
                            self.OutputSubDir = ListTargetNames[n]
                            self.OutputSubSubDir = ListTargetNamesFull[n]

                        if f.GetObsType() == 'FLAT,LAMP' and abs(float(f.GetDateObsJulian()) - float(ListDates[n])) < 0.05 and float(f.GetDateObsJulian()) - float(ListDates[n]) > 0:
                            self.OutputSubDir = ListTargetNames[n]
                            self.OutputSubSubDir = ListTargetNamesFull[n]

                        if f.GetObsType() == 'WAVE,LAMP' and abs(float(f.GetDateObsJulian()) - float(ListDates[n])) < 0.05 and float(f.GetDateObsJulian()) - float(ListDates[n]) > 0:
                            self.OutputSubDir = ListTargetNames[n]
                            self.OutputSubSubDir = ListTargetNamesFull[n]

                        OutputSubSubSubDir = f.GetObsType()
                        self.OutputSubSubSubDir = OutputSubSubSubDir

                        OutputSubSubSubSubDir = 'Quadrant'+f.GetQuadrantNumber()
                        self.OutputSubSubSubSubDir = OutputSubSubSubSubDir

                        if f.GetObsType() == '':
                            self.OutputSubDir = 'Unmatched_files'
                            self.OutputSubSubDir = ''
                            self.OutputSubSubSubDir = ''
                            self.OutputSubSubSubSubDir = ''

                        # Creating directory name with name of object
                        if os.path.exists(self.OutputDir+'/'+self.OutputSubDir) == False:
                            print 'Subdirectory with name '+self.OutputSubDir+' does not exist.'
                            commands.getoutput('mkdir '+self.OutputDir+'/'+self.OutputSubDir)
                            print 'Subdirectory with name '+self.OutputSubDir+' has now been created.\n'

                        # Creating directory name with name of data type
                        if os.path.exists(self.OutputDir+'/'+self.OutputSubDir+'/'+self.OutputSubSubDir) == False:
                            print 'Subdirectory with name '+self.OutputSubSubDir+' does not exist.'
                            commands.getoutput('mkdir '+self.OutputDir+'/'+self.OutputSubDir+'/'+self.OutputSubSubDir)
                            print 'Subdirectory with name '+self.OutputSubSubDir+' has now been created.\n'
                        # Creating directory name with quadrant number
                        if os.path.exists(self.OutputDir+'/'+self.OutputSubDir+'/'+self.OutputSubSubDir+'/'+self.OutputSubSubSubDir) == False:
                            print 'Subdirectory with name '+self.OutputSubSubSubDir+' does not exist.'
                            commands.getoutput('mkdir '+self.OutputDir+'/'+self.OutputSubDir+'/'+self.OutputSubSubDir+'/'+self.OutputSubSubSubDir)
                            print 'Subdirectory with name '+self.OutputSubSubSubDir+' has now been created.\n'

                        if os.path.exists(self.OutputDir+'/'+self.OutputSubDir+'/'+self.OutputSubSubDir+'/'+self.OutputSubSubSubDir+'/'+self.OutputSubSubSubSubDir) == False:
                            print 'Subdirectory with name '+self.OutputSubSubSubSubDir+' does not exist.'
                            commands.getoutput('mkdir '+self.OutputDir+'/'+self.OutputSubDir+'/'+self.OutputSubSubDir+'/'+self.OutputSubSubSubDir+'/'+self.OutputSubSubSubSubDir)
                            print 'Subdirectory with name '+self.OutputSubSubSubSubDir+' has now been created.\n'

                        # Copying files into corresponding directory
                        if os.path.isfile(self.OutputDir+'/'+self.OutputSubDir+'/'+self.OutputSubSubDir+'/'+self.OutputSubSubSubDir+'/'+'/'+self.OutputSubSubSubSubDir+'/'+f.GetShortName()) == False:
                            print 'Copying file of type '+f.GetObsType()+' to directory '+self.OutputDir+'/'+self.OutputSubDir+'/'+self.OutputSubSubDir+'/'+self.OutputSubSubSubDir+'/'+self.OutputSubSubSubSubDir+'/'
                            commands.getoutput('cp '+f.GetFitsName()+' '+self.OutputDir+'/'+self.OutputSubDir+'/'+self.OutputSubSubDir+'/'+self.OutputSubSubSubDir+'/'+self.OutputSubSubSubSubDir+'/')

        STDList = []
        for f in self.files:
            if f.GetObsType() == 'OBJECT' or f.GetObsType() == 'STD':
                if f.GetQuadrantNumber() == '1':
                    dummy = [f.GetDateObs(),f.GetObsType(),f.GetObsTarget()]
                    STDList.append(dummy)
        np.savetxt('Sorted_Data/Listoffiles',STDList, fmt='%s %s %s')
        print 'The files have been sorted according to appropriate header-keywords.'


if __name__ == '__main__':



    listoffiles = glob.glob("path_to_files/*.fits")


    x = VISMOS_sort()

    x.InputFiles(listoffiles)


    #x.Printer()
    x.RunSort()
