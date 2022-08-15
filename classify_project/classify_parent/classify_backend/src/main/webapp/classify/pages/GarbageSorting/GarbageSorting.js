// pages/GarbageSorting/GarbageSorting.js
Page({
  data: {
      Filepath:"../../images/_plus.png",
      resultimgpath:"../../images/_plus.png",
      resultText:"信息",
      isshow:false
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
          Filepath:res.tempFiles[0].tempFilePath,
          isshow:false
        })
        console.log(res.tempFiles[0].tempFilePath)
      },
      fail: (res) => {},
      complete: (res) => {},
    })
  },

  regition(){
    var that = this
    if(that.data.Filepath=="../../images/_plus.png"){
        wx.showToast({
          title: '请选择图片',
          icon:'error',
          duration:1000
        })
        return 
    }
    this.setData({
      resultimgpath:that.data.Filepath,
      // isshow:true
    })
    wx.showLoading({
      title: '识别中',
      mask: true,
    })
    wx.uploadFile({
      url: '',
      filePath: that.data.Filepath,
      name: 'imagefile',
      success: (res) => {
        var message = res.message
        console.log(res)
        if(res.data.flag==true){
          wx.hideLoading({
            success: (res) => {},
          })
          that.setData({
            show:true
          })
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
        setTimeout(function () {
          wx.hideLoading()
        }, 2000)
        
        注意
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