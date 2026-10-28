const reduceMotion = matchMedia("(prefers-reduced-motion: reduce)").matches;

// Safari tints the status bar from a fixed element at the top; hand it back once the aurora has scrolled away.
const tint = document.querySelector(".tint");
if (tint) {
  const update = () => tint.classList.toggle("off", scrollY > 320);
  addEventListener("scroll", update, { passive: true });
  update();
}

if (!reduceMotion && "IntersectionObserver" in window) {
  const observer = new IntersectionObserver((entries) => {
    for (const entry of entries) {
      if (!entry.isIntersecting) continue;
      entry.target.classList.remove("pending");
      observer.unobserve(entry.target);
    }
  }, { rootMargin: "0px 0px -6% 0px" });
  for (const el of document.querySelectorAll(".rise")) {
    if (el.getBoundingClientRect().top < innerHeight) continue;
    el.classList.add("pending");
    observer.observe(el);
  }
}

if (matchMedia("(hover: hover) and (prefers-reduced-motion: no-preference)").matches) {
  for (const tile of document.querySelectorAll(".tilt")) {
    tile.addEventListener("pointermove", (event) => {
      const box = tile.getBoundingClientRect();
      tile.style.setProperty("--ry", `${((event.clientX - box.left) / box.width - 0.5) * 7}deg`);
      tile.style.setProperty("--rx", `${(0.5 - (event.clientY - box.top) / box.height) * 7}deg`);
    }, { passive: true });
    tile.addEventListener("pointerleave", () => {
      tile.style.removeProperty("--rx");
      tile.style.removeProperty("--ry");
    });
  }
}

const rotator = document.querySelector(".rotator");
if (rotator && !reduceMotion) {
  const words = [...rotator.children];
  let word = 0;
  setInterval(() => {
    const previous = words[word];
    word = (word + 1) % words.length;
    previous.classList.replace("on", "out");
    words[word].classList.remove("out");
    words[word].classList.add("on");
    setTimeout(() => previous.classList.remove("out"), 500);
  }, 2400);
}
