# import gradio as gr
# import inspect
#
#
# def create_interface(register_employee):
#     """
#     创建并返回 Gradio Blocks 实例。
#     说明:
#         - 采⽤分层架构，UI 层只负责界⾯渲染
#         - 回调函数由 app.py 层注⼊，实现解耦
#     """
#     with gr.Blocks(title="智能⻔禁系统") as demo:
#         # 系统标题
#         gr.Markdown("""
#         # 🚪 智能⻔禁系统（增强版）
#         基于华为云⼈脸识别服务 | 集成活体检测+尾随检测+语⾳迎宾
#         """)
#
#         with gr.Tabs():
#             with gr.Tab("👤 员⼯注册"):
#                 gr.Markdown("### 注册新员⼯")
#                 with gr.Row():
#                     with gr.Column():
#                         employee_id = gr.Textbox(
#                             label="员⼯编号",
#                             placeholder="如：EMP001",
#                             value="EMP001",
#                         )
#                         name = gr.Textbox(
#                             label="员⼯姓名",
#                             placeholder="请输⼊姓名",
#                             value="张三",
#                         )
#                         reg_image = gr.Image(
#                             label="⼈脸照⽚",
#                             type="pil",
#                             sources=["upload", "webcam"],
#                             height=300,
#                         )
#                         reg_btn = gr.Button(
#                             "📝 注册员⼯",
#                             variant="primary",
#                             size="lg"
#                         )
#                     with gr.Column():
#                         reg_output = gr.Textbox(
#                             label="注册结果",
#                             lines=10,
#                             interactive=False,
#                         )
#                         reg_preview = gr.Image(
#                             label="照⽚预览",
#                             visible=True
#                         )
#
#                 # 事件绑定：点击注册按钮触发 register_employee 回调
#                 reg_btn.click(
#                     fn=register_employee,  # 从 app.py 注⼊的回调函数
#                     inputs=[employee_id, name, reg_image],
#                     outputs=[reg_output, reg_preview]
#                 )
#
#             with gr.Tab("🔐 ⻔禁验证"):
#                 gr.Markdown("### ⼈脸验证开⻔（已集成活体检测+尾随检测+语⾳迎宾）")
#                 with gr.Row():
#                     with gr.Column():
#                         latest_frame = gr.State(value=None)
#                         latest_source = gr.State(value="unknown")
#
#                         verify_webcam = gr.Image(
#                             label="摄像头画⾯（可直接开始验证）",
#                             type="pil",
#                             sources=["webcam"],
#                             height=350,
#                         )
#                         verify_upload = gr.Image(
#                             label="或上传照⽚",
#                             type="pil",
#                             sources=["upload"],
#                             height=200,
#                         )
#                         verify_btn = gr.Button(
#                             "🔍 开始验证",
#                             variant="primary",
#                             size="lg"
#                         )
#                         tailgating_status = gr.Textbox(
#                             label="尾随检测状态",
#                             value="",
#                             interactive=False,
#                             lines=1,
#                         )
#                     with gr.Column():
#                         verify_result = gr.HTML(
#                             label="验证结果",
#                             value='<div style="padding: 40px; color: #9ca3af; text-align: center; border: 2px dashed #e5e7eb; border-radius: 16px; background: #f9fafb;">等待验证...</div>',
#                         )
#                         verify_status = gr.Label(
#                             label="⻔禁状态",
#                             value="等待验证..."
#                         )
#                         voice_status = gr.Textbox(
#                             label="语⾳播报状态",
#                             value="等待播报...",
#                             interactive=False,
#                         )
#                         voice_audio = gr.Audio(
#                             label="语⾳播报",
#                             interactive=False,
#                             type="filepath",
#                         )
#
#             with gr.Tab("🔄 ⼈脸⽐对"):
#                 gr.Markdown("### 1:1 ⼈脸⽐对")
#                 with gr.Row():
#                     compare_img1 = gr.Image(
#                         label="照⽚1",
#                         type="pil",
#                         sources=["upload", "webcam"],
#                         height=250,
#                     )
#                     compare_img2 = gr.Image(
#                         label="照⽚2",
#                         type="pil",
#                         sources=["upload", "webcam"],
#                         height=250,
#                     )
#                     compare_btn = gr.Button(
#                         "🔍 开始⽐对",
#                         variant="primary",
#                         size="lg"
#                     )
#                 with gr.Row():
#                     compare_result = gr.Textbox(
#                         label="⽐对结果",
#                         lines=4,
#                         interactive=False,
#                     )
#                     similarity_gauge = gr.Number(
#                         label="相似度",
#                         value=0,
#                         minimum=0,
#                         maximum=1,
#                     )
#
#             with gr.Tab("📋 员⼯管理"):
#                 gr.Markdown("### 查看和管理员⼯")
#                 with gr.Row():
#                     list_btn = gr.Button(
#                         "📋 列出所有员⼯",
#                         variant="primary"
#                     )
#                     refresh_btn = gr.Button(
#                         "🔄 刷新",
#                         variant="secondary"
#                     )
#                 employee_list = gr.Textbox(
#                     label="员⼯列表",
#                     lines=15,
#                     interactive=False,
#                 )
#                 gr.Markdown("### 删除员⼯")
#                 with gr.Row():
#                     del_id = gr.Textbox(
#                         label="员⼯编号",
#                         placeholder="输⼊要删除的员⼯编号"
#                     )
#                     del_btn = gr.Button(
#                         "🗑 删除",
#                         variant="stop"
#                     )
#                 del_result = gr.Textbox(
#                     label="删除结果",
#                     interactive=False
#                 )
#                 reg_btn.click(
#                     fn=register_employee, inputs=[employee_id, name, reg_image], outputs=[reg_output, reg_preview],
#                 )
#                 # --- 5. 访问日志 ---
#             with gr.Tab("📋 访问日志"):
#                 log_refresh_btn = gr.Button("🔎 获取最新访问记录")
#                 log_display = gr.Markdown("暂无日志记录")
#
#     return demo
#
#
#
#
#
#
# def _capture_latest_frame_with_source(source):
#     """把图像和来源（webcam/upload）⼀起写⼊ Gradio State。
#     说明:
#     - 界⾯上有两路输⼊：摄像头与上传
#     - 按钮点击时不直接使⽤组件本身的值，⽽是使⽤ State 中缓存的"最新帧"
#     - 这样可以区分图⽚是来⾃摄像头还是上传，⽤于后续活体检测策略
#     """
#
#     def _fn(image):
#         return image, source
#
#     return _fn
#
#
# def create_interface(
#         init_result,
#         register_employee,
#         verify_access,
#         compare_faces,
#         list_employees,
#         delete_employee,
#         view_logs,
#         tailgating_detector,
# ):
#     """创建并返回 Gradio Blocks 实例。
#     参数:
#     - init_result: ⼈脸库初始化结果字符串
#     - verify_access: ⻔禁验证回调函数
#     - tailgating_detector: 尾随检测器实例（⽤于显示实时状态）
#     """
#     with gr.Blocks(title="智能⻔禁系统") as demo:
#         gr.Markdown(
#             """
#             智能⻔禁系统（增强版）
#             基于华为云⼈脸识别服务 | 集成活体检测 + 尾随检测 + 语⾳迎宾
#             """
#         )
#
#         with gr.Tabs():
#             # ... 其他 Tab ...
#             with gr.Tab("⻔禁验证"):
#                 gr.Markdown("### ⼈脸验证开⻔（已集成活体检测+尾随检测+语⾳迎宾）")
#
#                 with gr.Row():
#                     with gr.Column():
#                         # State 管理：存储最新帧和输⼊来源
#                         latest_frame = gr.State(value=None)
#                         latest_source = gr.State(value="unknown")
#
#                         # 摄像头输⼊
#                         verify_webcam = gr.Image(
#                             label="摄像头画⾯（可直接开始验证）",
#                             type="pil",
#                             sources=["webcam"],
#                             height=350,
#                         )
#
#                         # 上传输⼊
#                         verify_upload = gr.Image(
#                             label="或上传照⽚",
#                             type="pil",
#                             sources=["upload"],
#                             height=200,
#                         )
#
#                         verify_btn = gr.Button(
#                             "开始验证", variant="primary", size="lg"
#                         )
#
#                         # 实时状态显示
#                         tailgating_status = gr.Textbox(
#                             label="尾随检测状态",
#                             value=tailgating_detector.get_status_text(),
#                             interactive=False,
#                             lines=1,
#                         )
#
#                     with gr.Column():
#                         # 富⽂本结果展示
#                         verify_result = gr.HTML(
#                             label="验证结果",
#                             value=(
#                                 '<div style="padding: 40px; color: #9ca3af; '
#                                 'text-align: center; border: 2px dashed  # e5e7eb; '
#                                 'border-radius: 16px; background:  # f9fafb;">'
#                                 "等待验证...</div>"
#                             ),
#                         )
#                         verify_status = gr.Label(
#                             label="⻔禁状态", value="等待验证..."
#                         )
#                         voice_status = gr.Textbox(
#                             label="语⾳播报状态",
#                             value="等待播报...",
#                             interactive=False,
#                         )
#                         voice_audio = gr.Audio(
#                             label="语⾳播报",
#                             interactive=False,
#                             type="filepath",
#                         )
#
#                 # ========== 事件绑定 ==========
#                 # 摄像头变化时更新 State
#                 verify_webcam.change(
#                     fn=_capture_latest_frame_with_source("webcam"),
#                     inputs=verify_webcam,
#                     outputs=[latest_frame, latest_source],
#                     show_progress=False,
#                 )
#
#                 # ⽀持实时视频流（如果 Gradio 版本⽀持）
#                 if hasattr(verify_webcam, "stream"):
#                     verify_webcam.stream(
#                         fn=_capture_latest_frame_with_source("webcam"),
#                         inputs=verify_webcam,
#                         outputs=[latest_frame, latest_source],
#                         show_progress=False,
#                     )
#
#                 # 上传变化时更新 State
#                 verify_upload.change(
#                     fn=_capture_latest_frame_with_source("upload"),
#                     inputs=verify_upload,
#                     outputs=[latest_frame, latest_source],
#                     show_progress=False,
#                 )
#
#                 # 验证按钮点击
#                 verify_btn.click(
#                     fn=verify_access,
#                     inputs=[latest_frame, latest_source],
#                     outputs=[
#                         verify_result,
#                         verify_status,
#                         voice_status,
#                         voice_audio,
#                         tailgating_status,
#                     ],
#                 )
#
#                 # ... 其他 Tab ...
#
#         return demo
#
#
# def format_result_card(status, title, message, timestamp, **kwargs):
#     """构造验证结果的 HTML 卡片。
#
#     参数:
#     - status: success/reject/security_reject/alert/warning/error
#     - title/message/timestamp: 卡片主标题、正文与时间
#     - kwargs: 不同状态的附加字段（如 similarity/attributes/face_count 等）
#
#     返回:
#     - str: HTML 字符串，用于 `gr.HTML` 组件展示
#     """
#     styles = {
#         "success": {
#             "border": "#10b981",
#             "bg": "linear-gradient(135deg, #d1fae5 0%, #ecfdf5 100%)",
#             "icon": "✅",
#             "title_color": "#047857",
#         },
#         "reject": {
#             "border": "#ef4444",
#             "bg": "linear-gradient(135deg, #fee2e2 0%, #fef2f2 100%)",
#             "icon": "❌",
#             "title_color": "#b91c1c",
#         },
#         "security_reject": {
#             "border": "#dc2626",
#             "bg": "linear-gradient(135deg, #fecaca 0%, #fef2f2 100%)",
#             "icon": "⛔",
#             "title_color": "#991b1b",
#         },
#         "alert": {
#             "border": "#f59e0b",
#             "bg": "linear-gradient(135deg, #fef3c7 0%, #fffbeb 100%)",
#             "icon": "⚠",
#             "title_color": "#b45309",
#         },
#         "warning": {
#             "border": "#f97316",
#             "bg": "linear-gradient(135deg, #ffedd5 0%, #fff7ed 100%)",
#             "icon": "⚡",
#             "title_color": "#c2410c",
#         },
#         "error": {
#             "border": "#6b7280",
#             "bg": "linear-gradient(135deg, #f3f4f6 0%, #fafafa 100%)",
#             "icon": "❗",
#             "title_color": "#374151",
#         },
#     }
#
#     style = styles.get(status, styles["error"])
#
#     details_html = ""
#
#     if status == "success":
#         attr = kwargs.get('attributes', {})
#         details_html = f"""
#         <div style="margin-top: 16px; padding-top: 16px; border-top: 1px solid rgba(0,0,0,0.1);">
#             <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; font-size: 14px; color: #374151;">
#                 <div style="background: rgba(255,255,255,0.6); padding: 8px; border-radius: 6px;">
#                     <span style="color: #6b7280;">工号</span><br>
#                     <strong style="color: #111827; font-size: 16px;">{kwargs.get('employee_id', 'N/A')}</strong>
#                 </div>
#                 <div style="background: rgba(255,255,255,0.6); padding: 8px; border-radius: 6px;">
#                     <span style="color: #6b7280;">相似度</span><br>
#                     <strong style="color: #059669; font-size: 16px;">{kwargs.get('similarity', 0):.1%}</strong>
#                 </div>
#                 <div style="background: rgba(255,255,255,0.6); padding: 8px; border-radius: 6px;">
#                     <span style="color: #6b7280;">年龄</span><br>
#                     <strong style="color: #111827;">{attr.get('age', '未知')} 岁</strong>
#                 </div>
#                 <div style="background: rgba(255,255,255,0.6); padding: 8px; border-radius: 6px;">
#                     <span style="color: #6b7280;">表情</span><br>
#                     <strong style="color: #111827;">{attr.get('expression', '未知')}</strong>
#                 </div>
#                 <div style="background: rgba(255,255,255,0.6); padding: 8px; border-radius: 6px;">
#                     <span style="color: #6b7280;">活体置信度</span><br>
#                     <strong style="color: #059669;">{kwargs.get('live_confidence', 0):.2f}</strong>
#                 </div>
#                 <div style="background: rgba(255,255,255,0.6); padding: 8px; border-radius: 6px;">
#                     <span style="color: #6b7280;">画面人数</span><br>
#                     <strong style="color: {'#dc2626' if kwargs.get('face_count', 1) > 1 else '#059669'};">
#                         {kwargs.get('face_count', 1)} 人
#                     </strong>
#                 </div>
#             </div>
#         </div>
#         """
#     elif status == "security_reject":
#         if kwargs.get('confidence') is not None:
#             details_html = f"""
#             <div style="margin-top: 12px; padding: 8px; background: rgba(255,255,255,0.5); border-radius: 6px; font-size: 12px; color: #7f1d1d;">
#                 安全评分: {kwargs["confidence"]:.2f} (阈值: 0.70)
#             </div>
#             """
#     elif status == "alert":
#         details_html = f"""
#         <div style="margin-top: 12px; padding: 12px; background: rgba(255,255,255,0.6); border-radius: 8px; border-left: 4px solid #f59e0b;">
#             <div style="font-size: 14px; color: #92400e; font-weight: 600;">
#                 检测到 {kwargs.get("face_count", 0)} 个人脸进入验证区域
#             </div>
#             <div style="font-size: 12px; color: #b45309; margin-top: 4px;">
#                 请保持一人通行，避免尾随风险
#             </div>
#         </div>
#         """
#     elif status == "reject" and kwargs.get('attributes'):
#         attr = kwargs['attributes']
#         details_html = f"""
#         <div style="margin-top: 12px; font-size: 13px; color: #6b7280; text-align: center;">
#             检测到特征：{attr.get("age", "?")}岁 · {attr.get("gender", "?")} · {attr.get("expression", "?")}
#         </div>
#         """
#
#     html = f"""
#     <div style="border-radius: 16px; padding: 24px; background: {style['bg']}; border: 2px solid {style['border']};
#         box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
#         font-family: system-ui, -apple-system, sans-serif; animation: slideIn 0.3s ease-out;">
#         <div style="display: flex; align-items: flex-start; gap: 16px;">
#             <div style="font-size: 40px; line-height: 1; filter: drop-shadow(0 2px 4px rgba(0,0,0,0.1));">
#                 {style['icon']}
#             </div>
#             <div style="flex: 1;">
#                 <div style="font-size: 20px; font-weight: bold; color: {style['title_color']}; margin-bottom: 4px;">
#                     {title}
#                 </div>
#                 <div style="font-size: 12px; color: #6b7280; font-weight: 500; text-transform: uppercase;
#                     letter-spacing: 0.05em; margin-bottom: 8px;">
#                     {timestamp}
#                 </div>
#                 <div style="font-size: 16px; color: #1f2937; line-height: 1.5; font-weight: 500;">
#                     {message}
#                 </div>
#                 {details_html}
#             </div>
#         </div>
#     </div>
#     <style>
#     @keyframes slideIn {{
#         from {{ opacity: 0; transform: translateY(-10px); }}
#         to {{ opacity: 1; transform: translateY(0); }}
#     }}
#     </style>
#     """
#     return html
#
#

import gradio as gr
import inspect


def _capture_latest_frame_with_source(source):
    """捕捉图像及其来源（摄像头或上传）"""

    def _fn(image):
        return image, source

    return _fn


def create_interface(
        init_result,
        register_employee,
        verify_access,
        compare_faces,
        list_employees,
        delete_employee,
        view_logs,
        tailgating_detector,
):
    """
    完整的界面生成函数
    注意：参数顺序必须与 app.py 中的调用严格一致
    """
    with gr.Blocks(title="智能门禁系统", theme=gr.themes.Soft()) as demo:
        gr.Markdown(f"""
        # 🚪 智能门禁系统（增强版）
        **系统初始化状态：** {init_result}
        """)

        with gr.Tabs():
            # ---------- Tab 1: 门禁验证 (核心功能) ----------
            with gr.Tab("🔐 门禁验证"):
                gr.Markdown("### 人脸验证开门（集成活体检测+尾随检测）")
                with gr.Row():
                    with gr.Column():
                        latest_frame = gr.State(value=None)
                        latest_source = gr.State(value="unknown")

                        verify_webcam = gr.Image(label="摄像头画面", type="pil", sources=["webcam"], height=350)
                        verify_upload = gr.Image(label="或上传照片", type="pil", sources=["upload"], height=200)
                        verify_btn = gr.Button("🔍 开始验证", variant="primary", size="lg")

                        tailgating_status = gr.Textbox(
                            label="尾随检测状态",
                            value=tailgating_detector.get_status_text() if tailgating_detector else "未初始化",
                            interactive=False
                        )
                    with gr.Column():
                        verify_result = gr.HTML(label="验证结果",
                                                value='<div style="padding:40px;text-align:center;border:2px dashed #eee;">等待验证...</div>')
                        verify_status = gr.Label(label="门禁状态", value="等待验证...")
                        # voice_audio = gr.Audio(label="语音迎宾", interactive=False, type="filepath")
                        # 修改点：添加 autoplay=True
                        voice_audio = gr.Audio(
                            label="语音迎宾",
                            interactive=False,
                            type="filepath",
                            autoplay=True  # 核心修改：让声音自动出来
                        )
                        voice_status = gr.Textbox(label="播报状态", interactive=False)

                # 事件绑定
                verify_webcam.change(fn=_capture_latest_frame_with_source("webcam"), inputs=verify_webcam,
                                     outputs=[latest_frame, latest_source])
                verify_upload.change(fn=_capture_latest_frame_with_source("upload"), inputs=verify_upload,
                                     outputs=[latest_frame, latest_source])
                verify_btn.click(
                    fn=verify_access,
                    inputs=[latest_frame, latest_source],
                    outputs=[verify_result, verify_status, voice_status, voice_audio, tailgating_status]
                )

            # ---------- Tab 2: 员工注册 ----------
            with gr.Tab("👤 员工注册"):
                with gr.Row():
                    with gr.Column():
                        employee_id = gr.Textbox(label="员工编号", placeholder="EMP001")
                        name = gr.Textbox(label="姓名")
                        reg_image = gr.Image(label="注册照片", type="pil")
                        reg_btn = gr.Button("注册", variant="primary")
                    with gr.Column():
                        reg_output = gr.Textbox(label="结果", lines=10)
                        reg_preview = gr.Image(label="预览")

                reg_btn.click(fn=register_employee, inputs=[employee_id, name, reg_image],
                              outputs=[reg_output, reg_preview])

            # ---------- Tab 3: 人脸比对 ----------
            with gr.Tab("🔄 人脸比对"):
                with gr.Row():
                    img1 = gr.Image(label="照片1", type="pil")
                    img2 = gr.Image(label="照片2", type="pil")
                compare_btn = gr.Button("开始比对")
                compare_res = gr.Textbox(label="比对结果")
                similarity = gr.Number(label="相似度")

                compare_btn.click(fn=compare_faces, inputs=[img1, img2], outputs=[compare_res, similarity])

            # ---------- Tab 4: 员工管理 ----------
            with gr.Tab("📋 员工管理"):
                with gr.Row():
                    list_btn = gr.Button("刷新员工列表")
                employee_list = gr.Textbox(label="所有员工", lines=10)

                gr.Markdown("---")
                with gr.Row():
                    del_id = gr.Textbox(label="要删除的员工ID")
                    del_btn = gr.Button("确认删除", variant="stop")
                del_res = gr.Textbox(label="删除状态")

                list_btn.click(fn=list_employees, outputs=employee_list)
                del_btn.click(fn=delete_employee, inputs=del_id, outputs=del_res)

            # with gr.Tab(" 员⼯管理"):
            #     gr.Markdown("### 查看和管理员⼯")
            # with gr.Row():
            #     list_btn = gr.Button(" 列出所有员⼯", variant="primary")
            # refresh_btn = gr.Button(" 刷新", variant="secondary")
            # employee_list = gr.Textbox(
            #     label="员⼯列表",
            #     lines=15,
            #     interactive=False,
            # )
            # list_btn.click(fn=list_employees, outputs=employee_list)
            # refresh_btn.click(fn=list_employees, outputs=employee_list)

            # gr.Markdown("### 删除员⼯")
            # with gr.Row():
            #     del_id = gr.Textbox(label="员⼯编号", placeholder="输⼊要删除的员⼯编号")
            #     del_btn = gr.Button(" 删除", variant="stop")
            #     del_result = gr.Textbox(label="删除结果", interactive=False)
            # del_btn.click(
            #     fn=delete_employee,
            #     inputs=[del_id],
            #     outputs=del_result,
            # )

            # ---------- Tab 5: 访问日志 ----------
            with gr.Tab("📜 访问日志"):
                gr.Markdown("### 实时访问日志")

                # 1. 新增：控制显示条数的拖动条 (Slider)
                log_limit = gr.Slider(
                    minimum=5,
                    maximum=100,
                    value=20,
                    step=5,
                    label="获取最近记录条数 (拖动以调整)"
                )

                # 2. 修改：为 Markdown 增加 height 参数
                # 设置固定高度后，当日志内容超过此高度时，Gradio 会自动生成垂直滚动条
                log_output = gr.Markdown(
                    value="点击下方按钮获取最新日志信息...",
                    label="日志列表",
                    height=500,  # 设置固定高度（像素），激活滚动条
                    container=True  # 增加边框容器感
                )

                refresh_log_btn = gr.Button("🔄 刷新访问日志", variant="primary")

                # 3. 修改：点击事件绑定 log_limit 作为输入
                refresh_log_btn.click(
                    fn=view_logs,
                    inputs=[log_limit],  # 将拖动条的值传给 view_logs 函数
                    outputs=log_output
                )

    return demo


def format_result_card(status, title, message, timestamp, **kwargs):
    styles = {
        "success": {
            "border": "#10b981",
            "bg": "linear-gradient(135deg, #d1fae5 0%, #ecfdf5 100%)",
            "icon": "✅",
            "title_color": "#047857",
        },
        "reject": {
            "border": "#ef4444",
            "bg": "linear-gradient(135deg, #fee2e2 0%, #fef2f2 100%)",
            "icon": "❌",
            "title_color": "#b91c1c",
        },
        "security_reject": {
            "border": "#dc2626",
            "bg": "linear-gradient(135deg, #fecaca 0%, #fef2f2 100%)",
            "icon": "⛔",
            "title_color": "#991b1b",
        },
        "alert": {
            "border": "#f59e0b",
            "bg": "linear-gradient(135deg, #fef3c7 0%, #fffbeb 100%)",
            "icon": "⚠",
            "title_color": "#b45309",
        },
        "warning": {
            "border": "#f97316",
            "bg": "linear-gradient(135deg, #ffedd5 0%, #fff7ed 100%)",
            "icon": "⚡",
            "title_color": "#c2410c",
        },
        "error": {
            "border": "#6b7280",
            "bg": "linear-gradient(135deg, #f3f4f6 0%, #fafafa 100%)",
            "icon": "❗",
            "title_color": "#374151",
        },
    }

    style = styles.get(status, styles["error"])

    details_html = ""

    if status == "success":
        attr = kwargs.get('attributes', {})
        details_html = f"""
            <div style="margin-top: 16px; padding-top: 16px; border-top: 1px solid rgba(0,0,0,0.1);">
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; font-size: 14px; color: #374151;">
                    <div style="background: rgba(255,255,255,0.6); padding: 8px; border-radius: 6px;">
                        <span style="color: #6b7280;">工号</span><br>
                        <strong style="color: #111827; font-size: 16px;">{kwargs.get('employee_id', 'N/A')}</strong>
                    </div>
                    <div style="background: rgba(255,255,255,0.6); padding: 8px; border-radius: 6px;">
                        <span style="color: #6b7280;">相似度</span><br>
                        <strong style="color: #059669; font-size: 16px;">{kwargs.get('similarity', 0):.1%}</strong>
                    </div>
                    <div style="background: rgba(255,255,255,0.6); padding: 8px; border-radius: 6px;">
                        <span style="color: #6b7280;">年龄</span><br>
                        <strong style="color: #111827;">{attr.get('age', '未知')} 岁</strong>
                    </div>
                    <div style="background: rgba(255,255,255,0.6); padding: 8px; border-radius: 6px;">
                        <span style="color: #6b7280;">表情</span><br>
                        <strong style="color: #111827;">{attr.get('expression', '未知')}</strong>
                    </div>
                    <div style="background: rgba(255,255,255,0.6); padding: 8px; border-radius: 6px;">
                        <span style="color: #6b7280;">活体置信度</span><br>
                        <strong style="color: #059669;">{kwargs.get('live_confidence', 0):.2f}</strong>
                    </div>
                    <div style="background: rgba(255,255,255,0.6); padding: 8px; border-radius: 6px;">
                        <span style="color: #6b7280;">画面人数</span><br>
                        <strong style="color: {'#dc2626' if kwargs.get('face_count', 1) > 1 else '#059669'};">
                            {kwargs.get('face_count', 1)} 人
                        </strong>
                    </div>
                </div>
            </div>
            """
    elif status == "security_reject":
        if kwargs.get('confidence') is not None:
            details_html = f"""
                <div style="margin-top: 12px; padding: 8px; background: rgba(255,255,255,0.5); border-radius: 6px; font-size: 12px; color: #7f1d1d;">
                    安全评分: {kwargs["confidence"]:.2f} (阈值: 0.70)
                </div>
                """
    elif status == "alert":
        details_html = f"""
            <div style="margin-top: 12px; padding: 12px; background: rgba(255,255,255,0.6); border-radius: 8px; border-left: 4px solid #f59e0b;">
                <div style="font-size: 14px; color: #92400e; font-weight: 600;">
                    检测到 {kwargs.get("face_count", 0)} 个人脸进入验证区域
                </div>
                <div style="font-size: 12px; color: #b45309; margin-top: 4px;">
                    请保持一人通行，避免尾随风险
                </div>
            </div>
            """
    elif status == "reject" and kwargs.get('attributes'):
        attr = kwargs['attributes']
        details_html = f"""
            <div style="margin-top: 12px; font-size: 13px; color: #6b7280; text-align: center;">
                检测到特征：{attr.get("age", "?")}岁 · {attr.get("gender", "?")} · {attr.get("expression", "?")}
            </div>
            """

    html = f"""
        <div style="border-radius: 16px; padding: 24px; background: {style['bg']}; border: 2px solid {style['border']};
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
            font-family: system-ui, -apple-system, sans-serif; animation: slideIn 0.3s ease-out;">
            <div style="display: flex; align-items: flex-start; gap: 16px;">
                <div style="font-size: 40px; line-height: 1; filter: drop-shadow(0 2px 4px rgba(0,0,0,0.1));">
                    {style['icon']}
                </div>
                <div style="flex: 1;">
                    <div style="font-size: 20px; font-weight: bold; color: {style['title_color']}; margin-bottom: 4px;">
                        {title}
                    </div>
                    <div style="font-size: 12px; color: #6b7280; font-weight: 500; text-transform: uppercase;
                        letter-spacing: 0.05em; margin-bottom: 8px;">
                        {timestamp}
                    </div>
                    <div style="font-size: 16px; color: #1f2937; line-height: 1.5; font-weight: 500;">
                        {message}
                    </div>
                    {details_html}
                </div>
            </div>
        </div>
        <style>
        @keyframes slideIn {{
            from {{ opacity: 0; transform: translateY(-10px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        </style>
        """
    return html
