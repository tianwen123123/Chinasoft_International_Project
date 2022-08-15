// pages/GarbageSorting/GarbageSorting.js
Page({
  data: {
      Filepath:"",
  },
  onLoad(options) {

  },
  onReady() {

  },
  onShow() {

  },
  PhotoRecognition(){
    var that = this
    wx.chooseMedia({
      camera: 'back',
      count: 1,
      mediaType: ['image'],
      sourceType: ['album', 'camera'],
      camera: 'back',
      success(res) {
        that.setData({
          Filepath:res.tempFiles[0].tempFilePath
        })
        console.log(res.tempFiles[0].tempFilePath)
        wx.uploadFile({
          filePath: that.data.Filepath,
          name: 'imagefile',
          url: '',
          success: (result) => {
            wx.navigateTo({
              url: '../result/result?Filepath='+that.data.Filepath,
            })
          },
          fail: (res) => {},
          complete: (res) => {},
        })
      },
      fail: (res) => {},
      complete: (res) => {},
    })
  },
  VedioRecognition(){
    var that = this
    wx.chooseMedia({
      camera: 'back',
      count: 1,
      mediaType: ['video'],
      sourceType: ['album', 'camera'],
      success(res) {
        that.setData({
          Filepath:res.tempFiles[0].tempFilePath
        })
        console.log(res.tempFiles[0].tempFilePath)
        wx.uploadFile({
          filePath: that.data.Filepath,
          name: 'vediofile',
          url: '',
          success: (result) => {
            wx.navigateTo({
              url: '../result/result?Filepath='+that.data.Filepath,
            })
          },
          fail: (res) => {},
          complete: (res) => {},
        })
      },
      fail: (res) => {},
      complete: (res) => {},
    })
  }

})