from gridfs import GridFS

from db import *


# open/close


def fs_open():
    log("fs_open()")
    if not hasattr(g, "fs"):
        db = db_open()
        g.fs = GridFS(db)
        db_close(db)
    return g.fs


def fs_close(fs):
    log("fs_close()")
    fs.close()


# read/write


def fs_write(fs, file):
    log("fs_write(fs=%s, file=%s)" % (fs, file))
    return fs.put(file)


def fs_read(fs, id):
    log("fs_read(fs=%s, id=%s)" % (fs, id))
    return fs.get(id)
