/*
recording-ui.js

Javascript Module for Recording UI


Latest Update:  26 September 2019

Author:         John Poncini
Title:          Video and Informatics Systems Associate
License:        GPLv2

Copyright 2019 MAPS Public Benefit Corporation
*/

function startTime() {
    var today = new Date();
    var h = today.getHours();
    var m = today.getMinutes();
    var s = today.getSeconds();
    m = checkTime(m);
    s = checkTime(s);
};
function checkTime(i) {
    if (i < 10) {i = "0" + i}; 
    return i;
};
function upTime(countTo) {
    now = new Date();
    countTo = new Date(countTo);
    diff = (now-countTo);

    hours = Math.floor((diff%(60*60*1000*24))/(60*60*1000)*1);
    mins = Math.floor(((diff%(60*60*1000*24))%(60*60*1000))/(60*1000)*1);
    secs = Math.floor((((diff%(60*60*1000*24))%(60*60*1000))%(60*1000))/1000*1);

    hours = checkTime(hours);
    mins = checkTime(mins);
    secs = checkTime(secs);

    document.getElementById('elapsed_time').innerHTML = 
        hours + ":" + mins + ":" + secs;

    clearTimeout(upTime.to);
    upTime.to=setTimeout(function(){ upTime(countTo); },1000);
};

function pause() {
    document.getElementById("main_stop_button").style.display = "none";
    document.getElementById("pause_button").style.display = "none";
    document.getElementById("resume_button").style.display = "inline";
    document.getElementById("aux_stop_button").style.display = "inline";
    document.getElementById("recording_circle").style.display = "none";
    document.getElementById("recording_state").innerHTML = "PAUSED";
    $.get("/pause_recording");
    clearTimeout(upTime.to);
};

function resume() {
    document.getElementById("main_stop_button").style.display = "inline";
    document.getElementById("pause_button").style.display = "inline";
    document.getElementById("resume_button").style.display = "none";
    document.getElementById("aux_stop_button").style.display = "none";
    document.getElementById("recording_circle").style.display = "inline";
    document.getElementById("recording_state").innerHTML = "IN PROGRESS";
    $.get("/resume_recording");
    upTime(Date())
}
