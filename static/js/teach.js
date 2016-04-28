var TeachingPage = {};

TeachingPage.snackClassList = 0;
TeachingPage.snackBlobs = 0;
TeachingPage.isInitialized = false;

TeachingPage.initialize = function() {
  //make AJAX calls for our data.
  jQuery.get('../api/snacks/class/names', function(data) {
    console.log('GOT THE DATA!\n' + JSON.stringify(data, null, 4));
    TeachingPage.snackClassList = data;
  });
  jQuery.get('../api/snacks/state/auto', function(data) {
    console.log('GOT THE DATA!\n' + JSON.stringify(data, null, 4));
    TeachingPage.snackBlobs = data;
  });
}

TeachingPage.reloadSnacks = function() {
  return 0;
}

TeachingPage.renderSnacks = function() {
  for(var p = 0; p < TeachingPage.snackBlobs.length; p++) {
    var currentBlob = TeachingPage.snackBlobs[p];
    var htmlForImage = this.getHtmlForImage(currentBlob["img_path"], currentBlob["uid"]["$oid"]);
    $('#image-classification-row').append(htmlForImage);
  }
}

TeachingPage.getHtmlForImage = function(imgSource, imgId) {
// Returns HTML for an image in the query.
	var htmlString = "<div class=\"teaching-group col-xs-6 col-sm-4\">" +
                "<img src=\"http://" + window.location.host + "/" + imgSource + "\" class=\"teaching-img-thumb img-responsive\" title=\"Delicious snack image\">" +
		"<select class=\"teaching-dropdown\">";

	for(var i = 0; i < this.snackClassList.length; i++) {
		htmlString += "<option>"+ this.snackClassList[i] +"</option>";
	}
        htmlString += "</select>" +
                "<input type=\"hidden\" class=\"teaching-blob-uid\" value=\"" + imgId + "\"/>" +
                "<button type=\"button\" class=\"btn btn-primary teaching-button-confirm\">Submit</button>" +
            "</div>";
    return htmlString;
}

TeachingPage.submitImage = function(teachingGroup, blobUID, imageClass) {
  var putData = [
    {
      uid: blobUID,
      c1ass: imageClass,
      c1ass_state: 'trained'
    }
  ];

  console.log('attempting to send data...' + JSON.stringify(putData, null, 4));

  $.ajax({
    url: '../api/snacks/state',
    type: 'PUT',
    contentType: 'application/json',
    data: JSON.stringify(putData),
    success: function(result) {
      console.log('WE PUT THE DATA!');
    },
    complete: function(jqXHR, textStatus) {
      console.log('AJAX COMPLETE!');
    },
    beforeSend: function(jqXHR, settings) {
      console.log('AJAX BEFORE SENDING!');
    }
  });
}

$(document).ready(function() {
  console.log('host: ' + window.location.host);
  console.log('href: ' + window.location.href);

  TeachingPage.initialize();

  $('#reload-images-button').click(function() {
    // reload page for now.
    // Switch to an AJAX call if necessary
    document.location.reload();
  });
});

$(document).ajaxStop(function(event, xhr, settings) {
  console.log('AJAX requests complete!');
  if(TeachingPage.isInitialized == false) {
    TeachingPage.renderSnacks();

    $('.teaching-button-confirm').click(function() {
      console.log('teaching button clicked!');
      var teachingGroup = $(this).closest('.teaching-group');
      var blobUID = $(this).siblings('.teaching-blob-uid').val();
      var imageClass = $(this).siblings('.teaching-dropdown').val();
      var imageUrl = $(this).siblings('.teaching-img-thumb').attr('src');
      var host = 'http://' + window.location.host + '/';

      //JSON call to assign a class to that image.
      TeachingPage.submitImage(teachingGroup, blobUID, imageClass);

      teachingGroup.fadeOut();
    });
  }

  TeachingPage.isInitialized = true;
});
