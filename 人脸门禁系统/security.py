import time
from collections import deque


class TailgatingDetector:
    """尾随检测器 - 维护检测状态，防⽌尾随和⾼频通⾏。"""

    def __init__(self, window_seconds: int, threshold: int):
        """初始化尾随检测器。
        参数:
        window_seconds: 检测时间窗⼝（秒），超过窗⼝的历史记录会被丢弃
        threshold: 同⼀帧/同⼀次开⻔检测到 >= threshold 个脸则告警
        """
        self.window_seconds = window_seconds  # 默认3秒
        self.threshold = threshold  # 默认2⼈
        self.passing_records = deque(maxlen=50)  # 通⾏记录队列
        self.last_open_time = 0  # 最后⼀次开⻔时间
        self.alert_cooldown = 0  # 告警冷却时间戳

    def check_tailgating(self, face_count, door_opening=False):
        """执⾏⼀次尾随检测。
        检测规则：
        1. 尾随告警：开⻔时画⾯出现 >= threshold 张⼈脸
        2. ⾼频告警：3秒内开⻔次数 >= 3次
        参数:
        face_count: 当前画⾯检测到的⼈脸数量
        door_opening: 是否把这次检测视为"将要开⻔"的事件
        返回:
        (is_alert, message, alert_type)
        - is_alert: bool，是否触发告警
        - message: str，告警描述
        - alert_type: str，告警类型（tailgating/frequency/None）
        """

        current_time = time.time()

        # 清理时间窗⼝外的记录
        while (
            self.passing_records
            and current_time - self.passing_records[0]['time'] > self.window_seconds
        ):
            self.passing_records.popleft()

        # 记录当前检测
        self.passing_records.append({
            'time': current_time,
            'face_count': face_count,
            'door_opening': door_opening,
        })

        # 告警冷却：避免同⼀种异常连续刷屏
        if current_time < self.alert_cooldown:
            return False, "冷却中", None

        # 规则1：开⻔时画⾯出现多张⼈脸
        if door_opening and face_count >= self.threshold:
            self.alert_cooldown = current_time + 5  # 5秒冷却
            return True, f" 尾随告警：检测到{face_count}⼈同时通过（授权1⼈）", "tailgating"

        # 规则2：短时间内开⻔次数过多
        recent_openings = [r for r in self.passing_records if r['door_opening']]
        if len(recent_openings) >= 3:
            unique_times = set([int(r['time']) for r in recent_openings])
            if len(unique_times) <= 2:  # 3次开⻔发⽣在2秒内
                self.alert_cooldown = current_time + 5
                return True, " ⾼频通⾏告警：检测到异常⾼频通⾏", "frequency"

        return False, "正常", None

    def record_opening(self):
        """记录⼀次"开⻔事件"。
        ⻔禁验证通过后调⽤，⽤于后续的⾼频通⾏检测。
        """
        self.last_open_time = time.time()
        self.passing_records.append({
            'time': self.last_open_time,
            'face_count': 1,
            'door_opening': True,
        })

    def get_status_text(self):
        """给 UI 层展示⽤的状态⽂本（近 10 秒通⾏次数）。"""
        current_time = time.time()
        recent_count = len([r for r in self.passing_records if current_time - r['time'] < 10])
        status = '正常' if recent_count < 3 else ' 频繁'
        return f"近10秒通⾏记录：{recent_count}次 | 状态：{status}"
