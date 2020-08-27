

[RFC 7519](https://link.zhihu.com/?target=https%3A//tools.ietf.org/html/rfc7519)

jwt就是一种**特殊格式**的token。普通的oauth2颁发的就是一串随机hash字符串，本身无意义，而jwt格式的token是有特定含义的，分为三部分：

- 头部`Header`
- 载荷`Payload`
- 签名`Signature`

这三部分均用base64进行编码，当中用`.`进行分隔，一个典型的jwt格式的token类似`xxxxx.yyyyy.zzzzz`。

第一部分是请求头由两部分组成，alg与typ,第一个指定的是算法，第二指定的是类型。

```json
{
  "alg": "HS256",
  "typ": "JWT"
}
```

第二部分是主体信息组成,用来存储JWT基本信息，或者是我们的信息。

根据JWT的标准，这些claims可以分为以下三种类型： 

-  Reserved claims

    它的含义就像是编程语言的保留字一样，属于JWT标准里面规定的一些claim。JWT标准里面定好的claim有：

    iss(Issuser)：代表这个JWT的签发主体；

    sub(Subject)：代表这个JWT的主体，即它的所有人；

    aud(Audience)：代表这个JWT的接收对象；

    exp(Expiration time)：是一个时间戳，代表这个JWT的过期时间；

    nbf(Not Before)：是一个时间戳，代表这个JWT生效的开始时间，意味着在这个时间之前验证JWT是会失败的；

    iat(Issued at)：是一个时间戳，代表这个JWT的签发时间；

    jti(JWT ID)：是JWT的唯一标识。

- Public claims

    

-  Private claims

    这个指的就是自定义的claim。比如前面那个结构举例中的admin和name都属于自定的claim。这些claim跟JWT标准规定的claim区别在于：JWT规定的claim，JWT的接收方在拿到JWT之后，都知道怎么对这些标准的claim进行验证；而private claims不会验证，除非明确告诉接收方要对这些claim进行验证以及规则才行。

第三部分为签名

```javascript
HMACSHA256(
  base64UrlEncode(header) + "." +
  base64UrlEncode(payload),
  secret)
```



