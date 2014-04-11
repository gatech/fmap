#!/usr/bin/python
# encoding: utf-8
'''
Fmap (Feature Matcher Across Platforms) is a tool to match features across different client versions of a web application.

@author:     Shauvik Roy Choudhary

@copyright:  2014 Georgia Tech. All rights reserved.

@license:    MIT License

@contact:    shauvik@gatech.edu
'''

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import os, inspect, traceback, errno
from time import localtime, strftime

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter

from feature.extract import Extract
from feature import subjects
from feature import utils



__all__ = []
__version__ = 0.1
__date__ = '2014-04-11'
__updated__ = '2014-04-11'

DEBUG = 0
TESTRUN = 0
PROFILE = 0

class CLIError(Exception):
    '''Generic exception to raise and log different fatal errors.'''
    def __init__(self, msg):
        super(CLIError).__init__(type(self))
        self.msg = "E: %s" % msg
    def __str__(self):
        return self.msg
    def __unicode__(self):
        return self.msg

def main(argv=None): # IGNORE:C0111
    '''Command line options.'''

    global verbose

    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)

    program_name = os.path.basename(sys.argv[0])
    program_version = "v%s" % __version__
    program_build_date = str(__updated__)
    program_version_message = '%%(prog)s %s (%s)' % (program_version, program_build_date)
    program_shortdesc = __import__('__main__').__doc__.split("\n\n")[0]
    program_license = '''%s

  Created by Shauvik Roy Choudhary on %s.
  Copyright 2014 Georgia Tech. All rights reserved.

  Licensed under the MIT License
  http://opensource.org/licenses/MIT

  Distributed on an "AS IS" basis without warranties
  or conditions of any kind, either express or implied.

USAGE
''' % (program_shortdesc, str(__date__))

    try:
        all_subj = inspect.getmembers(subjects, inspect.isfunction)
        subj_names = ""
        for subj in all_subj:
          subj_names += subj[0] + ", "

        # Setup argument parser
        parser = ArgumentParser(description=program_license, formatter_class=RawDescriptionHelpFormatter)
        parser.add_argument(dest="subjects", help="ALL or (space separated) names of subjects from [%s]"%(subj_names[:-2]), metavar="subject", nargs="+")
        parser.add_argument("-b", "--baseline", dest="baseline", help="use the URL based baseline technique for clustering [default=%(default)s]", action="count", default=False)
        parser.add_argument("-p", "--print-cluster", dest="print_cluster", help="print intermediate clustering details [default=%(default)s]", action="count", default=False)
        parser.add_argument("-o", "--outdir", dest="outdir", help="Output directory [default=%(default)s]", action="count", default='./output')

        parser.add_argument("-v", "--verbose", dest="verbose", action="count", help="set verbosity level")
        parser.add_argument('-V', '--version', action='version', version=program_version_message)

        # Process arguments
        args = parser.parse_args()

        verbose = args.verbose
        utils.verbose = verbose

        log("Verbose mode on")

        result_type = '_FMAP'
        if args.baseline:
          result_type = '_BASELINE'

        mkdir_p(args.outdir)

        # Select subjects to process
        if(len(args.subjects) > 0):
          if (args.subjects[0].lower() == 'all'):
            selected_subjects = [t[1] for t in all_subj]
          else:
            try:
              selected_subjects = [getattr(subjects,t) for t in args.subjects]
            except AttributeError as ae:
              print "Subjects not found. Please use the right casing"
              print ae
              return 0

        orig_stdout = sys.stdout
        outDir = os.path.abspath(args.outdir)

        for subj in selected_subjects:
          subject = subj.func_name
          log("Processing "+ subject)

          outfile = strftime(outDir+"/"+subject+result_type+"_Results_%Y-%m-%d_%I-%M_%p.txt", localtime())
          log("Sending output to " + outfile)
          sys.stdout = open(outfile, 'w')

          if args.baseline:
            subj(URL_CLUSTER=True)
          else:
            subj()
          sys.stdout = orig_stdout

        return 0
    except KeyboardInterrupt:
        ### handle keyboard interrupt ###
        return 0
    except Exception, e:
        if DEBUG or TESTRUN:
            print traceback.format_exc()
            # raise(e)
        indent = len(program_name) * " "
        sys.stderr.write(program_name + ": " + repr(e) + "\n")
        sys.stderr.write(indent + "  for help use --help\n")
        return 2

def log(str):
  if verbose > 0:
    print str

def mkdir_p(path):
  try:
    os.makedirs(path)
  except OSError as exc: # Python >2.5
    if exc.errno == errno.EEXIST and os.path.isdir(path):
      pass
    else: raise

if __name__ == "__main__":
    if DEBUG:
        sys.argv.append("-v")
    if TESTRUN:
        import doctest
        doctest.testmod()
    if PROFILE:
        import cProfile
        import pstats
        profile_filename = 'Fmap_profile.txt'
        cProfile.run('main()', profile_filename)
        statsfile = open("profile_stats.txt", "wb")
        p = pstats.Stats(profile_filename, stream=statsfile)
        stats = p.strip_dirs().sort_stats('cumulative')
        stats.print_stats()
        statsfile.close()
        sys.exit(0)
    sys.exit(main())
