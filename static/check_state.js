time=setInterval(function(){
    $.get("http://127.0.0.1:5000/state", function(data) {
        var split_string = data.split(":");
        var state = split_string[0];
        console.log("Current state: " + split_string);
        if (state == "request") {
            var requested_file = split_string[1];
            // console.log("Requested file: " + requested_file);
						$("#content").empty();
						requested_file = "/static/assets/" + requested_file;
						// console.log(requested_file);
						// If it is Audio...
						if ((requested_file.search(".wav") != -1) || (requested_file.search(".mp3") != -1)) {
								// Hide the visual
								$("#overlayImage").attr("width", "0%");
								$("#overlayImage").attr("height", "0%");
								var currentAudio = $("#overlayAudio");
								currentAudio.attr("src", requested_file);
								currentAudio.get(0).play();
								// Bind and event to it to end it after it finishes
								currentAudio.bind("ended", function() {
										console.log("Song finished! Resetting state");
										$.get("http://127.0.0.1:5000/reset_state")  ;
								});
						} else if (requested_file.search(".gif") != -1) {
								// Show the gif
								$("#overlayImage").attr("width", "100%");
								$("#overlayImage").attr("height", "100%");
								// If gif
								$("#overlayImage").attr("src", requested_file);
						} else {
								// Set the video src

						}
						$("#content").append(requested_file);
        }  else {
            $("#content").empty();
        }
    });
}, 2000);