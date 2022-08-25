// pages/videoRecognization/videoRecognization.js
Page({
  data: {
    Filepath: "../../images/_plus.png",
    isshow: false, //结果是否显示
    telephone: '',
    imgisshow: true, //上传样式图片是否显示
    videoPath: '', //本地视频路径
    resultvideopath: '', //返回结果视频路径
    buttonshow: false, //识别按钮是否可用
    resultinfo: [], //结果信息
    telephone: '',
  },

  // 页面每次加载获取缓存
  onShow() {
    this.setData({
      telephone: wx.getStorageSync("telephone")
    })
    console.log(this.data.telephone)
  },

  //选择视频
  upLoadVedio() {
    var that = this
    that.setData({
      buttonshow: false,
    })
    // 选择文件
    wx.chooseMedia({
      camera: 'back',
      count: 1,
      mediaType: ['video'],
      sourceType: ['album', 'camera'],
      maxDuration: 7,
      success(res) {
        var vediopath = res.tempFiles[0].tempFilePath
        if (res.tempFiles[0].duration > 7) {
          wx.showToast({
            title: '视频过长，请选择7秒以内的视频',
            icon: 'none',
            duration: 1500,
          })
        } else {
          that.setData({
            videoPath: vediopath,
            imgisshow: false,
            isshow: false
          })
          console.log(vediopath)
          console.log("大小：" + res.tempFiles[0].size / 1024 / 1024 + "   时长：" + res.tempFiles[0].duration)
          //上传视频
          wx.uploadFile({
            url: getApp().globalData.webUrl + '/video',
            filePath: that.data.videoPath,
            formData: {
              'telephone': that.data.telephone
            },
            method: 'post',
            name: 'videoFile',
            success: (res) => {
              console.log(res)
              var jsonObj = JSON.parse(res.data)
              if (jsonObj.flag == true) {
                wx.showToast({
                  title: jsonObj.message,
                  icon: "none",
                  duration: 1000
                })
                that.setData({
                  buttonshow: true
                })
              } else {
                wx.showToast({
                  title: jsonObj.message,
                  icon: 'none',
                  duration: 1000,
                })
              }
            },
            fail: (res) => {
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
  Recognization() {
    var that = this
    that.setData({
      isshow: false
    })
    if (that.data.videoPath == "") {
      wx.showToast({
        title: '请上传视频',
        icon: 'error',
        duration: 1000
      })
      return
    }
    if (that.data.buttonshow) {
      wx.showLoading({
        title: '识别中',
        mask: true,
      })
      wx.request({
        url: getApp().globalData.webUrl + '/video?telephone=' + that.data.telephone,
        method: 'get',
        success: (res) => {
          var message = res.data.message
          console.log(res)
          if (res.data.flag == true) {
            wx.hideLoading({
              success: (res) => {},
            })
            wx.showToast({
              title: message,
              icon: 'none',
              duration: 1000
            })
            that.setData({
              resultvideopath: "http://rgbvrgbry.hb-bkt.clouddn.com/" + res.data.data[3],
            })
            var result = [];
            var index = res.data.data[0];
            for (var i = 0; i <= index; i++) {
              var turle = {
                path: "http://rgbvrgbry.hb-bkt.clouddn.com/" + i + "_" + res.data.data[1],
                text: res.data.data[2][i]
              }
              result.push(turle)
            }
            that.setData({
              resultinfo: result,
              isshow: true,
            })
            console.log(that.data.resultinfo)
            console.log(that.data.resultvideopath)
          } else {
            wx.showToast({
              title: message,
              icon: 'none',
              duration: 1000
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
    } else {
      wx.showToast({
        title: '视频未上传成功，不可识别',
        icon: 'none',
        duration: 1000,
      })
    }
  },
})