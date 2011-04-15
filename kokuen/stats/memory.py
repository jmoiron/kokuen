#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Memory stats gathering."""

import re
from subprocess import Popen, PIPE
from kokuen.utils import to_bytes

class MemoryStatus(object):
    """Fetch the memory usage for a given PID.  Note that this is designed
    mostly to read the current processes memory size;  it won't work well on
    non-linux machines when trying to find the mem usage of a process not owned
    by the current user.  Reading from proc is almost 600x faster than using
    the ps fallback."""
    matcher = re.compile('VmSize:\s*(\d+\s*\w+)')
    ps_fallback = False

    def __init__(self, pid):
        self.pid = int(pid)
        self.procpath = '/proc/%s/status' % pid
        if not os.path.exists(self.procpath):
            self.ps_fallback = True

    def usage(self):
        if self.ps_fallback:
            return self.ps_fallback_usage()
        return self.proc_usage()

    def proc_usage(self):
        """Memory usage for given PID."""
        try:
            with open(self.procpath) as f:
                content = f.read()
            size = self.matcher.search(content).groups()[0]
            return to_bytes(size)
        except:
            return self.ps_fallback_usage()

    def ps_fallback_usage(self):
        """Memory usage for the given PID using ps instead of proc."""
        p = Popen(['ps', 'u', '-p', str(self.pid)], stdout=PIPE)
        output = p.stdout.read().split('\n')
        output = filter(None, output)
        process_line = output[-1].split()
        vsize_in_kb = process_line[5] + ' kB'
        return to_bytes(vsize_in_kb)

