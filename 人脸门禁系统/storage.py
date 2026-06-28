import threading
import json
import os


class JsonEmployeeStore:
    """员⼯库 JSON存储。

    格式：
    ```json
        {
          "EMP001": {
            "employee_id": "EMP001",
            "name": "张三",
            "face_id": "xxx",
            "registered_at": "YYYY-mm-dd HH:MM:SS",
            "attributes": {...}
          }
        }
    ```
    """

    def __init__(self, path: str):
        self.path = path
        self._lock = threading.Lock()

    def load(self):
        """读取员⼯库数据。
        从JSON⽂件加载员⼯数据，如果⽂件不存在或为空则返回空字典。
        读取失败时打印错误信息并返回空字典，避免程序崩溃。

        返回:
            dict:员⼯数据字典，key为employee_id，value为员⼯信息
            返回空字典表⽰⽆数据或读取失败

        异常处理:
        -⽂件不存在:返回空字典
        -⽂件为空:返回空字典
        - JSON解析错误:打印错误，返回空字典
        -其他IO错误:打印错误，返回空字典
        """
        if not os.path.exists(self.path):
            return {}
        try:
            with open(self.path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if not content:
                    return {}
                return json.loads(content)
        except Exception as e:
            print(f"读取员⼯数据失败: {e}")
            return {}

    def save(self, data):
        """
        保存员⼯库数据（覆盖写）。

        将员⼯数据字典写⼊JSON⽂件，采⽤覆盖写模式。
        写⼊时加锁，确保多线程环境下数据⼀致性。

        参数:
           data (dict):员⼯数据字典，key为employee_id，value为员⼯信息

        说明:
           -采⽤覆盖写⽽⾮追加写，⼩数据量场景下⾜够⾼效
           -使⽤indent=2格式化输出，便于⼈⼯查看
           - ensure_ascii=False确保中⽂正常显⽰
           -写⼊操作是原⼦的（加锁保护）

        线程安全:
            使⽤self._lock确保同⼀时间只有⼀个线程执⾏写⼊
        """

        with self._lock:
            with open(self.path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)


class JsonAccessLogStore:
    """访问⽇志 JSON 存储（append-only）。
     ⽇志格式为 list，每条记录是⼀个 dict，包含：
     - timestamp: 时间戳
     - access_granted: 是否允许通⾏
     - employee_id: 员⼯编号（可能为None）
     - similarity: 相似度
     - reason: 拒绝原因（如有）
     - alert_type: 告警类型（如有）
    - live_confidence: 活体置信度
    - face_count: 画⾯⼈脸数量
    """

    def __init__(self, path: str):
        self.path = path
        self._lock = threading.Lock()

    def append(self, log_entry):
        """追加⼀条⽇志记录。
         实现策略：
         - 读出原有 list
         - append 新记录
         - 覆盖写回⽂件
         线程安全：
         - 使⽤ self._lock 确保写⼊原⼦性
         """
        logs = []
        if os.path.exists(self.path):
            try:
                with open(self.path, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                    if content:
                        logs = json.loads(content)
            except Exception:
                pass

        logs.append(log_entry)
        try:
            with self._lock:
                with open(self.path, 'w', encoding='utf-8') as f:
                    json.dump(logs, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存⽇志失败: {e}")

    def read_latest(self, limit=20):
        """读取最近 N 条⽇志（倒序返回，最新在前）。"""
        if not os.path.exists(self.path):
            return []

        try:
            with open(self.path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if not content:
                    return []
                logs = json.loads(content)
        except Exception:
            return []
        if not logs:
            return []

        # 取最后 limit 条，然后倒序（最新在前）
        logs = logs[-limit:]
        logs.reverse()
        return logs

