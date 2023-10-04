(function($){
	function floatLabel(inputType){
		$(inputType).each(function(){
			var $this = $(this);
			// on focus add cladd active to label
			$this.focus(function(){
				$this.next().addClass("active");
			});
			//on blur check field and remove class if needed
			$this.blur(function(){
				if($this.val() === '' || $this.val() === 'blank'){
					$this.next().removeClass();
				}
			});
		});
	}
	// just add a class of "floatLabel to the input field!"
	floatLabel(".floatLabel");
})(jQuery);

let darkMode = localStorage.getItem("darkMode");
const darkModeToggle = document.querySelector("#dark-mode-toggle");

// console.log(darkMode);

const enableDarkMode = () => {
  document.body.classList.add("darkmode");

  localStorage.setItem("darkMode", "enabled");

}

const disableDarkMode = () => {
  document.body.classList.remove("darkmode");

  localStorage.setItem("darkMode", null);

}

if (darkMode === "enabled") {
  enableDarkMode();
}

darkModeToggle.addEventListener("click", () => {

  darkMode = localStorage.getItem("darkMode");
  // console.log("test");
  if (darkMode !== "enabled") {
    enableDarkMode();
    console.log(darkMode);

  } else {
    disableDarkMode();
    console.log(darkMode);
  }

});