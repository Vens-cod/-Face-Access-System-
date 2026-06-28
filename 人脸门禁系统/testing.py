# # 独⽴测试代码
# from storage import JsonAccessLogStore
# import time
# store = JsonAccessLogStore('test_access_log.json')
# # 测试追加⽇志
# store.append({
#     'timestamp': '2024-01-01 10:00:00',
#     'access_granted': True,
#     'employee_id': 'EMP001',
#     'similarity': 0.85,
#     'live_confidence': 0.92
# })
# store.append({
#     'timestamp': '2024-01-01 10:05:00',
#     'access_granted': False,
#     'employee_id': None,
#     'reason': '活体检测失败',
#     'live_confidence': 0.3
# })
# # 测试查询
# logs = store.read_latest(limit=10)
# print(f"查询到 {len(logs)} 条⽇志")
# for log in logs:
#     status = "通过" if log['access_granted'] else "拒绝"
#     print(f"[{log['timestamp']}] {status}")
# print(" 访问⽇志存储类测试通过")


# 测试代码（需使⽤真实⼈脸照⽚）
# from PIL import Image
# from config import Config
# from face_service import FaceRecognitionService
# face_service = FaceRecognitionService(
#     ak=Config.HUAWEI_AK,
#     sk=Config.HUAWEI_SK,
#     project_id=Config.HUAWEI_PROJECT_ID,
#     region=Config.HUAWEI_REGION,
#     face_set_name=Config.FACE_SET_NAME,
# )
# # 测试真⼈照⽚
# img_real = Image.open('test.jpg')
# is_alive, confidence, msg = face_service.live_detect_silent(img_real)
# print(f"真⼈照⽚ - 活体: {is_alive}, 置信度: {confidence:.2f}, 消息: {msg}")
# # 测试⾮活体（如⼿机屏幕照⽚）
# img_screen = Image.open('test3.jpg')
# is_alive, confidence, msg = face_service.live_detect_silent(img_screen)
# print(f"屏幕照⽚ - 活体: {is_alive}, 置信度: {confidence:.2f}, 消息: {msg}")


# 测试代码（需先注册员⼯到⼈脸库）
# from PIL import Image
# from config import Config
# from face_service import FaceRecognitionService
#
# face_service = FaceRecognitionService(
#     ak=Config.HUAWEI_AK,
#     sk=Config.HUAWEI_SK,
#     project_id=Config.HUAWEI_PROJECT_ID,
#     region=Config.HUAWEI_REGION,
#     face_set_name=Config.FACE_SET_NAME,
# )
# face_service.init_face_set()  # 确保⼈脸库已创建
# # 搜索员⼯
# img = Image.open('test1.jpg')
# results = face_service.search_face(img, top_n=1,
#                                    threshold=Config.SIMILARITY_THRESHOLD)
# if results:
#     matched = results[0]
#     print(f" 匹配成功!")
#     print(f" 员⼯编号: {matched.external_image_id}")
#     print(f" 相似度: {matched.similarity:.2%}")
#     print(f" Face ID: {matched.face_id}")
# else:
#     print(" 未找到匹配员⼯")

# 测试代码
# from security import TailgatingDetector
# detector = TailgatingDetector(window_seconds=3, threshold=2)
# # 测试场景1：正常单⼈通过
# is_alert, msg, alert_type = detector.check_tailgating(1, door_opening=True)
# print(f"单⼈通过: 告警={is_alert}, 消息={msg}")
# detector.record_opening()
# # 测试场景2：尾随（多⼈同时）
# is_alert, msg, alert_type = detector.check_tailgating(3, door_opening=True)
# print(f"3⼈通过: 告警={is_alert}, 消息={msg}, 类型={alert_type}")
# # 测试场景3：⾼频通⾏（模拟3秒内3次开⻔）
# detector2 = TailgatingDetector(window_seconds=3, threshold=2)
# detector2.record_opening()
# detector2.record_opening()
# detector2.record_opening()
# is_alert, msg, alert_type = detector2.check_tailgating(1, door_opening=True)
# print(f"⾼频通⾏: 告警={is_alert}, 消息={msg}, 类型={alert_type}")
# # 测试状态⽂本
# print(f"状态⽂本: {detector.get_status_text()}")
# print("✅尾随检测器测试完成")


# 测试代码
# from PIL import Image
# from config import Config
# from face_service import FaceRecognitionService
# from features import compare_faces
#
# face_service = FaceRecognitionService(
#     ak=Config.HUAWEI_AK,
#     sk=Config.HUAWEI_SK,
#     project_id=Config.HUAWEI_PROJECT_ID,
#     region=Config.HUAWEI_REGION,
#     face_set_name=Config.FACE_SET_NAME,
#
# )
# img1 = Image.open('test3.jpg')  # 同⼀个⼈的照⽚1
# img2 = Image.open('test4.jpg')  # 同⼀个⼈的照⽚2
# img3 = Image.open('test.jpg')  # 另⼀个⼈的照⽚
# # 测试同⼀⼈
# result, sim = compare_faces(face_service, img1, img2)
# print(f"同⼀⼈⽐对：{result}, 相似度={sim:.2%}")
# # 测试不同⼈
# result, sim = compare_faces(face_service, img1, img3)
# print(f"不同⼈⽐对：{result}, 相似度={sim:.2%}")


# 测试代码
# from storage import JsonAccessLogStore
# from features import view_logs
#
# log_store = JsonAccessLogStore('access_log.json')
# # 添加测试⽇志
# log_store.append({
#     'timestamp': '2024-01-01 10:00:00',
#     'access_granted': True,
#     'employee_id': 'EMP001',
#     'similarity': 0.85,
#     'live_confidence': 0.92,
#     'face_count': 1
# })
# log_store.append({
#     'timestamp': '2024-01-01 10:05:00',
#     'access_granted': False,
#     'reason': '尾随告警',
#     'alert_type': 'tailgating',
#     'face_count': 3
# })
# # 查看⽇志
# logs_text = view_logs(log_store, limit=10)
# print(logs_text)

# 完整⻔禁验证测试
# from PIL import Image
# from config import Config
# from face_service import FaceRecognitionService
# from tts_service import VoiceService
# from security import TailgatingDetector
# from storage import JsonEmployeeStore, JsonAccessLogStore
# from features import verify_access
#
# face_service = FaceRecognitionService(
#     ak=Config.HUAWEI_AK,
#     sk=Config.HUAWEI_SK,
#     project_id=Config.HUAWEI_PROJECT_ID,
#     region=Config.HUAWEI_REGION,
#     face_set_name=Config.FACE_SET_NAME,
# )
# face_service.init_face_set()
#
# voice_service = VoiceService(
#     ak=Config.HUAWEI_AK, sk=Config.HUAWEI_SK,
#     project_id=Config.HUAWEI_PROJECT_ID, region=Config.SIS_REGION
# )
#
# employee_store = JsonEmployeeStore('employee_db.json')
# log_store = JsonAccessLogStore('access_log.json')
# tailgating_detector = TailgatingDetector(
#     window_seconds=Config.TAILGATING_WINDOW,
#     threshold=Config.TAILGATING_THRESHOLD
# )
#
# # 测试场景1：⽆图⽚
# html, status, voice_text, voice_audio, tail_status = verify_access(
#     face_service, voice_service, employee_store, log_store,
#     tailgating_detector, None, "upload"
# )
# print(f"场景1（⽆图）: {status}")
#
# # 测试场景2：已注册员⼯验证（使⽤真实照⽚）
# img = Image.open('test2.jpg')
# html, status, voice_text, voice_audio, tail_status = verify_access(
#     face_service, voice_service, employee_store, log_store,
#     tailgating_detector, img, "upload"
# )
# print(f"场景2（已注册员⼯）: {status}")
# print(f"语⾳消息: {voice_text}")
#
# # 测试场景3：尾随检测（模拟多⼈画⾯）
# # 这⾥通过多次调⽤来模拟
# for _ in range(3):
#     html, status, voice_text, voice_audio, tail_status = verify_access(
#         face_service, voice_service, employee_store, log_store,
#         tailgating_detector, img, "upload"
#     )
# print(f"场景3（⾼频后）: {tail_status}")
#
# # 查看访问⽇志
# logs = log_store.read_latest(limit=10)
# print(f"\n最近 {len(logs)} 条访问记录:")
# for log in logs:
#     print(f" [{log['timestamp']}] {'通过' if log['access_granted'] else '拒绝'}")

