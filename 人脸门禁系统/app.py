import os
import gradio as gr

from config import Config
from ui import create_interface
from face_service import FaceRecognitionService
from features import (
    compare_faces as _compare_faces,
    delete_employee as _delete_employee,
    list_employees as _list_employees,
    register_employee as _register_employee,
    verify_access as _verify_access,
    view_logs as _view_logs,
)
from security import TailgatingDetector
from tts_service import VoiceService
from storage import JsonAccessLogStore, JsonEmployeeStore

# ========== 初始化服务 ==========
face_service = FaceRecognitionService(
    ak=Config.HUAWEI_AK,
    sk=Config.HUAWEI_SK,
    project_id=Config.HUAWEI_PROJECT_ID,
    region=Config.HUAWEI_REGION,
    face_set_name=Config.FACE_SET_NAME,
    face_set_capacity=Config.FACE_SET_CAPACITY,
)

if getattr(Config, "HUAWEI_PROJECT_NAME", ""):
    face_service.project_name = Config.HUAWEI_PROJECT_NAME

init_result = face_service.init_face_set()

employee_store = JsonEmployeeStore('employee_db.json')
log_store = JsonAccessLogStore('access_log.json')

tailgating_detector = TailgatingDetector(
    window_seconds=Config.TAILGATING_WINDOW,
    threshold=Config.TAILGATING_THRESHOLD,
)

voice_service = VoiceService(
    ak=Config.HUAWEI_AK,
    sk=Config.HUAWEI_SK,
    project_id=Config.HUAWEI_PROJECT_ID,
    region=Config.SIS_REGION,
)


# ========== Gradio 回调函数（依赖注入） ==========

def register_employee(employee_id, name, image):
    """Gradio 回调：员工注册。"""
    return _register_employee(face_service, employee_store, employee_id, name, image)


def verify_access(image, image_source="unknown"):
    """Gradio 回调：门禁验证。"""
    return _verify_access(
        face_service,
        voice_service,
        employee_store,
        log_store,
        tailgating_detector,
        image,
        image_source,
    )


def compare_faces(image1, image2):
    """Gradio 回调：人脸比对。"""
    return _compare_faces(face_service, image1, image2)


def list_employees():
    """Gradio 回调：员工列表。"""
    return _list_employees(employee_store)


def delete_employee(employee_id):
    """Gradio 回调：删除指定员工。"""
    return _delete_employee(face_service, employee_store, employee_id)


def view_logs(limit=20):
    """Gradio 回调：查看日志。"""
    return _view_logs(log_store, limit=limit)  #修改点


def create_app():
    """创建 Gradio app（Blocks）。
     将业务回调和初始化状态传⼊ UI 层。
    """
    return create_interface(
        init_result=init_result,
        register_employee=register_employee,
        verify_access=verify_access,  # 注⼊⻔禁验证回调
        compare_faces=compare_faces,  # 注⼊⼈脸⽐对回调
        list_employees=list_employees,
        delete_employee=delete_employee,
        view_logs=view_logs,  # 注⼊⽇志查看回调
        tailgating_detector=tailgating_detector,
    )


# ========== 启动⼊⼝ ==========
if __name__ == '__main__':
    demo = create_app()
    preferred_port = int(os.getenv("GRADIO_SERVER_PORT", "6006"))
    try:
        demo.launch(
            server_name='127.0.0.1',
            server_port=preferred_port,
            share=False,
            show_error=True,
            theme=gr.themes.Soft()
        )
    except OSError as e:
        if "Cannot find empty port" in str(e):
            demo.launch(
                server_name='127.0.0.1',
                share=False,
                show_error=True,
                theme=gr.themes.Soft()
            )
        else:
            raise
