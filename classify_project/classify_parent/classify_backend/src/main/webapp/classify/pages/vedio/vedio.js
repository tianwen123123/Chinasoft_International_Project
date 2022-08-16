// pages/vedio/vedio.js
  Page({
    data: {
        Filepath:"../../images/_plus.png",
        resultimgpath:"../../images/_plus.png",
        resultText:"信息",
        isshow:false,
        telephone:'',
        imgisshow:true,
        videoPath:'',
        resultvediopath:'',
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
    Realtimerecogn(){
  
    },
    //识别
    regition(){
      var that = this
      if(that.data.vedioPath==""){
          wx.showToast({
            title: '请上传视频',
            icon:'error',
            duration:1000
          })
          return 
      }
      that.setData({
        resultvediopath:that.data.videoPath,
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
  
  
    VedioRecognition(){
      var that = this
      wx.chooseMedia({
        camera: 'back',
        count: 1,
        mediaType: ['video'],
        sourceType: ['album', 'camera'],
        success(res) {
          var vediopath = res.tempFiles[0].tempFilePath
          that.setData({
            videoPath:vediopath,
            imgisshow:false,
            isshow:false
          })
          console.log(vediopath)
          console.log(that.data.videoPath)
        },
        fail: (res) => {},
        complete: (res) => {},
      })
      wx.uploadFile({
        url: '',
        filePath: that.data.videoPath,
        name: 'vedioFile',
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
    }
  })