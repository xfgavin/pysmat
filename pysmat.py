#!/usr/bin/env python
######################################################
#Python engine for csv & mat conversion
#Created by: Feng Xue 09/20/2018 @UCSD
######################################################
import sys
import os
import csv
import time

#################################################################################################
#For matlab 7.3 format support, we should use hdf5storage.savemat and hdf5storage.loadmat instead
#################################################################################################

if len(sys.argv)!=5:
    print "Usage: "+ os.path.basename(sys.argv[0])+' mode file_in file_out variable'
    print "       mode 1: csv2mat"
    print "       mode 2: mat2csv"
    os._exit(0)
mode=int(sys.argv[1])
file_in=sys.argv[2]
file_out=sys.argv[3]
var=sys.argv[4]
if not os.path.isfile(file_in):
    print "Error: input file " + file_in + " doesn't exist"
    os._exit(-1)

t = time.time()
if mode==1:
    ################
    #csv to mat
    ################
    from numpy.core.records import fromarrays
    from scipy.io import savemat
    f = open(file_in, 'rb')
    reader = csv.reader(f)
    headers = reader.next()
    column = {}
    for colidx in range(len(headers)):
        column[colidx] = []
    for row in reader:
        for h, v in zip(headers, row):
            colidx=headers.index(h)
            try:
                column[colidx].append(int(v))
            except:
                try:
                    column[colidx].append(float(v))
                except:
                    column[colidx].append(v)
    f.close()
    data=[]
    for idx in range(len(headers)):
        data.append(column[idx])
    abcd_info = fromarrays(data, names=headers)
    savemat(file_out, {var: abcd_info}, oned_as='column')
elif mode==2:
    ################
    #mat to csv
    ################
    import scipy.io
    import numpy as np
    from itertools import chain

    data = scipy.io.loadmat(file_in)
    abcd_info = data[var]
    abcd_info_new = []
    for idx in range(len(abcd_info)):
        tmp = list(chain.from_iterable(abcd_info[idx]))
        for subidx in range(len(tmp)):
            if isinstance(tmp[subidx],np.ndarray):
                if len(tmp[subidx])==1:
                    tmp[subidx] = tmp[subidx][0]
                    if isinstance(tmp[subidx],np.ndarray):
                        if len(tmp[subidx])==1:
                            tmp[subidx] = tmp[subidx].flatten().tolist()[0]
                        elif len(tmp[subidx])==0:
                            tmp[subidx] = None
                        else:
                            print "Length is bigger than 1"
                            print tmp[subidx]
                        
                    elif isinstance(tmp[subidx],np.unicode):
                        tmp[subidx] = tmp[subidx].astype(str)
                    else:
                        print "unknow type:"
                        type(tmp[subidx])
                elif len(tmp[subidx])==0:
                    tmp[subidx] = None
                else:
                    print "Length is bigger than 1"
                    print tmp[subidx]
            else:
                print "type exception:"
                type(tmp[subidx])
                print tmp[subidx]
    
            if not isinstance(tmp[subidx],int) and not isinstance(tmp[subidx],float):
                try:
                    tmp[subidx] = int(tmp[subidx])
                except:
                    try:
                        tmp[subidx] = float(tmp[subidx])
                    except:
                        pass
        abcd_info_new.append(tmp)


    with open(file_out, 'wb') as fp:
        writer = csv.writer(fp, quoting=csv.QUOTE_NONNUMERIC)
        writer.writerow(abcd_info.dtype.names)
        writer.writerows(abcd_info_new)
    fp.close()

else:
    print "Error: Mode should be 1 or 2"
    os._exit(-1)
elapsed = time.time() - t
print ('Elapsed: '+ str(elapsed))
