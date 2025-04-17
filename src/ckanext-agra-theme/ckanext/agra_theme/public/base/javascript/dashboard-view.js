const iframe = document.getElementById("view-iframe");
iframe.onload = () => {
  iframe.style.height = iframe.contentWindow.document.body.scrollHeight + "px";
};
