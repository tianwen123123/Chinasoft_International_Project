// pages/realtimemonitor/realtimemonitor.js
Page({

  data:{
    imageArray:{},
    left:0,
    top:0,
    rectangleshow:false,
    base64:"",
    show:false,
    telephone:'',
    isshow:false,
    resultinfo:[
      {
        path:"../../images/_pic.png",
        text:"12324",
      },
      {
        path:"../../images/_pic_select.png",
        text:"456"
      }
    ],
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
    var source = new EventSource(url);
  },


  // start(){
  //   var that = this
  //   console.log("开始监听")
  //   that.listener.start()
  //   setTimeout(() => {
  //     that.requestarray =  setInterval(this.requestimg, 500);
  //   }, 1000);
  // },
  // stop(){
  //   var that = this
  //     that.listener.stop()
  //     console.log("停止监听")
  //     clearInterval(that.requestarray)
  //     that.setData({
  //       rectangleshow:false
  //     })
  // },

start(){
  var that = this
  that.setData({
    show:true
  })
  source.onopen = function (event) {
    // ...
  };
  // wx.request({
  //   url: 'url',
  //   header: header,
  //   method: method,
  //   success: (result) => {},
  //   fail: (res) => {},
  //   complete: (res) => {},
  // })
},
stop(){
  var that = this
  that.setData({
    show:false,
  })
},

  // takePhoto() {
  //   this.ctx.takePhoto({
  //     quality: 'high',
  //     success: (res) => {
  //       this.setData({
  //         src: res.tempImagePath,
  //         videoSrc:'',
  //       })
  //     }
  //   })
  // },
  // startRecord() {
  //   this.ctx.startRecord({
  //     success: (res) => {
  //       console.log('startRecord')
  //     }
  //   })
  // },
  // stopRecord() {
  //   this.ctx.stopRecord({
  //     success: (res) => {
  //       this.setData({
  //         // src: res.tempThumbPath,
  //         src:'',
  //         videoSrc: res.tempVideoPath
  //       })
  //     }
  //   })
  // },
  error(e) {
    console.log(e.detail)
  }
})