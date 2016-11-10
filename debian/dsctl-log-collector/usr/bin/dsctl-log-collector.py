#!/usr/bin/python
# Encoding: UTF-8

import gettext
import os
import sys
import tempfile
import shutil
import tarfile
import subprocess

def collect():
    logfiles = [ "auth.log", "syslog", "debug" ]
    procfiles = [ "cmdline", "cpuinfo" ]
    cmds = [ "lsmod", "pstree" ]
    td = tempfile.mkdtemp()
    os.makedirs("%s/var/log" % td)
    os.mkdir("%s/proc" % td)
    for lf in logfiles:
        shutil.copy("/var/log/%s" % lf, "%s/var/log/" % td)
    for pf in procfiles:
        shutil.copy("/proc/%s" % pf, "%s/proc/" % td)
    for cmd in cmds:
        f = open('%s/%s' % (td, cmd), 'w')
        subprocess.call([cmd], stdout=f)
        f.close()
    tar = tarfile.open("%s/dsctl-logfiles.tar.bz2" % os.environ['HOME'], 'w:bz2')
    tar.add(td)
    tar.close()
    shutil.rmtree(td)

if __name__ == "__main__":
    collect()
