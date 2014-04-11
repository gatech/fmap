import logging, utils, urlparse, urllib, re, numpy
from transformer import Transformer

# THRESHOLDS
T1 = 0.3 #SMALL
T2 = 0.8 #LARGE

class ActionRecognizer():
    def __init__(self, d, m):
        self.platform1 = d
        self.platform2 = m
        self.t = Transformer()

    def setConfig(self, conf):
        self.config = conf
        return self

    def run(self):
        self.clusterRequests()

        self.assignSymbols(self.platform1)
        self.mergeAndAssign(self.platform1, self.platform2)

    def clusterRequests(self):
        for p in [self.platform1, self.platform2]:
            logging.info("clustering platform "+ p.platformName)
            # extract words
            for k,v in sorted(p.traces.iteritems()):
                traceInfo = []
                for action in v:
                    if 'ID' in action:
                        url = urlparse.urlparse(action['REQUEST'])
                        urlPath = self.doIgnore(url.path)
                        kws = self.getKeywords(url.query, action)
                        allKeywords = self.getJointKws((urlPath, kws))

                        rel_uri = url.path + '?' + url.query
                        action['URI'] = rel_uri
                        action['URL_PATH'] = urlPath + '?' + url.query
                        action['INFO'] = traceInfo
                        action['KEYWORDS'] = allKeywords

#                         traceInfo.append([urlPath, kws, action['ID'], allKeywords])
                        traceInfo.append([urlPath + '?' + url.query, kws, action['ID'], allKeywords])

                p.keywords[k] = traceInfo
                #print traceInfo

#             ### SIMPLE URL BASED CLUSTERING
#             if(self.config["URL_CLUSTER"]):
#                 print "Simple URL based clustering for evaluation"
#
#                 mapCl= {}
#                 for k,v in sorted(p.keywords.iteritems()):
#                     for ti in v:
#                         url = ti[0] #ti[4]
#                         if url in mapCl:
#                             mapCl[url].append(ti)
#                         else:
#                             mapCl[url] = [ti]
#                 urlcluster = []
#                 for actions in mapCl.values():
#                     urlcluster.append(set([a[2] for a in actions]))
#
#                 p.cluster = urlcluster
#                 continue


            # level 1 clustering - combine with same url path
            mapCl= {}
            for k,v in sorted(p.keywords.iteritems()):
                for ti in v:
                    urlPath = ti[0]
                    if urlPath in mapCl:
                        mapCl[urlPath].append(ti)
                    else:
                        mapCl[urlPath] = [ti]

            #print len(mapCl)
            #print mapCl.keys()
            l1clusters = []
            for actions in mapCl.values():
                l1clusters.append(set([a[2] for a in actions]))
            #print "L1 CLUSTERS::", len(l1clusters), ">>", l1clusters


            ### SIMPLE URL BASED CLUSTERING
            if(self.config["URL_CLUSTER"]):
                print "Simple URL based clustering for evaluation"
                p.cluster = l1clusters
                continue



            # level 2 clustering
            # - agglomerate (combine small clusters with similar url path)
            # - divisive (split large clusters)
            smallClusters, largeClusters = [],[]
            for k,v in mapCl.iteritems():
                if len(v) == 1:
                    smallClusters.append((k,v))
                if len(v) > 1:
                    largeClusters.append((k,v))

            sClusters = []
            sLen = len(smallClusters)
            #print "Small Clusters", smallClusters

            if sLen > 1:
                for i in range(sLen-1):
                    for j in range(i+1, sLen):
                        #print i,j,smallClusters[i][1], smallClusters[j][1]
                        cluster1 = smallClusters[i][1][0] #get the first and only element
                        cluster2 = smallClusters[j][1][0]
                        a = cluster1[3]
                        b = cluster2[3]
                        if self.isSimilar(a, b):
                            #print "add mapping", (cluster1, cluster2)
                            utils.addMappingToList(sClusters, cluster1[2], cluster2[2])

            for sc in smallClusters:
                elem = sc[1][0][2]
                if not self.isPresent(sClusters, elem):
                    sClusters.append(set([elem]))

            #print len(sClusters), sClusters

            lClusters = []
            #print "Large Clusters::", len(largeClusters), ">>", largeClusters
            for lc in largeClusters:
                dist = self.getClusterDistance(lc[1])
                newCluster = self.doAgglomerativeClustering(lc[1], dist)
                lClusters.extend(newCluster)
            #print "new clusters::", len(lClusters), ">>", lClusters

            p.cluster = lClusters + sClusters
#             p.cluster = l1clusters


    def doAgglomerativeClustering(self, cl, dist):
        cluster = []
        n=len(dist)
        for i in range(0,n-1):
            for j in range(i+1,n):
                a = cl[i][2]
                b = cl[j][2]
                if dist[i,j] < T2:
                    # if a cluster already contains a
                    icl = self.isPresent(cluster, a)
                    if icl != None:
                        icl.add(b)
                        break
                    # if a cluster contains b (rare)
                    jcl = self.isPresent(cluster, b)
                    if jcl is not None:
                        jcl.add(b)
                    else:
                        cluster.append(set([a,b]))
            if not self.isPresent(cluster, a):
                cluster.append(set([a]))
        if not self.isPresent(cluster, cl[n-1][2]): #Edge case - last element
            cluster.append(set([cl[n-1][2]]))

        #print "  => Clusters:", cluster
        return cluster


    def isPresent(self, cluster, x):
        for cl in cluster:
            for c in cl:
                if c == x:
                    return cl
        return None

    def getClusterDistance(self, cl):
        n=len(cl)
        dist = numpy.zeros(shape=(n,n))
        for i in range(0,n):
            for j in range(0,n):
                dist[i,j] = utils.getJaccardDistance(cl[i][1], cl[j][1])
        return dist

    '''
    (url, kws) => [urlkws + kws]
    '''
    def getJointKws(self, tup):
        return self.getUrlPathKeywords(tup[0]) + tup[1]


    def isSimilar(self, a, b):
        if utils.getJaccardDistance(a, b) < T1: #THRESH
            return True
        return False

    def assignSymbols(self, p):
        logging.info("assign symbols to platform "+ p.platformName)
        cl = p.clusterLabels
        labels = utils.getUUChars()
        for c in p.cluster:
            l = labels[0]
            cl[l] = c
            labels.remove(l)
        #self.printClusterLabels(p)



    def printClusterLabels(self, p):
        cl = p.clusterLabels
        print "cluster lengths"
        for k in cl:
            print k,'\t',len(cl[k])
        print "cluster details"
        for k in cl:
            print k, ': (',len(cl[k]),') ', cl[k]
            for t in cl[k]:
                req = p.allReq[t]
                print "\t", req['REQUEST'], req['KEYWORDS'],
                if 'post_data' in req:
                    print "POST:", req['post_data']
                else: print

    def mergeAndAssign(self, d, m):
        logging.info("merge "+ d.platformName+ " clusters while assign corresponding symbols to "+ m.platformName)

        mLabels = {}

        for file1, tr1 in sorted(d.traces.iteritems()):
            for file2, tr2 in sorted(m.traces.iteritems()):
                if(self.config["URL_CLUSTER"]):
                    # Do simplistic URL based matching
                    mc = utils.getURLMatchSeqCount(tr1, tr2, d, m, mLabels)
                else:
                    mc = utils.getMatchSeqCount(tr1, tr2, d, m, mLabels, T1)

        cluster = m.cluster
        cl = m.clusterLabels
        dLabels = d.getLabels()

        chars = utils.getUUChars()
        charList = chars[len(dLabels):]

        for c in cluster:
            labels = set([])
            #print c, ":: ",
            for actionNum in c:
                if actionNum in mLabels:
                    labels = labels.union(mLabels[actionNum])
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
                        if l in dLabels and label in dLabels:
                            dLabels[label] = dLabels[label].union(dLabels[l])
                            del dLabels[l]
            if label in cl:
                cl[label].update(c)
            else:
                cl[label] = c


        # EVALUATION (RQ - step 1 effectiveness)
        print "%"*120, "\n\t START RQ1: (Action Recognition through Clustering) \n", "%"*120
#         print "Desktop URLs"
#         self.printOrderedReq(d.allReq)
#         print "-"*80
        print "Desktop Clusters"
        self.printClusterLabels(d)

#         print "Mobile URLs"
#         self.printOrderedReq(m.allReq)
#         print "-"*80
        print "Mobile Clusters"
        self.printClusterLabels(m)

        print "%"*120, "\n\t END RQ1: \n", "%"*120



    def printOrderedReq(self, req):
        requests = []
        for r in req:
            request = r['REQUEST']
            if 'post_data' in r:
                request = request + " POST:" + r['post_data']
            requests.append(request)
        requests = sorted(requests)
        for url in requests:
            print "\t-",url
    '''
    Utility functions for HTTP Request
    '''
    def getKeywords(self, query, action):
        qs = urlparse.parse_qs(query)
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
        # transform by applying map and filter
        return self.t.transform(qsw + postw)

    def getUrlPathKeywords(self, path):
        kws = re.compile('[\W]').split(path)
        return self.t.transform(kws)

    def doIgnore(self, path):
        prefixList = self.config["prefix"]
        if prefixList != None:
            prefixList.sort(key=len, reverse=True)
            if prefixList != None:
                for pf in prefixList:
                    path = re.sub(pf, '', path)
        path = path.rstrip('/')
        return path

    '''
    Utility functions for clustering
    '''
