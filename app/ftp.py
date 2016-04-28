import os
import socket
import ftplib
from ftplib import FTP
from log import *

from app.settings import (
    FTP_HOST,
    FTP_PORT,
    HTTP_PORT,
    FTP_USER,
    FTP_PASS
)

FTP_URL_PREFIX = "http://" + FTP_HOST + ":" + str(HTTP_PORT) + "/"


def ftp_open():
    log("ftp_open()")
    try:
        ftp = FTP()
        ftp.connect(FTP_HOST, FTP_PORT)
        ftp.login(FTP_USER, FTP_PASS)
        return ftp
    except ftplib.error_perm:
        log("ftp_error: failed to connect to ftp server")
        pass
    except socket.error:
        log("ftp_error: connection refused")
        pass
    return None


def ftp_close(ftp):
    log("ftp_close(ftp=%s)" % ftp)
    if not ftp:
        return
    ftp.quit()


def ftp_upload(ftp, path):
    log("ftp_upload(ftp=%s, path=%s)" % (ftp, path))
    if not ftp:
        return
    with open(path) as file:
        ftp.storbinary("STOR " + path, file)
    return FTP_URL_PREFIX + path


def ftp_mkdirs(ftp, path):
    log("ftp_mkdirs(ftp=%s, path=%s)" % (ftp, path))
    if not ftp:
        return
    (head, tail) = os.path.split(path)
    if not head:
        return
    ftp_mkdirs(ftp, head)
    try:
        ftp.mkd(head)
    except ftplib.error_perm:
        pass
