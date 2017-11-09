

var audio, playbtn, mutebtn, seekslider, volumeslider, seeking=false, seekto, mousemoving=false;
var req = new XMLHttpRequest();
function initAudioPlayer(){
	audio = new Audio();
	audio.src = "static/Stoker.mp3";
	audio.loop = true;
	//audio.addEventListener("ontimeupdate",setseektime)
	//audio.ontimeupdate=function(){setseektime()};
	audio.play();
	// Set object references
	playbtn = document.getElementById("playpausebtn");
	mutebtn = document.getElementById("mutebtn");
	seekslider = document.getElementById("seekslider");
	volumeslider = document.getElementById("volumeslider");
	
	// Add Event Handling
	var timer = setInterval(setseektime,1000);
	playbtn.addEventListener("click",playPause);
	mutebtn.addEventListener("click", mute);
	seekslider.addEventListener("mousedown", function(event){ seeking=true; seek(event); });
	seekslider.addEventListener("mousemove", function(event){ seek(event); });
	seekslider.addEventListener("mouseup",function(){ seeking=false; });
	volumeslider.addEventListener("mousemove", setvolume);
	// Functions
	function setseektime(){
		if(seeking == false){seekslider.value=(audio.currentTime/audio.duration) * 200;
		console.log("Seeked to : " + ((audio.currentTime/audio.duration) * 100))}
		//var timer = setTimeout(setseektime,1000);
	}
	function playPause(){
		if(audio.paused){
		    audio.play();
		    
		    req.open("POST","/play",true);
		    req.send()
		    console.log(req.responseText);
		    playbtn.style.background = "static/images/lplay.jpg no-repeat";
	    } else {
		    audio.pause();
		    playbtn.style.background = "static/images/pause.png no-repeat";
	    }
	    console.log("PlayPause called")
	}
	function mute(){
		if(audio.muted){
		    audio.muted = false;
		    mutebtn.style.background = "static/images/speaker.png no-repeat";
	    } else {
		    audio.muted = true;
		    mutebtn.style.background = "static/images/speaker_muted.png no-repeat";
	    }
	    console.log("Mute Called")
	}
	function seek(event){
	    if(seeking){
		    seekslider.value = event.clientX - seekslider.offsetLeft;
	        seekto = audio.duration * (seekslider.value / 200);
	        audio.currentTime = seekto;
	        //setInterval(setseektime,1000);
	    }
	    console.log("Seeked value " + seekslider.value);
    }
	function setvolume(){
	    audio.volume = volumeslider.value / 100;
    }
}
window.addEventListener("load", initAudioPlayer);
