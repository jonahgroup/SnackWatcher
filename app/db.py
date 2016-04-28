from pymongo import errors
from datetime import datetime

import pymongo

from bson.objectid import ObjectId

from log import *
from app.settings import (
    DB_CONNECT_STRING,
    DB
)

DB_IMAGES = "images"
DB_BACKGROUNDS = "backgrounds"


# helpers


def db_verify(obj, type):
    if not isinstance(obj, type):
        raise Exception("[{0}] is not of type [{1}]".format(obj, type))
    return obj


def to_list(cursor, inner_elem=None):
    if not cursor:
        return []
    elems = []
    for elem in cursor:
        elems.append(elem[inner_elem]) if inner_elem else elems.append(elem)
    return elems


# open/close


def db_open():
    log("db_open()")
    try:
        if DB_CONNECT_STRING != "":
            mongo = pymongo.MongoClient(DB_CONNECT_STRING)
        else:
            mongo = pymongo.MongoClient()
        db = mongo[DB]
        return db
    except errors.ConnectionFailure, e:
        log("db_error: %s" % e)
        raise


def db_close(db):
    log("db_close(db=%s)" % db)
    db.client.close()


# images


def db_image(title, date_created, date_modified, img_path, img_url, img_url_ext="", db_transforms=[], db_blobs=[]):
    return {
        "title": db_verify(title, str),
        "date_created": db_verify(date_created, datetime),
        "date_modified": db_verify(date_modified, datetime),
        "img_path": db_verify(img_path, str),
        "img_url": db_verify(img_url, str),
        "img_url_ext": db_verify(img_url_ext, str),
        "transforms": db_transforms,
        "blobs": db_blobs
    }


def db_images_write(db, db_image):
    log("db_images_write(db=%s, db_image=%s)" % (db, db_image))
    db[DB_IMAGES].create_index([("date_created", pymongo.DESCENDING)])
    return db[DB_IMAGES].insert_one(db_image).inserted_id


def db_images_read_latest(db):
    log("db_images_read_latest(db=%s)" % db)
    db_images = db_images_read_latest_n(db, 1)
    return None if len(db_images) == 0 else db_images[0]


def db_images_read_latest_n(db, n=None):
    log("db_images_read_latest_n(db=%s, n=%s)" % (db, n))
    db_images = to_list(db[DB_IMAGES].find(limit=n, sort=[("date_created", pymongo.DESCENDING)]))
    return db_images


def db_images_read_all(db):
    log("db_images_read_all(db=%s)" % db)
    return db_images_read_latest_n(db)


def db_images_read_by_id(db, id):
    log("db_images_read_by_id(db=%s, id=%s)" % (db, id))
    db_images = to_list(db[DB_IMAGES].find({'_id': ObjectId(id)}))
    return None if len(db_images) == 0 else db_images[0]


# transforms


def db_transform(uid, title, type, description, img_path, img_url, img_url_ext=""):
    return {
        "uid": db_verify(uid, ObjectId),
        "title": db_verify(title, str),
        "type": db_verify(type, str),
        "description": db_verify(description, str),
        "img_path": db_verify(img_path, str),
        "img_url": db_verify(img_url, str),
        "img_url_ext": db_verify(img_url_ext, str)
    }


def db_transforms_read_by_id_type(db, image_id, type):
    log("db_transforms_read_by_id_type(db=%s, image_id=%s, type=%s)" % (db, image_id, type))
    db_images = to_list(db[DB_IMAGES].find(limit=1, filter={"_id": ObjectId(image_id), "transforms.type": type},
                                           projection={"transforms.$": 1}))
    db_transforms = [] if len(db_images) == 0 else db_images[0]["transforms"]
    return None if len(db_transforms) == 0 else db_transforms[0]


# blobs


BLOB_STATE_NEW = "new"
BLOB_STATE_DUPLICATE = "duplicate"
BLOB_STATE_REMOVED = "removed"


def db_blob(uid, title, bounds, img_path, img_url, img_url_ext="", c1ass="unknown", c1ass_state="auto",
            state=BLOB_STATE_NEW):
    return {
        "uid": db_verify(uid, ObjectId),
        "title": db_verify(title, str),
        "bounds": {
            "x": db_verify(bounds["x"], int),
            "y": db_verify(bounds["y"], int),
            "w": db_verify(bounds["w"], int),
            "h": db_verify(bounds["h"], int)
        },
        "img_path": db_verify(img_path, str),
        "img_url": db_verify(img_url, str),
        "img_url_ext": db_verify(img_url_ext, str),
        "c1ass": db_verify(c1ass, str),
        "c1ass_state": db_verify(c1ass_state, str),
        "state": db_verify(state, str)
    }


def db_blobs_read_by_c1ass_state(db, c1ass_state, n=None):
    log("db_blobs_read_by_c1ass_state(db=%s, c1ass_state=%s, n=%s)" % (db, c1ass_state, n))
    db_blobs = to_list(db[DB_IMAGES].aggregate([
        {"$project": {"_id": 1, "blobs": 1}},
        {"$unwind": "$blobs"},
        {"$match": {"blobs.c1ass_state": c1ass_state, "blobs.state": {"$ne": BLOB_STATE_REMOVED}}},
        {"$sort": {"date_modified": -1}}
    ]), "blobs")
    return db_blobs


def db_blobs_update_states(db, blob_states):
    log("db_blobs_update_states(db=%s, blob_states=%s)" % (db, blob_states))
    for blob_state in blob_states:
        db[DB_IMAGES].update_one({"blobs.uid": ObjectId(blob_state["uid"])},
                                 {"$set": {
                                     "blobs.$.c1ass": blob_state["c1ass"],
                                     "blobs.$.c1ass_state": blob_state["c1ass_state"]
                                 }, "$currentDate": {"date_modified": True}})


# backgrounds


def db_background(date_created, mean_color):
    return {
        "date_created": db_verify(date_created, datetime),
        "mean_color": db_verify(mean_color, tuple)
    }


def db_backgrounds_write(db, db_background):
    log("db_backgrounds_write(db=%s, db_background=%s)" % (db, db_background))
    return db[DB_BACKGROUNDS].insert_one(db_background).inserted_id


def db_backgrounds_read_latest_n(db, n):
    log("db_backgrounds_read_latest_n(db=%s, n=%s)" % (db, n))
    db_backgrounds = to_list(db[DB_BACKGROUNDS].find(limit=n, sort=[("date_created", pymongo.DESCENDING)]))
    return db_backgrounds


def db_backgrounds_read_latest(db):
    log("db_backgrounds_read_latest(db=%s)" % db)
    db_backgrounds = db_backgrounds_read_latest_n(db, 1)
    return None if len(db_backgrounds) == 0 else db_backgrounds[0]
