// pages/registered/registered.js
Page({
  data: {
    // 验证手机号
    codeChange: true,
    isPhoneRight:false,
    hongyzphone: '',
    // 验证码是否正确
    zhengLove: true,
    huoLove: '',
    code: '获取验证码',
    Password:'',
    confirmPassword:'',
  },
  // 手机验证
  phoneInput: function (e) {
    let phone = e.detail.value;
    this.setData({ 
      hongyzphone: phone 
    })
    if (!(/^1[34578]\d{9}$/.test(phone))) {
      this.setData({
        isPhoneRight: false
      })
      if (phone.length >= 11) {
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
    let yanLove = e.detail.value;
    let huoLove = this.data.huoLove;
    this.setData({
      yanLove: yanLove,
      zhengLove: false,
    })
    if (yanLove.length >= 4) {
      if (yanLove == huoLove) {
        this.setData({
          zhengLove: true,
        })
      } else {
        this.setData({
          zhengLove: false,
        })
        wx.showToast({
          title: '验证码有误',
          icon:'error',
          duration:1000,
        })
      }
    }
  },
  passwordInput:function(e){
    let password = e.detail.value
    this.setData({
      Password:password
    })
  },
  confirmpasswordInput:function(e){
    let confirmpassword = e.detail.value
    this.setData({
      confirmPassword:confirmpassword
    })
  },
  isPasswordSame:function(){
    if(this.data.Password == this.data.confirmPassword){
      return true
    }else{
      return false
    }
  },
  // 验证码按钮
  getcode:function(res){
    let codeChange = this.data.codeChange;
    console.log(codeChange)
    let isPhoneRight = this.data.isPhoneRight;
    console.log(isPhoneRight)
    let phone = this.data.hongyzphone;
    console.log(phone)
    let n = 59;
    let that = this;
    if (!isPhoneRight) {
      wx.showToast({
        title: '手机号有误',
        icon:'error',
        duration: 1000
      })
    } else 
    {
      if (codeChange) {
        // this.setData({
        //   codeChange: false
        // })

        let time = setInterval(function () {
          let str = '(' + n + ')' + '重新获取'
          that.setData({
            code: str
          })
          if (n <= 0) {
            that.setData({
              codeChange: true,
              code: '重新获取'
            })
            clearInterval(time);
          }
          n--;
        }, 1000);
        wx.showToast({
          title: '验证码已发送',
          icon:'none',
        })
          wx.request({
            url: 'http://localhost:8081/user?telephone='+this.data.phone,
            method: "GET",
            header: { 
              'content-type': 'application/json'
            }, 
            success(res){
              console.log(res)
            }
          })
        //获取验证码接口写在这里
        //例子 并非真实接口
        // app.agriknow.sendMsg(phone).then(res => {
        //   console.log('请求获取验证码.res =>', res)
        // }).catch(err => {
        //   console.log(err)
        // })
      }
    }
  },
  //form表单提交
  formSubmit(e){
    if(this.isPasswordSame()){
    let val = e.detail.value 
    console.log('val', val)
    var phone = val.phone //电话
    var Code = val.Code //验证码
    var openid = wx.getStorageSync('openid')
    console.log(openid)
 
    wx.request({
      url: '',
      data:{
        phone:phone,
        code:Code,
        openid:openid
      },
      success(res){
        console.log(res)
        if(res){
          wx.navigateTo({
            url: '../login/login',
          })
        }
      }
    })
  }else{
    wx.showToast({
      title: '密码不一致',
      icon:'error'
    })
  }
}
})