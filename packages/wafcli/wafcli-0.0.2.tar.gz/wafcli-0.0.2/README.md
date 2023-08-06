# 腾讯T-Sec Web应用防火墙命令行工具
## 安装
```bash
pip install wafcli
```
## 配置
在用户目录下面创建一个`.waf`的目录,目录里面新建一个`waf.json`的配置文件
### linux
~/.waf/waf.json

### windows
c:\Users\xxxx\.waf\waf.json

### 配置项
- secret_id
- secret_key
- region
- edition (sparta-waf, clb-waf, cdn-waf)

