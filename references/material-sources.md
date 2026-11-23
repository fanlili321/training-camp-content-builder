# 常用素材来源与处理

## 原图去哪找

- 聊天里发来的图片会被压缩（曾收到只有187像素宽的长图），**不能直接拿来裁图**。要去飞书原始消息里下载原图。
- **股市牛熊信号板长图**：党振铭每天以卡片形式发在「226课程群」（chat_id `oc_ad278b7a15d31ab7a5ced19569769db8`），标题如“A股牛熊市信号板｜2026年11月19日”，卡片里带完整长图的 img_key。下载方式：
  ```bash
  lark-cli im +chat-messages-list --as user --chat-id oc_ad278b7a15d31ab7a5ced19569769db8 --start <起始时间> --order desc --no-reactions
  lark-cli im +messages-resources-download --as user --message-id <卡片消息om_id> --file-key <img_key> --type image --output long.png
  ```
  原图约1200像素宽、一万多像素高。

## 牛熊信号板拆成定量、定性两张图

课程里讲牛熊信号板时，用两张三栏图分别展示定量信号和定性信号，样式参照「投顾第一课」里的旧图：每个小卡片保留原图底色（定量灰蓝、定性橙色），三栏排开，栏间留白。

运行 [`assets/split_signal_board.py`](../assets/split_signal_board.py)：

```bash
python3 split_signal_board.py long.png 20261119 输出目录
```

- 2026-11-19版长图共14个小图：定量5个，定性9个（比旧图多“核心宽基ETF净流入”）。
- 定量排法：左栏星级+巴菲特，中栏市净率百分位，右栏市场在波动中上涨+股债性价比。
- 定性排法按长图顺序每栏3个：融资余额/成交额/ETF净流入，新股破发/全收益与M2/风格基金规模，新发基金规模/限购占比/市场消息。
- 指标数量或顺序变了，脚本会报错，按提示改脚本里的分组。
- 图里的指标变了，正文里介绍定量、定性信号的那句列表要同步改。
