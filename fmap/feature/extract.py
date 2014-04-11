'''
Created on Apr 28, 2013

@author: shauvik
'''

import glob, os, json, re, urlparse, urllib, os
import numpy, colorsys
from nltk.metrics import jaccard_distance
import utils
from transformer import Transformer

class Extract(object):
    '''
    classdocs
    '''
    ignore = ['', 'php', 'json', 'js'] #load these words from tech terms dictionary
    breakchars = ['']

    def __init__(self, platformName, tracedir, pattern="*.json", appDomains=[]):
        '''
        Constructor
        '''
        self.platformName = platformName
        self.tracedir = tracedir
        self.pattern = pattern
        self.appDomains = appDomains
        self.traces = {}
        self.keywords = {}

        #Clustering Nodes
        self.allReq = [] #flattened trace used by new approach
        self.allItems = [] #flattened trace
        self.allSeq = []
        self.cluster = []
        self.clusterLabels = {}
        self.t = Transformer()

        #Distances
        self.dist = {}
        self.THRESH = utils.getDefaultThresh()

        #Graph fields
        self.nodes = []
        self.edges = []

        # Load Traces and Extract Keywords
        self.loadTraces()
        #self.extractKeywords()
        #self.eliminateRedundantKws()


    def printLoadStats(self):
        print self.platformName, "Load Stats::"
        print " - Traces:", len(self.traces), "\tRequests:", len(self.allReq)
#         reqCnt = 0;
#         for t in self.traces:
#             for r in self.traces[t]:
#                 if 'REQUEST' in r:
#                     reqCnt = reqCnt + 1
#         print " - Requests:", reqCnt, ", average req/trace=", reqCnt/len(self.traces)


    def loadTraces(self):
        #print "Loading Traces in", self.tracedir, "with pattern", self.pattern
        os.chdir(self.tracedir)
        for tracefile in glob.glob(self.pattern):
            #print " - Loading", tracefile
            trace = open(tracefile)
            data = json.load(trace)

            self.traces[tracefile] = data
        cnt = 0
        ignoredDomains = set()
        for k,v in sorted(self.traces.iteritems()):
            for action in v:
                if 'REQUEST' in action and utils.isCodeOrData(action):
                    url = urlparse.urlparse(action['REQUEST'])
                    if url.netloc in self.appDomains:
                        action['ID'] = cnt
                        self.allReq.append(action)
                        cnt = cnt+1
                    else:
                        ignoredDomains.add(url.netloc)
        if len(ignoredDomains) > 0:
            print "Ignored request from domains", ignoredDomains, "for", self.platformName

    #Not used
    def extractKeywords(self, ignoredKeywords=None):
        for k,v in sorted(self.traces.iteritems()):
            #print "-->",k,v
            traceKeywords = []
            for action in v:
                if 'REQUEST' in action and utils.isCodeOrData(action):
                    #print urlparse.urlparse(action['REQUEST'])  ##
                    url = urlparse.urlparse(action['REQUEST'])
                    if url.netloc in self.appDomains:
                        rel_uri = url.path + '?' + url.query
                        action['URI'] = rel_uri

                        id = action['ID']


                        #get only path keywords
#                         kws = re.compile('[\W]').split(url.path)

                        #get only qs keys
#                         kws = [re.compile('[\W]').split(url.path)]
#                         qs_keys = urlparse.parse_qs(url.query).keys()
#                         post_data = urllib.unquote(action['post_data'])
#                         ps_keys = urlparse.parse_qs(post_data).keys()
#                         kws.append[qs_keys, ps_keys]

                        #get all words from keys and values
                        qs = urlparse.parse_qs(url.query)
                        qsw = []
                        for qk in qs.keys():
                            qsw.extend([qk, ",".join(qs[qk])])

                        #Fix, split words with separators like / (TODO: Add more separators)
                        nqsw = []
                        for w in qsw:
                            if '/' in w:
                                nqsw.extend(w.split('/'))
                            else:
                                nqsw.append(w)
                        qsw = nqsw

                        postw = []
                        if 'post_data' in action:
                            post_data = urllib.unquote(action['post_data'])
                            ps = urlparse.parse_qs(post_data)
                            for pk in ps.keys():
                                postw.extend([pk, ",".join(ps[pk])])
                        #print "POST_words::", postw

                        kws = re.compile('[\W]').split(url.path) + qsw + postw

                        #get all words combined
#                         kws = re.compile('[\W]').split(rel_uri)


                        #TODO fix these
                        if ignoredKeywords != None:
                            self.ignore.extend(ignoredKeywords)
                        kws = filter(lambda x : x not in self.ignore, kws)
                        kws = self.t.transform(kws)


                        action['KEYWORDS'] = kws

                        traceKeywords.append((rel_uri, kws, id))
                        self.keywords[k] = traceKeywords

    def eliminateRedundantKws(self):
        redundant = None
        for k,v in self.keywords.iteritems():
            for tup in v:
                if redundant is None:
                    redundant = set(tup[1])
                else:
                    redundant = redundant & set(tup[1])
        keys = self.keywords.keys()
        for i in range(len(self.keywords)):
            k = keys[i]
            v = self.keywords[k]
            for j in range(len(v)):
                v[j] = (v[j][0], [t for t in v[j][1] if t not in redundant], v[j][2])
        for k,v in self.traces.iteritems():
            for a in v:
                if 'KEYWORDS' in a:
                    a['KEYWORDS'] = [t for t in a['KEYWORDS'] if t not in redundant]

    def printKeywords(self):
        #print "Printing URIs"
        for k,v in sorted(self.keywords.iteritems()):
            print k
            for tup in v:
                print "  %d. %s"%(tup[2],tup[1])
                #print "   ", tup[0]

    def recognizeActions(self):
        cluster = self.cluster




    def clusterActions(self, thresh=None):
        print "Matching keywords to generate associations"
        self.computeDistances()
#         for k, v in self.keywords.iteritems():
#             for tup in v:
#                 keywords = tup
#                 idx = getMatchedNode(keywords)
#                 if idx == None:
#                     self.nodes.append((keywords))
        if thresh:
            self.THRESH = thresh

        #agglomerative clustering
        cluster = self.cluster
        n=len(self.dist)
        for i in range(0,n-1):
            for j in range(i+1,n):
                if self.dist[i,j] < self.THRESH:
                    # if a cluster already contains i
                    icl = self.isPresent(cluster, i)
                    if icl != None:
                        icl.add(j)
                        break
                    # if a cluster contains j (rare)
                    jcl = self.isPresent(cluster, j)
                    if jcl is not None:
                        jcl.add(i)
                    else:
                        cluster.append(set([i,j]))
            if not self.isPresent(cluster, i):
                cluster.append(set([i]))
        if not self.isPresent(cluster, n-1):
            cluster.append(set([n-1]))

        print "  => Clusters:", cluster
        #print self.doCount(cluster)
        #self.printClusters(cluster)
        #print self.allSeq

    def printClusters(self):
        for cl in self.cluster:
            print cl
            for c in cl:
                print "\t", self.allItems[c]

    def assignLabelsUsingClustering(self, thresh=None):
        self.clusterActions(thresh)
        cluster = self.cluster
        #print cluster
        cl = self.clusterLabels
        labels = utils.getUUChars()
        for c in cluster:
            l = labels[0]
            cl[l] = c
            labels.remove(l)

    def printClusterLabels(self):
        cl = self.clusterLabels
        for k in cl:
            print k, ':', cl[k]

    def printLabeledTraces(self):
        for k,v in sorted(self.traces.iteritems()):
            print k
            for action in v:
                if 'ID' in action:
                    print " ", self.getLabel(action['ID']), action['KEYWORDS']

                    # Print URL
                    print "\t",
                    if 'post_data' in action: print "POST",
                    print action['URI']

    def getLabel(self, actionNum):
        cl = self.clusterLabels
        for k in cl:
            if actionNum in cl[k]:
                return k
        print "## ERROR: cluster doesn't contain ", actionNum, ", platform:", self.tracedir

    def getLabels(self):
        return self.clusterLabels

    # Assign label based on other platform
    def assignLabels(self, labelMap, platform):
        cluster = self.cluster
        cl = self.clusterLabels
        pLabels = platform.getLabels()

        chars = utils.getUUChars()
        charList = chars[len(pLabels):]

        for c in cluster:
            labels = set([])
            #print c, ":: ",
            for actionNum in c:
                if actionNum in labelMap:
                    labels = labels.union(labelMap[actionNum])
            #print "= Same cluster labels", labels
            label = None
            if len(labels) == 0:
                label = charList[0]
                charList.remove(label)
            else:
                sLabels = list(labels)
                sLabels.sort()
                label = sLabels[0]
                labels.remove(label)
                if len(labels) > 0:
                    print "- merging desktop labels",
                    utils.printSet(sLabels)
                    #merge similar labels from other platform
                    for l in labels:
                        if l in pLabels and label in pLabels:
                            pLabels[label] = pLabels[label].union(pLabels[l])
                            del pLabels[l]
            if label in cl:
                cl[label].update(c)
            else:
                cl[label] = c

    # Old code. Single label assigner
#     def assignLabels(self, labelMap, charList):
#         cluster = self.cluster
#         cl = self.clusterLabels
#         for c in cluster:
#             label = None
#             #print c, ":: ",
#             for actionNum in c:
#                 if actionNum in labelMap:
#                     label = iter(labelMap[actionNum]).next() #get first label
#                     # TODO: check possibility: same cluster in mobile have different corresponding labels
#                     break
#             if label is None:
#                 label = charList[0]
#                 charList.remove(label)
#             cl[label] = c

    def printActionLabel(self, actionNum, labelMap):
        print actionNum,
        for l in labelMap[actionNum]:
            print l,
        print

    def doCount(self, cluster):
        cnt = 0
        for cl in cluster:
            cnt = cnt+len(cl)
        return cnt

    def isPresent(self, cluster, x):
        for cl in cluster:
            for c in cl:
                if c == x:
                    return cl
        return None

    def computeDistances(self):
        for k, v in sorted(self.keywords.iteritems()):
            prev = None
            for tup in v:
                self.allItems.append((tup[0], tup[1], k))
                cnt = len(self.allItems)-1
                if prev != None:
                    self.allSeq.append([prev, cnt, k])
                prev = cnt

        n=len(self.allItems)
        self.dist = numpy.zeros(shape=(n,n))
        for i in range(0,n):
            for j in range(0,n):
                try:
                    self.dist[i,j] = jaccard_distance(set(self.allItems[i][1]), set(self.allItems[j][1]))
                except ZeroDivisionError:
                    self.dist[i,j] = 0 #sys.maxint

#         fileName = os.getcwd().split('/')[-1]+".csv"
#         print self.platformName, "Distances saved to", fileName
#         numpy.savetxt(fileName, self.dist, '%.4e')


    def printGraphViz(self):
        print "*"*80
        print "Graphviz Output::"
        print "*"*80
        print "digraph {"
        num2Node = {}
        # Add Nodes
        cl = self.cluster
        for c in range(0, len(cl)) :
            lbl = set()
            for en in cl[c]:
                lbl.add(self.allItems[en][0])
                num2Node[en] = "A%d"%(c)
            print "  A%d [label=\"%s\"];"%(c, "\\n".join(lbl))

        #Generate colors to be assigned to Edges
        colorMap = {}
        traceFiles = self.keywords.keys()
        N = len(traceFiles)
        HSV_tuples = [(x*1.0/N, 0.5, 0.5) for x in range(N)]
        colors = map(lambda x: colorsys.hsv_to_rgb(*x), HSV_tuples) #RGB colors
        for i in range(0, N):
            colorMap[traceFiles[i]] = colors[i]
        #print colorMap

        # Add Edges
        for edge in self.allSeq:
            c = colorMap[edge[2]]
            color = "#%02x%02x%02x"%(255*c[0], 255*c[1], 255*c[2])
            print "  ", num2Node[edge[0]], "->", num2Node[edge[1]], " [color=\"%s\", label=\"%s\", fontcolor=\"%s\"];"%(color, edge[2], color)


        print "}"

    def normalize(self, label):
        return re.sub("([a-z])([A-Z])","\g<1> \g<2>",label)
