正方教务系统验证码识别 (CNN)


# grpc server
## 运行
```shell
    python grpcServer/ImageToLabelServer.py
```
## 使用
```shell
    // 使用参考 grpcServer/testClient.py
```
# http server
## 运行
```shell
  python httpServer/imageToLabelServer.py
```

## 使用
接口：

    | 接口地址    | 参数             |  说明                 |
    | --------   | ---------------: | :------------------: |
    | /image_to_label  | 文件字段名 captcha      |   传入验证码文件返回验证码字符    |

# 返回

```javascript
    {'code': 1, 'captcha_label': '返回的验证码字符串'}
```
```javascript
    {'code': -1, 'captcha_label': '验证码文件有误'}
```
```javascript
    {'code': -1, 'captcha_label': '请上传验证码文件'}
```