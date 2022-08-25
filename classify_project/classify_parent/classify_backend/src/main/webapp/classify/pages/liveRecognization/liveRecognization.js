// pages/liveRecognization/liveRecognization.js
Page({
  data: {
    show: false,
    telephone: '',
    isshow: false,
    startopen: true,
    stopopen: false,
    resultinfo: [],
    title: "http://rh5dq0hiv.hb-bkt.clouddn.com/",
    flag: false,
    radioItems: [{
        name: '使用1',
        value: '美国',
        checked: 'true'
      },
      {
        name: '使用2',
        value: '中国'
      }
    ],
    selectedindex: 0,
    method0: true,
    method1: false,
  },
  onLoad() {

  },
  onShow() {
    var that = this
    that.setData({
      imageArray: {},
      telephone: wx.getStorageSync('telephone')
    })
  },
  start() {
    var that = this
    if (that.data.startopen) {
      that.setData({
        show: true,
        startopen: false,
        stopopen: true,
        isshow: false,
        resultinfo: [],
        flag: false
      })
      //发送请求
      wx.request({
        url: "http://127.0.0.1:5000/live_start?telephone=" + that.data.telephone,
        method: 'get',
        success: (res) => {
          console.log("请求成功")
        },
        fail: (res) => {
          console.log("请求失败")
        },
        complete: (res) => {},
      })
    } else {
      wx.showToast({
        title: '正在识别,请勿重复点击',
        icon: 'none',
        duration: 1000,
      })
    }
  },
  stop() {
    var that = this
    if (that.data.stopopen) {

      //发送请求
      wx.request({
        url: "http://127.0.0.1:5000/live_stop?telephone=" + that.data.telephone,
        method: 'get',
        success: (res) => {
          that.setData({
            show: false,
            stopopen: false,
            startopen: true,
            resultinfo: res.data.licenselist,
            isshow: true,
          })
          if (res.data.len == 0) {
            that.setData({
              flag: true
            })
          } else {
            that.setData({
              flag: false
            })
          }
          wx.showToast({
            title: '监测结束',
            icon: 'none',
            duration: 1500,
          })
          console.log(res)
          console.log(that.data.resultinfo)
        },
        fail: (res) => {
          console.log("请求失败")
        },
        complete: (res) => {},
      })
    } else {
      wx.showToast({
        title: '还未开始监测',
        icon: 'none',
        duration: 1000,
      })
    }
  },
  //点击选项
  radioChange(e) {
    var that = this
    console.log(e)
    const checked = e.detail.value
    const changed = {}
    for (let i = 0; i < that.data.radioItems.length; i++) {
      if (checked.indexOf(that.data.radioItems[i].name) !== -1) {
        changed['radioItems[' + i + '].checked'] = true
        that.setData({
          selectedindex: i
        })
      } else {
        changed['radioItems[' + i + '].checked'] = false
      }
    }
    that.setData(changed)
    if (that.data.selectedindex == 0) {
      that.setData({
        method0: true,
        method1: false,
      })
    } else if (that.data.selectedindex == 1) {
      that.setData({
        method0: false,
        method1: true
      })
    }
  },

  error(e) {
    console.log(e.detail)
  }
})