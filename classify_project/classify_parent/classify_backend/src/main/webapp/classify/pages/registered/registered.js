// pages/registered/registered.js
Page({
  data: {
    codeChange: true,           //获取验证码是否可用
    isPhoneRight: false,        //手机号格式是否正确
    telephone: '',
    isconfirm: true,            //确认密码是否与密码一致
    validate_code: '',          //验证码
    codestr: '获取验证码',
    password: '',
    reconfirm_password: '',     //确认密码
  },

  // 手机号输入 验证格式
  phoneInput: function (e) {
    var par = /^((13[0-9])|(14[0-9])|(15[0-9])|(17[0-9])|(18[0-9]))\d{8}$/
    let telephone = e.detail.value;
    console.log(telephone)
    this.setData({
      telephone: telephone
    })
    if (!(par.test(telephone))) {
      this.setData({
        isPhoneRight: false
      })
      if (telephone.length >= 11) {
        wx.showToast({
          title: '手机号输入有误',
          icon: 'none',
          duration: 1000
        })
      }
    } else {
      this.setData({
        isPhoneRight: true
      })
    }
  },

  // 验证码输入
  codeInput: function (e) {
    let validate_code = e.detail.value;
    this.setData({
      validate_code: validate_code,
      isconfirm: false,
    })
    if (validate_code.length > 6) {
      if (validate_code == '') {
        this.setData({
          isconfirm: true,
        })
      } else {
        this.setData({
          isconfirm: false,
        })
        wx.showToast({
          title: '验证码有误',
          icon: 'error',
          duration: 1000,
        })
      }
    }
  },

  // 密码输入
  passwordInput: function (e) {
    let password = e.detail.value
    this.setData({
      password: password
    })
  },
  // 确认密码输入
  confirmpasswordInput: function (e) {
    let reconfirm_password = e.detail.value
    this.setData({
      reconfirm_password: reconfirm_password
    })
  },
  // 密码是否一致
  isPasswordSame: function () {
    if (this.data.password == this.data.reconfirm_password) {
      return true
    } else {
      return false
    }
  },

  // 获取验证码
  getcode: function (res) {
    let codeChange = this.data.codeChange;
    console.log(codeChange)
    let isPhoneRight = this.data.isPhoneRight;
    console.log(isPhoneRight)
    let telephone = this.data.telephone;
    console.log(telephone)
    //60秒倒计时
    let n = 59;
    let that = this;
    if (!isPhoneRight) {
      wx.showToast({
        title: '手机号有误',
        icon: 'error',
        duration: 1000
      })
    } else {
      if (codeChange) {
        console.log("发送验证码请求")
        that.setData({
          codeChange: false
        })
        let time = setInterval(function () {
          let str = '(' + n + ')' + '重新获取'
          that.setData({
            codestr: str
          })
          if (n <= 0) {
            that.setData({
              codeChange: true,
              codestr: '重新获取'
            })
            clearInterval(time);
          }
          n--;
        }, 1000);
        //发送验证码请求
        wx.request({
          url: getApp().globalData.webUrl + '/user?telephone=' + this.data.telephone,
          method: 'GET',
          success(res) {
            console.log(res)
            if (res.data.flag == true) {
              wx.showToast({
                title: '验证码已发送',
                icon: 'none'
              })
            }
          }
        })
      }
    }
  },

  //form表单提交
  formSubmit(e) {
    // console.log(e)
    var val = e.detail.value
    console.log('val', val)
    var par = /^((13[0-9])|(14[0-9])|(15[0-9])|(17[0-9])|(18[0-9]))\d{8}$/
    var telephone = val.telephone                       //电话
    var Code = val.validate_code                        //验证码
    var Password = val.password                         //密码
    var reconfirm_password = val.reconfirm_password     //确认密码
    if (telephone == "" || Code == "" || Password == "" || reconfirm_password == "") {
      wx.showToast({
        title: '请输入完整信息',
        icon: 'error',
        duration: 1000
      })
    } else if (!(par.test(telephone))) {
      wx.showToast({
        title: '手机号格式错误',
        icon: 'error',
        duration: 1000
      })
    } else {
      if (this.isPasswordSame()) {
        console.log("注册")
        wx.request({
          url: getApp().globalData.webUrl + '/user',
          method: 'PUT',
          data: {
            'telephone': telephone,
            'password': Password,
            'reconfirm_password': reconfirm_password,
            'validate_code': Code
          },
          success(res) {
            let message = res.data.message
            console.log(res)
            if (res.data.flag == true) {
              wx.setStorageSync('telephone', telephone);
              wx.setStorageSync('password', Password);
              wx.showToast({
                title: message,
                icon: 'success',
                duration: 1000
              })
              setTimeout(function () {
                wx.redirectTo({
                  url: '../login/login'
                })
              }, 500)
            } else {
              wx.showToast({
                title: message,
                icon: 'success',
                duration: 1000
              })
            }
          }
        })
      } else {
        wx.showToast({
          title: '密码不一致',
          icon: 'error',
          duration: 1000
        })
      }
    }
  }
})