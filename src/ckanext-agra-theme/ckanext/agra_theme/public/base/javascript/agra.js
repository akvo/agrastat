// if landing page .masthead backgroun should be transparent
if (window.location.pathname === "/") {
  const header = document.querySelector(".masthead");
  const navLinks = document.querySelectorAll(".masthead .nav > li > a");
  header.style.backgroundColor = "transparent";
  navLinks.forEach((link) => {
    link.style.color = "white";
  });
}
