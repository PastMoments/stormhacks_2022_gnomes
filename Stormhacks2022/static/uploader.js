console.log("loaded")

var dragHandler = function(evt){
    evt.preventDefault();
};

var dropHandler = function(evt){
    evt.preventDefault();
    var files = evt.dataTransfer.files;

    var formData = new FormData();
    formData.append("file", files[0]);

    document.getElementById("filename").innerHTML = files[0].name;
    var req = {
        url: "/uploader",
        method: "post",
        processData: false,
        contentType: false,
        data: formData
    };

    var promise = $.ajax(req);
};
