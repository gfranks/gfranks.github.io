if (matchMedia("(hover: hover) and (prefers-reduced-motion: no-preference)").matches) {
  for (const card of document.querySelectorAll(".app")) {
    card.addEventListener("pointermove", (event) => {
      const box = card.getBoundingClientRect();
      const x = (event.clientX - box.left) / box.width;
      const y = (event.clientY - box.top) / box.height;
      card.style.setProperty("--mx", `${x * 100}%`);
      card.style.setProperty("--my", `${y * 100}%`);
      card.style.setProperty("--ry", `${(x - 0.5) * 16}deg`);
      card.style.setProperty("--rx", `${(0.5 - y) * 16}deg`);
    });
    card.addEventListener("pointerleave", () => {
      card.style.setProperty("--rx", "0deg");
      card.style.setProperty("--ry", "0deg");
    });
  }
}

const rotator = document.querySelector(".rotator");
if (rotator && matchMedia("(prefers-reduced-motion: no-preference)").matches) {
  const words = [...rotator.children];
  let current = 0;
  setInterval(() => {
    const previous = words[current];
    current = (current + 1) % words.length;
    previous.classList.replace("on", "out");
    words[current].classList.remove("out");
    words[current].classList.add("on");
    setTimeout(() => previous.classList.remove("out"), 500);
  }, 2400);
}

if (matchMedia("(prefers-reduced-motion: reduce)").matches) {
  for (const clip of document.querySelectorAll("video[autoplay]")) {
    clip.removeAttribute("autoplay");
    clip.pause();
    clip.currentTime = 0;
  }
}
