// app.js
App({
  onLaunch() {
    // 登录
    wx.login({
      success: res => {
        // 发送 res.code 到后台换取 openId, sessionKey, unionId
      }
    })
  },
  globalData: {
    webUrl:"http://127.0.0.1:8081",
    liveRequestUrl:"http://127.0.0.1:5000",
    userInfo: null
  }
})
