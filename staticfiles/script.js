document.addEventListener('DOMContentLoaded', function(){
	let theme = localStorage.getItem('theme')
	if(theme == null){
		setTheme('light')
	}else{
		setTheme(theme)
	}
})

let themeDots = document.getElementsByClassName('theme-dot')


for (var i=0; themeDots.length > i; i++){
	themeDots[i].addEventListener('click', function(){
		let mode = this.dataset.mode
		setTheme(mode)
	})
}

function setTheme(mode){
	if(mode == 'light'){
		document.getElementById('theme-style').href = '/static/default.css'
	}

	if(mode == 'blue'){
		document.getElementById('theme-style').href = '/static/blue.css'
	}

	if(mode == 'green'){
		document.getElementById('theme-style').href = '/static/green.css'
	}

	if(mode == 'purple'){
		document.getElementById('theme-style').href = '/static/purple.css'
	}
	if(mode == 'pink'){
		document.getElementById('theme-style').href = '/static/pink.css'
	}

	localStorage.setItem('theme', mode)
}

document.querySelectorAll('.input-field').forEach(input => input.addEventListener('focusin', ()=>{
	input.nextElementSibling.style.width = '100%'
}))
document.querySelectorAll('.input-field').forEach(input => input.addEventListener('focusout', ()=>{
	input.nextElementSibling.style.width = '0%'
}))