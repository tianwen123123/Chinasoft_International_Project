// pages/login/login.js
Page({
	data: {
		telephone: null,
		password: null
	},
	onLoad: function (options) {
      this.setData({
		  telephone : wx.getStorageSync('telephone'),
      password : wx.getStorageSync('password'),
    })
    if(!(options == null || options == '')){
      this.setData({
        telephone:options.telephone,
        password:options.password,
      })
    }
  },
	inputTelephone: function (e) {
    let phone = e.detail.value
		this.setData({
			telephone: phone
		})
    console.log("telephone:" + phone);
    if(phone.length>11){
      wx.showToast({
        title: '手机号输入有误',
        icon: 'none',
        duration: 1000
      })
    }
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
    var par = /^((13[0-9])|(14[0-9])|(15[0-9])|(17[0-9])|(18[0-9]))\d{8}$/
		if (this.data.telephone==null||this.data.password==null||this.data.telephone==''||this.data.password=='') {
			wx.showToast({
				title: '输入不能为空',
				icon: 'error',
				duration: 1000
			});
    }
    else if(!(par.test(this.data.telephone)) || this.data.telephone.length != 11){
      wx.showToast({
				title: '手机号格式有误',
				icon: 'error',
				duration: 1000
			});
    }
    else {
			wx.showToast({
				title: '登录中',
				icon: 'loading',
				duration: 1000
			});
      // wx.switchTab({
      //   url: '../GarbageSorting/GarbageSorting',
      // })

      
			wx.request({
				url: "http://localhost:8081/user",
				method: "post",
				data: {
					telephone: this.data.telephone,
					password: this.data.password,
					method: "login"
				},
				header: { 
					'content-type': 'application/json'
				}, 
				success: (res) => {
          console.log(res)
          var message = res.data.message
					console.log(res.header["Set-Cookie"]);
					if (res.data.flag == true) {
						wx.showToast({
							title: message,
							icon: 'success',
							duration: 1000
						});
						wx.setStorageSync('telephone',this.data.telephone);
						wx.setStorageSync('password',this.data.password);
						var phone = this.data.telephone
						setTimeout(function(){
						wx.switchTab({
							url: '../GarbageSorting/GarbageSorting?telephone='+phone,
							success: function (res) {}
						})},500)
					} else {
						wx.showToast({
							title: message,
							icon: "error",
							duration: 1000
						});
					}
				}
			})	
		}
	}
})