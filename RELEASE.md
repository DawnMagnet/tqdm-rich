# 发布指南

## 概览

tqdm-rich 的发布流程使用自动化的 GitHub Actions 工作流程。本文档说明如何发布新版本。

## 前置条件

1. GitHub 账户和对仓库的写入权限
2. PyPI 账户和 API token

## 发布流程

### 1. 准备发布

首先，更新以下文件中的版本号：

- **pyproject.toml**: 更新 `version` 字段
- **CHANGELOG.md**: 添加新版本的更新日志
- **src/tqdm_rich/**init**.py**: 更新 `__version__` 变量

### 2. 提交更改

```bash
git add .
git commit -m "chore: bump version to X.Y.Z"
git push origin main
```

### 3. 创建发布标签

```bash
git tag -a vX.Y.Z -m "Release version X.Y.Z"
git push origin vX.Y.Z
```

### 4. GitHub 自动化流程

当推送标签时，GitHub Actions 会自动：

1. ✅ 运行所有测试
2. ✅ 执行代码质量检查
3. ✅ 构建源码包和 wheel 包
4. ✅ 创建 GitHub Release
5. ✅ 上传构建产物到 Release
6. ✅ 发布到 PyPI（如果配置了 token）

## 配置 PyPI 发布

要启用自动发布到 PyPI，需要在 GitHub 设置中添加 Secret：

1. 进入仓库设置 → Secrets and variables → Actions
2. 点击 "New repository secret"
3. 添加 `PYPI_API_TOKEN`：
   - 获取方式：在 PyPI 账户中生成 API token
   - 在 https://pypi.org/manage/account/tokens/ 创建 token

## 工作流文件说明

### tests.yml

- 在每次 push 和 PR 时运行
- 在多个 Python 版本和操作系统上测试
- 运行 linting、formatting 和类型检查
- 上传覆盖率报告到 Codecov

### release.yml

- 在创建版本标签时触发
- 构建分发包
- 创建 GitHub Release
- 上传构建产物
- 发布到 PyPI

### quality.yml

- 在每次 push 和 PR 时运行
- 执行代码质量检查
- 生成覆盖率报告
- 上传 HTML 覆盖率报告为构件

## 版本命名规约

遵循 [语义化版本](https://semver.org/lang/zh-CN/) 规范：

- **主版本号 (MAJOR)**：不兼容的 API 更改
- **次版本号 (MINOR)**：向后兼容的功能添加
- **修订号 (PATCH)**：向后兼容的问题修复

### 版本标签格式

使用 `vX.Y.Z` 格式，例如：

- `v0.1.0` - 首次发布
- `v0.1.1` - 补丁版本
- `v0.2.0` - 新功能版本
- `v1.0.0` - 稳定版本

## 发布检查清单

在创建发布标签前，确保：

- [ ] 所有测试都通过 (`pytest tests/`)
- [ ] 代码格式正确 (`black src/ tests/`)
- [ ] 没有 linting 错误 (`ruff check src/ tests/`)
- [ ] 类型检查通过 (`mypy src/`)
- [ ] CHANGELOG.md 已更新
- [ ] pyproject.toml 中版本已更新
- [ ] **init**.py 中 **version** 已更新
- [ ] README.md 中的文档已更新
- [ ] Git 历史记录干净（无未提交的更改）

## 故障排除

### Release 工作流失败

1. 检查 GitHub Actions 日志以查看具体错误
2. 常见问题：
   - `PYPI_API_TOKEN` 未配置或已过期
   - 版本号不符合 Python 版本规范
   - 依赖冲突

### 发布到 PyPI 失败

1. 确保 `PYPI_API_TOKEN` 有效
2. 检查版本号是否唯一（不能发布已存在的版本）
3. 查看 PyPI 的 API 错误消息

## 手动发布

如果自动工作流失败，可以手动发布：

```bash
# 构建分发包
uv build

# 发布到 PyPI（需要安装 twine）
pip install twine
twine upload dist/*
```

## 发布后

1. 验证 PyPI 上已发布新版本：https://pypi.org/project/tqdm-rich/
2. 验证 GitHub Release 已创建：https://github.com/DawnMagnet/tqdm-rich/releases
3. 在新闻或社交媒体上宣布发布

## 相关链接

- [PyPI tqdm-rich 项目](https://pypi.org/project/tqdm-rich/)
- [GitHub 仓库](https://github.com/DawnMagnet/tqdm-rich)
- [GitHub Actions 文档](https://docs.github.com/en/actions)
- [语义化版本规范](https://semver.org/lang/zh-CN/)
