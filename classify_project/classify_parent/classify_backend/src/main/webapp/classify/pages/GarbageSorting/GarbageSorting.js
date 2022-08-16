// pages/GarbageSorting/GarbageSorting.js
Page({
  data: {
      Filepath:"../../images/_plus.png",
      resultimgpath:"../../images/_plus.png",
      resultText:"信息",
      isshow:false,
      telephone:'',
  },
  onLoad(options) {
    console.log(options)
      this.setData({
        telephone:options.telephone
      })
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
    wx.uploadFile({
      url: getApp().globalData.webUrl+'/picture?telephone'+that.data.telephone,
      filePath: that.data.Filepath,
      name: 'imgFile',
      success:(res)=>{
        console.log(res)
        let message = res.message
        if(res.data.flag==true){
          wx.showToast({
            title: message,
            icon:"none",
            duration:1000
          })
        }else{
          wx.showToast({
            title: message,
            icon:'none',
            duration:1000,
          })
        }
      },
    })
  },
  Realtimerecogn(){

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
    that.setData({
      resultimgpath:that.data.Filepath,
      isshow:true
    })
    wx.showLoading({
      title: '识别中',
      mask: true,
    })
    wx.request({
      url: 'url',
      method:'',
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
      },
      fail: (res) => {},
      complete: (res) => {
        setTimeout(function () {
          wx.hideLoading()
        }, 2000)
      },
    })
  },
})