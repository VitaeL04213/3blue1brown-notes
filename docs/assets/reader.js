"use strict";
document.querySelectorAll(".load-video").forEach(button => {
  button.addEventListener("click", () => {
    const id = button.dataset.video;
    if (!/^[A-Za-z0-9_-]{11}$/.test(id)) return;
    const frame = document.createElement("iframe");
    frame.src = "https://www.youtube-nocookie.com/embed/" + id + "?rel=0";
    frame.title = "3Blue1Brown 原课程视频";
    frame.allow = "accelerometer; encrypted-media; gyroscope; picture-in-picture; fullscreen";
    frame.allowFullscreen = true;
    frame.referrerPolicy = "strict-origin-when-cross-origin";
    button.parentElement.querySelector(".embed-slot").replaceChildren(frame);
    button.remove();
  });
});
