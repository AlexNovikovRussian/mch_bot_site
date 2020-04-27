$(".logout").click((event) => {
	$(".button-collapse").sideNav("hide")
	Swal.fire({
		title: 'Are you sure?',
		text: "You won't be able to revert this!",
		icon: 'warning',
		showCancelButton: true,
		confirmButtonColor: '#3085d6',
		cancelButtonColor: '#d33',
		confirmButtonText: 'Yes, log out!'
	  }).then((result) => {
		if (result.value) {
		  document.location = $("#logout_url").text()
		}
	  })
});

$('document').ready(function(){
	$('.modal').modal();
	$('.button-collapse').sideNav();
});
