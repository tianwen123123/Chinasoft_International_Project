// pages/result/result.js
Page({
  data: {
    Filepath:'',
    result:"",
  },

  onLoad(options) {
      console.log(options.Filepath)
      this.setData({
        Filepath:options.Filepath
      })
  },

  onReady() {

  },

  onShow() {

  },

  onHide() {

  },

  onUnload() {

  },

  onPullDownRefresh() {

  },

  onReachBottom() {

  },

  onShareAppMessage() {

  }
})