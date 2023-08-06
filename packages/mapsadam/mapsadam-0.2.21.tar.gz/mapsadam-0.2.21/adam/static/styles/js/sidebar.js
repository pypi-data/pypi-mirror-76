/*
sidebar.js

Javascript Module for Displaying the Sidebar


Latest Update:  26 September 2019

Author:         John Poncini
Title:          Video and Informatics Systems Associate
License:        GPLv2

Copyright 2019 MAPS Public Benefit Corporation
*/

var state = "closed";

function open() {
    state = "open";
    document.getElementById("menu").style.width = "250px";
    document.getElementById("menu").style.transition = "0s";
    document.getElementById("main").style.marginLeft = "250px";
    document.getElementById("main").style.transition = "0s";
    document.getElementById("collapse-btn").style.marginLeft = "-60px";
    document.getElementById("collapse-btn").style.backgroundColor = "rgb(17, 17, 17)";
    document.getElementById("collapse-btn").style.transition = "0s";
}

/* Set the width of the sidebar to 250px and the left margin of the page content to 250px */
function toggle() {

  if (state == "closed") {
    document.getElementById("menu").style.width = "250px";

    document.getElementById("main").style.marginLeft = "250px";

    document.getElementById("collapse-btn").style.marginLeft = "-60px";
    document.getElementById("collapse-btn").style.backgroundColor = "rgb(17, 17, 17)";

    state = "open";
    $("#collapse-btn").hover(function(){
      $(this).css("background-color", "#9dcfff");
      }, function(){
      $(this).css("background-color", "#111");
      }
    );
    $.get("/toggle_sidebar", {
      state: state
      }
    );        
  }
  else {
    document.getElementById("menu").style.width = "0";
    document.getElementById("menu").style.transition = "0.5s";
    document.getElementById("main").style.marginLeft = "0";
    document.getElementById("main").style.transition = "0.5s";
    document.getElementById("collapse-btn").style.marginLeft = "20px";
    document.getElementById("collapse-btn").style.backgroundColor = "rgb(0, 30, 59)";
    document.getElementById("collapse-btn").style.transition = "0.3s";
    state = "closed";
    $("#collapse-btn").hover(function(){
      $(this).css("background-color", "#9dcfff");
      }, function(){
      $(this).css("background-color", "#001e3b");
      }
    );
    $.get("/toggle_sidebar", {
      state: state
      }
    );
  }
}

$("#collapse-btn").hover(function(){
  $(this).css("background-color", "#9dcfff");
  }
);
