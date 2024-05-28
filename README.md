# 校园快递超市微信小程序后端接口
## 前端项目：
[校园快递超市微信小程序](https://github.com/ranjingya/miniprogram_express)  

## 项目概述  

### 开发环境  
系统：Ubuntu 22.04  
Python：3.11  
IDE：PyCharm 2024  
数据库：MongoDB 7.0  
Redis：7.0
  
后端分成两层：**视图层**和**数据控制层**（我是这么命名的）  

### 视图层  
负责提供前端请求的路径，同时调用数据控制层的静态方法  
![image](https://github.com/ranjingya/miniprogram_express_backend/assets/109840550/c912a756-01df-44c8-8e4b-9c959ca44b31)

### 数据控制层  
负责与数据库、redis的交互，处理前端请求参数并返回需要的数据  
![image](https://github.com/ranjingya/miniprogram_express_backend/assets/109840550/91242ea6-4c9a-48db-a1ff-3397df0fdfc5)  

### login过滤器  
过滤器负责过滤前端请求  
除了天气和登陆接口，其他都需要经过过滤器以验证token  

![image](https://github.com/ranjingya/miniprogram_express_backend/assets/109840550/2ac1c0b3-8f69-4509-a8d8-365809953345)  

过滤器中实现验证token状态、token无感刷新  
这里每次发放的token有效期都是7天（太长了，但是方便实现）  
每次前端请求到达时验证token中的有效期，如果到了第6天，先删除redis中的此token，重新生成新的并发送给前端，前端接收到新token后先删除保存在localstorage中的旧token，保存此次接收到的token，实现无感刷新  

![IMG_20240528_142422](https://github.com/ranjingya/miniprogram_express_backend/assets/109840550/9bc79e4a-9c0a-480a-b6ca-6f6fb25672a7)
