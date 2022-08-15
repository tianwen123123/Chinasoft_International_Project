// pages/login/login.js
Page({
	data: {
		username: null,
		password: null
	},
	onLoad: function () {
      this.setData({
		  // username : wx.getStorageSync('username'),
		  // password : wx.getStorageSync('password'),
	  })
  },
	inputUsername: function (e) {
		this.setData({
			username: e.detail.value
		})
		console.log("username:" + this.data.username);
	},
	inputPassword: function (e) {
		this.setData({
			password: e.detail.value
		})
		console.log("password:" + this.data.password);
  },
  registered:function(){
    wx.navigateTo({
      url: '../registered/registered',
      success: (result) => {},
      fail: (res) => {},
      complete: (res) => {},
    })
  },
	login: function () {
		if (this.data.username == null || this.data.password == null) {
			wx.showToast({
				title: '请输入账号密码',
				icon: 'error',
				duration: 1000
			});
		} else {
			wx.showToast({
				title: '登录中',
				icon: 'loading',
				duration: 1000
			});
			
			wx.request({
				url: "http://localhost:8081/user",
				method: "post",
				data: {
					telephone: this.data.username,
					password: this.data.password,
					method: "login"
				},
				header: { 
					'content-type': 'application/json'
				}, 
				success: (res) => {
					console.log("1111111")
					console.log(res.header["Set-Cookie"]);
					if (res.data == 1) {
						wx.showToast({
							title: '登录成功',
							icon: 'success',
							duration: 1000
						});
						var j = res.header["Set-Cookie"];
						var str = j.split(';');
						console.log(str[0]);
						wx.setStorageSync('Cookie', str[0]);
						wx.setStorageSync('username',this.data.username);
						wx.setStorageSync('password',this.data.password);
						setTimeout(function(){
						wx.navigateTo({
							url: '../GarbageSorting/GarbageSorting',
							success: function (res) {}
						})},500)

					} else {
						wx.showToast({
							title: '账号或密码有误',
							icon: "error",
							duration: 1000
						});
						console.log(res)
					}
				}
			})	
		}
	}
})