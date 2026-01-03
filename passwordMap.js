// 口令库
const passwordMap = {
    "twgdh": "btzhy",
    "gtyyj": "ybbyb", 
    "pdxdpkq": "1223",
};

// 使用eval或Function动态执行代码
const encrypted = '66756e6374696f6e28297b636f6e736f6c652e6c6f67282253656372657422297d' // 十六进制
eval('0x' + encrypted.split('').map(c => c.charCodeAt(0).toString(16)).join(''))