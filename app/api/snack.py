import json
from bson import json_util

from flask import request, Response

from . import api
from ..utils import (
    take_and_process_image,
    get_image_class_names
)
from ..image_transforms import *

"""
@api {get} /snacks Get all images
@apiVersion 1.0.0
@apiName GetImage
@apiDescription This call returns the list of images (max 10) in order of date_created DESC in BSON format.
@apiGroup Image

@apiSuccess {dict[]} images The list of image objects (max 10)
@apiSuccess {str} images.title The title of the image
@apiSuccess {str} images.date_created The date (ISO format) when the image was created
@apiSuccess {str} images.date_modified The date (ISO format) when the image was last modified
@apiSuccess {str} images.img_path The local relative path of the raw image
@apiSuccess {str} images.img_url The local fully qualified url of the raw image
@apiSuccess {str} images.img_url_ext The local fully qualified url of the externalized raw image
@apiSuccess {dict[]} images.transforms The list of transforms executed on this image
@apiSuccess {str} images.transforms.title The title of the transform
@apiSuccess {str} images.transforms.date_created The date (ISO format) when the transform was created
@apiSuccess {str} images.transforms.date_modified The date (ISO format) when the transform was last modified
@apiSuccess {str} images.transforms.img_path The local relative path of the generated transform image
@apiSuccess {str} images.transforms.img_url The local fully qualified url of the generated transform image
@apiSuccess {str} images.transforms.img_url_ext The local fully qualified url of the externalized generated transform image
@apiSuccess {dict[]} images.blobs The list of blobs identified in this image
@apiSuccess {str} images.blobs.title The title of the blob
@apiSuccess {dict} images.blobs.bounds The bounding box of the blob
@apiSuccess {int} images.blobs.bounds.x The upper-left x coordinate
@apiSuccess {int} images.blobs.bounds.y The upper-left y coordinate
@apiSuccess {int} images.blobs.bounds.w The width dimension
@apiSuccess {int} images.blobs.bounds.h The height dimension
@apiSuccess {str} images.blobs.img_path The local relative path of the extracted blob image
@apiSuccess {str} images.blobs.img_url The local fully qualified url of the extracted blob image
@apiSuccess {str} images.blobs.img_url_ext The local fully qualified url of the externalized extracted blob image
@apiSuccess {str} images.blobs.c1ass The classification of the blob
@apiSuccess {str} images.blobs.c1ass_state The mode of classification of the blob
@apiSuccess {str} images.blobs.state The state [new, duplicate, removed] of the blob
"""


@api.route('/snacks', methods=['GET'])
def get_snacks():
    log("get_snacks()")
    db = db_open()
    try:
        db_images = db_images_read_latest_n(db, 10)
    except:
        db_images = None
    db_close(db)
    return Response(json.dumps(db_images, default=json_util.default), mimetype='application/json')


"""
@api {get} /snacks/snap Snap and get image
@apiVersion 1.0.0
@apiName SnapImage
@apiDescription This call takes a snapshot and then processes and returns the generated image.
@apiGroup Image

@apiSuccess {dict} image The image object
@apiSuccess {str} image.title The title of the image
@apiSuccess {str} image.date_created The date (ISO format) when the image was created
@apiSuccess {str} image.date_modified The date (ISO format) when the image was last modified
@apiSuccess {str} image.img_path The local relative path of the raw image
@apiSuccess {str} image.img_url The local fully qualified url of the raw image
@apiSuccess {str} image.img_url_ext The local fully qualified url of the externalized raw image
@apiSuccess {dict[]} image.transforms The list of transforms executed on this image
@apiSuccess {str} image.transforms.title The title of the transform
@apiSuccess {str} image.transforms.date_created The date (ISO format) when the transform was created
@apiSuccess {str} image.transforms.date_modified The date (ISO format) when the transform was last modified
@apiSuccess {str} image.transforms.img_path The local relative path of the generated transform image
@apiSuccess {str} image.transforms.img_url The local fully qualified url of the generated transform image
@apiSuccess {str} image.transforms.img_url_ext The local fully qualified url of the externalized generated transform image
@apiSuccess {dict[]} image.blobs The list of blobs identified in this image
@apiSuccess {str} image.blobs.title The title of the blob
@apiSuccess {dict} image.blobs.bounds The bounding box of the blob
@apiSuccess {int} image.blobs.bounds.x The upper-left x coordinate
@apiSuccess {int} image.blobs.bounds.y The upper-left y coordinate
@apiSuccess {int} image.blobs.bounds.w The width dimension
@apiSuccess {int} image.blobs.bounds.h The height dimension
@apiSuccess {str} image.blobs.img_path The local relative path of the extracted blob image
@apiSuccess {str} image.blobs.img_url The local fully qualified url of the extracted blob image
@apiSuccess {str} image.blobs.img_url_ext The local fully qualified url of the externalized extracted blob image
@apiSuccess {str} image.blobs.c1ass The classification of the blob
@apiSuccess {str} image.blobs.c1ass_state The mode of classification of the blob
@apiSuccess {str} image.blobs.state The state [new, duplicate, removed] of the blob
"""


@api.route('/snacks/snap', methods=['GET'])
def get_snacks_snap():
    log("get_snacks_snap()")
    db = db_open()
    try:
        take_and_process_image()
        db_image = db_images_read_latest(db)
    except:
        db_image = None
    db_close(db)
    return Response(json.dumps(db_image, default=json_util.default), mimetype='application/json')


"""
@api {get} /snacks/id/<id> Get image by _id
@apiVersion 1.0.0
@apiName GetImageById
@apiDescription This call gets an image by the database id. If it is not found, null is returned.
@apiGroup Image

@apiParam {int} id The database id of the image

@apiSuccess {dict} image The image object
@apiSuccess {str} image.title The title of the image
@apiSuccess {str} image.date_created The date (ISO format) when the image was created
@apiSuccess {str} image.date_modified The date (ISO format) when the image was last modified
@apiSuccess {str} image.img_path The local relative path of the raw image
@apiSuccess {str} image.img_url The local fully qualified url of the raw image
@apiSuccess {str} image.img_url_ext The local fully qualified url of the externalized raw image
@apiSuccess {dict[]} image.transforms The list of transforms executed on this image
@apiSuccess {str} image.transforms.title The title of the transform
@apiSuccess {str} image.transforms.date_created The date (ISO format) when the transform was created
@apiSuccess {str} image.transforms.date_modified The date (ISO format) when the transform was last modified
@apiSuccess {str} image.transforms.img_path The local relative path of the generated transform image
@apiSuccess {str} image.transforms.img_url The local fully qualified url of the generated transform image
@apiSuccess {str} image.transforms.img_url_ext The local fully qualified url of the externalized generated transform image
@apiSuccess {dict[]} image.blobs The list of blobs identified in this image
@apiSuccess {str} image.blobs.title The title of the blob
@apiSuccess {dict} image.blobs.bounds The bounding box of the blob
@apiSuccess {int} image.blobs.bounds.x The upper-left x coordinate
@apiSuccess {int} image.blobs.bounds.y The upper-left y coordinate
@apiSuccess {int} image.blobs.bounds.w The width dimension
@apiSuccess {int} image.blobs.bounds.h The height dimension
@apiSuccess {str} image.blobs.img_path The local relative path of the extracted blob image
@apiSuccess {str} image.blobs.img_url The local fully qualified url of the extracted blob image
@apiSuccess {str} image.blobs.img_url_ext The local fully qualified url of the externalized extracted blob image
@apiSuccess {str} image.blobs.c1ass The classification of the blob
@apiSuccess {str} image.blobs.c1ass_state The mode of classification of the blob
@apiSuccess {str} image.blobs.state The state [new, duplicate, removed] of the blob
"""


@api.route('/snacks/id/<id>', methods=['GET'])
def get_snacks_by_id(id):
    log("get_snacks_by_id(id=%s)" % id)
    db = db_open()
    try:
        db_image = db_images_read_by_id(db, id)
    except:
        db_image = None
    db_close(db)
    # json_util.default will convert datetime object to string properly
    # Hint: if want to deserialize, use the following
    # json.loads(json_string, object_hook=json_util.object_hook)
    return Response(json.dumps(db_image, default=json_util.default), mimetype='application/json')


"""
@api {get} /snacks/state/<c1ass_state> Get blobs by class_state
@apiVersion 1.0.0
@apiName GetBlobsByClassState
@apiDescription This call gets a list of blobs filtered by c1ass_state.
@apiGroup Blob

@apiParam {str} c1ass_state The class state [auto, trained] of the blob

@apiSuccess {dict[]} blobs The list of blobs object
@apiSuccess {str} blobs.title The title of the blob
@apiSuccess {dict} blobs.bounds The bounding box of the blob
@apiSuccess {int} blobs.bounds.x The upper-left x coordinate
@apiSuccess {int} blobs.bounds.y The upper-left y coordinate
@apiSuccess {int} blobs.bounds.w The width dimension
@apiSuccess {int} blobs.bounds.h The height dimension
@apiSuccess {str} blobs.img_path The local relative path of the extracted blob image
@apiSuccess {str} blobs.img_url The local fully qualified url of the extracted blob image
@apiSuccess {str} blobs.img_url_ext The local fully qualified url of the externalized extracted blob image
@apiSuccess {str} blobs.c1ass The classification of the blob
@apiSuccess {str} blobs.c1ass_state The mode of classification of the blob
@apiSuccess {str} blobs.state The state [new, duplicate, removed] of the blob
"""


@api.route('/snacks/state/<c1ass_state>', methods=['GET'])
def get_blobs_by_class_state(c1ass_state):
    log("get_blobs_by_class_state(c1ass_state=%s)" % c1ass_state)
    # use state='auto' to find the untrained blobs
    db = db_open()
    try:
        db_blobs = db_blobs_read_by_c1ass_state(db, c1ass_state=c1ass_state, n=10)
    except Exception as e:
        log("ERROR: %s" % e.message)
        db_blobs = None
    db_close(db)
    return Response(json.dumps(db_blobs, default=json_util.default), mimetype='application/json')


"""
@api {put} /snacks/state Update blobs state info by _id
@apiVersion 1.0.0
@apiName UpdateBlobStateClassStateById
@apiDescription This call accepts a list of id, c1ass, c1ass_state objects and updates the associated blobs in the database.
@apiGroup Blob

@apiParam {dict[]} dicts A custom list of objects
@apiParam {str} dicts.id The database id of the blob
@apiParam {str} dicts.c1ass The class of the blob
@apiParam {str} dicts.c1ass_state The class state [auto, trained] of the blob
"""


@api.route('/snacks/state', methods=['PUT'])
def get_snacks_update_state():
    log("get_snacks_update_state()")
    # put_data = json.loads(request.json, object_hook=json_util.object_hook)
    put_data = request.get_json(force=True)
    blob_states = []
    for blob_state in put_data:
        blob_states.append({
            "uid": blob_state["uid"],
            "c1ass": blob_state["c1ass"],
            "c1ass_state": blob_state["c1ass_state"]
        })
    db = db_open()
    db_blobs_update_states(db, blob_states)
    db_close(db)
    return Response({}, status=201, mimetype='application/json')


"""
@api {get} /snacks/class/names Get list of class names
@apiVersion 1.0.0
@apiName GetClassNames
@apiDescription This call returns a list of the possible class names that a blob can be classified by.
@apiGroup Blob

@apiSuccess {str[]} strs The list of class names
"""


@api.route('/snacks/class/names', methods=['GET'])
def get_snacks_class_names():
    log("get_snacks_class_names()")
    name_list = get_image_class_names()
    return Response(json.dumps(name_list), mimetype='application/json')


"""
@api {get} /snacks/last Get last image
@apiVersion 1.0.0
@apiName GetLastImage
@apiDescription This call returns the latest image by date_created DESC. If none exist, null is returned.
@apiGroup Image

@apiSuccess {dict} image The image object
@apiSuccess {str} image.title The title of the image
@apiSuccess {str} image.date_created The date (ISO format) when the image was created
@apiSuccess {str} image.date_modified The date (ISO format) when the image was last modified
@apiSuccess {str} image.img_path The local relative path of the raw image
@apiSuccess {str} image.img_url The local fully qualified url of the raw image
@apiSuccess {str} image.img_url_ext The local fully qualified url of the externalized raw image
@apiSuccess {dict[]} image.transforms The list of transforms executed on this image
@apiSuccess {str} image.transforms.title The title of the transform
@apiSuccess {str} image.transforms.date_created The date (ISO format) when the transform was created
@apiSuccess {str} image.transforms.date_modified The date (ISO format) when the transform was last modified
@apiSuccess {str} image.transforms.img_path The local relative path of the generated transform image
@apiSuccess {str} image.transforms.img_url The local fully qualified url of the generated transform image
@apiSuccess {str} image.transforms.img_url_ext The local fully qualified url of the externalized generated transform image
@apiSuccess {dict[]} image.blobs The list of blobs identified in this image
@apiSuccess {str} image.blobs.title The title of the blob
@apiSuccess {dict} image.blobs.bounds The bounding box of the blob
@apiSuccess {int} image.blobs.bounds.x The upper-left x coordinate
@apiSuccess {int} image.blobs.bounds.y The upper-left y coordinate
@apiSuccess {int} image.blobs.bounds.w The width dimension
@apiSuccess {int} image.blobs.bounds.h The height dimension
@apiSuccess {str} image.blobs.img_path The local relative path of the extracted blob image
@apiSuccess {str} image.blobs.img_url The local fully qualified url of the extracted blob image
@apiSuccess {str} image.blobs.img_url_ext The local fully qualified url of the externalized extracted blob image
@apiSuccess {str} image.blobs.c1ass The classification of the blob
@apiSuccess {str} image.blobs.c1ass_state The mode of classification of the blob
@apiSuccess {str} image.blobs.state The state [new, duplicate, removed] of the blob
"""


@api.route('/snacks/last', methods=['GET'])
def get_snacks_last():
    log("get_snacks_last()")
    db = db_open()
    try:
        db_images = db_images_read_latest(db)
    except:
        db_images = None
    db_close(db)
    return Response(json.dumps(db_images, default=json_util.default), mimetype='application/json')


"""
@api {get} /snacks/last/<int:n> Get last n images
@apiVersion 1.0.0
@apiName GetLastNImages
@apiDescription This call returns a list of the latest images by date_created DESC.
@apiGroup Image

@apiSuccess {dict[]} images The list of image objects (max 10)
@apiSuccess {str} images.title The title of the image
@apiSuccess {str} images.date_created The date (ISO format) when the image was created
@apiSuccess {str} images.date_modified The date (ISO format) when the image was last modified
@apiSuccess {str} images.img_path The local relative path of the raw image
@apiSuccess {str} images.img_url The local fully qualified url of the raw image
@apiSuccess {str} images.img_url_ext The local fully qualified url of the externalized raw image
@apiSuccess {dict[]} images.transforms The list of transforms executed on this image
@apiSuccess {str} images.transforms.title The title of the transform
@apiSuccess {str} images.transforms.date_created The date (ISO format) when the transform was created
@apiSuccess {str} images.transforms.date_modified The date (ISO format) when the transform was last modified
@apiSuccess {str} images.transforms.img_path The local relative path of the generated transform image
@apiSuccess {str} images.transforms.img_url The local fully qualified url of the generated transform image
@apiSuccess {str} images.transforms.img_url_ext The local fully qualified url of the externalized generated transform image
@apiSuccess {dict[]} images.blobs The list of blobs identified in this image
@apiSuccess {str} images.blobs.title The title of the blob
@apiSuccess {dict} images.blobs.bounds The bounding box of the blob
@apiSuccess {int} images.blobs.bounds.x The upper-left x coordinate
@apiSuccess {int} images.blobs.bounds.y The upper-left y coordinate
@apiSuccess {int} images.blobs.bounds.w The width dimension
@apiSuccess {int} images.blobs.bounds.h The height dimension
@apiSuccess {str} images.blobs.img_path The local relative path of the extracted blob image
@apiSuccess {str} images.blobs.img_url The local fully qualified url of the extracted blob image
@apiSuccess {str} images.blobs.img_url_ext The local fully qualified url of the externalized extracted blob image
@apiSuccess {str} images.blobs.c1ass The classification of the blob
@apiSuccess {str} images.blobs.c1ass_state The mode of classification of the blob
@apiSuccess {str} images.blobs.state The state [new, duplicate, removed] of the blob
"""


@api.route('/snacks/last/<int:n>', methods=['GET'])
def get_snacks_last_n(n):
    log("get_snacks_last_n()")
    db = db_open()
    try:
        db_images = db_images_read_latest_n(db, n)
    except:
        db_images = None
    db_close(db)
    return Response(json.dumps(db_images, default=json_util.default), mimetype='application/json')


"""
@api {get} /snacks/last/summary Get latest summary
@apiVersion 1.0.0
@apiName GetLastSummary
@apiDescription This call returns a summary of the latest processed images including the new, duplicate and removed blobs. If no images exist, it returns null.
@apiGroup Summary

@apiSuccess {dict} dict The summary
@apiSuccess {str} dict.image_id The database id of the last image
@apiSuccess {str} dict.img_marked_url The local fully qualified url of the marked image
@apiSuccess {str} dict.img_marked_url_ext The local fully qualified url of the externalized marked image
@apiSuccess {int} dict.blob_count_new The number of new blobs identified
@apiSuccess {int} dict.blob_count_duplicate The number of duplicate blobs identified
@apiSuccess {int} dict.blob_count_removed The number of removed blobs identified
"""


@api.route('/snacks/last/summary', methods=['GET'])
def get_snacks_last_summary():
    log("get_snacks_last_summary()")
    db = db_open()
    try:
        db_image = db_images_read_latest(db)
        if db_image:
            image_id = str(db_image["_id"])
            db_blobs = db_image["blobs"]
            # count the state totals
            blob_count_duplicate = 0
            blob_count_new = 0
            blob_count_removed = 0
            for db_blob in db_blobs:
                state = db_blob["state"]
                if state == BLOB_STATE_DUPLICATE:
                    blob_count_duplicate += 1
                if state == BLOB_STATE_NEW:
                    blob_count_new += 1
                if state == BLOB_STATE_REMOVED:
                    blob_count_removed += 1
            db_transform = db_transforms_read_by_id_type(db, image_id, TR_TYPE_BLOBS_CLASSIFIED)
            data = {
                "image_id": image_id,
                "blob_count_duplicate": blob_count_duplicate,
                "blob_count_new": blob_count_new,
                "blob_count_removed": blob_count_removed,
                "img_marked_url": db_transform["img_url"] if db_transform else "",
                "img_marked_url_ext": db_transform["img_url_ext"] if db_transform else ""
            }
        else:
            data = None
    except:
        data = None
    db_close(db)
    return Response(json.dumps(data), mimetype='application/json')
