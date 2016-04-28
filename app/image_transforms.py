import json
import os
import urllib2
from shutil import copyfile

from flask import url_for

from SimpleCV import Color, DrawingLayer

from errors import *
from fs import *
from app.settings import (
    USE_COLOR_DISTANCE_FOR_BACKGROUND,
    BACKGROUND_MASK_THRESHOLD,
    USE_CLASSIFIER,
    CLASSIFIER_URL,
    SHOW_REMOVED_SNACKS
)

TR_TYPE_MASK = "mask"
TR_TYPE_MASK_CLEAN = "mask_clean"
TR_TYPE_MASKED = "masked"
TR_TYPE_BLOBS = "blobs"
TR_TYPE_BLOB_STATE_CHANGE = "blob_state_change"
TR_TYPE_BLOBS_CLASSIFIED = "blobs_classified"


# transform utils


def tr_find_by_type(db_transforms, type):
    for db_transform in db_transforms:
        if db_transform["type"] == type:
            return db_transform


# transforms


def transform_create_mask_by_color_distance(processing_path, img, bg_color, thresh):
    log("transform_create_mask_by_color_distance(processing_path=%s, img=%s, bg_color=%s, thresh=%s)" % (
        processing_path, img, bg_color, thresh))
    img_distance = img.colorDistance(bg_color)
    img_mask = img_distance.binarize(thresh)
    img_mask_name = TR_TYPE_MASK + ".png"
    img_mask_path = processing_path + img_mask_name
    img_mask.save(img_mask_path)
    return db_transform(
        uid=ObjectId(),
        title="mask from bg",
        type=TR_TYPE_MASK,
        description="create mask covering [WHITE] to [WHITE - threshold]",
        img_path=img_mask_path,
        img_url=url_for("static", filename=os.path.relpath(img_mask_path, "static"), _external=True)
    ), img_mask


def transform_create_mask(processing_path, img, bg_color, thresh):
    log("transform_create_mask(processing_path=%s, img=%s, bg_color=%s, thresh=%s)" % (
        processing_path, img, bg_color, thresh))
    color1 = (bg_color[0] - thresh / 2, bg_color[1] - thresh / 2, bg_color[2] - thresh / 2)
    color2 = (bg_color[0] + thresh / 2, bg_color[1] + thresh / 2, bg_color[2] + thresh / 2)
    img_mask = img.createBinaryMask(color1=color1, color2=color2)
    img_mask_name = TR_TYPE_MASK + ".png"
    img_mask_path = processing_path + img_mask_name
    img_mask.save(img_mask_path)
    return db_transform(
        uid=ObjectId(),
        title="mask from bg",
        type=TR_TYPE_MASK,
        description="create mask covering [WHITE] to [WHITE - threshold]",
        img_path=img_mask_path,
        img_url=url_for("static", filename=os.path.relpath(img_mask_path, "static"), _external=True)
    ), img_mask


def transform_cleanup_mask(processing_path, img_mask, erode):
    log("transform_cleanup_mask(processing_path=%s, img_mask=%s, erode=%s)" % (processing_path, img_mask, erode))
    # clean it up a bit
    img_mask_clean = img_mask \
        .erode(erode) \
        .invert()
    img_mask_clean_name = TR_TYPE_MASK_CLEAN + ".png"
    img_mask_clean_path = processing_path + img_mask_clean_name
    img_mask_clean.save(img_mask_clean_path)
    return db_transform(
        uid=ObjectId(),
        title="cleanup mask",
        type=TR_TYPE_MASK_CLEAN,
        description="clean up the mask to make it more continuous",
        img_path=img_mask_clean_path,
        img_url=url_for("static", filename=os.path.relpath(img_mask_clean_path, "static"), _external=True)
    ), img_mask_clean


def transform_apply_mask(processing_path, img, img_mask):
    log("transform_apply_mask(processing_path=%s, img=%s, img_mask=%s)" % (processing_path, img, img_mask))
    img_masked = img.applyBinaryMask(img_mask)
    if not img_masked:
        raise FailedTransformException("Application of binary mask failed")
    img_masked_name = TR_TYPE_MASKED + ".png"
    img_masked_path = processing_path + img_masked_name
    img_masked.save(img_masked_path)
    return db_transform(
        uid=ObjectId(),
        title="apply mask",
        type=TR_TYPE_MASKED,
        description="apply the mask to the image",
        img_path=img_masked_path,
        img_url=url_for("static", filename=os.path.relpath(img_masked_path, "static"), _external=True)
    ), img_masked


def transform_extract_blobs(processing_path, img, img_mask, minsize):
    log("transform_extract_blobs(processing_path=%s, img=%s, img_mask=%s, minsize=%s)" % (
        processing_path, img, img_mask, minsize))
    img_copy = img.copy()
    blobs = img_copy.findBlobsFromMask(img_mask, minsize=minsize)
    if blobs:
        # draw blobs
        blobs.draw(color=Color.RED, width=3)
    else:
        blobs = []
    # save image (blobs or not)
    img_blobs_name = TR_TYPE_BLOBS + ".png"
    img_blobs_path = processing_path + img_blobs_name
    img_copy.save(img_blobs_path)
    # traverse blobs
    i = 1
    db_blobs = []
    for blob in blobs:
        # crop image to blob
        blob_img = img.crop(blob)
        blob_img_name = "blob_" + str(i).zfill(2) + ".png"
        blob_img_path = processing_path + blob_img_name
        blob_img.save(blob_img_path)
        # create db_blob
        db_blobs.append(db_blob(
            uid=ObjectId(),
            title="blob " + str(i).zfill(2),
            bounds={"x": blob.minX(), "y": blob.minY(), "w": blob.width(), "h": blob.height()},
            img_path=blob_img_path,
            img_url=url_for("static", filename=os.path.relpath(blob_img_path, "static"), _external=True)))
        i += 1
    return db_transform(
        uid=ObjectId(),
        title="extract blobs",
        type=TR_TYPE_BLOBS,
        description="use the mask to extract the blobs",
        img_path=img_blobs_path,
        img_url=url_for("static", filename=os.path.relpath(img_blobs_path, "static"), _external=True)
    ), db_blobs


def transform_blob_state_changes(processing_path, img, db_blobs_now, db_blobs_prev, max_offset):
    log("transform_blob_state_changes(processing_path=%s, img=%s, db_blobs_now=%s,\
         db_blobs_prev=%s, max_offset=%s)" % (processing_path, img, db_blobs_now, db_blobs_prev, max_offset))
    # create markup layer
    img_markups = DrawingLayer(img.size())
    # count the state totals
    blob_count_duplicate = 0
    blob_count_new = 0
    blob_count_removed = 0
    # traverse db_blobs
    for db_blob_now in db_blobs_now:
        found_in_prev = False
        bn = db_blob_now["bounds"]
        for i, db_blob_prev in enumerate(db_blobs_prev):
            bp = db_blob_prev["bounds"]
            if abs(bn["x"] - bp["x"]) <= max_offset \
                    and abs(bn["y"] - bp["y"]) <= max_offset \
                    and abs(bn["w"] - bp["w"]) <= max_offset \
                    and abs(bn["h"] - bp["h"]) <= max_offset \
                    and db_blob_prev["state"] != BLOB_STATE_REMOVED:
                found_in_prev = True
                # remove item and immediately break
                db_blobs_prev.pop(i)
                break
        # set the state and associated color
        if found_in_prev:
            state = BLOB_STATE_DUPLICATE
            color = Color.ORANGE
            blob_count_duplicate += 1
        else:
            state = BLOB_STATE_NEW
            color = Color.GREEN
            blob_count_new += 1
        db_blob_now["state"] = state
        # draw blob rectangle
        img_markups.rectangle(topLeft=(bn["x"], bn["y"]), dimensions=(bn["w"], bn["h"]), color=color, width=3)
        # draw class text
        img_markups.text(text=state, location=(bn["x"], bn["y"] - 15), color=color)
    if SHOW_REMOVED_SNACKS:
        # draw removed items
        for db_blob_prev in db_blobs_prev:
            # ignore if prev was removed
            if db_blob_prev["state"] == BLOB_STATE_REMOVED:
                continue
            color = Color.RED
            state = BLOB_STATE_REMOVED
            blob_count_removed += 1
            bp = db_blob_prev["bounds"]
            # copy the prev blob images and add it to db_blobs_now
            i = len(db_blobs_now) + 1
            blob_img_name = "blob_" + str(i).zfill(2) + ".png"
            blob_img_path = processing_path + blob_img_name
            copyfile(db_blob_prev["img_path"], blob_img_path)
            db_blobs_now.append(db_blob(
                uid=ObjectId(),
                title="blob " + str(i).zfill(2),
                bounds=db_blob_prev["bounds"],
                img_path=blob_img_path,
                img_url=url_for("static", filename=os.path.relpath(blob_img_path, "static"), _external=True),
                state=state
            ))
            # draw blob rectangle
            img_markups.rectangle(topLeft=(bp["x"], bp["y"]), dimensions=(bp["w"], bp["h"]), color=color, width=3)
            # draw class text
            img_markups.text(text=state, location=(bp["x"], bp["y"] - 15), color=color)
    # if only duplicates, throw exception
    if blob_count_new == 0 and blob_count_removed == 0:
        raise NoBlobChangesDetectedException("No changes were detected.")
    # copy image and add markups
    img_marked = img.copy()
    img_marked.addDrawingLayer(img_markups)
    img_marked_name = TR_TYPE_BLOB_STATE_CHANGE + ".png"
    img_marked_path = processing_path + img_marked_name
    img_marked.save(img_marked_path)
    return db_transform(
        uid=ObjectId(),
        title="state changes",
        type=TR_TYPE_BLOB_STATE_CHANGE,
        description="compare all of the blobs and determine which ones are new, duplicated and removed",
        img_path=img_marked_path,
        img_url=url_for("static", filename=os.path.relpath(img_marked_path, "static"), _external=True)
    ), db_blobs_now


def classify_blob(image_url):
    if USE_CLASSIFIER:
        classify_url = CLASSIFIER_URL + '/classify' + '?image=' + image_url
        log("classify_blobs(classify_url=%s)" % (classify_url))
        try:
            classify_service = urllib2.urlopen(classify_url)
            classify_result = json.loads(classify_service.read())
            if classify_result:
                c1ass = classify_result['class']
            else:
                c1ass = "unknown"
            log("classify_blobs(%s as %s)" % (image_url, c1ass))
        except:
            log("classify_blobs(service failed, %s as unknown)" % (image_url))
            c1ass = "unknown"
    else:
        c1ass = "unknown"
    return c1ass


def transform_classify_blobs(processing_path, img, db_blobs):
    log("transform_classify_blobs(processing_path=%s, img=%s, db_blobs=%s)" % (
        processing_path, img, db_blobs))
    # create markup layer
    img_markups = DrawingLayer(img.size())
    # traverse blobs
    for db_blob in db_blobs:
        b = db_blob["bounds"]
        # call external service to classify a blob image as a class category
        c1ass = classify_blob(db_blob["img_url"])
        db_blob["c1ass"] = c1ass
        db_blob["c1ass_state"] = "auto"
        # get the state color
        state = db_blob["state"]
        color = Color.RED if state == BLOB_STATE_REMOVED else (
            Color.ORANGE if state == BLOB_STATE_DUPLICATE else Color.GREEN)
        # draw blob rectangle
        img_markups.rectangle(topLeft=(b["x"], b["y"]), dimensions=(b["w"], b["h"]), color=color, width=3)
        # draw class text
        img_markups.text(text=c1ass, location=(b["x"], b["y"] - 15), color=color)
    # copy image and add markups
    img_marked = img.copy()
    img_marked.addDrawingLayer(img_markups)
    img_marked_name = TR_TYPE_BLOBS_CLASSIFIED + ".png"
    img_marked_path = processing_path + img_marked_name
    img_marked.save(img_marked_path)
    return db_transform(
        uid=ObjectId(),
        title="classify blobs",
        type=TR_TYPE_BLOBS_CLASSIFIED,
        description="use the classifier to classify the blob",
        img_path=img_marked_path,
        img_url=url_for("static", filename=os.path.relpath(img_marked_path, "static"), _external=True)
    ), db_blobs


def apply_transforms(processing_path, img, bg_color):
    log("apply_transforms(processing_path=%s, img=%s, bg_color=%s)" % (
        processing_path, img, bg_color))
    if not os.path.exists(processing_path):
        os.makedirs(processing_path)
    db_transforms = []
    if USE_COLOR_DISTANCE_FOR_BACKGROUND:
        (db_transform, img_mask) = transform_create_mask_by_color_distance(
            processing_path, img, bg_color, thresh=BACKGROUND_MASK_THRESHOLD)
    else:
        (db_transform, img_mask) = transform_create_mask(
            processing_path, img, bg_color, thresh=BACKGROUND_MASK_THRESHOLD)

    db_transforms.append(db_transform)
    (db_transform, img_mask_clean) = transform_cleanup_mask(processing_path, img_mask, erode=5)
    db_transforms.append(db_transform)
    (db_transform, img_masked) = transform_apply_mask(processing_path, img, img_mask_clean)
    db_transforms.append(db_transform)
    (db_transform, db_blobs) = transform_extract_blobs(processing_path, img, img_mask_clean, minsize=500)
    db_transforms.append(db_transform)
    db = db_open()
    db_image_latest = db_images_read_latest(db)
    db_close(db)
    db_blobs_latest = db_image_latest["blobs"] if db_image_latest else []
    (db_transform, db_blobs) = transform_blob_state_changes(processing_path, img, db_blobs, db_blobs_latest,
                                                            max_offset=10)
    db_transforms.append(db_transform)
    (db_transform, db_blobs) = transform_classify_blobs(processing_path, img, db_blobs)
    db_transforms.append(db_transform)
    return db_transforms, db_blobs
