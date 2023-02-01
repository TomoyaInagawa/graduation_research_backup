document.querySelectorAll('.left').forEach(elm => {
	elm.onclick = function () {
		let ul = elm.parentNode.querySelector('ul');
		ul.scrollLeft -= ul.clientWidth;
	};
});
document.querySelectorAll('.right').forEach(elm => {
	elm.onclick = function () {
		let ul = elm.parentNode.querySelector('ul');
		ul.scrollLeft += ul.clientWidth;
	};
});