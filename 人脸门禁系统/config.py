import os


class Config:
    """项⽬配置集中定义｡
    说明:
    大多数配置项支持从环境变量读取(便于部署/避免写死密钥)
    这⾥保留了默认值,适合本地快速跑通 demo;⽣产环境请务必使⽤环境变量覆盖
    """
    # ==================== 华为云 FRS(人脸识别)配置 ====================
    # 从环境变量读取(建议⽣产/演示都⽤环境变量覆盖,避免泄露)
    HUAWEI_AK = os.getenv('HUAWEI_AK', 'HPUAAWDHP0BM9NC8AEC5')
    HUAWEI_SK = os.getenv('HUAWEI_SK', '8VTItCw5Lg1GIL8TUFeN2IvFFnsfNu2qu0XsnMv9')
    HUAWEI_PROJECT_ID = os.getenv('HUAWEI_PROJECT_ID', 'c8b642bd783941eeb4a29eab4577628f')
    HUAWEI_PROJECT_NAME = os.getenv('HUAWEI_PROJECT_NAME', 'cn-north-4')
    HUAWEI_REGION = os.getenv('HUAWEI_REGION', 'cn-north-4')

    # 人脸库名称:注册入库与⻔禁验证搜索必须一致
    FACE_SET_NAME = os.getenv('FACE_SET_NAME', 'employee_db')
    FACE_SET_CAPACITY = 10000

    # 阈值类配置:决定“严格程度”(越严格越安全,但可能更容易拒绝)
    SIMILARITY_THRESHOLD = 0.75
    QUALITY_THRESHOLD = 0.4

    # ==================== 活体检测配置 ====================
    LIVE_DETECT_THRESHOLD = 0.7
    # True 时会尝试动作活体(一般要求来⾃摄像头);否则⽤静默活体
    USE_ACTION_LIVE = False

    # ==================== 语⾳合成(SIS)配置 ====================
    SIS_REGION = os.getenv('SIS_REGION', 'cn-north-4')
    # 允许通过环境变量覆盖 endpoint
    SIS_ENDPOINT = os.getenv('SIS_ENDPOINT', '')
    VOICE_TYPE = 'xiaoyan'
    VOICE_SPEED = 0
    VOICE_VOLUME = 80

    # ==================== 尾随检测配置 ====================
    TAILGATING_WINDOW = 3
    TAILGATING_THRESHOLD = 2

    # ==================== 活体检测配置（新增） ====================
    LIVE_DETECT_THRESHOLD = 0.7  # 活体置信度阈值（主要⽤于展示）
    USE_ACTION_LIVE = False  # False=静默活体（单张图），True=动作活体

    # ==================== 语⾳合成(SIS)配置（新增） ====================
    SIS_REGION = os.getenv('SIS_REGION', 'cn-north-4')
    SIS_ENDPOINT = os.getenv('SIS_ENDPOINT', '')
    VOICE_TYPE = 'xiaoyan'  # ⾳⾊
    VOICE_SPEED = 0  # 语速：-500~500
    VOICE_VOLUME = 80  # ⾳量：0~100
    ENABLE_VOICE = True  # 语⾳开关
    # ==================== 尾随检测配置（新增） ====================
    TAILGATING_WINDOW = 3  # 检测时间窗⼝（秒）
    TAILGATING_THRESHOLD = 2  # 触发告警的⼈脸数量阈值
