// MOBILE FRIENDLY MENU

const menuLinks = document.querySelector(".navbar__links");
const menuToggle = document.querySelector(".navbar__menu-toggle");
const highlight = document.querySelector(".mobile-highlight");
const dropdowns = document.querySelectorAll(".dropdown");

function close() {
  menuLinks.setAttribute("data-visible", false);
  dropdowns.forEach((el) => {el.removeAttribute("open")});
  highlight.setAttribute("closing", '');

  highlight.addEventListener("animationend", () => {
    highlight.removeAttribute("closing");
    highlight.setAttribute("data-visible", false);
  }, {once: true});
}

function open() {
  menuLinks.setAttribute("data-visible", true);
  highlight.setAttribute("data-visible", true);
}

menuToggle.addEventListener("click", (e) => {
  const visibility = menuLinks.getAttribute("data-visible");

  if (visibility === "false") open()
  else if (visibility === "true") close()

});

highlight.addEventListener("click", (e) => {
  const visibility = menuLinks.getAttribute("data-visible");

  if (visibility === "true") close()
});
