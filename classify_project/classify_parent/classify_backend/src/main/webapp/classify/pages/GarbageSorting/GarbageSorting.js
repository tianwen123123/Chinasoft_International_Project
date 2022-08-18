// pages/GarbageSorting/GarbageSorting.js
Page({
  data: {
      Filepath:"../../images/_plus.png",
      resultimgpath:"../../images/_plus.png",
      resultText:'',
      isshow:false,
      telephone:'',
  },
  onLoad(options) {
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
        wx.uploadFile({
          url: getApp().globalData.webUrl+'/picture',
          filePath: that.data.Filepath,
          formData: {
            'telephone':that.data.telephone
          },
          method:'post',
          name: 'imgFile',
          success:(res)=>{
            console.log(res)
            var jsonObj=JSON.parse(res.data)
            if(jsonObj.flag==true){
              wx.showToast({
                title: jsonObj.message,
                icon:"none",
                duration:1000
              })
            }else{
              wx.showToast({
                title: jsonObj.message,
                icon:'none',
                duration:1000,
              })
            }
          },
          fail:(res)=>{
            console.log("上传失败")
          }
        })
      },
      fail: (res) => {},
      complete: (res) => {},
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
    wx.showLoading({
      title: '识别中',
      mask: true,
    })
    wx.request({
      url: getApp().globalData.webUrl+'/picture?telephone='+that.data.telephone,
      method:'get',
      success: (res) => {
        var message = res.data.message
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
          that.setData({
            resultimgpath: "http://rgbvrgbry.hb-bkt.clouddn.com/"+res.data.data,
            isshow:true
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