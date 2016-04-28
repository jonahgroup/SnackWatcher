define({ "api": [
  {
    "type": "get",
    "url": "/snacks/state/<c1ass_state>",
    "title": "Get blobs by class_state",
    "version": "1.0.0",
    "name": "GetBlobsByClassState",
    "description": "<p>This call gets a list of blobs filtered by c1ass_state.</p> ",
    "group": "Blob",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "<p>str</p> ",
            "optional": false,
            "field": "c1ass_state",
            "description": "<p>The class state [auto, trained] of the blob</p> "
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "<p>dict[]</p> ",
            "optional": false,
            "field": "blobs",
            "description": "<p>The list of blobs object</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>str</p> ",
            "optional": false,
            "field": "blobs.title",
            "description": "<p>The title of the blob</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>dict</p> ",
            "optional": false,
            "field": "blobs.bounds",
            "description": "<p>The bounding box of the blob</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>int</p> ",
            "optional": false,
            "field": "blobs.bounds.x",
            "description": "<p>The upper-left x coordinate</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>int</p> ",
            "optional": false,
            "field": "blobs.bounds.y",
            "description": "<p>The upper-left y coordinate</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>int</p> ",
            "optional": false,
            "field": "blobs.bounds.w",
            "description": "<p>The width dimension</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>int</p> ",
            "optional": false,
            "field": "blobs.bounds.h",
            "description": "<p>The height dimension</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>str</p> ",
            "optional": false,
            "field": "blobs.img_path",
            "description": "<p>The local relative path of the extracted blob image</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>str</p> ",
            "optional": false,
            "field": "blobs.img_url",
            "description": "<p>The local fully qualified url of the extracted blob image</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>str</p> ",
            "optional": false,
            "field": "blobs.img_url_ext",
            "description": "<p>The local fully qualified url of the externalized extracted blob image</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>str</p> ",
            "optional": false,
            "field": "blobs.c1ass",
            "description": "<p>The classification of the blob</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>str</p> ",
            "optional": false,
            "field": "blobs.c1ass_state",
            "description": "<p>The mode of classification of the blob</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>str</p> ",
            "optional": false,
            "field": "blobs.state",
            "description": "<p>The state [new, duplicate, removed] of the blob</p> "
          }
        ]
      }
    },
    "filename": "api/snack.py",
    "groupTitle": "Blob"
  },
  {
    "type": "get",
    "url": "/snacks/class/names",
    "title": "Get list of class names",
    "version": "1.0.0",
    "name": "GetClassNames",
    "description": "<p>This call returns a list of the possible class names that a blob can be classified by.</p> ",
    "group": "Blob",
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "<p>str[]</p> ",
            "optional": false,
            "field": "strs",
            "description": "<p>The list of class names</p> "
          }
        ]
      }
    },
    "filename": "api/snack.py",
    "groupTitle": "Blob"
  },
  {
    "type": "put",
    "url": "/snacks/state",
    "title": "Update blobs state info by _id",
    "version": "1.0.0",
    "name": "UpdateBlobStateClassStateById",
    "description": "<p>This call accepts a list of id, c1ass, c1ass_state objects and updates the associated blobs in the database.</p> ",
    "group": "Blob",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "<p>dict[]</p> ",
            "optional": false,
            "field": "dicts",
            "description": "<p>A custom list of objects</p> "
          },
          {
            "group": "Parameter",
            "type": "<p>str</p> ",
            "optional": false,
            "field": "dicts.id",
            "description": "<p>The database id of the blob</p> "
          },
          {
            "group": "Parameter",
            "type": "<p>str</p> ",
            "optional": false,
            "field": "dicts.c1ass",
            "description": "<p>The class of the blob</p> "
          },
          {
            "group": "Parameter",
            "type": "<p>str</p> ",
            "optional": false,
            "field": "dicts.c1ass_state",
            "description": "<p>The class state [auto, trained] of the blob</p> "
          }
        ]
      }
    },
    "filename": "api/snack.py",
    "groupTitle": "Blob"
  },
  {
    "type": "get",
    "url": "/snacks",
    "title": "Get all images",
    "version": "1.0.0",
    "name": "GetImage",
    "description": "<p>This call returns the list of images (max 10) in order of date_created DESC in BSON format.</p> ",
    "group": "Image",
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "<p>dict[]</p> ",
            "optional": false,
            "field": "images",
            "description": "<p>The list of image objects (max 10)</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>str</p> ",
            "optional": false,
            "field": "images.title",
            "description": "<p>The title of the image</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>str</p> ",
            "optional": false,
            "field": "images.date_created",
            "description": "<p>The date (ISO format) when the image was created</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>str</p> ",
            "optional": false,
            "field": "images.date_modified",
            "description": "<p>The date (ISO format) when the image was last modified</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>str</p> ",
            "optional": false,
            "field": "images.img_path",
            "description": "<p>The local relative path of the raw image</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>str</p> ",
            "optional": false,
            "field": "images.img_url",
            "description": "<p>The local fully qualified url of the raw image</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>str</p> ",
            "optional": false,
            "field": "images.img_url_ext",
            "description": "<p>The local fully qualified url of the externalized raw image</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>dict[]</p> ",
            "optional": false,
            "field": "images.transforms",
            "description": "<p>The list of transforms executed on this image</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>str</p> ",
            "optional": false,
            "field": "images.transforms.title",
            "description": "<p>The title of the transform</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>str</p> ",
            "optional": false,
            "field": "images.transforms.date_created",
            "description": "<p>The date (ISO format) when the transform was created</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>str</p> ",
            "optional": false,
            "field": "images.transforms.date_modified",
            "description": "<p>The date (ISO format) when the transform was last modified</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>str</p> ",
            "optional": false,
            "field": "images.transforms.img_path",
            "description": "<p>The local relative path of the generated transform image</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>str</p> ",
            "optional": false,
            "field": "images.transforms.img_url",
            "description": "<p>The local fully qualified url of the generated transform image</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>str</p> ",
            "optional": false,
            "field": "images.transforms.img_url_ext",
            "description": "<p>The local fully qualified url of the externalized generated transform image</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>dict[]</p> ",
            "optional": false,
            "field": "images.blobs",
            "description": "<p>The list of blobs identified in this image</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>str</p> ",
            "optional": false,
            "field": "images.blobs.title",
            "description": "<p>The title of the blob</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>dict</p> ",
            "optional": false,
            "field": "images.blobs.bounds",
            "description": "<p>The bounding box of the blob</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>int</p> ",
            "optional": false,
            "field": "images.blobs.bounds.x",
            "description": "<p>The upper-left x coordinate</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>int</p> ",
            "optional": false,
            "field": "images.blobs.bounds.y",
            "description": "<p>The upper-left y coordinate</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>int</p> ",
            "optional": false,
            "field": "images.blobs.bounds.w",
            "description": "<p>The width dimension</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>int</p> ",
            "optional": false,
            "field": "images.blobs.bounds.h",
            "description": "<p>The height dimension</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>str</p> ",
            "optional": false,
            "field": "images.blobs.img_path",
            "description": "<p>The local relative path of the extracted blob image</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>str</p> ",
            "optional": false,
            "field": "images.blobs.img_url",
            "description": "<p>The local fully qualified url of the extracted blob image</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>str</p> ",
            "optional": false,
            "field": "images.blobs.img_url_ext",
            "description": "<p>The local fully qualified url of the externalized extracted blob image</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>str</p> ",
            "optional": false,
            "field": "images.blobs.c1ass",
            "description": "<p>The classification of the blob</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>str</p> ",
            "optional": false,
            "field": "images.blobs.c1ass_state",
            "description": "<p>The mode of classification of the blob</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>str</p> ",
            "optional": false,
            "field": "images.blobs.state",
            "description": "<p>The state [new, duplicate, removed] of the blob</p> "
          }
        ]
      }
    },
    "filename": "api/snack.py",
    "groupTitle": "Image"
  },
  {
    "type": "get",
    "url": "/snacks/id/<id>",
    "title": "Get image by _id",
    "version": "1.0.0",
    "name": "GetImageById",
    "description": "<p>This call gets an image by the database id. If it is not found, null is returned.</p> ",
    "group": "Image",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "<p>int</p> ",
            "optional": false,
            "field": "id",
            "description": "<p>The database id of the image</p> "
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "<p>dict</p> ",
            "optional": false,
            "field": "image",
            "description": "<p>The image object</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>str</p> ",
            "optional": false,
            "field": "image.title",
            "description": "<p>The title of the image</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>str</p> ",
            "optional": false,
            "field": "image.date_created",
            "description": "<p>The date (ISO format) when the image was created</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>str</p> ",
            "optional": false,
            "field": "image.date_modified",
            "description": "<p>The date (ISO format) when the image was last modified</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>str</p> ",
            "optional": false,
            "field": "image.img_path",
            "description": "<p>The local relative path of the raw image</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>str</p> ",
            "optional": false,
            "field": "image.img_url",
            "description": "<p>The local fully qualified url of the raw image</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>str</p> ",
            "optional": false,
            "field": "image.img_url_ext",
            "description": "<p>The local fully qualified url of the externalized raw image</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>dict[]</p> ",
            "optional": false,
            "field": "image.transforms",
            "description": "<p>The list of transforms executed on this image</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>str</p> ",
            "optional": false,
            "field": "image.transforms.title",
            "description": "<p>The title of the transform</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>str</p> ",
            "optional": false,
            "field": "image.transforms.date_created",
            "description": "<p>The date (ISO format) when the transform was created</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>str</p> ",
            "optional": false,
            "field": "image.transforms.date_modified",
            "description": "<p>The date (ISO format) when the transform was last modified</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>str</p> ",
            "optional": false,
            "field": "image.transforms.img_path",
            "description": "<p>The local relative path of the generated transform image</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>str</p> ",
            "optional": false,
            "field": "image.transforms.img_url",
            "description": "<p>The local fully qualified url of the generated transform image</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>str</p> ",
            "optional": false,
            "field": "image.transforms.img_url_ext",
            "description": "<p>The local fully qualified url of the externalized generated transform image</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>dict[]</p> ",
            "optional": false,
            "field": "image.blobs",
            "description": "<p>The list of blobs identified in this image</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>str</p> ",
            "optional": false,
            "field": "image.blobs.title",
            "description": "<p>The title of the blob</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>dict</p> ",
            "optional": false,
            "field": "image.blobs.bounds",
            "description": "<p>The bounding box of the blob</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>int</p> ",
            "optional": false,
            "field": "image.blobs.bounds.x",
            "description": "<p>The upper-left x coordinate</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>int</p> ",
            "optional": false,
            "field": "image.blobs.bounds.y",
            "description": "<p>The upper-left y coordinate</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>int</p> ",
            "optional": false,
            "field": "image.blobs.bounds.w",
            "description": "<p>The width dimension</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>int</p> ",
            "optional": false,
            "field": "image.blobs.bounds.h",
            "description": "<p>The height dimension</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>str</p> ",
            "optional": false,
            "field": "image.blobs.img_path",
            "description": "<p>The local relative path of the extracted blob image</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>str</p> ",
            "optional": false,
            "field": "image.blobs.img_url",
            "description": "<p>The local fully qualified url of the extracted blob image</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>str</p> ",
            "optional": false,
            "field": "image.blobs.img_url_ext",
            "description": "<p>The local fully qualified url of the externalized extracted blob image</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>str</p> ",
            "optional": false,
            "field": "image.blobs.c1ass",
            "description": "<p>The classification of the blob</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>str</p> ",
            "optional": false,
            "field": "image.blobs.c1ass_state",
            "description": "<p>The mode of classification of the blob</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>str</p> ",
            "optional": false,
            "field": "image.blobs.state",
            "description": "<p>The state [new, duplicate, removed] of the blob</p> "
          }
        ]
      }
    },
    "filename": "api/snack.py",
    "groupTitle": "Image"
  },
  {
    "type": "get",
    "url": "/snacks/last",
    "title": "Get last image",
    "version": "1.0.0",
    "name": "GetLastImage",
    "description": "<p>This call returns the latest image by date_created DESC. If none exist, null is returned.</p> ",
    "group": "Image",
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "<p>dict</p> ",
            "optional": false,
            "field": "image",
            "description": "<p>The image object</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>str</p> ",
            "optional": false,
            "field": "image.title",
            "description": "<p>The title of the image</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>str</p> ",
            "optional": false,
            "field": "image.date_created",
            "description": "<p>The date (ISO format) when the image was created</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>str</p> ",
            "optional": false,
            "field": "image.date_modified",
            "description": "<p>The date (ISO format) when the image was last modified</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>str</p> ",
            "optional": false,
            "field": "image.img_path",
            "description": "<p>The local relative path of the raw image</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>str</p> ",
            "optional": false,
            "field": "image.img_url",
            "description": "<p>The local fully qualified url of the raw image</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>str</p> ",
            "optional": false,
            "field": "image.img_url_ext",
            "description": "<p>The local fully qualified url of the externalized raw image</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>dict[]</p> ",
            "optional": false,
            "field": "image.transforms",
            "description": "<p>The list of transforms executed on this image</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>str</p> ",
            "optional": false,
            "field": "image.transforms.title",
            "description": "<p>The title of the transform</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>str</p> ",
            "optional": false,
            "field": "image.transforms.date_created",
            "description": "<p>The date (ISO format) when the transform was created</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>str</p> ",
            "optional": false,
            "field": "image.transforms.date_modified",
            "description": "<p>The date (ISO format) when the transform was last modified</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>str</p> ",
            "optional": false,
            "field": "image.transforms.img_path",
            "description": "<p>The local relative path of the generated transform image</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>str</p> ",
            "optional": false,
            "field": "image.transforms.img_url",
            "description": "<p>The local fully qualified url of the generated transform image</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>str</p> ",
            "optional": false,
            "field": "image.transforms.img_url_ext",
            "description": "<p>The local fully qualified url of the externalized generated transform image</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>dict[]</p> ",
            "optional": false,
            "field": "image.blobs",
            "description": "<p>The list of blobs identified in this image</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>str</p> ",
            "optional": false,
            "field": "image.blobs.title",
            "description": "<p>The title of the blob</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>dict</p> ",
            "optional": false,
            "field": "image.blobs.bounds",
            "description": "<p>The bounding box of the blob</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>int</p> ",
            "optional": false,
            "field": "image.blobs.bounds.x",
            "description": "<p>The upper-left x coordinate</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>int</p> ",
            "optional": false,
            "field": "image.blobs.bounds.y",
            "description": "<p>The upper-left y coordinate</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>int</p> ",
            "optional": false,
            "field": "image.blobs.bounds.w",
            "description": "<p>The width dimension</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>int</p> ",
            "optional": false,
            "field": "image.blobs.bounds.h",
            "description": "<p>The height dimension</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>str</p> ",
            "optional": false,
            "field": "image.blobs.img_path",
            "description": "<p>The local relative path of the extracted blob image</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>str</p> ",
            "optional": false,
            "field": "image.blobs.img_url",
            "description": "<p>The local fully qualified url of the extracted blob image</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>str</p> ",
            "optional": false,
            "field": "image.blobs.img_url_ext",
            "description": "<p>The local fully qualified url of the externalized extracted blob image</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>str</p> ",
            "optional": false,
            "field": "image.blobs.c1ass",
            "description": "<p>The classification of the blob</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>str</p> ",
            "optional": false,
            "field": "image.blobs.c1ass_state",
            "description": "<p>The mode of classification of the blob</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>str</p> ",
            "optional": false,
            "field": "image.blobs.state",
            "description": "<p>The state [new, duplicate, removed] of the blob</p> "
          }
        ]
      }
    },
    "filename": "api/snack.py",
    "groupTitle": "Image"
  },
  {
    "type": "get",
    "url": "/snacks/last/<int:n>",
    "title": "Get last n images",
    "version": "1.0.0",
    "name": "GetLastNImages",
    "description": "<p>This call returns a list of the latest images by date_created DESC.</p> ",
    "group": "Image",
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "<p>dict[]</p> ",
            "optional": false,
            "field": "images",
            "description": "<p>The list of image objects (max 10)</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>str</p> ",
            "optional": false,
            "field": "images.title",
            "description": "<p>The title of the image</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>str</p> ",
            "optional": false,
            "field": "images.date_created",
            "description": "<p>The date (ISO format) when the image was created</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>str</p> ",
            "optional": false,
            "field": "images.date_modified",
            "description": "<p>The date (ISO format) when the image was last modified</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>str</p> ",
            "optional": false,
            "field": "images.img_path",
            "description": "<p>The local relative path of the raw image</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>str</p> ",
            "optional": false,
            "field": "images.img_url",
            "description": "<p>The local fully qualified url of the raw image</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>str</p> ",
            "optional": false,
            "field": "images.img_url_ext",
            "description": "<p>The local fully qualified url of the externalized raw image</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>dict[]</p> ",
            "optional": false,
            "field": "images.transforms",
            "description": "<p>The list of transforms executed on this image</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>str</p> ",
            "optional": false,
            "field": "images.transforms.title",
            "description": "<p>The title of the transform</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>str</p> ",
            "optional": false,
            "field": "images.transforms.date_created",
            "description": "<p>The date (ISO format) when the transform was created</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>str</p> ",
            "optional": false,
            "field": "images.transforms.date_modified",
            "description": "<p>The date (ISO format) when the transform was last modified</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>str</p> ",
            "optional": false,
            "field": "images.transforms.img_path",
            "description": "<p>The local relative path of the generated transform image</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>str</p> ",
            "optional": false,
            "field": "images.transforms.img_url",
            "description": "<p>The local fully qualified url of the generated transform image</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>str</p> ",
            "optional": false,
            "field": "images.transforms.img_url_ext",
            "description": "<p>The local fully qualified url of the externalized generated transform image</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>dict[]</p> ",
            "optional": false,
            "field": "images.blobs",
            "description": "<p>The list of blobs identified in this image</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>str</p> ",
            "optional": false,
            "field": "images.blobs.title",
            "description": "<p>The title of the blob</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>dict</p> ",
            "optional": false,
            "field": "images.blobs.bounds",
            "description": "<p>The bounding box of the blob</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>int</p> ",
            "optional": false,
            "field": "images.blobs.bounds.x",
            "description": "<p>The upper-left x coordinate</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>int</p> ",
            "optional": false,
            "field": "images.blobs.bounds.y",
            "description": "<p>The upper-left y coordinate</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>int</p> ",
            "optional": false,
            "field": "images.blobs.bounds.w",
            "description": "<p>The width dimension</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>int</p> ",
            "optional": false,
            "field": "images.blobs.bounds.h",
            "description": "<p>The height dimension</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>str</p> ",
            "optional": false,
            "field": "images.blobs.img_path",
            "description": "<p>The local relative path of the extracted blob image</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>str</p> ",
            "optional": false,
            "field": "images.blobs.img_url",
            "description": "<p>The local fully qualified url of the extracted blob image</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>str</p> ",
            "optional": false,
            "field": "images.blobs.img_url_ext",
            "description": "<p>The local fully qualified url of the externalized extracted blob image</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>str</p> ",
            "optional": false,
            "field": "images.blobs.c1ass",
            "description": "<p>The classification of the blob</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>str</p> ",
            "optional": false,
            "field": "images.blobs.c1ass_state",
            "description": "<p>The mode of classification of the blob</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>str</p> ",
            "optional": false,
            "field": "images.blobs.state",
            "description": "<p>The state [new, duplicate, removed] of the blob</p> "
          }
        ]
      }
    },
    "filename": "api/snack.py",
    "groupTitle": "Image"
  },
  {
    "type": "get",
    "url": "/snacks/snap",
    "title": "Snap and get image",
    "version": "1.0.0",
    "name": "SnapImage",
    "description": "<p>This call takes a snapshot and then processes and returns the generated image.</p> ",
    "group": "Image",
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "<p>dict</p> ",
            "optional": false,
            "field": "image",
            "description": "<p>The image object</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>str</p> ",
            "optional": false,
            "field": "image.title",
            "description": "<p>The title of the image</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>str</p> ",
            "optional": false,
            "field": "image.date_created",
            "description": "<p>The date (ISO format) when the image was created</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>str</p> ",
            "optional": false,
            "field": "image.date_modified",
            "description": "<p>The date (ISO format) when the image was last modified</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>str</p> ",
            "optional": false,
            "field": "image.img_path",
            "description": "<p>The local relative path of the raw image</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>str</p> ",
            "optional": false,
            "field": "image.img_url",
            "description": "<p>The local fully qualified url of the raw image</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>str</p> ",
            "optional": false,
            "field": "image.img_url_ext",
            "description": "<p>The local fully qualified url of the externalized raw image</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>dict[]</p> ",
            "optional": false,
            "field": "image.transforms",
            "description": "<p>The list of transforms executed on this image</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>str</p> ",
            "optional": false,
            "field": "image.transforms.title",
            "description": "<p>The title of the transform</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>str</p> ",
            "optional": false,
            "field": "image.transforms.date_created",
            "description": "<p>The date (ISO format) when the transform was created</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>str</p> ",
            "optional": false,
            "field": "image.transforms.date_modified",
            "description": "<p>The date (ISO format) when the transform was last modified</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>str</p> ",
            "optional": false,
            "field": "image.transforms.img_path",
            "description": "<p>The local relative path of the generated transform image</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>str</p> ",
            "optional": false,
            "field": "image.transforms.img_url",
            "description": "<p>The local fully qualified url of the generated transform image</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>str</p> ",
            "optional": false,
            "field": "image.transforms.img_url_ext",
            "description": "<p>The local fully qualified url of the externalized generated transform image</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>dict[]</p> ",
            "optional": false,
            "field": "image.blobs",
            "description": "<p>The list of blobs identified in this image</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>str</p> ",
            "optional": false,
            "field": "image.blobs.title",
            "description": "<p>The title of the blob</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>dict</p> ",
            "optional": false,
            "field": "image.blobs.bounds",
            "description": "<p>The bounding box of the blob</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>int</p> ",
            "optional": false,
            "field": "image.blobs.bounds.x",
            "description": "<p>The upper-left x coordinate</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>int</p> ",
            "optional": false,
            "field": "image.blobs.bounds.y",
            "description": "<p>The upper-left y coordinate</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>int</p> ",
            "optional": false,
            "field": "image.blobs.bounds.w",
            "description": "<p>The width dimension</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>int</p> ",
            "optional": false,
            "field": "image.blobs.bounds.h",
            "description": "<p>The height dimension</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>str</p> ",
            "optional": false,
            "field": "image.blobs.img_path",
            "description": "<p>The local relative path of the extracted blob image</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>str</p> ",
            "optional": false,
            "field": "image.blobs.img_url",
            "description": "<p>The local fully qualified url of the extracted blob image</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>str</p> ",
            "optional": false,
            "field": "image.blobs.img_url_ext",
            "description": "<p>The local fully qualified url of the externalized extracted blob image</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>str</p> ",
            "optional": false,
            "field": "image.blobs.c1ass",
            "description": "<p>The classification of the blob</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>str</p> ",
            "optional": false,
            "field": "image.blobs.c1ass_state",
            "description": "<p>The mode of classification of the blob</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>str</p> ",
            "optional": false,
            "field": "image.blobs.state",
            "description": "<p>The state [new, duplicate, removed] of the blob</p> "
          }
        ]
      }
    },
    "filename": "api/snack.py",
    "groupTitle": "Image"
  },
  {
    "type": "get",
    "url": "/snacks/last/summary",
    "title": "Get latest summary",
    "version": "1.0.0",
    "name": "GetLastSummary",
    "description": "<p>This call returns a summary of the latest processed images including the new, duplicate and removed blobs. If no images exist, it returns null.</p> ",
    "group": "Summary",
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "<p>dict</p> ",
            "optional": false,
            "field": "dict",
            "description": "<p>The summary</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>str</p> ",
            "optional": false,
            "field": "dict.image_id",
            "description": "<p>The database id of the last image</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>str</p> ",
            "optional": false,
            "field": "dict.img_marked_url",
            "description": "<p>The local fully qualified url of the marked image</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>str</p> ",
            "optional": false,
            "field": "dict.img_marked_url_ext",
            "description": "<p>The local fully qualified url of the externalized marked image</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>int</p> ",
            "optional": false,
            "field": "dict.blob_count_new",
            "description": "<p>The number of new blobs identified</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>int</p> ",
            "optional": false,
            "field": "dict.blob_count_duplicate",
            "description": "<p>The number of duplicate blobs identified</p> "
          },
          {
            "group": "Success 200",
            "type": "<p>int</p> ",
            "optional": false,
            "field": "dict.blob_count_removed",
            "description": "<p>The number of removed blobs identified</p> "
          }
        ]
      }
    },
    "filename": "api/snack.py",
    "groupTitle": "Summary"
  }
] });