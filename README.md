# 🚪 智能人脸门禁系统

基于 **华为云 FRS（人脸识别服务）** 和 **SIS（语音交互服务）** 构建的智能门禁管理系统，搭载 **Gradio** Web 界面，集成活体检测、尾随检测、语音迎宾、访问日志等企业级功能。

## 功能概览

| 功能 | 说明 |
|------|------|
| **🔐 人脸验证开门** | 华为云 FRS 1:N 人脸搜索，快速识别员工身份并开启门禁 |
| **🛡️ 静默活体检测** | 单张图片判断是否为真人，防止照片/视频/屏幕攻击 |
| **🚨 尾随检测** | 基于时间窗口检测多人同时通行 & 短时高频通行告警 |
| **🎙️ 智能语音迎宾** | 华为云 SIS TTS 合成欢迎语音，按时间段自动切换问候语 |
| **👤 员工管理** | 人脸注册（含质量校验）、列表查看、删除 |
| **🔄 1:1 人脸比对** | 上传两张照片，判断是否为同一人，用于人工复核 |
| **📜 访问日志** | 完整记录每次验证结果（成功/失败/告警），支持按条数查询 |
| **🌐 Web 界面** | 基于 Gradio 构建，支持摄像头实时采集和图片上传 |

## 系统架构

```
┌─────────────────────────────────────────────────────────┐
│                     Web 界面 (Gradio)                     │
│  ┌─────────┐ ┌──────────┐ ┌────────┐ ┌──────┐ ┌──────┐  │
│  │ 门禁验证 │ │ 员工注册  │ │人脸比对│ │员工管理│ │访问日志│ │
│  └────┬────┘ └────┬─────┘ └───┬────┘ └──┬───┘ └──┬───┘  │
└───────┼───────────┼───────────┼─────────┼────────┼──────┘
        │           │           │         │        │
┌───────▼───────────▼───────────▼─────────▼────────▼──────┐
│                   业务逻辑层 (features.py)                 │
│  注册 ├ 验证 ├ 比对 ├ 列表 ├ 删除 ├ 日志                   │
└───────┬───────────┬───────────┬─────────┬────────────────┘
        │           │           │         │
┌───────▼──┐ ┌──────▼────┐ ┌───▼────┐ ┌──▼───────────┐
│face_     │ │tts_       │ │security│ │storage        │
│service.py│ │service.py │ │.py     │ │.py            │
│ (FRS SDK) │ │(SIS TTS)  │ │尾随检测 │ │JSON 持久化     │
└───────┬──┘ └──────┬────┘ └────────┘ └───────────────┘
        │           │
┌───────▼───────────▼────────────────────────────────────┐
│                    华为云 API                             │
│   FRS (人脸识别)         SIS (语音交互)                   │
└─────────────────────────────────────────────────────────┘
```

## 技术栈

- **人脸识别** — 华为云 FRS（Face Recognition Service）
- **语音合成** — 华为云 SIS（Speech Interaction Service）
- **Web 框架** — Gradio（Python UI 框架）
- **数据存储** — 本地 JSON 文件（线程安全）
- **运行环境** — Python 3.8+

## 快速开始

### 前置条件

- Python 3.8+
- 华为云账号，已开通 [FRS](https://console.huaweicloud.com/frs) 和 [SIS](https://console.huaweicloud.com/sis)
- 在[我的凭证](https://console.huaweicloud.com/iam)中获取 AK/SK/项目 ID

### 安装

```bash
# 克隆仓库
git clone https://github.com/<your-username>/face-access-control.git
cd face-access-control

# 安装依赖
pip install -r requirements.txt
```

### 配置

设置华为云凭证（推荐使用环境变量，避免密钥泄露）：

```bash
# Windows PowerShell
$env:HUAWEI_AK = "your-access-key"
$env:HUAWEI_SK = "your-secret-key"
$env:HUAWEI_PROJECT_ID = "your-project-id"

# Linux / macOS
export HUAWEI_AK="your-access-key"
export HUAWEI_SK="your-secret-key"
export HUAWEI_PROJECT_ID="your-project-id"
```

或在 `config.py` 中直接修改默认值（仅限本地调试）：

| 环境变量 | 说明 | 默认值 |
|---------|------|--------|
| `HUAWEI_AK` | 华为云 Access Key | — |
| `HUAWEI_SK` | 华为云 Secret Key | — |
| `HUAWEI_PROJECT_ID` | 华为云项目 ID | — |
| `HUAWEI_REGION` | FRS 服务区域 | `cn-north-4` |
| `SIS_REGION` | SIS 服务区域 | `cn-north-4` |
| `FACE_SET_NAME` | 人脸库名称 | `employee_db` |
| `SIMILARITY_THRESHOLD` | 人脸搜索相似度阈值 | `0.75` |
| `QUALITY_THRESHOLD` | 人脸质量分阈值 | `0.4` |
| `ENABLE_VOICE` | 是否开启语音迎宾 | `True` |

### 运行

```bash
python app.py
```

启动后访问 **http://127.0.0.1:6006** 即可打开门禁系统界面。

## 使用指南

### 门禁验证流程

1. 进入 **门禁验证** 标签页
2. 通过摄像头拍照或上传照片
3. 点击 **开始验证**，系统自动执行：

```
活体检测 → 人脸检测 → 质量检查 → 尾随检测 → 1:N 身份搜索 → 记录日志 → 语音播报
```

### 员工注册流程

1. 进入 **员工注册** 标签页
2. 输入员工编号、姓名
3. 上传或拍摄人脸照片
4. 系统自动检测人脸质量分，合格后注册到华为云人脸库并保存到本地

## 项目结构

```
├── app.py              # 应用入口，初始化服务并组装 Gradio UI
├── config.py           # 全局配置（密钥、阈值、功能开关）
├── face_service.py     # 华为云 FRS SDK 封装（检测/入库/搜索/比对/活体）
├── features.py         # 核心业务逻辑（注册/验证/比对/日志/管理）
├── ui.py               # Gradio Web 界面（含 HTML 结果卡片渲染）
├── security.py         # 尾随检测器（时间窗口 + 高频通行检测 + 告警冷却）
├── storage.py          # JSON 文件存储（线程安全，员工库 + 访问日志）
├── tts_service.py      # 华为云 SIS TTS 语音合成（含本地缓存）
├── test_storage.py     # 存储层单元测试（文件不存在/空文件/损坏/并发）
├── testing.py          # 各模块集成测试脚本（按需取消注释运行）
└── requirements.txt    # Python 依赖
```

## 安全特性

| 特性 | 说明 |
|------|------|
| **静默活体检测** | 单张图片即可判断真伪，无需用户配合动作 |
| **尾随检测** | 开门时画面 ≥2 张人脸即告警，5 秒冷却防刷屏 |
| **高频通行检测** | 3 秒内开门 ≥3 次触发告警 |
| **人脸质量过滤** | 质量分低于阈值时拒绝注册/验证，确保识别精度 |
| **多线程安全** | 存储层使用锁机制，支持并发写入 |

## 测试

```bash
# 存储层单元测试
python test_storage.py

# 集成测试（取消注释 testing.py 中对应测试块后运行）
python testing.py
```


