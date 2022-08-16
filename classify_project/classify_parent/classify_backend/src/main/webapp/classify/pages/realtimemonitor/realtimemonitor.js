// pages/realtimemonitor/realtimemonitor.js

// var flag = true
// // const context = wx.createCameraContext()
// const listener = wx.createCameraContext().onCameraFrame((frame) => {
//   setInterval(function () {
//     console.log(Array.prototype.slice.call(new Uint8Array(frame.data)), frame.width, frame.height)   
// }, 500); 
// })
Page({

  data:{
    // context = wx.createCameraContext()
  },
  onLoad() {
    // this.ctx = wx.createCameraContext()
  },

  open(){
     console.log("开始监听")
     listener.start()
  },
  stop(){
      listener.stop()
      console.log("停止监听")
  },
  takePhoto() {
    this.ctx.takePhoto({
      quality: 'high',
      success: (res) => {
        this.setData({
          src: res.tempImagePath
        })
      }
    })
  },
  startRecord() {
    this.ctx.startRecord({
      success: (res) => {
        console.log('startRecord')
      }
    })
  },
  stopRecord() {
    this.ctx.stopRecord({
      success: (res) => {
        this.setData({
          src: res.tempThumbPath,
          videoSrc: res.tempVideoPath
        })
      }
    })
  },
  error(e) {
    console.log(e.detail)
  }
})