import operator

projects = [{
    "name":  "Apertium",
    "url":  "http://www.ohloh.net/p/apertium.xml",
    "homepage_url":  "http://www.apertium.org/",
    "user_count":  "10",
    "average_rating":  "5.0",
    "rating_count":  "6",
    "review_count":  "0"
},
{
    "name":  "Etherpad Lite",
    "url":  "http://www.ohloh.net/p/etherpad_lite.xml",
    "homepage_url":  "http://etherpad.org",
    "user_count":  "4",
    "average_rating":  "5.0",
    "rating_count":  "1",
    "review_count":  "0"
},
{
    "name":  "Etherpad Lite",
    "url":  "http://www.ohloh.net/p/etherpad_lite.xml",
    "homepage_url":  "http://etherpad.org",
    "user_count":  "4",
    "average_rating":  "5.0",
    "rating_count":  "1",
    "review_count":  "0"
},
{
    "name":  "django-myerscms",
    "url":  "http://www.ohloh.net/p/django-myerscms.xml",
    "homepage_url":  "http://code.google.com/p/django-myerscms",
    "user_count":  "0",
    "average_rating":  "None",
    "rating_count":  "0",
    "review_count":  "0"
},
{
    "name":  "ownCloud",
    "url":  "http://www.ohloh.net/p/ownCloud.xml",
    "homepage_url":  "http://ownCloud.org",
    "user_count":  "28",
    "average_rating":  "5.0",
    "rating_count":  "5",
    "review_count":  "0"
},
{
    "name":  "Globus Toolkit",
    "url":  "http://www.ohloh.net/p/6008.xml",
    "homepage_url":  "http://www.globus.org",
    "user_count":  "2",
    "average_rating":  "3.0",
    "rating_count":  "2",
    "review_count":  "0"
},
{
    "name":  "seafile",
    "url":  "http://www.ohloh.net/p/seafile.xml",
    "homepage_url":  "http://seafile.com",
    "user_count":  "1",
    "average_rating":  "5.0",
    "rating_count":  "1",
    "review_count":  "0"
},
{
    "name":  "FlowPlayer",
    "url":  "http://www.ohloh.net/p/flowplayer.xml",
    "homepage_url":  "http://flowplayer.org",
    "user_count":  "9",
    "average_rating":  "4.25",
    "rating_count":  "4",
    "review_count":  "1"
},
{
    "name":  "OpenNebula",
    "url":  "http://www.ohloh.net/p/opennebula.xml",
    "homepage_url":  "http://opennebula.org",
    "user_count":  "14",
    "average_rating":  "4.28571",
    "rating_count":  "7",
    "review_count":  "0"
},
{
    "name":  "NoseRub",
    "url":  "http://www.ohloh.net/p/NoseRub.xml",
    "homepage_url":  "http://www.noserub.com",
    "user_count":  "7",
    "average_rating":  "4.75",
    "rating_count":  "4",
    "review_count":  "0"
},
{
    "name":  "Gwibber",
    "url":  "http://www.ohloh.net/p/gwibber.xml",
    "homepage_url":  "https://launchpad.net/gwibber",
    "user_count":  "35",
    "average_rating":  "4.11111",
    "rating_count":  "18",
    "review_count":  "0"
},
{
},
{
    "name":  "MediaWiki",
    "url":  "http://www.ohloh.net/p/mediawiki.xml",
    "homepage_url":  "http://www.mediawiki.org/",
    "user_count":  "799",
    "average_rating":  "4.2438",
    "rating_count":  "242",
    "review_count":  "4"
},
{
    "name":  "iFolder",
    "url":  "http://www.ohloh.net/p/8386.xml",
    "homepage_url":  "http://www.ifolder.com",
    "user_count":  "3",
    "average_rating":  "None",
    "rating_count":  "0",
    "review_count":  "0"
},
{
    "name":  "Piwigo",
    "url":  "http://www.ohloh.net/p/piwigo.xml",
    "homepage_url":  "http://piwigo.org",
    "user_count":  "28",
    "average_rating":  "4.9",
    "rating_count":  "20",
    "review_count":  "1"
},
{
    "name":  "AppScale",
    "url":  "http://www.ohloh.net/p/appscale.xml",
    "homepage_url":  "http://appscale.cs.ucsb.edu/",
    "user_count":  "4",
    "average_rating":  "5.0",
    "rating_count":  "1",
    "review_count":  "0"
},
{
},
{
    "name":  "DokuWiki",
    "url":  "http://www.ohloh.net/p/dokuwiki.xml",
    "homepage_url":  "http://www.dokuwiki.org/",
    "user_count":  "205",
    "average_rating":  "4.53488",
    "rating_count":  "86",
    "review_count":  "5"
},
{
    "name":  "ocp-subsystems",
    "url":  "http://www.ohloh.net/p/ocp-subsystems.xml",
    "homepage_url":  "http://code.google.com/p/ocp-subsystems",
    "user_count":  "0",
    "average_rating":  "None",
    "rating_count":  "0",
    "review_count":  "0"
},
{
    "name":  "MiniG",
    "url":  "http://www.ohloh.net/p/12624.xml",
    "homepage_url":  "http://minig.org/",
    "user_count":  "56",
    "average_rating":  "4.71429",
    "rating_count":  "7",
    "review_count":  "0"
},
{
    "name":  "Open Journal Systems",
    "url":  "http://www.ohloh.net/p/ojs2.xml",
    "homepage_url":  "http://pkp.sfu.ca/ojs",
    "user_count":  "6",
    "average_rating":  "5.0",
    "rating_count":  "2",
    "review_count":  "0"
},
{
    "name":  "Friendica",
    "url":  "http://www.ohloh.net/p/friendica.xml",
    "homepage_url":  "http://friendica.com/",
    "user_count":  "9",
    "average_rating":  "5.0",
    "rating_count":  "3",
    "review_count":  "0"
},
{
    "name":  "TubePress",
    "url":  "http://www.ohloh.net/p/tubepress.xml",
    "homepage_url":  "http://tubepress.org",
    "user_count":  "1",
    "average_rating":  "5.0",
    "rating_count":  "1",
    "review_count":  "0"
},
{
    "name":  "Zimbra Collaboration Suite",
    "url":  "http://www.ohloh.net/p/zimbra.xml",
    "homepage_url":  "http://www.zimbra.com/community/downloads.html",
    "user_count":  "56",
    "average_rating":  "3.95",
    "rating_count":  "20",
    "review_count":  "2"
},
{
    "name":  "WordPress",
    "url":  "http://www.ohloh.net/p/wordpress.xml",
    "homepage_url":  "http://wordpress.org/",
    "user_count":  "1528",
    "average_rating":  "4.31718",
    "rating_count":  "454",
    "review_count":  "6"
},
{
    "name":  "bbPress",
    "url":  "http://www.ohloh.net/p/bbpress.xml",
    "homepage_url":  "http://bbpress.org/",
    "user_count":  "27",
    "average_rating":  "4.3",
    "rating_count":  "10",
    "review_count":  "0"
},
{
    "name":  "Gallery 2",
    "url":  "http://www.ohloh.net/p/gallery.xml",
    "homepage_url":  "http://gallery.menalto.com",
    "user_count":  "147",
    "average_rating":  "4.26",
    "rating_count":  "50",
    "review_count":  "4",
},
{
    "name":  "Elgg",
    "url":  "http://www.ohloh.net/p/elgg.xml",
    "homepage_url":  "http://elgg.org/",
    "user_count":  "37",
    "average_rating":  "4.0",
    "rating_count":  "11",
    "review_count":  "2"
},
{
    "name":  "Piwik",
    "url":  "http://www.ohloh.net/p/piwik.xml",
    "homepage_url":  "http://piwik.org",
    "user_count":  "40",
    "average_rating":  "4.58824",
    "rating_count":  "17",
    "review_count":  "0"
},
{
    "name":  "Funambol Client for Mozilla Thunderbird",
    "url":  "http://www.ohloh.net/p/funbird.xml",
    "homepage_url":  "https://mozilla-plugin.forge.funambol.org/",
    "user_count":  "926",
    "average_rating":  "4.66667",
    "rating_count":  "9",
    "review_count":  "0"
},
{
    "name":  "Funambol Client for Mozilla Thunderbird",
    "url":  "http://www.ohloh.net/p/funbird.xml",
    "homepage_url":  "https://mozilla-plugin.forge.funambol.org/",
    "user_count":  "926",
    "average_rating":  "4.66667",
    "rating_count":  "9",
    "review_count":  "0"
},
{
    "name":  "Adium",
    "url":  "http://www.ohloh.net/p/adium.xml",
    "homepage_url":  "http://www.adium.im/",
    "user_count":  "446",
    "average_rating":  "4.45517",
    "rating_count":  "145",
    "review_count":  "2"
},
{
    "name":  "Phorum",
    "url":  "http://www.ohloh.net/p/phorum.xml",
    "homepage_url":  "http://www.phorum.org",
    "user_count":  "8",
    "average_rating":  "4.85714",
    "rating_count":  "7",
    "review_count":  "0"
},
{
    "name":  "phpBB",
    "url":  "http://www.ohloh.net/p/phpbb.xml",
    "homepage_url":  "http://www.phpbb.com/",
    "user_count":  "879",
    "average_rating":  "4.1694",
    "rating_count":  "182",
    "review_count":  "4"
},
{
    "name":  "Mailman",
    "url":  "http://www.ohloh.net/p/mailman.xml",
    "homepage_url":  "http://www.list.org",
    "user_count":  "205",
    "average_rating":  "3.625",
    "rating_count":  "48",
    "review_count":  "0"
},
{
    "name":  "Eucalyptus",
    "url":  "http://www.ohloh.net/p/eucalyptus.xml",
    "homepage_url":  "http://www.eucalyptus.com",
    "user_count":  "18",
    "average_rating":  "4.33333",
    "rating_count":  "9",
    "review_count":  "0"
},
{
    "name":  "Vanilla Forums",
    "url":  "http://www.ohloh.net/p/vanillaforums.xml",
    "homepage_url":  "http://vanillaforums.org/",
    "user_count":  "21",
    "average_rating":  "3.92857",
    "rating_count":  "14",
    "review_count":  "2"
},
{
    "name":  "FluxBB",
    "url":  "http://www.ohloh.net/p/FluxBB.xml",
    "homepage_url":  "http://fluxbb.org",
    "user_count":  "16",
    "average_rating":  "4.71429",
    "rating_count":  "14",
    "review_count":  "0"
},
{
    "name":  "StatusNet",
    "url":  "http://www.ohloh.net/p/statusnet.xml",
    "homepage_url":  "http://status.net",
    "user_count":  "36",
    "average_rating":  "4.63636",
    "rating_count":  "22",
    "review_count":  "0"
},
{
    "name":  "Roundcube Webmail",
    "url":  "http://www.ohloh.net/p/roundcube.xml",
    "homepage_url":  "http://www.roundcube.net",
    "user_count":  "214",
    "average_rating":  "4.32353",
    "rating_count":  "68",
    "review_count":  "4"
},
{
},
{
    "name":  "Plumi",
    "url":  "http://www.ohloh.net/p/plumi.xml",
    "homepage_url":  "http://www.plumi.org",
    "user_count":  "5",
    "average_rating":  "4.6",
    "rating_count":  "5",
    "review_count":  "0"
},
{
    "name":  "Twitter/identi.ca micro-blogging bot",
    "url":  "http://www.ohloh.net/p/mb-chatbot.xml",
    "homepage_url":  "http://sourceforge.net/projects/mb-chatbot/",
    "user_count":  "0",
    "average_rating":  "None",
    "rating_count":  "0",
    "review_count":  "0"
},
{
    "name":  "libre.fm",
    "url":  "http://www.ohloh.net/p/librefm.xml",
    "homepage_url":  "http://libre.fm",
    "user_count":  "15",
    "average_rating":  "4.0",
    "rating_count":  "8",
    "review_count":  "0"
},
{
    "name":  "OpenLayers",
    "url":  "http://www.ohloh.net/p/openlayers.xml",
    "homepage_url":  "http://openlayers.org/",
    "user_count":  "147",
    "average_rating":  "4.7",
    "rating_count":  "50",
    "review_count":  "2"
},
{
    "name":  "phpGroupWare",
    "url":  "http://www.ohloh.net/p/phpgroupware.xml",
    "homepage_url":  "http://phpgroupware.org",
    "user_count":  "5",
    "average_rating":  "2.0",
    "rating_count":  "4",
    "review_count":  "0"
},
{
    "name":  "Feng Office",
    "url":  "http://www.ohloh.net/p/fengoffice.xml",
    "homepage_url":  "http://www.opengoo.org/",
    "user_count":  "16",
    "average_rating":  "4.08333",
    "rating_count":  "12",
    "review_count":  "1"
},
{
    "name":  "SquirrelMail",
    "url":  "http://www.ohloh.net/p/squirrelmail.xml",
    "homepage_url":  "http://squirrelmail.org",
    "user_count":  "134",
    "average_rating":  "3.72727",
    "rating_count":  "33",
    "review_count":  "3"
},
{
},
{
},
{
    "name":  "LimeSurvey",
    "url":  "http://www.ohloh.net/p/limesurvey.xml",
    "homepage_url":  "http://www.limesurvey.org",
    "user_count":  "36",
    "average_rating":  "4.0",
    "rating_count":  "16",
    "review_count":  "0"
},
{
    "name":  "Cheetah News",
    "url":  "http://www.ohloh.net/p/cheetah-news.xml",
    "homepage_url":  "http://www.cheetah-news.com/",
    "user_count":  "2",
    "average_rating":  "None",
    "rating_count":  "0",
    "review_count":  "0"
},
{
    "name":  "surforce-meneame",
    "url":  "http://www.ohloh.net/p/surforce-meneame.xml",
    "homepage_url":  "http://code.google.com/p/surforce-meneame",
    "user_count":  "0",
    "average_rating":  "None",
    "rating_count":  "0",
    "review_count":  "0"
},
{
    "name":  "Vote Up/Down",
    "url":  "http://www.ohloh.net/p/vote_up_down.xml",
    "homepage_url":  "http://drupal.org/project/vote_up_down",
    "user_count":  "5",
    "average_rating":  "3.0",
    "rating_count":  "1",
    "review_count":  "0"
},
{
},
{
    "name":  "Diaspora",
    "url":  "http://www.ohloh.net/p/diaspora.xml",
    "homepage_url":  "http://joindiaspora.com/",
    "user_count":  "25",
    "average_rating":  "4.25",
    "rating_count":  "8",
    "review_count":  "0"
},
{
    "name":  "SemanticScuttle",
    "url":  "http://www.ohloh.net/p/semanticscuttle.xml",
    "homepage_url":  "http://semanticscuttle.sourceforge.net/",
    "user_count":  "4",
    "average_rating":  "5.0",
    "rating_count":  "1",
    "review_count":  "0"
},
{
    "name":  "Rubric",
    "url":  "http://www.ohloh.net/p/8244.xml",
    "homepage_url":  "http://search.cpan.org/dist/Rubric/",
    "user_count":  "2",
    "average_rating":  "4.0",
    "rating_count":  "1",
    "review_count":  "0"
},
{
    "name":  "Connotea",
    "url":  "http://www.ohloh.net/p/5107.xml",
    "homepage_url":  "http://www.connotea.org/",
    "user_count":  "1",
    "average_rating":  "3.0",
    "rating_count":  "1",
    "review_count":  "0"
},
{
    "name":  "ShiftSpace",
    "url":  "http://www.ohloh.net/p/shiftspace.xml",
    "homepage_url":  "http://www.ShiftSpace.org",
    "user_count":  "4",
    "average_rating":  "5.0",
    "rating_count":  "2",
    "review_count":  "0"
},
{
},
{
    "name":  "Drupal (contributions)",
    "url":  "http://www.ohloh.net/p/drupal-contributions.xml",
    "homepage_url":  "http://drupal.org/",
    "user_count":  "314",
    "average_rating":  "4.31313",
    "rating_count":  "99",
    "review_count":  "4"
},
{
    "name":  "twitterizer",
    "url":  "http://www.ohloh.net/p/twitterizer.xml",
    "homepage_url":  "http://www.twitterizer.net/",
    "user_count":  "79",
    "average_rating":  "4.7",
    "rating_count":  "10",
    "review_count":  "1"
},
{
    "name":  "Tiki Wiki CMS Groupware",
    "url":  "http://www.ohloh.net/p/tikiwiki.xml",
    "homepage_url":  "http://tiki.org",
    "user_count":  "140",
    "average_rating":  "4.36364",
    "rating_count":  "66",
    "review_count":  "11"
},
{
},
{
    "name":  "eyeOS",
    "url":  "http://www.ohloh.net/p/eyeos.xml",
    "homepage_url":  "http://www.eyeos.org",
    "user_count":  "24",
    "average_rating":  "4.71429",
    "rating_count":  "14",
    "review_count":  "1"
},
{
    "name":  "croqodile",
    "url":  "http://www.ohloh.net/p/croqodile.xml",
    "homepage_url":  "http://code.google.com/p/croqodile",
    "user_count":  "0",
    "average_rating":  "None",
    "rating_count":  "0",
    "review_count":  "0"
},
{
    "name":  "OpenSimulator",
    "url":  "http://www.ohloh.net/p/opensimulator.xml",
    "homepage_url":  "http://www.opensimulator.org/",
    "user_count":  "55",
    "average_rating":  "4.71429",
    "rating_count":  "21",
    "review_count":  "0"
}]

print "Projects:", len(projects)
prMap = {}
for p in projects:
    if 'name' in p:
        prMap[p['name']] = int(p['user_count'])
        
sortedPrj = sorted(prMap.iteritems(), key=operator.itemgetter(1))
sortedPrj.reverse()
cnt=1
for p in sortedPrj:
    print cnt, p
    cnt+=1