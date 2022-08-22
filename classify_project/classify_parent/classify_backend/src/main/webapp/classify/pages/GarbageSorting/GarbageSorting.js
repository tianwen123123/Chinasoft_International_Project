// pages/GarbageSorting/GarbageSorting.js
Page({
  data: {
      Filepath:"../../images/_plus.png",
      resultimgpath:"../../images/_plus.png",
      resultText:'',
      isshow:false,
      telephone:'',
      resultinfo:[],
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
  PhotoRecognition(){
    var that = this
    that.setData({
      buttonshow:false,
    })
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
      },
      fail: (res) => {},
      complete: (res) => {},
    })

  },
  Realtimerecogn(){

  },
  regition(){
    var that = this
    if(that.data.buttonshow){
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
          wx.showToast({
            title: message,
            icon:'none',
            duration:1000
          })
          var result = [];
          var index = res.data.data[2];
          for(var i=0; i<=index;i++)
          {
            var turle ={
              path:"http://rgbvrgbry.hb-bkt.clouddn.com/" + i + "_" +res.data.data[i],
              text:res.data.data[1][i]
            }
            result.push(turle)
          }
          that.setData({
          //   resultimgpath: "http://rgbvrgbry.hb-bkt.clouddn.com/"+res.data.data[2]+"_"+res.data.data[0],
          //   resultText:res.data.data[1][res.data.data[2]],
            resultinfo:result,
            isshow:true
          })
        }else{
          wx.showToast({
            title: message,
            icon:'none',
            duration:1000
          })
        }
        console.log("结果数组"+that.data.resultinfo)
      },
      fail: (res) => {},
      complete: (res) => {
        setTimeout(function () {
          wx.hideLoading()
        }, 2000)
      },
    })
  }else{
    wx.showToast({
      title: '图片未上传成功，不可识别',
      icon:'none',
      duration:1000,
    })
  }
  },
})