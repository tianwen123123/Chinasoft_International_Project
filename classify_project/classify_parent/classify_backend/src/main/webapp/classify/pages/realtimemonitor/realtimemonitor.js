// pages/realtimemonitor/realtimemonitor.js
Page({
  data:{
    show:false,
    telephone:'',
    isshow:false,
    startopen:true,
    stopopen:false,
    resultinfo:[],
    title:"http://rgbvrgbry.hb-bkt.clouddn.com/",
    flag:false,
  },



  onLoad() {
//     var that = this
//     that.ctx = wx.createCameraContext()
//     var count=0
//     that.listener =  that.ctx.onCameraFrame((frame) => {
//       count+=1
//       if(count==100){
//         var array = Array.prototype.slice.call(new Uint8Array(frame.data))
//         var uint8array = new Uint8Array(frame.data)
//         // console.log(Array.prototype.slice.call(new Uint8Array(frame.data)), frame.width, frame.height)
//         // let url = that.arrayBufferToBase64(uint8array)
//         let url = wx.arrayBufferToBase64(uint8array)
//         let src = url
//         that.setData({
//           imageArray:array,
//           base64 : src
//         })
//         console.log("====="+that.data.base64+"====")
//         count=0 
//       }
// })
},
  onShow(){
    var that = this
    that.setData({
      imageArray:{},
      telephone:wx.getStorageSync('telephone')
    })
  },
start(){
  var that = this
  if(that.data.startopen){
  that.setData({
    show:true,
    startopen:false,
    stopopen:true,
    isshow:false,
    resultinfo:[],
    flag:false
  })
  //发送请求
  wx.request({
    url: "http://127.0.0.1:5000/live_start?telephone="+that.data.telephone,
    method: 'get' ,
    success: (res) => {
      console.log("请求成功")
    },
    fail: (res) => {
      console.log("请求失败")
    },
    complete: (res) => {},
  })
}else{
  wx.showToast({
    title: '正在识别,请勿重复点击',
    icon:'none',
    duration:1000,
  })
}
},
stop(){
  var that = this
  if(that.data.stopopen){

    //发送请求
    wx.request({
      url:  "http://127.0.0.1:5000/live_stop?telephone="+that.data.telephone,
      method:'get' ,
      success: (res) => {
        that.setData({
          show:false,
          stopopen:false,
          startopen:true,
          resultinfo:res.data.licenselist,
          isshow:true,
        })
        if(res.data.len==0){
          that.setData({
            flag:true
          })
        }else{
          that.setData({
            flag:false
          })
        }
        wx.showToast({
          title: '监测结束',
          icon:'none',
          duration:1500,
        })
        console.log(res)
        console.log(that.data.resultinfo)
      },
      fail: (res) => {
        console.log("请求失败")
      },
      complete: (res) => {},
    })
}else{
  wx.showToast({
    title: '还未开始监测',
    icon:'none',
    duration:1000,
  })
}
},

  error(e) {
    console.log(e.detail)
  }
})