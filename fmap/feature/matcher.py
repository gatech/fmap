from __future__ import division
import numpy, sys, os
import bipartitematching, utils
from nltk.metrics import distance

from extract import Extract
from clustering import ActionRecognizer

URL_THRESH = 0.8


def getIdenticalRows(mcs, numRows):
    iRows = []
    for i in range(numRows - 1):
        for j in range(i + 1, numRows):
            r1, r2 = mcs[i], mcs[j]
            r1Str = reduce(lambda x, y:x + y, r1)
            if r1Str != '' and set(r1) == set(r2): # BUG in numpy--> numpy.array_equal(r1, r2):
                utils.addMappingToList(iRows, i, j)

    return iRows


def getRowsToDel(features, iRows):
    rowsToDel = []
    for i in iRows:
        rowList = sorted(list(i))
        newRow = rowList.pop(0)
        for mergeRow in rowList:
            features[newRow].update(features[mergeRow])
            rowsToDel.append(mergeRow)
    rowsToDel.sort()
    return rowsToDel


def deleteRows(data, mcs, features, rowsToDel):
    delCnt = 0
    for r in rowsToDel:
        rowIdx = r - delCnt
        mcs = numpy.delete(mcs, rowIdx, 0)
        data = numpy.delete(data, rowIdx, 0)
        features.pop(rowIdx)
        delCnt += 1
    return data, mcs




def MatchURLTraces(d, m):
    dtraces = sorted(d.traces.iteritems())
    mtraces = sorted(m.traces.iteritems())

    dTrStr = utils.getURLFeatures(dtraces, d)
    mTrStr = utils.getURLFeatures(mtraces, m)

    print "*"*100
    print "Desktop features:", len(dTrStr)
    for tr in dTrStr:
        print '\t',tr[0]
    print "Mobile features:", len(mTrStr)
    for tr in mTrStr:
        print '\t',tr[0]
    print "*"*100

    x,y = len(dTrStr), len(mTrStr)
    data = numpy.zeros(shape=(x,y))

    for i in range(x):
        for j in range(y):
            df, dStr = dTrStr[i]
            mf, mStr = mTrStr[j]
            dist = distance.edit_distance(dStr,mStr)
            data[i,j] = dist

            ## try
            t = max(len(dStr), len(mStr))
            if dist < URL_THRESH * t:
                print "++",
                data[i,j] = dist
            else:
                print "--",
                data[i,j] = 100000000
            print dist, t, dStr, mStr, df, mf
#             if dist < 1:
#                 print '\t- perfect match', df, dStr, mf, mStr

#     exit()

    print data

    N = max(x,y)
    print "Resizing", x, y, " to ", N
    #data.resize((N,N))

    matrix = numpy.ones(shape=(N,N)) * 100000000
    matrix[:x,:y] = data

    #matrix = numpy.copy(data)

    mwbgm = bipartitematching.Munkres()
    indexes = mwbgm.compute(matrix)
    bipartitematching.print_matrix(matrix, msg='Lowest cost through this matrix:')
    total = 0
    for row, column in indexes:
        if row < x and column < y:
            value = data[row][column]
            if value > 10000000:
                continue
            total += value
            print '(%d, %d) -> %d ' % (row, column, value),
            print '==> %s = %s' %(dTrStr[row][0], mTrStr[column][0])
    print 'total cost: %d' % total

    print "*"*100


def MatchTraces(d, m):
    # Compute global action frequency
    dFreqMap = utils.computeActionFreq(d)
    mFreqMap = utils.computeActionFreq(m)

    dFeatures = utils.getFeatures(d, dFreqMap)
    mFeatures = utils.getFeatures(m, mFreqMap)

    x,y = len(dFeatures), len(mFeatures)
    data = numpy.zeros(shape=(x,y))
    mcs = numpy.chararray(shape=(x,y), unicode=True, itemsize=50)
    mcs[:] = ''
    avgTraceLen = numpy.zeros(shape=(x,y))
    tsm = utils.getTraceStringMap(d, m)
    #print tsm

    i=0
    for df in dFeatures:
        j=0
        dFile = sorted(list(df))[0]
        tr1 = d.traces[dFile]
        for mf in mFeatures:
            mFile = sorted(list(mf))[0]
            tr2 = m.traces[mFile]
            mcs[i,j], data[i,j] = utils.getWeightedMCSLength(tr1, tr2, d, m, dFreqMap, mFreqMap)
            avgTraceLen[i,j] = (float(len(tr1)+len(tr2))/2)
            j=j+1
        i = i+1

    if utils.verbose:
        print "MCS", mcs

    # Merge match-equivalent traces
    rLen = len(data)
    cLen = len(data[0])

    iRows = getIdenticalRows(mcs, rLen)
    if utils.verbose:
        print "Merging Match-Equivalent Trace Rows:", iRows
    rowsToDel = getRowsToDel(dFeatures, iRows)
    data, mcs = deleteRows(data, mcs, dFeatures, rowsToDel)

    iCols = getIdenticalRows(mcs.T, cLen)
    if utils.verbose:
        print "Merging Match-Equivalent Trace Cols:", iCols
    colsToDel = getRowsToDel(mFeatures, iCols)
    data, mcs = deleteRows(data.T, mcs.T, mFeatures, colsToDel)

    data = data.T
    mcs = mcs.T

    if utils.verbose:
        print data

    # Normalize the data (Scale within [0,1])
    maxim = 0.0
    for r in range(len(data)):
        for c in range(len(data[r])):
            data[r][c] = (data[r][c] / avgTraceLen[r][c])
            if(data[r][c]>maxim): maxim = data[r][c]
    for r in range(len(data)):
        for c in range(len(data[r])):
            if maxim > 0:
                data[r][c] = (data[r][c] / maxim)

#     if DEBUG:
    utils.printCSV(data, tsm, dFeatures, mFeatures)

    # Maximum Weight Bipartite Matching
    mwbgm = bipartitematching.Munkres()
    cost_matrix = bipartitematching.make_cost_matrix(data, lambda x : 100000000 - (x*10000))
    indexes = mwbgm.compute(cost_matrix)

    mapping = {}

    print "*"*120, "\n  MATCH DETAILS\n", "*"*120

    for row, column in indexes:
        value = data[row][column]
        if value > 0.1: #Be conservative with matching
            #print '(%d, %d) -> %f' % (row, column, value)
            df = ",".join(dFeatures[row])
            mf = ",".join(mFeatures[column])
            print '[%d,%d] (%s <-> %s) -> %f' % (row, column, df, mf, value)
            mapping[row] = column

    print "#"*120, "\n  LOAD STATS\n", "#"*120
    d.printLoadStats()
    m.printLoadStats()

    utils.printMatchStats(d, m, dFeatures, mFeatures, mapping)

    return mapping


def MatchAll(dDir, mDir, appDomains, pathPrefix=None, URL_CLUSTER=False):
    d = Extract("Desktop", dDir, "*.json", appDomains)
    m = Extract("Mobile", mDir, "*.json", appDomains)

    config = {"domains": appDomains, "prefix":pathPrefix, "URL_CLUSTER":URL_CLUSTER}
    ActionRecognizer(d, m).setConfig(config).run()

    if utils.verbose:
        print "*"*80
        print "Labelled Desktop Traces"
        d.printLabeledTraces()
        print "*"*80
        print "Labelled Mobile Traces"
        m.printLabeledTraces()

    if URL_CLUSTER:
        mapping = MatchURLTraces(d,m)
    else:
        mapping = MatchTraces(d, m)
