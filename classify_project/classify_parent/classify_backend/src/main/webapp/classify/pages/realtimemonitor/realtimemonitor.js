// pages/realtimemonitor/realtimemonitor.js
Page({

  data:{
  },
  onLoad() {
    this.ctx = wx.createCameraContext()
    this.listener =  this.ctx.onCameraFrame((frame) => {
      console.log(Array.prototype.slice.call(new Uint8Array(frame.data)), frame.width, frame.height)   
})
  },
  start(){
    console.log("开始监听")
     this.listener.start()
  },
  stop(){
      this.listener.stop()
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