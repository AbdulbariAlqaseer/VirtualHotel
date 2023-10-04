const menuBtn = document.querySelector('.menu-btn');
const btn = document.querySelector('.navbar-toggler');
const nav = document.querySelector('.navbar');
const address=document.querySelector('.nav-link1');
const hideAddress=document.querySelector('.nav-link1-collapse');
const backToTop= document.getElementById('back-to-top');
let menuOpen = false;
btn.addEventListener('click', () => {
  if(!menuOpen) {
    menuBtn.classList.add('open');
      nav.classList.add('black-back');
    nav.classList.remove('transparent-back');
    
    menuOpen = true;
   
    console.log('1');
  } else {
    menuBtn.classList.remove('open');
    if($(document).scrollTop() < 80)
    {nav.classList.add('transparent-back');
    nav.classList.remove('black-back');
    console.log('2');
    }
    menuOpen = false;
  }
});

$(window).scroll(function () {
  if ($(document).scrollTop() < 80) {
    backToTop.style.display= "none";
    if(!menuBtn.classList.contains('open'))
    {
      nav.style.background="#ffffff00";
     nav.classList.remove('black-back');
    // nav.classList.add('transparent-back');
}
  }
  else {
    if(!menuBtn.classList.contains('open'))
    {nav.style.background="#000814";
    //    nav.classList.add('black-back');
     nav.classList.remove('transparent-back');
    if ($(document).scrollTop() > 1500)
   {backToTop.style.display= "inline";}
  }
  }


});
// Get the modal
var modal = document.getElementById("myModal");

// Get the image and insert it inside the modal - use its "alt" text as a caption
var modalImg = document.getElementById("img01");
var captionText = document.getElementById("caption");
var img = document.getElementById('myImg');
function clickphoto(img) {
  modal.style.display = "block";
  modalImg.src = img.src;
  captionText.innerHTML = img.alt;
  console.log("click");
};

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

// When the user clicks on <span> (x), close the modal
span.onclick = function() { 
  modal.style.display = "none";
}

function active(){
  console.log(window.location.href);
  if(window.location.href ==="file:///F:/Sarpy/third%20year/%D9%81%D8%B5%D9%84%20%D8%AA%D8%A7%D9%86%D9%8A/%D9%85%D8%B4%D8%B1%D9%88%D8%B9%201/front/htmls/home.html#")
  { 
  $(window).ready(()=>{
    address.classList.add('active');
  hideAddress.classList.add('active');})
    
  }}

  active();