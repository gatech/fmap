FMAP Tool
====

### Technique Overview
This tool takes the traces from the desktop and mobile versions of a web
application and performs feature matching using the algorithm described in our
ISSTA 2014 paper titled "Cross-platform Feature Matching for Web Applications".

Basically, it first recognizes the actions invoked by each HTTP request and
groups similar actions together using clustering. Then, it looks at the sequence
of actions to identify unique features within the traces on each platform.
Finally, it finds a one-to-one mapping between cross-platform features using the
technique.

Thus, we believe that FMAP helps the developers find missing features across
platforms and to establish correspondence for other applications. This
hypothesis needs to be validated through user studies of cross-platform
developers.

### Tool Description
***fmap.py*** is the main entry point and provides the following command-line
options to run the tool on the subjects applications, which can be seen by
passing the -h (or --help) flag

```
$ ./fmap.py -h
usage: fmap.py [-h] [-b] [-o] [-v] [-V] subject [subject ...]

USAGE

positional arguments:
  subject         ALL or (space separated) names of subjects from [Drupal,
                  Elgg, Gallery, PhpBB, RoundCube, StackOverflow, Twitter,
                  Wikipedia, Wordpress]

optional arguments:
  -h, --help      show this help message and exit
  -b, --baseline  use the URL based baseline technique for clustering
                  [default=False]
  -o, --outdir    Output directory [default=./output]
  -v, --verbose   set verbosity level
  -V, --version   show program's version number and exit
```

The ***feature*** folder contains the code for doing the feature matching.
Subject application drivers are essentially functions located in ```feature/subjects.py```

Passing the `-b` flag to the tool makes it run in _BASELINE_ mode, which
uses a naive URL based action identification. This is the same baseline used to
evaluate our technique in the paper.

The tool can be run on all the subjects using:
```
$./fmap.py ALL
$./fmap.py -b ALL
```

This creates the results for both the FMAP and the BASELINE techniques in the
`./output/` folder. You can see more details on the screen by passing the -v
(or -verbose) flag.

Individual subjects can also be run by passing the subject names to the tool like.
```
$./fmap.py Wordpress Drupal
```

### Tool Output
Currently the tool output as well as intermediate results are stored in the same
report file in the ./output folder. The report name is of the format:
`<SUBJECT NAME>_<TECHNIQUE>_Results_<TIMESTAMP>.txt`.

Example: `Drupal_FMAP_Results_2014-04-10_10-46_PM.txt`

This report file has several sections. Snippets of a report is explained below

```

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
   START RQ1: (Action Recognition through Clustering)  --> These results analyzed manually to compute Action F-score
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
Desktop Clusters
cluster lengths  --> cluster labels and size reported here
Á 	6
Ã 	2
...
cluster details  --> contains info about how each URL got clustered
....

Mobile Clusters
cluster lengths
Ã 	2
Ç 	1
.....
cluster details ......
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
   END RQ1:
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
********************************************************************************
Labelled Desktop Traces  --> This section contains intermediate results.
d.addComment.json
  N []
  /drupal?
  F [u'node', u'destination'....
  POST /drupal/node?destination=node
...
replacing ÆXED in NFCÆXEDÆXED ...
 - merged traces  
...

************************************************************************************************************************************************************************************
MATCHING TABLE --> Intermediate info on how the bipartite edges were assigned weights
************************************************************************************************************************************************************************************
    m.login.json;m.error_login.json 	m.signup.json;m.error_signup.json 	m.add_comment.json 	m.add_page.json 	m.add_story.json 	m.change_password.json 	m.click_moreinfo.json 	m.edit_comment.json 	m.edit_page.json 	m.edit_story.json 	m.logout.json 	m.reply_comment.json 	m.request_password.json
    NF 	NÂÃ 	NFCD 	NFAZÀ 	NFAKL 	NFÊGH 	NFAZË 	NFOPD 	NFOVÅ 	NFOVW 	NFÇ 	NFOCD 	NRS
d.login.json;d.loginError.json 	NF 	0.03 	0.00 	0.02 	0.02 	0.02 	0.02 	0.02 	0.02 	0.02 	0.02 	0.02 	0.02 	0.00
d.addComment.json 	NFCÆXED 	0.01 	0.00 	0.45 	0.01 	0.01 	0.01 	0.01 	0.21 	0.01 	0.01 	0.01 	0.42 	0.00
d.addPage.json 	NFAZÆXÁEÀ 	0.01 	0.00 	0.01 	0.64 	0.19 	0.01 	0.40 	0.01 	0.01 	0.01 	0.01 	0.01 	0.00
d.addStory.json 	NFAKÆXÁEBL 	0.01 	0.00 	0.01 	0.21 	0.74 	0.01 	0.21 	0.01 	0.01 	0.01 	0.01 	0.01 	0.00
d.changePassword.json 	NFÊGÆXMBHÆXMB 	0.01 	0.00 	0.01 	0.01 	0.01 	0.81 	0.01 	0.01 	0.01 	0.01 	0.01 	0.01 	0.00
d.editComment.json 	NFOPÆXED 	0.01 	0.00 	0.19 	0.01 	0.01 	0.01 	0.01 	0.57 	0.15 	0.15 	0.01 	0.32 	0.00
d.editStory.json;d.editHomePage.json 	NFOVÆXÁEW 	0.01 	0.00 	0.01 	0.01 	0.01 	0.01 	0.01 	0.17 	0.41 	0.67 	0.01 	0.16 	0.00
d.logout.json 	NFÇ 	0.01 	0.00 	0.01 	0.01 	0.01 	0.01 	0.01 	0.01 	0.01 	0.01 	0.31 	0.01 	0.00
d.moreInfo.json 	NFAZÆXÁEËÆXY 	0.02 	0.00 	0.02 	0.62 	0.30 	0.02 	1.00 	0.02 	0.02 	0.02 	0.02 	0.02 	0.00
d.replyComment.json 	NFOCÆXED 	0.01 	0.00 	0.45 	0.01 	0.01 	0.01 	0.01 	0.37 	0.17 	0.17 	0.01 	0.57 	0.00
d.requestPassword.json 	NRS 	0.00 	0.00 	0.00 	0.00 	0.00 	0.00 	0.00 	0.00 	0.00 	0.00 	0.00 	0.00 	0.54
d.revertRevisions.json 	NFOÈÆXYIJÆXY 	0.02 	0.00 	0.02 	0.02 	0.02 	0.02 	0.02 	0.24 	0.24 	0.24 	0.02 	0.22 	0.00
d.signup.json;d.signupError.json 	NÂÆXMÃ 	0.00 	0.48 	0.00 	0.00 	0.00 	0.00 	0.00 	0.00 	0.00 	0.00 	0.00 	0.00 	0.00
************************************************************************************************************************************************************************************
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
   START RQ2: (MATCH DETAILS)  --> These were analyzed manually for FMAP & BASELINE to compute results in Table 2.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
[1,2] (d.addComment.json <-> m.add_comment.json) -> 0.445802
[2,3] (d.addPage.json <-> m.add_page.json) -> 0.644628
[3,4] (d.addStory.json <-> m.add_story.json) -> 0.744736
[4,5] (d.changePassword.json <-> m.change_password.json) -> 0.813481
...
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
   END RQ2:
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
########################################################################################################################
  LOAD STATS
########################################################################################################################
Desktop Load Stats::
 - Traces: 16 	Requests: 140
Mobile Load Stats::
 - Traces: 15 	Requests: 62
************************************************************************************************************************
  MAPPING RESULTS
************************************************************************************************************************
Desktop Actions: 32 	Features: 13
Mobile Actions: 23 	Features: 13
Matched Features: 12
************************************************************************************************************************

```
