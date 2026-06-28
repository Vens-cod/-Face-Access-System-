import json
import os
from datetime import datetime
import requests
from huaweicloudsdkcore.auth.credentials import BasicCredentials
from huaweicloudsdkcore.auth.credentials import DerivationAKSKSigner
from huaweicloudsdkcore.sdk_request import SdkRequest
from config import Config


class VoiceService:
    """语音服务（华为云 SIS TTS）。
    功能:
    - 根据姓名/人员类型生成欢迎语
    - 调用 SIS TTS 生成 wav 文件
    - 本地缓存（按 person_name + hour）避免重复请求
    """

    def __init__(self, ak, sk, project_id, region):
        self.ak = ak
        self.sk = sk
        self.project_id = project_id
        self.region = region
        # 修改点：改用相对路径，增加 Windows 兼容性
        self.cache_dir = os.path.join(os.getcwd(), "voice_cache")
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir, exist_ok=True)
        # self.cache_dir = "/tmp/voice_cache"
        # os.makedirs(self.cache_dir, exist_ok=True)

    def generate_welcome(self, person_name, person_type="employee"):
        """生成欢迎语音。
        参数:
        person_name: 人员姓名
        person_type: employee/vip/visitor（影响欢迎语文案）
        返回:
        (success, result)
        - success=True: result 为 wav 文件路径
        - success=False: result 为错误信息
        """
        try:
            # 根据时间段生成不同的问候语
            hour = datetime.now().hour
            if 5 <= hour < 12:
                greeting = "早上好"
            elif 12 <= hour < 14:
                greeting = "中午好"
            elif 14 <= hour < 18:
                greeting = "下午好"
            else:
                greeting = "晚上好"

            # 根据人员类型生成不同文案
            if person_type == "employee":
                text = f"{person_name}，{greeting}，欢迎回到公司，祝您工作愉快。"
            elif person_type == "vip":
                text = f"尊敬的{person_name}，{greeting}，欢迎莅临指导。"
            elif person_type == "visitor":
                text = f"尊敬的访客{person_name}，{greeting}，欢迎光临，请配合登记。"
            else:
                text = f"{greeting}，欢迎光临。"

            # 缓存：同一个人同一个小时使用同一份语音
            cache_file = os.path.join(
                self.cache_dir, f"welcome_{person_name}_{hour}.wav"
            )

            if os.path.exists(cache_file):
                return True, cache_file

            # 构建请求
            body = {
                "text": text,
                "config": {
                    "audio_format": "wav",
                    "sample_rate": "16000",
                    "property": "chinese_xiaoyan_common",
                    "speed": Config.VOICE_SPEED,
                    "pitch": 0,
                    "volume": Config.VOICE_VOLUME,
                },
            }
            body_json = json.dumps(body, ensure_ascii=False)

            # 发送请求（简化版，实际需处理多 endpoint 重试）
            host = f"sis.{self.region}.myhuaweicloud.com"
            resource_path = f"/v1/{self.project_id}/tts"

            signer = DerivationAKSKSigner(BasicCredentials(self.ak, self.sk))
            sdk_req = SdkRequest(
                method="POST",
                schema="https",
                host=host,
                resource_path=resource_path,
                query_params=[],
                header_params={"Content-Type": "application/json"},
                body=body_json,
            )

            # 签名请求
            sdk_req = signer.sign(sdk_req, derived_auth_service_name="sis", region_id=self.region)
            url = f"https://{host}{resource_path}"

            resp = requests.post(
                url,
                headers=sdk_req.header_params,
                data=body_json.encode("utf-8"),
                timeout=10
            )

            if resp.status_code == 200:
                with open(cache_file, "wb") as f:
                    f.write(resp.content)
                return True, cache_file
            else:
                return False, f"TTS 失败: {resp.status_code}, {resp.text}"

        except Exception as e:
            return False, str(e)

# import os
# import json
# from datetime import datetime
# from huaweicloudsdkcore.auth.credentials import BasicCredentials
# from huaweicloudsdksis.v1.region.sis_region import SisRegion
# from huaweicloudsdksis.v1 import *
# from huaweicloudsdkcore.exceptions import exceptions
# from config import Config
#
#
# class VoiceService:
#     def __init__(self, ak, sk, project_id, region):
#         # 初始化凭据
#         self.credentials = BasicCredentials(ak, sk)
#         self.project_id = project_id
#         self.region_id = region
#
#         # 初始化客户端
#         self.client = SisClient.new_builder() \
#             .with_credentials(self.credentials) \
#             .with_region(SisRegion.value_of(region)) \
#             .build()
#
#         # 缓存目录
#         self.cache_dir = os.path.join(os.getcwd(), "voice_cache")
#         if not os.path.exists(self.cache_dir):
#             os.makedirs(self.cache_dir, exist_ok=True)
#
#     def generate_welcome(self, person_name, person_type="employee"):
#         try:
#             # 1. 构造文案
#             hour = datetime.now().hour
#             greeting = "早上好" if 5 <= hour < 12 else "下午好" if 12 <= hour < 18 else "晚上好"
#             text = f"{person_name}，{greeting}！欢迎回来。"
#
#             # 2. 缓存检查
#             filename = f"{person_name}_{hour}.wav"
#             cache_file = os.path.join(self.cache_dir, filename)
#             if os.path.exists(cache_file):
#                 return True, cache_file
#
#             print(f"[TTS] 正在合成: {text}")
#
#             # 3. 构造请求对象 (官方 SDK 方式)
#             # 注意：property 的格式需严格遵守：chinese_{voice_type}_common
#             property_val = f"chinese_{Config.VOICE_TYPE}_common"
#
#             request = RunTtsRequest()
#             body = PostCustomTTSReq(
#                 text=text,
#                 config=TtsCustomConfig(
#                     audio_format="wav",
#                     sample_rate="16000",
#                     property=property_val,
#                     speed=Config.VOICE_SPEED,
#                     volume=Config.VOICE_VOLUME,
#                     pitch=0
#                 )
#             )
#             request.body = body
#
#             # 4. 发送请求
#             response = self.client.run_tts(request)
#
#             # 5. 保存文件
#             # 注意：SDK 返回的 result 里包含 result_base64 或者直接在某些版本返回 content
#             # SIS SDK 的 RunTtsResponse 通常直接包含 result 字段
#             if hasattr(response, 'result'):
#                 # 处理 base64 结果
#                 import base64
#                 with open(cache_file, "wb") as f:
#                     f.write(base64.b64decode(response.result.data))
#
#                 print(f"[TTS] 合成成功，文件已存至: {cache_file}")
#                 return True, cache_file
#             else:
#                 return False, "SDK 返回结果异常"
#
#         except exceptions.ClientRequestException as e:
#             error_msg = f"请求错误: {e.status_code}, {e.error_msg}"
#             print(f"[TTS Error] {error_msg}")
#             return False, error_msg
#         except Exception as e:
#             print(f"[TTS Exception] {str(e)}")
#             return False, str(e)