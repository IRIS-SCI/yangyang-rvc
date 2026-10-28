# 发布到 GitHub

> **本仓库采用的方案：仓库只放文档和脚本，四个模型文件挂在 Release 附件。**
> 原因：`.index` 单文件 378 MB，超过 GitHub 普通文件 100 MB 的硬上限；而 Release 附件上限 2 GB，
> 不占用 Git LFS 免费额度，别人 `git clone` 也不会被拖 557 MB。

---

## 步骤 1：推仓库（只有几十 KB）

1. 在 GitHub 网页新建一个空仓库（不要勾 README / .gitignore / license）
2. 本地执行：

```bash
cd E:/rvc-yangyang/github/yangyang-rvc
git remote add origin https://github.com/<你的用户名>/yangyang-rvc.git
git branch -M main
git push -u origin main
```

## 步骤 2：传模型（Release 附件）

网页进仓库 → 右侧 **Releases** → *Draft a new release*

- **Tag**：`v1.0.0`（新建 tag）
- **Title**：`秧秧 RVC v3 48k`
- **描述**：可以直接粘 README 第一节的「文件清单」表格
- **附件**（拖进 "Attach binaries" 区域）：
  - `models/yangyang_v3_48k.pth`（54.9 MB）
  - `models/yangyang_v3_48k.index`（377.8 MB）
  - `models/yangyang_v2_48k.pth`（54.9 MB，可选）
  - `models/yangyang_v2_48k.index`（69.0 MB，可选）
- 点 **Publish release**

传 378 MB 那个可能要几分钟，网页会显示进度条，别中途关页面。

> 装过 `gh` CLI 的话可以一条命令搞定：
> ```bash
> gh release create v1.0.0 models/yangyang_v3_48k.pth models/yangyang_v3_48k.index \
>   --title "秧秧 RVC v3 48k" --notes "见 README 的文件清单"
> ```

## 步骤 3：检查

- 仓库首页右侧出现 **Releases → v1.0.0**，点进去能看到 Assets 列表
- 仓库文件列表里**没有** `.pth` / `.index`——这是正常的，文件在 Releases 里
- README 里「下载方式」那段引导能看明白

---

## 备选：改用 Git LFS（模型随仓库一起）

如果你确实希望 `git clone` 一次就带上模型：

```bash
cd E:/rvc-yangyang/github/yangyang-rvc
git lfs install
# 把 .gitignore 里 models/*.pth 和 models/*.index 两行删掉
git lfs track "models/*.pth" "models/*.index"
git add .gitattributes models/
git commit -m "chore: 用 LFS 纳入模型权重"
git push
```

**代价**：免费账号 LFS 只有 1 GB 存储 + 1 GB/月流量。这套 557 MB，等于一个月只够 1-2 个人完整 clone；
超了 LFS 下载会被拒（仓库本身仍可访问）。

---

## 备选：只把 `.pth` 放进仓库

`.pth` 只有 55 MB，普通 git 允许（上限 100 MB），`.index` 仍挂 Release：

```bash
# .gitignore 里只保留 models/*.index，删掉 models/*.pth 那行
git add models/yangyang_v3_48k.pth
git commit -m "feat: 加入 v3 模型本体（index 见 Release）"
```

---

## 常见问题

**Q: 推送时报 `remote: error: GH001: Large files detected`？**
有 `.index` 被加进提交了。`git rm --cached models/*.index`，确认 `.gitignore` 生效后重新提交。

**Q: 之前误提交过大文件，怎么清？**
本仓库只有一次提交，最省事的做法是删掉 `.git` 重新 `git init`：
```bash
rm -rf .git && git init && git add -A && git commit -m "init"
```

**Q: Release 附件国内下载慢？**
可以同时传到蓝奏云/夸克网盘，在 README 里补一行备用链接。
