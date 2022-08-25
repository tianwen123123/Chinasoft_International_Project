// pages/login/login.js
Page({
  data: {
    telephone: '',
    password: '',
  },
  onLoad: function () {},

  //页面每次加载
  onShow() {
    this.setData({
      telephone: wx.getStorageSync('telephone'),
      password: wx.getStorageSync('password'),
    })
  },

  //手机号输入
  inputTelephone: function (e) {
    let phone = e.detail.value
    this.setData({
      telephone: phone
    })
    console.log("telephone:" + phone);
    if (phone.length > 11) {
      wx.showToast({
        title: '手机号输入有误',
        icon: 'none',
        duration: 1000
      })
    }
  },

  //密码输入
  inputPassword: function (e) {
    this.setData({
      password: e.detail.value
    })
    console.log("password:" + this.data.password);
  },

  //前往注册页面
  registered: function () {
    wx.navigateTo({
      url: '../registered/registered',
      success: (result) => {},
      fail: (res) => {},
      complete: (res) => {},
    })
  },

  //登录
  login: function () {
    var that = this
    var par = /^((13[0-9])|(14[0-9])|(15[0-9])|(17[0-9])|(18[0-9]))\d{8}$/
    //判断是否有空值
    if (that.data.telephone == null || that.data.password == null || that.data.telephone == '' || that.data.password == '') {
      wx.showToast({
        title: '输入不能为空',
        icon: 'error',
        duration: 1000
      });
    } else if (!(par.test(that.data.telephone)) || that.data.telephone.length != 11) { //手机号码格式与长度判断
      wx.showToast({
        title: '手机号格式有误',
        icon: 'error',
        duration: 1000
      });
    } else {
      wx.showToast({
        title: '登录中',
        icon: 'loading',
        duration: 1000
      });
      //发送登录请求
      wx.request({
        url: getApp().globalData.webUrl + '/user',
        method: "post",
        data: {
          telephone: that.data.telephone,
          password: that.data.password,
          method: "login"
        },
        header: {
          'content-type': 'application/json'
        },
        success: (res) => {
          console.log(res)
          var message = res.data.message
          if (res.data.flag == true) {
            wx.showToast({
              title: message,
              icon: 'success',
              duration: 1000
            });
            //缓存信息
            wx.setStorageSync('telephone', that.data.telephone);
            wx.setStorageSync('password', that.data.password);
            var phone = that.data.telephone
            setTimeout(function () {
              //跳转至图片识别界面
              wx.reLaunch({
                url: '../pictureRecognization/pictureRecognization?telephone=' + phone,
                success: function (res) {}
              })
            }, 500)
          } else {
            wx.showToast({
              title: message,
              icon: "error",
              duration: 1000
            });
          }
        },
        fail: (res) => {
          wx.showToast({
            title: '登录失败',
            icon: 'error',
            duration: 500
          })
        }
      })
    }
  }
})