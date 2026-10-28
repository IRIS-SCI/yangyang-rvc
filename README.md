# 秧秧 · RVC 语音模型（v3 · 48 kHz）

用《鸣潮》秧秧的语音训练的 RVC v2 音色模型。**只发布模型权重，不含任何原始音频。**

> 输入一段任意人声（TTS 或真人），输出同内容、秧秧音色的语音。
> 适合本地跑着玩、做二创、给自己的机器人配音。**禁止商用。**

---

## 一、文件清单

| 文件 | 大小 | 是否必需 | 说明 |
| --- | --- | --- | --- |
| `yangyang_v3_48k.pth` | 约 55 MB | ✅ 必需 | 模型本体（RVC v2 架构，48 kHz，HiFi-GAN 声码器，ContentVec 特征） |
| `yangyang_v3_48k.index` | 约 44 MB | ⬜ 可选 | faiss 检索索引，用来把音色再拉近一点；没有它就把 `index_rate` 设成 0 |
| `yangyang_v2_48k.pth` / `.index` | 55 MB / 69 MB | ⬜ 可选 | 早期版本（7.7 分钟素材、250 epoch），音色更"干净"但更像播音腔，对比用 |

下载方式：**仓库右侧 Releases → `v1.0.0` → Assets**，点开单下。

- 模型文件**不进 git 仓库**（大二进制不适合放版本库），统一挂 Release 附件
- Release 附件单个上限 2 GB，不占 Git LFS 额度，也不需要装 `git lfs`
- 仓库本身只有几十 KB，`git clone` 不会被拖几百 MB

> **关于索引的版本**：完整索引是 125,415 个 768 维向量（377 MB）。发布的是**压缩版**——
> 随机抽样 60,000 个向量 + 8-bit 标量量化（SQ8），44 MB。
> 实测 `k=8` 检索的近邻质量几乎不变（自检 top-1 距离 0.005），`index_rate=0.75` 下的听感差异可以忽略。
> 需要完整索引可以自己用训练特征重建，或用 `shrink_index.py` 的同款方法放大抽样比例。

---

## 二、推理参数（先用这套跑起来）

| 参数 | 推荐值 | 说明 |
| --- | --- | --- |
| `pitch` | `0` | 源音频是女声就用 0；男声源想自然点用 `+12`；想让她的声音更低可以给负数 |
| `index_rate` | `0.75` | 有 index 时用 0.75；想更"贴"参考可以到 1.0，太高会闷；没 index 就设 0 |
| `f0_method` | `rmvpe` | 音高提取，rmvpe 最稳，`harvest` 更平滑但慢 |
| `protect` | `0.33` | 保护清辅音/气声，0.2–0.5 之间调 |
| `filter_radius` | `3` | 默认即可 |
| `volume_envelope` | `1.0` | 1.0 = 保留原始音量起伏，不要设 0（会变平） |

---

## 三、三种用法

### 方式 1：WebUI（最省事）

1. 装一个 RVC 前端：[Applio](https://github.com/IAHispano/Applio) 或 [RVC WebUI](https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI)
2. 把 `yangyang_v3_48k.pth` 放进 `assets/weights/`，`yangyang_v3_48k.index` 放进 `assets/indices/`
3. 打开「推理」页：选模型 → 载入音频 → 参数按上面那张表填 → 转换
4. **48k 模型**要在设置里把采样率选成 48000，否则会有金属音

### 方式 2：命令行（Applio / RVC 自带脚本）

```bash
python infer_cli.py \
  --model assets/weights/yangyang_v3_48k.pth \
  --index assets/indices/yangyang_v3_48k.index \
  --input input.wav \
  --output output.wav \
  --pitch 0 --index-rate 0.75 --f0-method rmvpe --protect 0.33
```

（不同发行版脚本名不一样，Applio 里是 `infer_cli.py` / `run.py`，RVC 原版是 `infer_cli.py`；参数名以你那份为准。）

### 方式 3：Python API

见 [`examples/infer.py`](examples/infer.py)，改成你自己的路径后直接跑：

```bash
python examples/infer.py --input input.wav --output out.wav
```

脚本依赖你本机装好的 RVC/Applio 环境（它 import 的是 `rvc.infer.infer.VoiceConverter`）。

---

## 四、效果与局限（说清楚免得踩坑）

- 音色相似度（WavLM 余弦，对训练集质心）：自测约 **0.68**，她的原始素材自身在 **0.79–0.89**
- **它只换音色，不改语气**：源音频念得平，出来的也平。想要"活人感"要么源音频本身有起伏，要么换 TTS 前端
- 中文 4 声、气声、鼻音（`ng` 尾）偶尔会走形，尤其是很短的句子
- 唱歌可以用：24 秒以内的短句最稳；整首歌建议先分离人声再整轨转换

---

## 五、训练数据（不含音频）

| 项目 | 数值 |
| --- | --- |
| 原始素材 | 41.7 分钟切片（VAD 切分，1289 段） |
| 采样率 | 48 kHz |
| 训练轮数 | 20 epoch / 约 2860 step |
| 特征 | ContentVec + RMVPE f0 |
| 索引 | 由训练切片特征构建的 faiss 索引 |

原始音频**不在本仓库内**，也不提供下载。

---

## 六、许可与声明

- 模型权重以 **CC BY-NC 4.0** 发布：可自由用于个人学习、研究、非商业二创，需署名，**禁止商业用途**。
- 「秧秧」角色及相关素材版权归 **库洛游戏（Kuro Games）** 所有；本模型是非官方的粉丝作品，与官方无关。
- 请勿用于：冒充真人、诈骗、伪造他人言论、任何违法违规用途。
- 如果你是该角色的权利方并希望下架，请开 issue，我会立即删除。

详见 [NOTICE.md](NOTICE.md)。
