import matcher

BASE_PATH = "/Volumes/Secondary/Dropbox/Research/D2M/SubjectTraces/"

def Wikipedia(URL_CLUSTER=False):
    global TRACE_DIR, TRACE_DIR_MOBILE
    TRACE_DIR = BASE_PATH+"wikipedia"
#     TRACE_DIR = "/Volumes/Secondary/Dropbox/Research/D2M/test/wikipedia"
    TRACE_DIR_MOBILE = "%s%s"%(TRACE_DIR, "_mobile")

    appDomains = ['www.wikipedia.org', 'en.wikipedia.org', 'en.m.wikipedia.org', 'commons.m.wikimedia.org', 'commons.wikimedia.org', 'de.wikipedia.org', 'hi.wikipedia.org', 'meta.wikimedia.org', 'upload.wikimedia.org', '']

    print "#"*80, '\n\tWIKIPEDIA TRACES\n', "#"*80

    matcher.MatchAll(TRACE_DIR, TRACE_DIR_MOBILE, appDomains, None, URL_CLUSTER)


def Wordpress(URL_CLUSTER=False):
    global TRACE_DIR, TRACE_DIR_MOBILE
    TRACE_DIR = BASE_PATH+"wordpress"
    TRACE_DIR_MOBILE = "%s%s"%(TRACE_DIR, "_mobile")

    appDomains = ['localhost:8080', '']
    prefixPath = ['/wordpress']
    print "#"*80, '\n\tWORDPRESS TRACES\n', "#"*80

    matcher.MatchAll(TRACE_DIR, TRACE_DIR_MOBILE, appDomains, prefixPath, URL_CLUSTER)

def Drupal(URL_CLUSTER=False):
    global TRACE_DIR, TRACE_DIR_MOBILE
    TRACE_DIR = BASE_PATH+"drupal"
    TRACE_DIR_MOBILE = "%s%s"%(TRACE_DIR, "_mobile")

    appDomains = ['bear.cc.gt.atl.ga.us:8080', '']
    prefixPath = ['/drupal', '/drupal_mobile']

    print "#"*80, '\n\tDRUPAL TRACES\n', "#"*80

    matcher.MatchAll(TRACE_DIR, TRACE_DIR_MOBILE, appDomains, prefixPath, URL_CLUSTER)


def PhpBB(URL_CLUSTER=False):
    global TRACE_DIR, TRACE_DIR_MOBILE
    TRACE_DIR = BASE_PATH+"phpbb"
    TRACE_DIR_MOBILE = "%s%s"%(TRACE_DIR, "_mobile")

    appDomains = ['bear.cc.gt.atl.ga.us:8080', '']
    prefixPath = ['/phpbb', '/phpbb_mobile']

    print "#"*80, '\n\tPHPBB TRACES\n', "#"*80

    matcher.MatchAll(TRACE_DIR, TRACE_DIR_MOBILE, appDomains, prefixPath, URL_CLUSTER)

def RoundCube(URL_CLUSTER=False):
    global TRACE_DIR, TRACE_DIR_MOBILE
    TRACE_DIR = BASE_PATH+"roundcube"
    TRACE_DIR_MOBILE = "%s%s"%(TRACE_DIR, "_mobile")

    appDomains = ['bear.cc.gt.atl.ga.us:8888', '']
    prefixPath = ['/roundcube']

    print "#"*80, '\n\tROUNDCUBE TRACES\n', "#"*80

    matcher.MatchAll(TRACE_DIR, TRACE_DIR_MOBILE, appDomains, prefixPath, URL_CLUSTER)

def Elgg(URL_CLUSTER=False):
    global TRACE_DIR, TRACE_DIR_MOBILE
    TRACE_DIR = BASE_PATH+"elgg"
    TRACE_DIR_MOBILE = "%s%s"%(TRACE_DIR, "_mobile")

    appDomains = ['bear.cc.gt.atl.ga.us:8080', '']
    prefixPath = ['/elgg']

    print "#"*80, '\n\tELGG TRACES\n', "#"*80

    matcher.MatchAll(TRACE_DIR, TRACE_DIR_MOBILE, appDomains, prefixPath, URL_CLUSTER)

def Gallery(URL_CLUSTER=False):
    global TRACE_DIR, TRACE_DIR_MOBILE
    TRACE_DIR = BASE_PATH+"gallery"
    TRACE_DIR_MOBILE = "%s%s"%(TRACE_DIR, "_mobile")

    appDomains = ['bear.cc.gt.atl.ga.us:8080', '']
    prefixPath = ['/gallery3']

    print "#"*80, '\n\tGALLERY TRACES\n', "#"*80

    matcher.MatchAll(TRACE_DIR, TRACE_DIR_MOBILE, appDomains, prefixPath, URL_CLUSTER)

def Twitter(URL_CLUSTER=False):
    global TRACE_DIR, TRACE_DIR_MOBILE
    TRACE_DIR = BASE_PATH+"twitter"
    TRACE_DIR_MOBILE = "%s%s"%(TRACE_DIR, "_mobile")

    appDomains = ['mobile.twitter.com', 'twitter.com', 'platform.twitter.com', 'upload.twitter.com', '']

    print "#"*80, '\n\tTWITTER TRACES\n', "#"*80

    matcher.MatchAll(TRACE_DIR, TRACE_DIR_MOBILE, appDomains, None, URL_CLUSTER)

def StackOverflow(URL_CLUSTER=False):
    global TRACE_DIR, TRACE_DIR_MOBILE
    TRACE_DIR = BASE_PATH+"stackoverflow"
    TRACE_DIR_MOBILE = "%s%s"%(TRACE_DIR, "_mobile")

    # Domains used for the web app features accessed
    appDomains = ['stackoverflow.com', 'www.stackoverflow.com', 'openid.stackexchange.com',
                  'chat.stackoverflow.com', 'clients1.google.com', 'stackauth.com', '']

    print "#"*80, '\n\tSTACKOVERLOW TRACES\n', "#"*80

    matcher.MatchAll(TRACE_DIR, TRACE_DIR_MOBILE, appDomains, None, URL_CLUSTER)
