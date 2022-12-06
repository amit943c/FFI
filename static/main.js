const { S3Client, PutObjectCommand, ListObjectsCommand, DeleteObjectCommand, DeleteObjectsCommand } = require(['@aws-sdk/client-s3'], result => '@aws-sdk/client-s3' = result);
var AWS = require('aws-sdk');

var albumBucketName = "new-test-bkt-1";
var bucketRegion = "us-west-2";
var IdentityPoolId = 'us-west-2:2626660f-6389-4994-8771-7f99f6b62a71';

// Initialize the Amazon Cognito credentials provider
AWS.config.region = bucketRegion; // Region
AWS.config.credentials = new AWS.CognitoIdentityCredentials({
    IdentityPoolId: IdentityPoolId,
});

var s3 = new AWS.S3({
  apiVersion: "2006-03-01",
  params: { Bucket: albumBucketName }
});


function func() {
return ( ( ( 1+Math.random() ) * 0x10000 ) | 0 ).toString( 16 ).substring( 1 );
}
// For calling it, stitch '3' in the 3rd group
function create_uuid() {
  UUID = (func() + func() + "-" + func() + "-3" + func().substr(0,2) + "-" + func() + "-" + func() + func() + func()).toLowerCase();
  return UUID
}

function addPhoto() {
  albumName = 'camera_pics'
  var files = document.getElementById("img_file").files;
  if (!files.length) {
    return
     // alert("Please choose a file to upload first.");
  }
  var file = files[0];
  uuid = create_uuid()
  var fileName = uuid + file.name;
  var albumPhotosKey = encodeURIComponent(albumName) + "/";

  var photoKey = albumPhotosKey + fileName;

  // Use S3 ManagedUpload class as it supports multipart uploads
  var upload = new AWS.S3.ManagedUpload({
    params: {
      Bucket: albumBucketName,
      Key: photoKey,
      Body: file
    }
  });

  var promise = upload.promise();

  promise.then(
    function(data) {
      // alert("Successfully uploaded photo.");
      // viewAlbum(albumName);
      return fileName
    },
    function(err) {
      return ""
      // alert("There was an error uploading your photo: ", err.message);
    }
  );
}