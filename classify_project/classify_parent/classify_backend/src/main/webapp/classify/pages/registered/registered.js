// pages/registered/registered.js
Page({
  data: {
    // 验证手机号
    codeChange: true,
    isPhoneRight:false,
    telephone: '',
    isconfirm: true,
    validate_code:'',
    codestr: '获取验证码',
    reconfirm_password:'',
    password:'',
  },
  // 手机验证
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
    if (validate_code.length >= 6) {
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
          icon:'error',
          duration:1000,
        })
      }
    }
  },
  passwordInput:function(e){
    let password = e.detail.value
    this.setData({
      password:password
    })
  },
  confirmpasswordInput:function(e){
    let reconfirm_password = e.detail.value
    this.setData({
      reconfirm_password:reconfirm_password
    })
  },
  isPasswordSame:function(){
    if(this.data.password == this.data.reconfirm_password){
      return true
    }else{
      return false
    }
  },
  // 获取验证码按钮
  getcode:function(res){
    let codeChange = this.data.codeChange;
    console.log(codeChange)
    let isPhoneRight = this.data.isPhoneRight;
    console.log(isPhoneRight)
    let telephone = this.data.telephone;
    console.log(telephone)
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
        console.log("发送验证码请求")
        that.setData({
            codeChange:false
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
          wx.request({
            url: '',
            data:{
              telephone:telephone
            },
            success(res){
              console.log(res)
            }
          })
      }
    }
  },
  //form表单提交
  formSubmit(e){
    // console.log(e)
    var val = e.detail.value 
    console.log('val', val)
    var telephone = val.telephone //电话
    var Code = val.validate_code //验证码
    var Password = val.password  //密码
    var reconfirm_password = val.reconfirm_password  //确认密码
    if(telephone == "" || Code == ""|| Password == ""|| reconfirm_password == ""){
      wx.showToast({
        title: '请输入完整信息',
        icon:'error',
        duration:1000
      })
    }else{
    if(this.isPasswordSame()){
      console.log("注册")
    wx.request({
      url: '',
      data:{
        telephone:telephone,
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
      icon:'error',
      duration:1000
    })
  }
}
}
})