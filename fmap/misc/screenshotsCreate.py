import os, glob, shutil
from selenium import webdriver

SCREENDIR = "/Volumes/Secondary/Dropbox/Research/D2M/SubjectTraces/screens"
# PHANTOMJS = "/Volumes/Secondary/Tools/web/phantomjs-1.9.1-macosx/bin/phantomjs"
SCRIPTDIR = os.getcwd()
chromedriver = "/Volumes/Secondary/Tools/web/chromedriver"
os.environ["webdriver.chrome.driver"] = chromedriver


def mhtml2png():
    png = glob.glob("*.png")
    for mht in glob.glob("*.mhtml"):
        print "Converting", mht
        scFile = mht[:-5] + 'png'
        if scFile in png:
            print "Skipping", scFile
        else:
            saveScreenshot('file://' + SCREENDIR + '/' + mht, SCREENDIR + '/' + scFile)

def main():
    os.chdir(SCREENDIR)
    copyDat2Mhtml()
    mhtml2png()
#         cmd = " ".join([PHANTOMJS, SCRIPTDIR+"/screenshot.js", SCREENDIR, mht, mht[:-5]+'png'])
#         exit()

def saveScreenshot(htmlPath, screenshotFile):
    print "Capturing", htmlPath, "to", screenshotFile
    driver = webdriver.Chrome(chromedriver)
    driver.get(htmlPath)
    driver.get_screenshot_as_file(screenshotFile)
    driver.quit()

def copyDat2Mhtml():
    mhtml = glob.glob("*.mhtml")
    print mhtml
    for datfile in glob.glob("*.dat"):
        mhtFile = "%s.mhtml"%(datfile[:-4]) 
        if mhtFile in mhtml:
            print "Skipping", mhtFile
        else:
            print "Copying", datfile, "to", mhtFile
            shutil.copyfile(datfile, mhtFile)       

if __name__ == "__main__":
    main()