document.addEventListener('DOMContentLoaded', () => {
  if (!localStorage.getItem('lasttab')){
    localStorage.setItem('lasttab','Pizza');
    console.log("reset")
  }
  const food = localStorage.getItem('lasttab');
  choose_tab(food);
  document.querySelectorAll(".tablink").forEach(btn => {
    if (btn.innerHTML != food) {
      btn.className = btn.className.replace(" active","");
    }
    else {
      btn.className += " active";
    }
  });
  document.querySelectorAll(".tablink").forEach(link => {
    link.onclick = () => {
      const food = link.innerHTML;
      choose_tab(food);
      localStorage.setItem('lasttab',food);
      document.querySelectorAll(".tablink").forEach(btn => {
        if (btn.innerHTML != food) {
          btn.className = btn.className.replace(" active","");
        }
      })
      link.className += " active";
    }
  })
})

function choose_tab(food){
  document.querySelectorAll(".Menucontent").forEach(
    content => {
      if (content.id != food) {
        content.style.display = "none";
      }
      else {
        content.style.display = "block";
      }
    }
  )
}
