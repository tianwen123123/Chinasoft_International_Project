// pages/realtimemonitor/realtimemonitor.js
Page({
  globalData: {
    socketStatus: 'closed',  // 标识是否开启socket
    socketMsgQueue: ['hello'] // 发送的数据，也可以是其他形式
  },
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

  },


  initWebSocket(socket) {
    console.log(socket)
    console.log(11111111)
    socket.on('connect', () => {
        console.log('建立链接')
        socket.emit('message', { 'data': 'I\'m connected!' })
    })
    socket.on('disconnect', () => {
        console.log('连接断开')
        socket.emit('message', { 'data': 'I\'m disconnected!' });
    })
    socket.on('card message', msg => {
        // 接受数据
    })
    socket.on('error message', msg => {
        console.log('error:' + msg)
        
    })
    console.log(socket)
},
start(){
  var that = this
  that.setData({
    show:true,
  })
},
stop(){
  var that = this
  that.setData({
    show:false,
  })
},

  error(e) {
    console.log(e.detail)
  }
})