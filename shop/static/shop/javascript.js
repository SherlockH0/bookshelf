// MOBILE FRIENDLY MENU

const menuLinks = document.querySelector(".navbar__links");
const menuToggle = document.querySelector(".navbar__menu-toggle");
const highlight = document.querySelector(".mobile-highlight");
const dropdowns = document.querySelectorAll(".dropdown");

console.log(highlight);

menuToggle.addEventListener("click", (e) => {
  const visibility = menuLinks.getAttribute("data-visible");

  if (visibility === "false") {
    menuLinks.setAttribute("data-visible", true);
    highlight.setAttribute("data-visible", true);
  } else if (visibility === "true") {
    menuLinks.setAttribute("data-visible", false);
    dropdowns.forEach((el) => {el.removeAttribute("open")});
    highlight.setAttribute("closing", '');

    highlight.addEventListener("animationend", () => {
      highlight.removeAttribute("closing");
      highlight.setAttribute("data-visible", false);
    }, {once: true});
  }

});

highlight.addEventListener("click", (e) => {
  const visibility = menuLinks.getAttribute("data-visible");

  if (visibility === "true") {
    dropdowns.forEach((el) => {el.removeAttribute("open")});
    menuLinks.setAttribute("data-visible", false);
    highlight.setAttribute("closing", '');

    highlight.addEventListener("animationend", () => {
      highlight.removeAttribute("closing");
      highlight.setAttribute("data-visible", false);
    }, {once: true});
  }
});
