# -*- coding: utf-8 -*-
"""
Created on Fri Feb 22 22:01:25 2019

@author: RAMIAN
"""

#TODO: errorhandling


def Iqiq2Complex( iqData):
    """Returns a complex list of I/Q samples from a single list containing IQIQIQ values
    complexList = Iqiq2Complex(iqiqiqList)"""

    import logging
    
    if len(iqData) % 2 > 0:
        logging.warn("Expecting IQIQIQ order, input vector has odd number of samples!")

    NumberOfSamples = len(iqData) // 2
                    
    complexList = [ complex( iqData[2*n], iqData[2*n+1]) for n in range(NumberOfSamples)]    
    return complexList



def Iiqq2Complex( iqData):
    """Returns a complex list of I/Q samples from a single list containing IIIQQQ values
    complexList = Iiqq2Complex(iiiqqqList)"""
    
    import logging
    
    if len(iqData) % 2 > 0:
        logging.warn("Expecting IIIQQQ order, input vector has odd number of samples!")

    NumberOfSamples = len(iqData) // 2
                    
    complexList = [ complex( iqData[n], iqData[n+NumberOfSamples]) for n in range(NumberOfSamples)]    
    return complexList



def Complex2Iqiq( complexList):
    """Returns a list of I/Q samples from a complex list.
    iqiqiqList = Complex2Iqiq(complexList)"""
    
    f= lambda iq,i: iq.real if i==0 else iq.imag
    iqiqiqList = [ f(iq,i) for iq in complexList for i in range(2)]

    return iqiqiqList



def Complex2Iiqq( complexList):
    """Returns a list of I/Q samples from a complex list.
    iiiqqqList = Complex2Iiqq(complexList)"""
    
    iqiqiqList = [ iq.real for iq in complexList]
    iqiqiqList.append( [ iq.imag for iq in complexList])        

    return iqiqiqList


def WriteIqw( iqData, FileName):
    """Writes an IQW file (file of binary floats).
    iqData can be a list of complex or list of floats. List of floats will
    be written directly into iqw - regardles of order iiqq or iqiq.
    Note: IIIQQQ is a deprecated format, don't use it for new files.
    writtenSamples = WriteIqw( iqList, "MyFile.iqiq.iqw")."""
    
    import struct
    import logging
    
    #check if iqData is complex
    if isinstance(iqData[0], complex):
        iqData = Complex2Iqiq( iqData)
        
    NumberOfSamples = len(iqData) // 2
        
    try:
        file = open( FileName, "wb")
        file.write( struct.pack("f"*len(iqData),*iqData))
        file.close
    except:
        logging.error("File (" + FileName +") write error!" )
    
    return NumberOfSamples
  

      
def ReadIqw( FileName, iqiq = True):
    """Reads an IQW (can be iiqq or iqiq) file. Returns complex samples.
    If iqiq is True, samples are read pairwise (IQIQIQ),
    otherwise in blocks, i first then q (IIIQQQ)
    Note: IIIQQQ is a deprecated format, don't use it for new files.
    iqList = ReadIqw("MyFile.iqw", iqiq = True)"""
    
    import struct
    import logging
        
    BytesPerValue = 4
    
    try:
        file = open( FileName, "rb")
        data = file.read()
        file.close
    except:
        logging.error( "File open error ("+ FileName+")!")    
        
    ReadSamples = len(data) // BytesPerValue
    data = list(struct.unpack("f"*ReadSamples, data))
    if iqiq:
        data = Iqiq2Complex( data) 
    else:
        data = Iiqq2Complex( data)
    
    return data
        
                         

def WriteWv( iqData, fSamplingRate, FileName):
    """Writes a WV file.
    iqData can be a list of complex or list of floats (iqiqiq format mandatory).
    writtenSamples = WriteWv("MyFile.wv",complexList, fs)"""
    
    import struct
    from datetime import date
    import math
    import logging
    
    #check if iqData is complex
    if isinstance( iqData[0], complex):
        iqData = Complex2Iqiq( iqData)
        
    NumberOfSamples = len(iqData) // 2
         
    #Find maximum magnitude and scale for max to be FullScale (1.0)
    power = []
    for n in range(NumberOfSamples):
        power.append(abs(iqData[2*n]**2 + iqData[2*n+1]**2))
    scaling = math.sqrt( max(power))
    
    # normalize to magnitude 1
    iqData = [ iq / scaling for iq in iqData]
    
    #calculate rms in dB (below full scale)
    rms = math.sqrt(sum(power)/NumberOfSamples)/scaling
    rms = abs(20*math.log10( rms))
    # Convert to int16, use floor function, otherwise distribution is not correct
    iqData = [ math.floor(iq * 32767 +.5) for iq in iqData]
        
    try:
        file = open( FileName, "wb")
        file.write( "{TYPE: SMU-WV,0}".encode("ASCII"))
        file.write( "{COMMENT: R&S WaveForm, TheAE-RA}".encode("ASCII"))
        file.write( ("{DATE: " + str(date.today())+ "}").encode("ASCII"))
        file.write( ("{CLOCK:" +str(fSamplingRate) + "}").encode("ASCII"))
        file.write( ("{LEVEL OFFS:" +  "{:2.4f}".format(rms) + ",0}").encode("ASCII"))
        file.write( ("{SAMPLES:" + str(NumberOfSamples) + "}").encode("ASCII"))
    #TODO: markers
    #     if( m1start > 0 && m1stop > 0)
    #        %Control Length only needed for markers
    #        fprintf(file_id,'%s',['{CONTROL LENGTH:' num2str(data_length) '}']);
    #        fprintf(file_id,'%s',['{CLOCK MARKER:' num2str(fSamplingRate) '}']);
    #        fprintf(file_id,'%s',['{MARKER LIST 1: ' num2str(m1start) ':1;' num2str(m1stop) ':0}']);
    #    end
        file.write( ("{WAVEFORM-" +  str(4*NumberOfSamples+1) + ": #").encode("ASCII"))
        
        file.write( struct.pack("h"*len(iqData),*iqData))
        file.write( "}".encode("ASCII"))
        file.close()
    except:
        logging.error("File (" + FileName +") write error!" )
        
    return NumberOfSamples
    
    
def ReadWv( FileName):
    """Reads a WV file. Returns a list with complex numbers (I/Q) and the sampling rate
    iqiqiqList,fs = ReadWv("MyFile.wv")"""
    
    import re
    import struct
    import logging
    
    try:
        file = open(FileName, "rb")
        data = file.read()   
        file.close()
    except:
        logging.error( "File open error ("+ FileName+")!")

    binaryStart = 0
    tags = ""
    Counter = 0
    ConverterSize = 20
    while (binaryStart == 0) & (Counter < len(data)):
        tags += data[Counter:Counter+ConverterSize].decode("ASCII","ignore")
        Counter += ConverterSize
        #{WAVEFORM-20001: #
        res = re.search("WAVEFORM.{0,20}:.{0,3}#",tags)
        if res != None:
            binaryStart = res.span()[1]
    
    if (Counter > len(data)) & (binaryStart == 0):
        logging.warn( "Required tags not found, potentially incompatible file format!")
        
    res = re.search("SAMPLES[ ]*:[ ]*(?P<NumberOfSamples>[0-9]*)",tags)
    NumberOfSamples = int( res.group("NumberOfSamples"))
    res = re.search("CLOCK[ ]*:[ ]*(?P<SamplingRate>[0-9]*)",tags)
    SamplingRate = float( res.group("SamplingRate"))
    data = list(struct.unpack("h"*NumberOfSamples*2, data[binaryStart:-1]))
    data = list(map( lambda x: x/32767.0, data ))
    data = Iqiq2Complex( data)
    return data,SamplingRate



def __WriteXml( fs, NumberOfSamples, filenameiqw, filenamexml):
    """Function to write the xml part of the iq.tar
    __WriteXml( samplingrate, numberofsamples, filenameiqw, filenamexml)"""
    
    from datetime import datetime
    
    xmlfile = open ( filenamexml, "w")
    
    xmlfile.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
    xmlfile.write("<?xml-stylesheet type=\"text/xsl\" href=\"open_IqTar_xml_file_in_web_browser.xslt\"?>\n")
    xmlfile.write("<RS_IQ_TAR_FileFormat fileFormatVersion=\"2\" xsi:noNamespaceSchemaLocation=\"http://www.rohde-schwarz.com/file/RsIqTar.xsd\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\">\n")
    #Optional
    xmlfile.write("<Name>Python iq.tar Writer (iqdata.py)</Name>\n")
    #Optional
    xmlfile.write("<Comment>RS WaveForm, TheAE-RA</Comment>\n")
    xmlfile.write("<DateTime>"+ datetime.now(None).isoformat() +"</DateTime>\n")
    xmlfile.write("<Samples>" + str(NumberOfSamples) + "</Samples>\n")
    xmlfile.write("<Clock unit=\"Hz\">" + str(fs) + "</Clock>\n")
    xmlfile.write("<Format>complex</Format>\n")
    xmlfile.write("<DataType>float32</DataType>\n")
    #Optional
    xmlfile.write("<ScalingFactor unit=\"V\">1</ScalingFactor>\n")
    #Optional
    #xmlfile.write("<NumberOfChannels>1</NumberOfChannels>\n")
    xmlfile.write("<DataFilename>" + filenameiqw+ "</DataFilename>\n")
    #Optional
    #xmlfile.write("<UserData></UserData>\n")
    xmlfile.write("</RS_IQ_TAR_FileFormat>\n")
    xmlfile.close()
    
    return



def WriteIqTar( iqData, fs, FileName):
    """Writes an iq.tar file. Complex iqData values are interpreted as Volts.
    iqData can be a list of complex or list of floats (iqiqiq format).
    writtenSamples = WriteIqTar(iqList,fs,"MyFile.iq.tar")"""
    
    import tarfile
    import os
    import re
    import logging
    
    path,filename = os.path.split(FileName)
       
    #Create binary file
    binaryfile = re.sub( "iq.tar", "complex.1ch.float32", filename, flags=re.IGNORECASE)
    NumberOfSamples = WriteIqw( iqData, os.path.join(path, binaryfile))
    if NumberOfSamples == 0:
        return 0
    
    #xsltfilename = "open_IqTar_xml_file_in_web_browser.xslt"
    
    xmlfilename = re.sub( "iq.tar", "xml", filename, flags=re.IGNORECASE)
    __WriteXml( fs, NumberOfSamples, binaryfile, os.path.join(path, xmlfilename))
    
    try:
        tar = tarfile.open( FileName, "w")
        tar.add( os.path.join(path, binaryfile), arcname=binaryfile)
        #xslt is optional
        #tar.add( os.path.join(path, xsltfilename), arcname=xsltfilename)
        tar.add( os.path.join(path, xmlfilename), arcname=xmlfilename)
        tar.close()
        os.remove( os.path.join(path, binaryfile))
        os.remove( os.path.join(path, xmlfilename))
    except:
        logging.error("IqTar (" + FileName +") write error!" )
    
    return NumberOfSamples



def ReadIqTar( FileName, ChannelToRead = 1):
    """Reads an iq.tar file. 
    data,fs = ReadIqTar("MyFile.iq.tar", ChannelToRead = 1)
    ChannelToRead specifies the channel to be read. "0" reads all channels and returns a matrix."""
    
    import tarfile
    import os
    import xml.etree.ElementTree as ET
    import logging
    
    filename = os.path.split(FileName)[1]
    data=[]
    fs = 0
        
    try:
        tar = tarfile.open( FileName, "r:")
        a=tar.getnames()
        xmlfile = [filename for filename in a if ".xml" in filename.lower()]
        xmlfile = xmlfile[0]
        tar.extract(xmlfile)
        tree = ET.parse(xmlfile)
        root = tree.getroot()
        binaryfilename = root.find("DataFilename").text
        fs = float(root.find("Clock").text)

        helper = root.find("Samples")
        NumberOfSamples = 1
        if helper.text:
            NumberOfSamples = int(root.find("Samples").text)
        
        helper = root.find("ScalingFactor")
        ScalingFactor = 1
        if helper.text:
            if helper.get("unit")!="V":
                logging.warn("Only (V)olts scaling factor supported - assuming 1V!")
            else:
                ScalingFactor = float(root.find("ScalingFactor").text)

        helper = root.find("NumberOfChannels")
        NumberOfChannels = 1
        if helper != None:
            if helper.text:
                NumberOfChannels = int(root.find("NumberOfChannels").text)
                    
        os.remove( xmlfile)
        del root
        tar.extract(binaryfilename)
        tar.close()
        data = ReadIqw( binaryfilename)
        os.remove( binaryfilename)
        
    except:
        logging.error("IqTar (" + FileName + ") read error!" )
    
    #Apply scaling factor
    if ScalingFactor != 1:
        data = [sample * ScalingFactor for sample in data]

    #separate channels
    if NumberOfChannels > 1:
        
        if (ChannelToRead > NumberOfChannels):
            logging.warn("File " + FileName + " only contains " + str(NumberOfChannels) + " channels, using channel 1!")
            ChannelToRead = 1
        if ChannelToRead > 0:
            data1 = []
            #for n in range(NumberOfSamples):
                #data1.append( data[n*NumberOfChannels+ChannelToRead-1])
            data1 = data[ChannelToRead-1::NumberOfChannels]
        else:
            import numpy
            data1 = numpy.empty((NumberOfSamples,NumberOfChannels),dtype = complex)
            for n in range(NumberOfSamples):
                for m in range(NumberOfChannels):
                    if m==0:
                        data1[n][m] = data[n*NumberOfChannels+m]
        data = data1

    return data,fs



def Iqw2Iqtar( FileName, fs, keepIqw = False):
    """Converts an iqw file into iq.tar. Suggested to use after directly reading
    binary data from instrument into file (iqw).
    Note: iqw must be in iqiqiq format
    writtenSamples = WriteIqTar(iqList,fs,"MyFile.iq.tar")"""

    import os
    import tarfile
    import re
    import logging
    
    NumberOfSamples = 0
    
    if os.path.isfile( FileName):
        NumberOfSamples = os.stat( FileName).st_size // 8
    else:
        logging.error("File "+ FileName+" does not exist!")
    
    path,filename = os.path.split(FileName)
    iqtarfile = re.sub( "iqw", "iq.tar", filename, flags=re.IGNORECASE)
    xmlfile = re.sub( "iqw", "xml", filename, flags=re.IGNORECASE)
    binaryfile = re.sub( "iqw", "complex.1ch.float32", filename, flags=re.IGNORECASE)
    os.rename( FileName, os.path.join(path, binaryfile))
    
    __WriteXml( fs, NumberOfSamples, binaryfile, os.path.join(path, xmlfile))
                          
    try:
        tar = tarfile.open( os.path.join(path, iqtarfile), "w")
        tar.add( os.path.join(path, binaryfile), arcname=binaryfile)
        #xslt is optional
        #tar.add( os.path.join(path, xsltfilename), arcname=xsltfilename)
        tar.add( os.path.join(path, xmlfile), arcname=xmlfile)
        tar.close()
        if keepIqw == False:
            os.remove( os.path.join(path, binaryfile))
        else:
            os.rename( os.path.join(path, binaryfile), FileName)
        os.remove( os.path.join(path, xmlfile))
    except:
        logging.error("IqTar (" + FileName +") write error!" )
    
    return
    

    
if __name__ == "__main__":
    # execute only if run as a script
    pass   
