// pages/liveRecognization/liveRecognization.js
Page({
  data: {
    show: false,          //正在识别字样显示
    telephone: '',
    isshow: false,        //识别结果
    startopen: true,      //识别按钮
    stopopen: false,      //停止识别按钮
    startopen1:true,      //定位按钮
    stopopen2:false,      //停止定位按钮
    resultinfo: [],       
    title: "http://rh5dq0hiv.hb-bkt.clouddn.com/",
    flag: false,          //'未监测到车牌'字样显示
    radioItems: [{
        name: '实时识别',
        value: '实时识别',
        checked: 'true',
        disabled:false,
      },
      {
        name: '车牌定位',
        value: '车牌定位',
        disabled:false,
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
  //开始识别
  start() {
    var that = this
    var disabled = "radioItems["+ 1 +"].disabled"
    if (that.data.startopen) {
      that.setData({
        show: true,
        startopen: false,
        stopopen: true,
        isshow: false,
        resultinfo: [],
        flag: false,
        [disabled]:true,
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

  //停止识别
  stop() {
    var that = this
    var disabled = "radioItems["+ 1 +"].disabled"
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
            [disabled]:false,
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

  //开始车牌定位
  live_start() {
    var that = this
    var disabled = "radioItems["+ 0 +"].disabled"
    if (that.data.startopen1) {
      that.setData({
        show: true,
        startopen1: false,
        stopopen1: true,
        [disabled]:true,
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

  //停止车牌定位
  live_stop() {
    var that = this
    var disabled = "radioItems["+ 0 +"].disabled"
    if (that.data.stopopen1) {
      //发送请求
      wx.request({
        url: "http://127.0.0.1:5000/live_stop?telephone=" + that.data.telephone,
        method: 'get',
        success: (res) => {
          that.setData({
            show: false,
            stopopen1: false,
            startopen1: true,
            [disabled]:false,
          })
          wx.showToast({
            title: '监测结束',
            icon: 'none',
            duration: 1500,
          })
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
    console.log(e.detail)
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