---
layout:     post
title:      "HTTP Range 请求总结"
subtitle:   "HTTP Range"
date:       2023-06-01
author:     "Hunter"
header-img: "img/http.jpg"
tags:
    - 后端
---
# **HTTP Range 请求总结**

HTTP range 请求允许我们从服务器上只发送HTTP消息的一部分到客户端。这样的部分请求对于大型媒体、具有中断和恢复下载进度的下载文件请求很有帮助。

## **检查服务器是否支持 HTTP Range 请求**

在进行HTTP range 请求之前，先检查服务器是否支持部分请求

如果请求一个资源时， HTTP响应中出现如下所示的 'Accept-Ranges'， 且其值不是none， 那么服务器支持范围请求。

```
curl -I http://i.imgur.com/z4d4kWk.jpg

HTTP/1.1 200 OK
...
Accept-Ranges: bytes
Content-Length: 146515
```

在如上响应中，Accept-Ranges: bytes 代表可以使用字节作为单位来定义请求范围。这里的 Response Headers中的 Content-Length: 146515 则代表该资源的完整大小。

如果站点响应中未返回 Accept-Ranges 响应头，或者其值为none，那么这意味着server不支持HTTP range请求。

## **给服务器发HTTP Range请求**

### **一、单范围请求**

我们可以对一个资源发起单个范围请求：

```
curl http://i.imgur.com/z4d4kWk.jpg -i -H "Range: bytes=0-1023"
```

发出的请求如下：

> GET /z4d4kWk.jpg HTTP/1.1 Host: [i.imgur.com](http://i.imgur.com/) Range: bytes=0-1023

正常情况下 server 返回 206 部分内容响应：

> HTTP/1.1 206 Partial Content Content-Range: bytes 0-1023/146515 Content-Length: 1024 ... (binary content)

这次并非检查server是否支持range请求，故Content-Length表示的是现在请求的范围大小，而Content-Range则表示的是这部分消息在完整资源中的位置。

### **二、多范围请求**

```
curl http://www.example.com -i -H "Range: bytes=0-50, 100-150"
```

用逗号隔开多个范围，即可同时请求多部分资源。

响应如下：

> HTTP/1.1 206 Partial Content Content-Type: multipart/byteranges; boundary=3d6b6a416f9b5 Content-Length: 282 --3d6b6a416f9b5 Content-Type: text/html Content-Range: bytes 0-50/1270

该响应有：

- 206部分响应码：
- Content-Type: multipart/byteranges;boundary=3d6b6a416f9b5——>表示遵循多部分 byterange

每个部分包含自己的Content-Type 和 Content-Range

### **三、条件范围请求**

当继续请求更多资源时，你需要确保被存储的资源在上一帧收到后没有被改变。

If-Range HTTP请求创建了一个带条件的range HTTP请求，如果条件得到满足，range请求将会被发出，server 发回带有适当正文的206 partial content 应答，如果条件不满足则返回完整资源，并显示200 OK状态。这个头可以与Last-Modified 验证程序，或者与 ETag 一起使用。

> If-Range: Wed, 21 Oct 2015 07:28:00 GMT

## **HTTP Range 请求响应**

在处理HTTP Range 请求时，有三个相关的状态：

- 206 Partial Content——> HTTP Range 请求成功
- 416 Requested Range Not Satisfiable status.——> HTTP Range 请求超出界限
- 200 OK——> 不支持范围请求

## **与分块相比**

Transfer-Encoding 请求头允许分块编码，这在服务器给客户端发送大量的数据，且响应总大小直到请求结束才能确定时很有用，如果服务器直接发送数据给客户端而不缓存响应，或者确定具体响应大小的话，会产生延迟。HTTP Range 请求和分块是兼容的，一起用或者不一起用均可。