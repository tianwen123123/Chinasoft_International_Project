// pages/vedio/vedio.js
  Page({
    data: {
        Filepath:"../../images/_plus.png",
        resultText:"信息",
        isshow:false,
        telephone:'',
        imgisshow:true,
        videoPath:'',
        resultvideopath:'',
        buttonshow:false,
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

    //选择视频
    VedioRecognition(){
      var that = this
      that.setData({
        buttonshow:false,
      })
      wx.chooseMedia({
        camera: 'back',
        count: 1,
        mediaType: ['video'],
        sourceType: ['album', 'camera'],
        maxDuration:7,
        success(res) {
          var vediopath = res.tempFiles[0].tempFilePath
          if(res.tempFiles[0].duration > 7){
            wx.showToast({
              title: '视频过长，请选择7秒以内的视频',
              icon:'none',
              duration:1500,
            })
          }else{
          that.setData({
            videoPath:vediopath,
            imgisshow:false,
            isshow:false
          })
          console.log(vediopath)
          console.log("大小："+res.tempFiles[0].size/1024/1024+"   时长："+res.tempFiles[0].duration)
          //上传视频
          wx.uploadFile({
            url: getApp().globalData.webUrl+'/video',
            filePath: that.data.Filepath,
            formData: {
              'telephone':that.data.telephone
            },
            method:'post',
            name: 'videoFile',
            success:(res)=>{
              console.log(res)
              var jsonObj=JSON.parse(res.data)
              if(jsonObj.flag==true){
                wx.showToast({
                  title: jsonObj.message,
                  icon:"none",
                  duration:1000
                })
                that.setData({
                  buttonshow:true
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
        }
        },
        fail: (res) => {},
        complete: (res) => {},
      })
    },

    //识别
    regition(){
      var that = this
      if(that.data.videoPath==""){
          wx.showToast({
            title: '请上传视频',
            icon:'error',
            duration:1000
          })
          return 
      }
      if(that.data.buttonshow){
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
            wx.showToast({
              title: message,
              icon:'none',
              duration:1000
            })
            var index = res.data.data[2];
            that.setData({
              resultvideopath:"http://rgbvrgbry.hb-bkt.clouddn.com/" + index + "_" +res.data.data[i],
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
    }
  else{
    wx.showToast({
      title: '视频未上传成功，不可识别',
      icon:'none',
      duration:1000,
    })
  }
  },
  })