window.addEventListener("load", () => {

  /* --- List Hierarchy management --- */

  for (let list of document.querySelectorAll(".concept-list ul li ul")) {
    let tog = document.createElement("div");
    tog.innerHTML = list.previousSibling.textContent;
    tog.className = "toggle";
    tog.onclick = () => tog.classList.toggle("show");
    list.parentElement.removeChild(list.previousSibling);
    list.parentElement.insertBefore(tog, list);
  }

  for (let list of document.querySelectorAll(".list-hierarchy")) {

    // do not place btn controls for lists that aren't nested
    // more than 3 levels deep
    if(list.querySelector("li ul li ul") == null) { continue; }

    let btn_expand = document.createElement("button");
    btn_expand.innerHTML = "expand all";
    btn_expand.className = "btn-expand";
    btn_expand.onclick = () => {
      for (let div of list.getElementsByTagName("div")) {
        if (div.classList.contains("show")) { }
        else { div.classList.add("show"); }
      }
    };

    let btn_collapse = document.createElement("button");
    btn_collapse.innerHTML = "collapse all";
    btn_collapse.className = "btn-collapse";
    btn_collapse.onclick = () => {
      for (let div of list.getElementsByTagName("div")) {
        if (div.classList.contains("show")) { div.classList.remove("show"); }
        else { }
      }
    };
    let btn_div = document.createElement("div");
    btn_div.className = "btn-hierarchy";
    btn_div.appendChild(btn_expand);
    btn_div.appendChild(btn_collapse);
    list.insertBefore(btn_div, list.firstChild);
  }

  /* if term is defined on page - use local links, else - IRI (default) */
  for(let item of document.querySelectorAll('.local-link')) {
    let ref = item.href.split('#')[1];
    if(document.getElementById(ref)) {
      item.href = '#' + ref;
    }
  }
});