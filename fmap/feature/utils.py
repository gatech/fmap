import unicodedata as ud
from nltk.metrics import jaccard_distance
import numpy, re
from bisect import bisect_left

class MetaData():
    def __init__(self, rows, cols, traceStringMap):
        self.rows = rows
        self.cols = cols
        self.traceStringMap = traceStringMap


def getUUChars():
    '''
    get Unicode Uppercase Chars
    '''
    all_unicode = [unichr(i) for i in xrange(65536)]
    return [c for c in all_unicode if ud.category(c) == 'Lu']

# def getMatchCount(a, b):
#     matches = 0
#     tab = numpy.zeros(shape=(len(a), len(b)))
#     i=0
#     for x in a:
#         j=0
#         for y in b:
#             if 'ID' in x and 'ID' in y:
#                 try:
#                     jd = jaccard_distance(set(x['KEYWORDS']), set(y['KEYWORDS']))
#                 except ZeroDivisionError:
#                     jd = 0
#                 tab[i,j] = jd
#                 #print "\t", x['ID'], y['ID'], jd,
#                 #print x['KEYWORDS'], y['KEYWORDS']
#                 if jd < thresh:
#                     matches = matches + 1
#             j = j+1
#         i = i+1
#     return tab

def getJaccardDistance(a, b):
    try:
        jd = jaccard_distance(set(a), set(b))
    except ZeroDivisionError:
        jd = 0
    return jd

'''
Args: trace1, trace2
'''
def getMatches(a, b, thresh):
    matchList = []
    tab = numpy.zeros(shape=(len(a), len(b)))
    for x in a:
        for y in b:
            if 'ID' in x and 'ID' in y:
                if getJaccardDistance(x['KEYWORDS'], y['KEYWORDS']) < thresh:
                    matchList.append((x['ID'], y['ID']))
    return matchList

'''
Args: trace1, trace2, (Extract) desktop, (Extract) mobile, labels
'''
def getMatchSeqCount(a, b, d, m, mLabels, t):
    matches = getMatches(a, b, t)
    for k, v in matches:
        # print k, v, d.getLabel(k)
        if v in mLabels:
            mLabels[v].add(d.getLabel(k))
        else:
            mLabels[v] = set([d.getLabel(k)])
    return len(matches)

'''
Simplistic URL based matching
Args: trace1, trace2
'''
def getURLMatches(a, b):
    matchList = []
    tab = numpy.zeros(shape=(len(a), len(b)))
    for x in a:
        for y in b:
            if 'ID' in x and 'ID' in y:
                if x['URL_PATH'] == y['URL_PATH']:
                    matchList.append((x['ID'], y['ID']))
    return matchList

'''
Do simplistic URL based matching for evaluation
Args: trace1, trace2, (Extract) desktop, (Extract) mobile, labels
'''
def getURLMatchSeqCount(a, b, d, m, mLabels):
    matches = getURLMatches(a, b)
    for k, v in matches:
        # print k, v, d.getLabel(k)
        if v in mLabels:
            mLabels[v].add(d.getLabel(k))
        else:
            mLabels[v] = set([d.getLabel(k)])
    return len(matches)

'''
Maximum Weighted Longest Common Subsequence
Args: String1, String2, FreqMap1, FreqMap2
Based on http://rosettacode.org/wiki/Longest_common_subsequence
Note: Lower the freq, rarer it is, more is (1-w)
'''
def mcs(a, b, f1, f2):
    lengths = [[0 for j in range(len(b) + 1)] for i in range(len(a) + 1)]
    # row 0 and column 0 are initialized to 0 already
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            if x == y:
                lengths[i + 1][j + 1] = lengths[i][j] + (1 - f1[x] / f1['TOTAL']) * (1 - f2[y] / f2['TOTAL']) # OR 1- f1[x] / f1['TOTAL'] *  f2[y] / f2['TOTAL']
            else:
                lengths[i + 1][j + 1] = max(lengths[i + 1][j], lengths[i][j + 1])
    # read the substring out from the matrix
    result = ""
    x, y = len(a), len(b)
    while x != 0 and y != 0:
        if lengths[x][y] == lengths[x - 1][y]:
            x -= 1
        elif lengths[x][y] == lengths[x][y - 1]:
            y -= 1
        else:
            assert a[x - 1] == b[y - 1]
            result = a[x - 1] + result
            x -= 1
            y -= 1
    return result


'''
Longest Common Subsequence
Args: String1, String2
http://rosettacode.org/wiki/Longest_common_subsequence
'''
def lcs(a, b):
    lengths = [[0 for j in range(len(b) + 1)] for i in range(len(a) + 1)]
    # row 0 and column 0 are initialized to 0 already
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            if x == y:
                lengths[i + 1][j + 1] = lengths[i][j] + 1
            else:
                lengths[i + 1][j + 1] = max(lengths[i + 1][j], lengths[i][j + 1])
    # read the substring out from the matrix
    result = ""
    x, y = len(a), len(b)
    while x != 0 and y != 0:
        if lengths[x][y] == lengths[x - 1][y]:
            x -= 1
        elif lengths[x][y] == lengths[x][y - 1]:
            y -= 1
        else:
            assert a[x - 1] == b[y - 1]
            result = a[x - 1] + result
            x -= 1
            y -= 1
    return result

# From http://stackoverflow.com/questions/9079797/detect-repetitions-in-string
def repetitions(s):
   r = re.compile(r"(.+?)\1+")
   for match in r.finditer(s):
       yield (match.group(1), len(match.group(0))/len(match.group(1)))

def replaceRepeated(str):
    toBeRep = list(repetitions(str))
    rep=set([])
    for r in toBeRep:
        rep.add(r[0])
    rep = list(rep)
    rep.sort(key = len, reverse=True)
#     print toBeRep, rep
    nstr = str
    for r in rep:
        nstr = re.sub('('+r+')+', r, nstr)
        print "replacing", r, "in", str, '->', nstr
    return nstr

def getLabelString(trace, extract, REPEAT_REPLACE=True):
    str = ''
    try:
        for action in trace:
            if 'ID' in action:
                str = str + extract.getLabel(action['ID'])
    except:
        print "ERROR", action

    if REPEAT_REPLACE:
        str = replaceRepeated(str)

    return str

def getLCSLength(t1, t2, d, m):
    a = getLabelString(t1, d)
    b = getLabelString(t2, m)
    lcsStr = lcs(a, b)
    # print a, " -- ", b, " >> ", lcsStr
    return len(lcsStr)

def getWeightedMCSLength(t1, t2, d, m, dFreq, mFreq):
    a = getLabelString(t1, d)
    b = getLabelString(t2, m)
    mcsStr = mcs(a, b, dFreq, mFreq)
    wl = 0
    for char in mcsStr:
        wl = wl + (1 - (float(dFreq[char]) / dFreq['TOTAL'])) * (1 - (float(mFreq[char]) / mFreq['TOTAL']))
    return mcsStr, wl

def getWeightedLCSLength(t1, t2, d, m, dFreq, mFreq):
    a = getLabelString(t1, d)
    b = getLabelString(t2, m)
    lcsStr = lcs(a, b)
    wl = 0

    for char in lcsStr:
#         wl = wl + (1.0/freqMap[char])
#         (actionCnt, totalActions) = getActionFreq(char, t1, t2, d, m)
#         wl = wl + (1 - (float(freqMap[char])/freqMap['TOTAL']) + (float(actionCnt)/totalActions ))
        wl = wl + (1 - (float(dFreq[char]) / dFreq['TOTAL'])) * (1 - (float(mFreq[char]) / mFreq['TOTAL']))
    return wl


def getActionFreq(char, t1, t2, d, m):
    ac = 0; ta = 0
    for a in t1:
        if 'ID' in a:
            ta = ta + 1
            if char == d.getLabel(a['ID']):
                ac = ac + 1
    for b in t2:
        if 'ID' in b:
            ta = ta + 1
            if char == m.getLabel(b['ID']):
                ac = ac + 1
    # print char, "ActionFreq=", ac, "TotAct=", ta
    return (ac, ta)

def printSet(s):
    for i in s:
        print i,
    print

def incrementSetFreq(mySet, item):
    if item in mySet:
        mySet[item] = mySet[item] + 1
    else:
        mySet[item] = 1

def computeActionFreq(platform):
    freqMap = {}
    cnt = 0
    for t in platform.traces:
        cnt = cnt + 1
        traceLabels = set([])  # unique set of action labels
        for action in platform.traces[t]:
            if 'ID' in action:
                traceLabels.add(platform.getLabel(action['ID']))
        for label in traceLabels:
            incrementSetFreq(freqMap, label)
    freqMap['TOTAL'] = cnt
    return freqMap

def matches(s1, s2, freqMap):
    if s1 == s2:
        return True
    #TODO: Weighted match
    return False

def getURLFeatures(traces, p):
    traceStr = []
    revTraceMap = {}
    for i in range(len(traces)):
        file, tr = traces[i]
        label = getLabelString(tr, p, REPEAT_REPLACE=False)
        if label in revTraceMap.keys():
            revTraceMap[label] = revTraceMap[label]+','+file
        else:
            revTraceMap[label] = file
    traceMap={}
    for label, file in revTraceMap.iteritems():
        traceMap[file] = label

    for file in sorted(traceMap.keys()):
        traceStr.append((file, traceMap[file]))

    return traceStr

def getFeatures(platform, freqMap):
    features = [] # list of sets
    traces = sorted(platform.traces.iteritems())
    for i in range(len(traces)):
        for j in range(i+1, len(traces)):
            #print "Checking\n -", traces[i], "\n -", traces[j]
            file1, tr1 = traces[i]
            file2, tr2 = traces[j]

            s1 = getLabelString(tr1, platform)
            s2 = getLabelString(tr2, platform)
            if matches(s1, s2, freqMap):
                print " - merged traces ", file1, file2, "into same feature; labelstrings=", s1, s2
                addMappingToList(features, file1, file2)

    # add unique traces as features
    for file, tr in traces:
        found = False
        for f in features:
            if file in f:
                found = True
                break
        if not found:
            features.append(set((file,)))

    print platform.platformName, features
    return features

def addMappingToList(lst, a, b):
    added = False
    for item in lst:
        if a in item or b in item:
            item.update((a, b))
            added = True
    if not added:
        item = set((a,b))
        lst.append(item)

def printMatchStats(d, m, df, mf, mapping):
    print "*"*120, "\n  MAPPING RESULTS\n", "*"*120
    print "Desktop Actions:", len(d.clusterLabels), "\tFeatures:", len(df)
    print "Mobile Actions:", len(m.clusterLabels), "\tFeatures:", len(mf)

    print "Matched Features:",len(mapping)
    print "*"*120

def getSortedValueIndexList(data):
    val = []
    idx = []
    for i in range(len(data)):
        for j in range(len(data[0])):
            index = bisect_left(val, data[i,j])
            val.insert(index, data[i,j])
            idx.insert(index, (i,j))
    return val, idx

def getDefaultThresh():
    return 0.5

def getTraceStringMap(d, m):
    # Populate labeled strings
    tsm = {}
    for fil, tr in sorted(d.traces.iteritems()):
        tsm[fil] = getLabelString(tr, d)

    for fil, tr in sorted(m.traces.iteritems()):
        tsm[fil] = getLabelString(tr, m)

    return tsm

def printCSV(data, tsm, df, mf):
    rows, cols = [], []
    for f in df:
        rows.append(f)

    for f in mf:
        cols.append(f)

    delim = '\t'
#     delim = ','
    print "*" * 180
    print "MATCHING TABLE"
    print "*" * 180
    print delim + delim,
    for c in cols:
        print ";".join(c), delim,

    print "\n", delim, delim,
    for c in cols:
        fil = sorted(list(c))[0]
        print tsm[fil], delim,
    print
    i = 0
    for row in data:
        fil = sorted(rows[i])[0]
        print ";".join(rows[i]), delim, tsm[fil], delim,
        for col in row:
            print "%0.2f" % (col), delim,
        print
        i = i + 1

    print "*" * 180

def pretty(d, indent=0):
    for key, value in d.iteritems():
        print '\t' * indent + str(key)
        if isinstance(value, dict):
            pretty(value, indent+1)
        else:
            print '\t' * (indent+1) + str(value)

def isCodeOrData(action):
    if 'RESPONSE' in action:
        mime = action['RESPONSE'].split(', ')[1]
        if mime in ['text/html','text/javascript', 'text/xml', 'application/javascript', 'application/json', 'application/xml', 'application/x-javascript']:
            return True
    return False

if __name__ == "__main__":
#     print lcs('helo', 'heol')
#     w = {'h':0.2, 'e':0.2, 'l': 0.2, 'o':0.1}
#     print mcs("helo", "heol", w, w)
#     a = [u'_default_addressbook', u'_section', u'addressbook', u'surname', u'_token', u'_action', u'save-prefs', u'_framed', u'_task', u'setting']
#     b = [u'_section', u'general', u'_timezone', u'Pacific/Midway', u'_token', u'_action', u'save-prefs', u'_framed', u'_time_format', u'H:i', u'_date_format', u'Y-m-d', u'_pretty_date', u'_skin', u'larry', u'_language', u'en_US', u'_task', u'setting', u'_refresh_interval']
    a = [u'_task', u'setting', u'_action', u'edit-prefs', u'_section', u'general', u'_framed']
    b = [u'_task', u'setting', u'_action', u'edit-prefs', u'_section', u'addressbook', u'_framed']
    print getJaccardDistance(a, b)
