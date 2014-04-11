#!/usr/bin/python
"""
This script queries Ohloh for project names and gets 
basic project details such as project location, 
user count and ratings

It is based on the Ohloh API Sample from Python.
Modified by: Shauvik Roy Choudhary (shauvik@gatech.edu)
"""

import urllib, elementtree.ElementTree as ET

# Connect to the Ohloh website and retrieve the account data.
params = urllib.urlencode({'api_key': 'VzWWP8TCGDkdxd9evaDszg', 'v': 1})

def printUserCount(prj):
    url = "http://www.ohloh.net/projects.xml?query=%s&%s" % (prj, params)
    print url
    f = urllib.urlopen(url)
    
    # Parse the response into a structured XML object
    tree = ET.parse(f)
    
    # Did Ohloh return an error?
    elem = tree.getroot()
    error = elem.find("error")
    if error != None:
        print 'Ohloh returned:', ET.tostring(error),
        sys.exit()
    
    # Output all the immediate child properties of the first project
    firstPrj = elem.find("result/project")
    print '{'
    if firstPrj != None:
        for node in firstPrj:
            if node.tag in ['name', 'url', 'homepage_url', 'user_count', 'average_rating', 'rating_count', 'review_count']:
                print "\t%s:\t%s," % (node.tag, node.text)
    print '},'
    
if __name__ == '__main__':
    # Project list from Wikipedia
    # http://en.wikipedia.org/wiki/List_of_free_software_web_applications
    projects = ["Apertium", "Etherpad", "Etherpad", "CiteSeerX", "ownCloud", "Globus Toolkit", "Seafile", "Flowplayer", 
                "OpenNebula", "Noserub", "Jaiku", "Xuheki", "Mediawiki", "iFolder", "Piwigo", "AppScale", "Tahoe Least-Authority Filesystem", 
                "DokuWiki", "OpenConf", "IMP", "Open Journal Systems", "Friendica", "TubePress", "Zimbra", "WordPress", "BuddyPress", "Gallery 2", 
                "Elgg", "Piwik", "Funambol", "Funambol", "LiveJournal", "Phorum", "phpBB", "Mailman", "Eucalyptus (computing)", "Vanilla", "FluxBB", 
                "StatusNet", "Roundcube", "AbiCollab", "Plumi", "Identi.ca", "Libre.fm", "OpenStreetMap", "PHPGroupware", "Feng Office", 
                "Squirrelmail", "JSN PowerAdmin", "EasyChair", "LimeSurvey", "Cheetah News", "Meneame", "Reddit", "Mixx", "Diaspora", "Scuttle", 
                "Rubric", "Connotea", "ShiftSpace", "Ma.gnolia 2", "OpenID", "OAuth", "Shibboleth", "CAcert.org", "EyeOS", "OpenCroquet", "OpenSimulator"]
    
    for p in projects:
        printUserCount(p)