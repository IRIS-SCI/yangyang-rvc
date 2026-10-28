# 发布到 GitHub 的三种方式

> 结论先说：**`.pth`（55 MB）可以直接提交；`.index`（378 MB）不行**——GitHub 单个文件硬上限 100 MB，
> 超了会被拒绝推送。所以 `.index` 只能走 Release 附件或 Git LFS。

---

## 方案 A（推荐）：仓库只放说明，模型挂 Release

仓库体积小、克隆快，下载者点一次就行。

1. 在 GitHub 网页新建一个空仓库（不要勾选 README / .gitignore）
2. 本地执行：

```bash
cd E:/rvc-yangyang/github/yangyang-rvc
git remote add origin https://github.com/<你的用户名>/yangyang-rvc.git
git branch -M main
git push -u origin main
```

3. 网页进仓库 → 右侧 **Releases** → *Draft a new release*
   - Tag：`v1.0.0`
   - 标题：`秧秧 RVC v3 48k`
   - 说明：粘一段 README 的「文件清单」
   - 附件（拖动上传）：
     - `models/yangyang_v3_48k.pth`（55 MB）
     - `models/yangyang_v3_48k.index`（378 MB）
     - 可选：`models/yangyang_v2_48k.pth` + `.index`
   - 发布

> Release 单个附件上限 2 GB，378 MB 完全没问题。

---

## 方案 B：用 Git LFS 把模型也纳入仓库

适合你想 `git clone` 一次就拿到模型的情况。**注意免费额度**：LFS 存储 1 GB、流量 1 GB/月，
一次完整克隆就吃掉 430 MB 流量。

```bash
cd E:/rvc-yangyang/github/yangyang-rvc
git lfs install
git lfs track "models/*.pth" "models/*.index"
git add .gitattributes
git add models/yangyang_v3_48k.pth models/yangyang_v3_48k.index
git commit -m "chore: 用 LFS 加入模型权重"
git remote add origin https://github.com/<你的用户名>/yangyang-rvc.git
git push -u origin main
```

`.gitignore` 里默认忽略了 `models/*.pth` 和 `models/*.index`，方案 B 需要先把这两行删掉，
或者用 `git add -f` 强加。`.gitattributes` 里的 LFS 规则已经写好了。

---

## 方案 C：只传 `.pth`，不传 `.index`

`.index` 是**可选**的：没有它把 `index_rate` 设成 `0` 也能用，只是音色贴合度略降（自测 0.71 → 0.68 左右）。

```bash
# 删掉 .gitignore 里 models/*.pth 那一行（保留 *.index）
git add models/yangyang_v3_48k.pth
git commit -m "feat: 加入 v3 48k 模型权重"
```

55 MB 在普通 git 里完全合法，缺点是之后每次克隆都要拉这 55 MB 的历史。

---

## 常见问题

**Q: 推送时报 `remote: error: GH001: Large files detected`？**
`.index` 被加进提交了。执行 `git rm --cached models/yangyang_v3_48k.index`，确认 `.gitignore` 生效后重新提交，然后
`git push --force`（如果上一次推送被拒，本地还没推上去，正常 push 即可）。

**Q: 历史上已经提交过大文件怎么办？**
用 `git filter-repo` 或 BFG 清理，或者最省事：删掉本地 `.git` 重新 `git init` + 提交（本仓库只有一次提交，重建成本几乎为零）。

**Q: 想让别人不用翻墙下载？**
Release 附件走的是 GitHub 的 CDN，国内偶尔慢；可以同时传到蓝奏云/夸克网盘，README 里补一个备用链接。
