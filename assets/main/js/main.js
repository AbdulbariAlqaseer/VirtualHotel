const menuBtn = document.querySelector('.menu-btn');
const btn = document.querySelector('.navbar-toggler');
const nav = document.querySelector('.navbar');
const address=document.querySelector('.nav-link1');
const hideAddress=document.querySelector('.nav-link1-collapse');
const backToTop= document.getElementById('back-to-top');
const bookBtn=document.getElementById("book");
const mess= document.querySelector(".back-message");
const board= document.querySelector(".listed");
const boardI= document.querySelector(".listed i");
const sideBar =document.getElementById('sidebar');
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




function active(){
  if(window.location.href ==="file:///F:/Sarpy/third%20year/%D9%81%D8%B5%D9%84%20%D8%AA%D8%A7%D9%86%D9%8A/%D9%85%D8%B4%D8%B1%D9%88%D8%B9%201/front/htmls/home.html#")
  { 
  $(window).ready(()=>{
    address.classList.add('active');
  hideAddress.classList.add('active');})
    
  }}

  active();
  function openModal() {
    document.getElementById("myModal-gal").style.display = "block";
  }
  function closeModal() {
    modal.style.display = "none";
    document.getElementById("myModal-gal").style.display = "none";
   
  }
  
  var slideIndex = 1;
  showSlides(slideIndex);
  
  function plusSlides(n) {
    showSlides(slideIndex += n);
  }
  
  function currentSlide(n) {
    showSlides(slideIndex = n);
  }
  
  function showSlides(n) {
    var i;
    var slides = document.getElementsByClassName("mySlides");
    var dots = document.getElementsByClassName("demo");
    var captionText = document.getElementById("caption-gal");
    if (n > slides.length) {slideIndex = 1}
    if (n < 1) {slideIndex = slides.length}
    for (i = 0; i < slides.length; i++) {
        slides[i].style.display = "none";
    }
    for (i = 0; i < dots.length; i++) {
        dots[i].className = dots[i].className.replace(" active", "");
    }
    slides[slideIndex-1].style.display = "block";
    dots[slideIndex-1].className += " active";
    captionText.innerHTML = dots[slideIndex-1].alt;
  }
  // cardInfo.addEventListener('click', () =>{
  //   console.log(cardInfo.getAttribute('aria-expanded'));
  //  if( cardInfo.getAttribute('aria-expanded')=="true")
  //  {
  //   cardInfo.firstChild.classList.add('fas fa-chevron-up');
  //   cardInfo.firstChild.classList.remove('fas fa-chevron-down');
  //  }
  //  if( cardInfo.getAttribute('aria-expanded')=="false")
  //  {
  //   cardInfo.firstChild.classList.add('fas fa-chevron-down');
  //   cardInfo.firstChild.classList.remove('fas fa-chevron-up');

  //  }

  // });
  function tog(x) {
    if( x.parentElement.getAttribute('aria-expanded')=="true")
  {x.classList.remove("fa-chevron-up");
     x.classList.add("fa-chevron-down");
  

  }

  if( x.parentElement.getAttribute('aria-expanded')=="false")
  {x.classList.remove("fa-chevron-down");
    x.classList.add("fa-chevron-up");
  }
  
  }
  
// function togl(x) {
//  console.log("jwk");
//   if( board.getAttribute('aria-expanded')=="true")
//   {console.log("lel");
//     x.classList.remove("fa-chevron-up");
//      x.classList.add("fa-chevron-down");
//      sideBar.style.marginBottom= "100px";
  
//   }
//   if( board.getAttribute('aria-expanded')=="false")
//   {x.classList.remove("fa-chevron-down");
//     x.classList.add("fa-chevron-up");
//   }
//   }
  function print(){
    console.log(document.querySelector('#booking input[type="text"]').value)
  }
  board.addEventListener('click', () => {

    if( boardI.parentElement.getAttribute('aria-expanded')=="true")
    {
      boardI.classList.remove("fa-chevron-up");
       boardI.classList.add("fa-chevron-down");
       sideBar.style.marginBottom= "100px";
    
    }
    if( boardI.parentElement.getAttribute('aria-expanded')=="false")
    {boardI.classList.remove("fa-chevron-down");
      boardI.classList.add("fa-chevron-up");
    }

  })

bookBtn.addEventListener("click",() => {
mess.innerHTML="wrong";
mess.style.color=" red";
alert("wrong booking");
})
function closeMessage() {
  document.getElementById("message").style.display = "none";
}