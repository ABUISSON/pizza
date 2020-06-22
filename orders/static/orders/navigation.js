document.addEventListener('DOMContentLoaded', () => {
  choose_tab("Pizza")
  document.querySelectorAll(".tablink").forEach(link => {
    link.onclick = () => {
      const food = link.innerHTML;
      choose_tab(food);
      document.querySelectorAll(".tablink").forEach(btn => {
        if (btn != link) {
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
