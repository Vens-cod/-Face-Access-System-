from config import Config
from ui import format_result_card
from datetime import datetime


def register_employee(face_service, employee_store, employee_id, name, image):
    import os
    print(">>> features.register_employee ENTER",
          os.getpid(), "image_is_none=", image is None)
    print("=== register_employee called ===", employee_id, name, image is None)
    try:
        # 参数校验
        if not employee_id or not name:
            return "❌ 请填写员⼯编号和姓名", None
        if image is None:
            return "❌ 请上传⼈脸照⽚", None

        result = face_service.detect_face(image)
        print("detect_face result type:", type(result), "value:", result)

        if isinstance(result, dict) and 'error' in result:
            return f"❌ ⼈脸检测失败: {result['error']}", None
        if not result or not getattr(result, "faces", None):
            # 兼容：result.faces 或 result['faces']
            return "❌ 未检测到⼈脸，请重新上传", None

        face = result.faces[0]
        attrs = face_service.extract_attributes(face)
        print("extract_attributes:", attrs)

        quality_score = attrs.get('quality_score', 0)
        print("quality_score:", quality_score, "threshold:", Config.QUALITY_THRESHOLD)

        if quality_score < Config.QUALITY_THRESHOLD:
            return f"❌ ⼈脸质量过低({quality_score:.2f})，请重新拍摄", None

        face_id = face_service.add_face(image, employee_id)
        print("add_face face_id:", face_id)

        if not face_id:
            return "❌ ⼈脸⼊库失败，请稍后重试", None

        employees = employee_store.load()
        employees[employee_id] = {
            'employee_id': employee_id,
            'name': name,
            'face_id': face_id,
            'registered_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'attributes': attrs,
        }
        employee_store.save(employees)
        print("employee_store saved ok:", employee_id)

        info = f"✅ 注册成功！员工编号：{employee_id}"
        return info, image

    except Exception as e:
        import traceback
        print(">>> features.register_employee EXCEPT")
        import traceback
        traceback.print_exc()
        print("=== register_employee exception ===")
        traceback.print_exc()
        return f"❌ 注册异常：{repr(e)}", None


def verify_access(face_service, voice_service, employee_store, log_store,
                  tailgating_detector, image, image_source="unknown"):
    """门禁验证（增强版）。

    核心能力:
    - 活体检测（静默/动作活体的兼容降级）
    - 人脸检测 + 质量检查
    - 尾随/高频通行检测（在开门前触发告警）
    - 1:N人脸搜索识别员工身份
    - 写访问日志（成功/失败/告警）
    - 语音迎宾（可通过配置开关降级为文字）

    返回:
        (html, status_label, voice_text, voice_audio, tailgating_status)
    """
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[verify] {timestamp} source={image_source} has_image={image is not None}")

    # ========== 步骤1: 图片空检查 ==========
    if image is None:
        return (
            format_result_card(
                "warning",
                "未检测到图像",
                "请上传照片，或开启摄像头后先点击画面下方的拍照/相机按钮抓取图片，再点击开始验证",
                timestamp
            ),
            "等待验证...", "请先拍照再验证", None,
            tailgating_detector.get_status_text()
        )

    # ========== 步骤2: 活体检测 ==========
    live_ok = False
    try:
        if getattr(Config, "USE_ACTION_LIVE", False):
            if image_source == "webcam" and hasattr(face_service, "live_detect_action"):
                is_alive, live_confidence, live_msg = face_service.live_detect_action(image)
            else:
                is_alive, live_confidence, live_msg = face_service.live_detect_silent(image)
                live_msg = f"静默活体（上传/无摄像头降级）：{live_msg}"
        else:
            is_alive, live_confidence, live_msg = face_service.live_detect_silent(image)

        live_ok = True
    except Exception as e:
        print(f"活体检测异常（继续流程）: {e}")
        is_alive, live_confidence, live_msg = True, 0.0, \
            f"活体检测服务异常，已跳过（{type(e).__name__}）"

    # 活体检测明确失败：记录⽇志并拒绝通⾏
    if not is_alive:
        log_entry = {
            'timestamp': timestamp,
            'access_granted': False,
            'employee_id': None,
            'similarity': 0,
            'reason': '活体检测失败',
            'detail': live_msg,
            'live_confidence': live_confidence,
        }
        log_store.append(log_entry)

        return (
            format_result_card(
                "security_reject",
                "安全验证未通过",
                "请使用真实人脸进行验证，不要使用照片、视频或屏幕",
                timestamp,
                confidence=live_confidence
            ),
            "禁止通行", "请使用真实人脸", None,
            tailgating_detector.get_status_text()
        )

    # ========== 步骤3: 人脸检测 ==========
    result = face_service.detect_face(image)

    if isinstance(result, dict) and 'error' in result:
        return (
            format_result_card(
                "error",
                "检测服务异常",
                "暂时无法处理图像，请检查网络连接",
                timestamp,
                details=result['error']
            ),
            "系统错误", "请稍后重试", None,
            tailgating_detector.get_status_text()
        )

    if not result or not result.faces:
        return (
            format_result_card(
                "warning",
                "未检测到人脸",
                "请调整位置确保面部清晰可见，避免侧脸或遮挡",
                timestamp
            ),
            "验证失败", "请调整位置", None,
            tailgating_detector.get_status_text()
        )

    face = result.faces[0]
    attrs = face_service.extract_attributes(face)
    face_count = len(result.faces)

    # ========== 步骤4: 质量检查 ==========
    quality_score = attrs.get('quality_score', 0)
    if quality_score < Config.QUALITY_THRESHOLD:
        return (
            format_result_card(
                "warning",
                "图像质量不佳",
                "请确保光线充足，面部无遮挡，正对摄像头",
                timestamp,
                quality=quality_score
            ),
            "验证失败", "请调整光线", None,
            tailgating_detector.get_status_text()
        )

    # ========== 步骤5: 尾随检测 ==========
    is_alert, alert_msg, alert_type = tailgating_detector.check_tailgating(
        face_count, door_opening=True
    )

    if is_alert:
        log_entry = {
            'timestamp': timestamp,
            'access_granted': False,
            'employee_id': None,
            'similarity': 0,
            'reason': alert_msg,
            'alert_type': alert_type,
            'face_count': face_count,
        }
        log_store.append(log_entry)

        return (
            format_result_card(
                "alert",
                "安全告警",
                "检测到异常通行行为，请单独通过验证区域",
                timestamp,
                alert_type=alert_type,
                face_count=face_count
            ),
            "告警触发", "请联系安保人员", None,
            tailgating_detector.get_status_text()
        )

    # ========== 步骤6: 1:N 人脸搜索 ==========
    search_results = face_service.search_face(
        image, threshold=Config.SIMILARITY_THRESHOLD
    )

    if not search_results:
        log_entry = {
            'timestamp': timestamp,
            'access_granted': False,
            'employee_id': None,
            'similarity': 0,
            'reason': '未找到匹配员工',
            'live_confidence': live_confidence,
            'attributes': attrs,
        }
        log_store.append(log_entry)

        return (
            format_result_card(
                "reject",
                "身份未识别",
                "您不在员工库中，请联系管理员注册人脸信息",
                timestamp,
                attributes=attrs,
                live_confidence=live_confidence
            ),
            "禁止通行", "非授权人员", None,
            tailgating_detector.get_status_text()
        )

    # ========== 步骤7: 匹配成功 ==========
    matched = search_results[0]
    similarity = matched.similarity
    employee_id = matched.external_image_id

    employees = employee_store.load()
    employee = employees.get(employee_id, {})
    emp_name = employee.get('name', '访客')

    tailgating_detector.record_opening()

    # ========== 步骤8: 语音 ==========
    voice_msg = f"欢迎，{emp_name}"
    voice_audio = None

    if getattr(Config, "ENABLE_VOICE", True):
        try:
            success, result_path = voice_service.generate_welcome(emp_name, "employee")
            if success:
                voice_audio = result_path
        except Exception as e:
            print(f"语音合成异常（已降级）: {e}")
    else:
        voice_msg = "语音已关闭"

    # ========== 步骤9: 记录日志 ==========
    log_entry = {
        'timestamp': timestamp,
        'access_granted': True,
        'employee_id': employee_id,
        'similarity': similarity,
        'attributes': attrs,
        'live_confidence': live_confidence,
        'face_count': face_count,
    }
    log_store.append(log_entry)

    live_note = "" if live_ok else f"（{live_msg}）"

    # ========== 步骤10: 返回 ==========
    return (
        format_result_card(
            "success",
            "验证通过",
            f"欢迎回来，{emp_name}！门禁已开启，请通行{live_note}",
            timestamp,
            employee_id=employee_id,
            name=emp_name,
            similarity=similarity,
            attributes=attrs,
            live_confidence=live_confidence,
            face_count=face_count
        ),
        "已开门",
        voice_msg,
        voice_audio,
        tailgating_detector.get_status_text()
    )


def compare_faces(face_service, image1, image2):
    """1:1 人脸比对。

    返回:
        (text, similarity_float) - 文本结果和相似度数值
    """
    if image1 is None or image2 is None:
        return "请上传两张人脸照片", 0

    similarity = face_service.compare_faces(image1, image2)
    result = "同一人" if similarity >= 0.75 else "不同人"

    info = f"""相似度：{similarity:.2%}

判断结果：{result}"""

    return info, similarity


def view_logs(log_store, limit=20):
    """读取并格式化最近 N 条访问记录。
     参数:
     log_store: JsonAccessLogStore 实例
     limit: 返回的最⼤记录数
     返回:
     str: 格式化后的⽇志⽂本
     """
    logs = log_store.read_latest(limit=limit)
    if not logs:
        return "暂⽆访问记录"
    info = " 最近访问记录：\n\n"
    for log in logs:
        status = " 通过" if log.get('access_granted') else " 拒绝"
        alert_info = ""
        if log.get('alert_type'):
            alert_info = f" [{log['alert_type']}]"

        info += f"[{log.get('timestamp', '未知')}] {status}{alert_info}\n"
        info += f" 员⼯：{log.get('employee_id', '未知')}\n"
        if log.get('similarity'):
            info += f" 相似度：{log['similarity']:.2%}\n"
        if log.get('live_confidence'):
            info += f" 活体置信度：{log['live_confidence']:.2f}\n"
        if log.get('face_count'):
            info += f" 画⾯⼈数：{log['face_count']}⼈\n"
        if log.get('reason'):
            info += f" 原因：{log.get('reason')}\n"
        info += "\n"

    return info


def list_employees(employee_store):
    employees = employee_store.load()
    if not employees:
        return "暂无员工"

    info = "员工列表：\n\n"
    # for emp_id, emp in employees.items():
    #     info += f"{emp_id} - {emp.get('name')}\n"
    for emp_id, emp in employees.items():
        info += f" {emp_id} - {emp.get('name', '未知')}\n"
        info += f" 注册时间：{emp.get('registered_at', '未知')}\n"
        info += f" 年龄：{emp.get('attributes', {}).get('age', '未知')}\n\n"

    return info


def delete_employee(face_service, employee_store, employee_id):
    if not employee_id:
        return "❌ 请输入员工编号"

    employees = employee_store.load()

    if employee_id not in employees:
        return f"❌ 员工{employee_id}不存在"

    # ❗这里只删除本地（简单版）
    # 如果你想连华为云一起删，需要调用 delete_face API
    del employees[employee_id]
    employee_store.save(employees)

    return f"✅ 已删除员工 {employee_id}"
