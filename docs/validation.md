# 归档验证

更新日期：2026-10-20。

## 原工程实践

作者确认原工程此前已完成 TouchWin 编译与硬件验证。本仓库整理触摸屏方案及相关文件，个人负责内容为触摸屏界面和手动控制相关工作。

## 本次公开归档

- 主操作画面 13 页、报警定义 14 条；全部 78 个工程页面（包括系统页）保留。
- 对比原件与公开副本：控件类型、位置和尺寸保留，4647 个地址、动作及相关属性字段比较一致。
- 107 份内嵌资源文件的原始资源数据保留。
- 处理 11 个原非空口令字段、194 个本机路径，移除 1 个锁文件，并统一工程名称及页面抬头。
- 13 个预览图片全部检查；浏览器检查覆盖全部页面切换、图片加载、桌面及移动端布局。
- GitHub Actions 运行 `tools/inspect_hmi.py` 和静态网站打包，属于归档结构检查。

原工程的编译和设备验证为作者此前完成的实践；本次归档检查不代表重新完成了设备下载。公开副本处理说明见 [engineering.md](engineering.md)。

## 文件指纹

公开工程 `engineering/industrial-panel-demo.xjp` 的 SHA-256：

```text
3a6d7f74813db33bae1034f59735e1063123b1774f2f3ad12df6114a045b05ff
```

原件指纹及结构摘要见 [project-summary.json](project-summary.json)，本次检查记录见 [archive-validation.json](archive-validation.json)。

## 本地检查

```bash
python tools/inspect_hmi.py
python tools/build_site.py
```

检查程序按普通 ZIP 与 JSON 数据读取工程，不执行工程中的宏或 .NET 类型。
