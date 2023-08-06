# BOTLIB - the bot library !
#
#

import os, sys, traceback

def __dir__():
    return ("get_exception",)

def get_exception(txt="", sep=" "):
    exctype, excvalue, tb = sys.exc_info()
    trace = traceback.extract_tb(tb)
    result = []
    for elem in trace:
        fname = elem[0]
        linenr = elem[1]
        func = elem[2]
        if fname.endswith(".py"):
            plugfile = fname[:-3].split(os.sep)
        else:
            plugfile = fname.split(os.sep)
        mod = []
        for element in plugfile[::-1]:
            mod.append(element)
            if "bot" in element:
                break
        ownname = ".".join(mod[::-1])
        if "bot" not in ownname:
            continue
        result.append("%s:%s" % (ownname, linenr))
    res = "%s %s: %s %s" % (sep.join(result), exctype, excvalue, str(txt))
    del trace
    return res
