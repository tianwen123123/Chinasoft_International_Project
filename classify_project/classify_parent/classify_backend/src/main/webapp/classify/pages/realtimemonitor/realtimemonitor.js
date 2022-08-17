// pages/realtimemonitor/realtimemonitor.js
Page({

  data:{
    imageArray:{},
    left:0,
    top:0,
    rectangleshow:false,
  },
  onLoad() {
    var that = this
    that.ctx = wx.createCameraContext()
    var count=0
    that.listener =  that.ctx.onCameraFrame((frame) => {
      count+=1
      if(count==30){
        var array = Array.prototype.slice.call(new Uint8Array(frame.data))
        // console.log(Array.prototype.slice.call(new Uint8Array(frame.data)), frame.width, frame.height)
        that.setData({
          imageArray:array
        })  
        count=0 
      }
})
},
  onShow(){
    var that = this
    that.setData({
      imageArray:{},
    })
  },
  requestimg(){
    var that = this
    console.log(that.data.imageArray)
      that.setData({
        left: (that.data.left+10)<=280?(that.data.left+10):10,
        top: (that.data.top+10)<=330?(that.data.top+10):10,
      })
      console.log(that.data.left)
    // wx.request({
    //   url: '',
    //   method:'',
    //   success: (result) => {},
    //   fail: (res) => {},
    //   complete: (res) => {},
    // })
    that.setData({
      rectangleshow:true
    })
  },
  start(){
    var that = this
    console.log("开始监听")
    that.listener.start()
    setTimeout(() => {
      that.requestarray =  setInterval(this.requestimg, 500);
    }, 1000);
  },
  stop(){
    var that = this
      that.listener.stop()
      console.log("停止监听")
      clearInterval(that.requestarray)
      that.setData({
        rectangleshow:false
      })
  },

  takePhoto() {
    this.ctx.takePhoto({
      quality: 'high',
      success: (res) => {
        this.setData({
          src: res.tempImagePath,
          videoSrc:'',
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
          // src: res.tempThumbPath,
          src:'',
          videoSrc: res.tempVideoPath
        })
      }
    })
  },
  error(e) {
    console.log(e.detail)
  }
})