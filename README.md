# 炉石卡牌资源提取器

## 简单介绍
提供一个用于解析炉石传说卡牌图片和音频资源的命令行工具。

## 如何使用

### 基本用法
如果你已经安装了python，可以直接运行脚本
```bash
python -m src [OPTIONS]
```
如果你使用的release版本，则
```bash
card-asset [OPTION]
```


### 参数说明

#### 输入输出参数
- `--input`：炉石传说资源文件夹路径
  - 默认值：自动检测游戏安装路径
  - 例如：`--input "C:\Program Files (x86)\Hearthstone"`

- `--output`：提取资源的输出文件夹路径
  - 默认值：`./output`
  - 例如：`--output ./extracted_assets`

#### 资源类型参数
- `--image`：要提取的图片类型
  - 可选值：
    - `all`
    - `normal`
    - `signature`
    - `none`
  - 默认值：`none`
  - 例如：`--image all` 或 `--image normal,signature`

- `--audio`：要提取的音频类型
  - 可选值：
    - `all`
    - `none`
    - `additional-play`
    - `attack`
    - `death`
    - `lifetime`
    - `trigger`
    - `sub-option`
    - `reset-game`
    - `sub-spell`
    - `emote`
    - `play`
  - 默认值：`none`
  - 例如：`--audio attack,death`

#### 语言参数
- `--locale`：要提取的语言版本
  - 可选值：
    - `all`
    - `enus`
    - `zhcn`
    - `zhtw`
    - `jajp`
    - `eses`
    - `kokr`
    - `ptbr`
    - `ruru`
    - `frfr`
    - `esmx`
    - `itit`
    - `dede`
    - `plpl`
    - `thth`
  - 默认值：`zhcn`
  - 例如：`--locale zhcn,enus`

#### 卡牌ID参数
- `--id`：要提取的卡牌ID列表（逗号分隔）
  - 默认值：`all`（提取所有卡牌）
  - 例如：`--id HERO_01,HERO_02`

#### 其他参数
- `-v`、`--version`：显示工具版本
  - 例如：`--version`

- `--ensure_ascii`：确保输出使用 ASCII 编码
  - 默认值：`false`（使用 UTF-8 编码）
  - 例如：`--ensure_ascii`

- `--enable_sub_struct`：控制是否在子文件夹输出struct.json
  - 默认值：`false`（只在card_id文件夹下输出总体的struct.json）
  - 例如：`--sub_struct`（在card_id文件夹和子文件夹下都输出struct.json）
  - 注意：无论是否开启此参数，都会在card_id文件夹下输出总体的struct.json

- `--no_assets`：仅输出struct.json，不输出资源文件
  - 默认值：`false`
  - 例如：`--no_assets`
  - 说明：给想要快速查看文件结构的人使用

- `--merged_struct`：将output/{card_id}/struct.json合并为output/struct.json
  - 默认值：`false`
  - 例如：`--merged_struct`
  - 注意：如果开启了enable_sub_struct，那么output/{card_id}/struct.json仍然会输出；否则，仅在output/下输出合并后的struct.json

- `--log_level`：设置日志记录等级
  - 默认值：`info`
  - 可选值：`debug`, `info`, `warning`, `error`, `critical`
  - 例如：`--log_level debug` 或 `--log_level error`

### 使用示例

1. 提取所有卡牌的普通图片和攻击音频（中文）：
```bash
card-asset --image normal --audio attack
```

2. 提取特定卡牌的所有图片和音频（英文）：
```bash
card-asset --id HERO_01,HERO_02 --image all --audio all --locale enus
```

3. 自定义输入输出路径：
```bash
card-asset --input "C:\Hearthstone" --output ./my_assets --image all
```

## 使用风险
- 本程序需要读取炉石传说游戏文件夹中的资源文件，某些安全软件可能会将其判定为风险程序。
- 请确保您只在自己的计算机上使用本工具，并遵守相关法律法规。

## 如何构建可执行文件

### 安装项目
```bash
uv sync
```

### 执行构建命令
```bash
build
```

### 构建结果
构建完成后，可执行文件将生成在`dist`目录中：
- Windows: `dist/card-asset.exe`

## 许可证
ISC License

Copyright (c) 2025 Octasin

Permission to use, copy, modify, and/or distribute this software for any purpose with or without fee is hereby granted, provided that the above copyright notice and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.