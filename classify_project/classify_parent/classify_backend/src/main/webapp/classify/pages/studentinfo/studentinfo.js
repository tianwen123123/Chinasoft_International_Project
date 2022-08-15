// pages/studentinfo/studentinfo.js
Page({

  /**
   * 页面的初始数据
   */
  data: {
    date:"",
    range:["00:00-01:59","02:00-03:59","04:00-05:59","06:00-07:59","08:00-09:59",
          "10:00-11:59","12:00-13:59","14:00-15:59","16:00-17:59","18:00-19:59",
          "20:00-21:59","22:00-23:59"],
    time:"",
    studentname:"",
    studentId:"",
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad(options) {

  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady() {

  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow() {

  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide() {

  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload() {

  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh() {

  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom() {

  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage() {

  },
  studentnameInput:function(e){
    let studentname = e.detail.value
    this.setData({
      studentname:studentname
    })
  },
  studentIdInput:function(e){
    let studentId = e.detail.value
    this.setData({
      studentId:studentId
    })
  },
  bindDateChange(e){
    console.log(e.detail.value)
    this.setData({
      date:e.detail.value
    })
  },
  bindtimeChange(e){
    console.log(e.detail.value)
    let index = e.detail.value
    this.setData({
      time:this.data.range[index]
    })
  },
  formSubmit(e){
    console.log(e)
    wx.request({
      url: 'url',
      data: data,
      dataType: dataType,
      enableCache: true,
      enableHttp2: true,
      enableQuic: true,
      header: header,
      method: method,
      responseType: responseType,
      timeout: 0,
      success: (result) => {},
      fail: (res) => {},
      complete: (res) => {},
    })
  }
})