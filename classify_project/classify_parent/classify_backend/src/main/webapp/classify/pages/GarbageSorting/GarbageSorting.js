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
      },
      fail: (res) => {},
      complete: (res) => {},
    })
  },

  regition(){
    var that = this
    wx.uploadFile({
      url: '',
      filePath: that.data.Filepath,
      name: 'imagefile',
      success: (res) => {
        var message = res.message
        console.log(res)
        if(res.data.flag==true){
            wx.showToast({
              title: message,
              icon:'none',
              duration:1000
            })
        }else{
          wx.showToast({
            title: message,
            icon:'none',
            duration:1000
          })
        }

        // wx.navigateTo({
        //   url: '../result/result?Filepath='+that.data.Filepath,
        // })
      },
      fail: (res) => {},
      complete: (res) => {
        // wx.navigateTo({
        //   url: '../result/result?Filepath='+that.data.Filepath,
        // })
      },
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