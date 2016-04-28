import subprocess
from random import randint

from SimpleCV import Camera, Image

from app.settings import (
    DEBUG,
    HAS_FTP,
    PRE_INIT_CAMERA,
    USE_WEB_CAMERA,
    USE_MOTION_CAMERA,
    MOTION_CAMERA_SNAPSHOT,
    CROP_IMAGE_BORDERS,
    BACKGROUND_AUTO_CALIBRATE
)
from image_transforms import *
from db import *
from errors import *
from ftp import *

ACTION_NAME_PATTERN = "snack-%d_%02d_%02d-%02d_%02d_%02d"
IMAGES_FOLDER_PATH = "static/images/"
TEMP_FOLDER_PATH = IMAGES_FOLDER_PATH + "_temp/"
STATIC_IMAGE_NAME_PATTERN = "static_image_%02d.png"
STATIC_BACKGROUND_NAME = "static_background.png"

# pre-initialize Camera object, this is needed for MacOSX
if PRE_INIT_CAMERA:
    if USE_WEB_CAMERA:
        cam = Camera()
else:
    cam = None


def capture_pi_cam_image(filename, width, height):
    log("capture_pi_cam_image(filename=%s, width=%s, height=%s)")
    subprocess.call("raspistill -w %d -h %d -t 0 -e jpg -q 15 -o %s" % (
        width, height, filename), shell=True)


def capture_camera_image():
    log("capture_camera_image()")
    image = None
    if USE_MOTION_CAMERA:
        image = Image(MOTION_CAMERA_SNAPSHOT)
    else:  # default to USE_WEB_CAMERA
        if cam is None:
            image = Camera().getImage()
        else:
            image = cam.getImage()

    size = image.size()

    # dynamic background mean color calculation
    if (BACKGROUND_AUTO_CALIBRATE):
        x = CROP_IMAGE_BORDERS[0]
        y = CROP_IMAGE_BORDERS[1]
        if (x > 0 and y > 0):
            background = image.crop(0, 0, x, y)
            mean_color = background.meanColor()
            log("background as (%d, %d, %d)" % (mean_color[0], mean_color[1], mean_color[2]))
            # save it
            db = db_open()
            db_backgrounds_write(db, db_background(date_created=datetime.now(), mean_color=mean_color))
            db_close(db)

    # if image border needs to be cropped
    x = CROP_IMAGE_BORDERS[0]
    y = CROP_IMAGE_BORDERS[1]
    if (x > 0 and y > 0):
        width = size[0] - 2 * x
        height = size[1] - 2 * y
        cropped = image.crop(x, y, width, height)
    else:
        cropped = image
    return cropped


def take_and_process_image():
    log("take_and_process_image()")
    img = take_raw_image()
    bg_color = get_background_color()
    process_image(img, bg_color)


def take_raw_image():
    log("take_raw_image()")
    if DEBUG:
        img = Image(TEMP_FOLDER_PATH + STATIC_IMAGE_NAME_PATTERN % randint(0, 8))
    else:
        img = capture_camera_image()
    return img.toRGB()


def take_background():
    log("take_background()")
    # get background snapshot
    if DEBUG:
        img = Image(TEMP_FOLDER_PATH + STATIC_BACKGROUND_NAME)
    else:
        img = capture_camera_image()
    # get mean_color
    mean_color = img.meanColor()
    # save it
    db = db_open()
    db_backgrounds_write(db, db_background(date_created=datetime.now(), mean_color=mean_color))
    db_close(db)


def get_background_color():
    log("get_background_color()")
    db = db_open()
    db_background = db_backgrounds_read_latest(db)
    db_close(db)
    if not db_background:
        raise NotCalibratedException("There are no background records. Run \"Calibrate\" first.")
    return db_background["mean_color"]


def get_image_class_names():
    log("get_image_class_names()")
    class_names = ['brownie', 'candy', 'cookie', 'package', 'unknown']
    return class_names


def process_image(img, bg_color):
    log("process_image(img=%s, bg_color=%s)" % (img, bg_color))
    # current date
    now = datetime.now()
    processing_name = ACTION_NAME_PATTERN % (now.year, now.month, now.day, now.hour, now.minute, now.second)
    processing_folder_name = processing_name + "/"
    # path of working directory
    processing_path = IMAGES_FOLDER_PATH + processing_folder_name
    os.makedirs(processing_path)
    # save image to be processed
    img_name = "img.png"
    img_path = processing_path + img_name
    img.save(img_path)
    # apply the transforms
    (db_transforms, db_blobs) = apply_transforms(img=img, processing_path=processing_path, bg_color=bg_color)
    # check if any blobs
    if len(db_blobs) == 0:
        raise NoBlobsDetectedException("No blob changes were identified.")
    # get the img_url for classified blobs
    db_transform = tr_find_by_type(db_transforms, TR_TYPE_BLOBS_CLASSIFIED)
    img_classified_url = db_transform["img_url"]
    img_classified_url_ext = ""
    # if FTP is enabled, externalize the img_url
    if HAS_FTP:
        ftp = ftp_open()
        ftp_mkdirs(ftp, processing_path)
        img_classified_url_ext = db_transform["img_url_ext"] = ftp_upload(ftp, db_transform["img_path"])
        ftp_close(ftp)
    # create and write db_image
    db = db_open()
    db_images_write(db, db_image(
        title="processed image",
        date_created=now,
        date_modified=now,
        img_path=img_path,
        img_url=img_classified_url,
        img_url_ext=img_classified_url_ext,
        db_transforms=db_transforms,
        db_blobs=db_blobs))
    db_close(db)


def track_click(url):
    log("track_click(url=%s)" % url)
    return True
