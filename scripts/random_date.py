import random
import time
from datetime import datetime

def strTimeProp(start, end, format, prop):
    """Get a time at a proportion of a range of two formatted times.

    start and end should be strings specifying times formated in the
    given format (strftime-style), giving an interval [start, end].
    prop specifies how a proportion of the interval to be taken after
    start.  The returned time will be in the specified format.
    """

    stime = time.mktime(time.strptime(start, format))
    etime = time.mktime(time.strptime(end, format))

    ptime = stime + prop * (etime - stime)

    return time.strftime(format, time.localtime(ptime)), datetime.fromtimestamp(ptime)


def randomDate(start, end, prop, format=None):
    return strTimeProp(start, end, '%m/%d/%Y %I:%M %p' if not format else format, prop)[1]

print randomDate("1/1/2008", "1/1/2012", random.random(), format='%d/%m/%Y')