// pages/pictureRecognization/pictureRecognization.js
Page({
  data: {
      Filepath:"../../images/_plus.png",
      isshow:false,         //识别结果显示
      telephone:'',
      resultinfo:[],        //请求到的信息结果
      buttonshow:false,     //识别按钮是否可用
  },
  onLoad(options) {    //获取传递到的手机号码
      this.setData({
        telephone:options.telephone
      })
  },

  //上传图片
  upLoadPicture(){
    var that = this
    that.setData({
      buttonshow:false,
    })
    //选择图片
    wx.chooseMedia({
      camera: 'back',
      count: 1,
      mediaType: ['image'],
      sourceType: ['album', 'camera'],
      camera: 'back',
      success(res) {
        that.setData({
          Filepath:res.tempFiles[0].tempFilePath,   //本地图片路径
          isshow:false
        })
        console.log(res.tempFiles[0].tempFilePath)
        //向后端上传图片
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

  //识别
  Recognization(){
    var that = this
    that.setData({
      isshow:false
    })
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
    //发送识别请求
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
          // for循环将返回结果存储在result数组中
          var result = [];
          var index = res.data.data[2];
          for(var i=0; i<=index;i++)
          {
            var turle ={
              path:"http://rgbvrgbry.hb-bkt.clouddn.com/" + i + "_" +res.data.data[i],
              text:res.data.data[1][i]
            }
            result.push(turle)        //将每一个字典放到数组中
          }
          that.setData({
            resultinfo:result,
            isshow:true               //展示结果
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