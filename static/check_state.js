var tick_delay = 1000;

image_types = [".png", ".jpg"];
audio_types = [".wav", ".mp3", ".ogg"];
video_types = [".mp4"];

time = setInterval(function(){
    $.get("http://127.0.0.1:5000/state", function(data) {
        var split_string = data.split(":");
        var state = split_string[0];
        console.log("Current state: " + split_string);
        if (state == "request") {
            var requested_file = split_string[1];
            var file_format = requested_file.split(".")[requested_file.split(".").length - 1];
            var file_timeout = split_string[2] * 1000;
            // Set the state to busy
            $.get("http://127.0.0.1:5000/set_busy_state");
						$("#content").empty();
						requested_file = "/static/assets/" + requested_file;
						$("#content").append(requested_file);
						// Determine if it is audio, a gif, an image or a video
						var is_audio = (audio_types.indexOf(file_format) > -1);
						var is_image = (image_types.indexOf(file_format) > -1);
						var is_video = (video_types.indexOf(file_format) > -1);
						var is_gif = (file_format.indexOf(".gif") > -1);
						// Act according to the file type
						if (is_audio) {
								// Hide the visual
								$("#overlayImage").attr("width", "0%");
								var currentAudio = $("#overlayAudio");
								currentAudio.attr("src", requested_file);
								currentAudio.get(0).play();
								// Bind and event to it to end it after it finishes
								currentAudio.bind("ended", function() {
										console.log("Song finished.");
										// Reset the state to ready
										$.get("http://127.0.0.1:5000/reset_state");
								});
						} else if (is_gif) {
								// Stopping the interval first
								//clearInterval(time);
								// Show the gif
								$("#overlayImage").attr("width", "100%");
								// If gif
								$("#overlayImage").attr("src", requested_file);
								setTimeout(function() {
										console.log("Timeout for " + requested_file + " of " + file_timeout + "ms finished.");
										$("#overlayImage").attr("src", "");
										$("#overlayImage").attr("width", "0%");
										// Reset the state to ready
										$.get("http://127.0.0.1:5000/reset_state");
								}, file_timeout);
						} else if (is_image) {
								// TODO: Fill in for image files
						} else if (is_video) {
								// TODO: Fill in for video files
						} else {
								console.log("ERROR: Unrecognized file type or could not determine file type");
						}
        } else {
            // If the  request state is not for a new request, just clear the content.
            $("#content").empty();
        }
    });
}, tick_delay);