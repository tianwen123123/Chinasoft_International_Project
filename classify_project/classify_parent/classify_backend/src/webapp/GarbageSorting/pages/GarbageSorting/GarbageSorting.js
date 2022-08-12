// pages/GarbageSorting/GarbageSorting.js
Page({
  data: {

  },

  onLoad(options) {

  },
  onReady() {

  },
  onShow() {

  },


  PhotoRecognition(){
    wx.chooseMedia({
      camera: 'back',
      count: 1,
      mediaType: ['image'],
      sourceType: ['album', 'camera'],
      success: (res) => {
          console.log(res.tempFiles.tempFilePath)
          wx.showLoading({
            title: '识别中',
          })
      },
      fail: (res) => {},
      complete: (res) => {},
    })
  },
  VedioRecognition(){
    wx.chooseMedia({
      camera: 'back',
      count: 1,
      mediaType: ['video'],
      sourceType: ['album', 'camera'],
      success: (res) => {
          console.log(res.tempFiles.tempFilePath)
      },
      fail: (res) => {},
      complete: (res) => {},
    })
  }

})