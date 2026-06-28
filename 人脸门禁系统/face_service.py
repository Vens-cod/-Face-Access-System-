# face_service.py
import base64
import io
from PIL import Image
from huaweicloudsdkcore.auth.credentials import BasicCredentials
from huaweicloudsdkfrs.v2.region.frs_region import FrsRegion
from huaweicloudsdkcore.exceptions import exceptions
from huaweicloudsdkfrs.v2 import *


class FaceRecognitionService:
    """
    华为云⼈脸识别服务封装类。
    该类封装了华为云FRS（Face Recognition Service）SDK的调⽤，提供更简洁的接⼝供上层业务使⽤。
    主要功能：
    -⼈脸检测：检测图像中的⼈脸并返回属性
    -⼈脸⼊库：将⼈脸添加到华为云⼈脸库
    -⼈脸搜索：1:N搜索（后续实现）
    -⼈脸⽐对：1:1⽐对（后续实现）
    -活体检测：静默活体检测（后续实现）
    """

    def __init__(self, ak, sk, project_id, region, face_set_name, face_set_capacity=10000):
        """初始化⼈脸服务客⼾端。
        参数:
            ak (str):华为云访问密钥ID (Access Key)获取⽅式：华为云控制台→我的凭证→访问密钥
            sk (str):华为云访问密钥密码(Secret Key)与AK配对使⽤，⽤于请求签名
            project_id (str):华为云项⽬ID获取⽅式：华为云控制台→我的凭证→项⽬列表
            region (str):服务区域代码，如'cn-north-4'（北京四）不同区域的服务端点不同
            face_set_name (str):⼈脸库名称，需在华为云控制台预先创建
            face_set_capacity (int):⼈脸库容量限制，默认10000单个⼈脸库最⼤⽀持的⼈脸数量
        """
        self.ak = ak
        self.sk = sk
        self.project_id = project_id
        self.region = region
        self.face_set_name = face_set_name
        self.face_set_capacity = face_set_capacity

        # 初始化客⼾端
        credentials = BasicCredentials(ak, sk)
        self.client = (
            FrsClient.new_builder()
            .with_credentials(credentials)
            .with_region(FrsRegion.value_of(region))
            .build()
        )
        self.face_search_enabled = False  # 后续步骤完善

    def init_face_set(self):
        """

        初始化⼈脸库
        若⼈脸库不存在，则创建
        若已存在

        则

        将⼈脸库的标记改为
        True

        返回值                str
        ⽤于在⻚⾯上显⽰⼈脸库的状态
        """
        try:
            # 发起请求

            request = CreateFaceSetRequest()
            request.body = CreateFaceSetReq(
                face_set_name=self.face_set_name,
                face_set_capacity=self.face_set_capacity
            )
            print(request.body)
            self.client.create_face_set(request)

            #修改标记

            self.face_search_enabled = True
            return "⼈脸库创建成功"
        except exceptions.ClientRequestException as e:
            if "FRS.0032" in str(e.error_code) or "exist" in str(e.error_msg):
                #⼈脸库已经存在

                self.face_search_enabled = True
                return "⼈脸库已经存在"
            return f"⼈脸库创建失败：{e.error_msg}"

    def pil_to_base64(self, pil_image):
        """PIL图⽚转 base64字符串。

        华为云接⼝这⾥使⽤base64传图。
        """
        # 统⼀转成JPEG，避免不同输⼊格式导致的编码差异
        buffer = io.BytesIO()
        pil_image.save(buffer, format='JPEG')
        return base64.b64encode(buffer.getvalue()).decode()

    def detect_face(self, pil_image, attributes="2,4,6,7,12,13"):
        """⼈脸检测。

        参数:
        - pil_image: PIL.Image
        - attributes:需要返回的⼈脸属性字段（由华为云接⼝定义）
        2=年龄, 4=性别, 6=表情, 7=⼝罩, 12=质量分, 13=姿态
        返回:
        - DetectFaceByBase64Response或{"error": "..."}
        """
        try:
            request = DetectFaceByBase64Request()
            request.body = FaceDetectBase64Req(
                attributes=attributes,
                image_base64=self.pil_to_base64(pil_image)
            )
            return self.client.detect_face_by_base64(request)
        except exceptions.ClientRequestException as e:
            return {"error": str(e.error_msg)}

    def extract_attributes(self, face):
        """从 SDK的 face对象中提取常⽤属性。

        说明：
        - SDK返回对象字段是可选的（hasattr/None），这⾥做了兼容性判断。
        """
        result = {}
        if not face or not face.attributes:
            return result

        attrs = face.attributes

        if hasattr(attrs, 'age') and attrs.age:
            result['age'] = attrs.age
        if hasattr(attrs, 'gender') and attrs.gender:
            result['gender'] = attrs.gender
        if hasattr(attrs, 'mask') and attrs.mask:
            result['mask'] = attrs.mask
        if hasattr(attrs, 'expression') and attrs.expression:
            if hasattr(attrs.expression, 'type'):
                result['expression'] = attrs.expression.type
        if hasattr(attrs, 'quality') and attrs.quality:
            if hasattr(attrs.quality, 'total_score'):
                result['quality_score'] = attrs.quality.total_score

        return result

    def add_face(self, pil_image, external_image_id):
        """
        添加⼈脸到库。
        参数
        :- pil_image: PIL.Image- external_image_id:
        外部
         ID
        （项⽬⾥⽤员⼯编号）
        返回
        :- face_id
        或
         None
        """
        if not self.face_search_enabled:
            # FaceSet 未初始化成功时，不允许⼊库/搜索
            # 实际⽣产环境应先创建⼈脸库
            print("⚠ 警告：face_search_enabled = False ，但仍尝试⼊库")

        try:
            request = AddFacesByBase64Request()
            request.face_set_name = self.face_set_name
            request.body = AddFacesBase64Req(
                image_base64=self.pil_to_base64(pil_image),
                # external_image_id 会在 1:N 搜索命中时回传，⽤于与本地员⼯库关联
                external_image_id=external_image_id
            )
            response = self.client.add_faces_by_base64(request)
            # SDK 可能返回多张⼈脸，这⾥取第⼀张 face_id
            face_id = response.faces[0].face_id if response.faces else None
            print(f"✅ ⼈脸⼊库成功，face_id: {face_id}")
            return face_id

        except exceptions.ClientRequestException as e:
            print(f"❌ 添加⼈脸失败: {e.error_msg}")
            return None

    def live_detect_silent(self, pil_image):
        """静默活体检测 - 单张图⽚判断是否为真⼈。
         适⽤场景：
         - 摄像头实时抓拍验证
         - 上传照⽚验证
         参数:
         pil_image: PIL.Image 对象
         返回:
         (is_alive, confidence, message)
         - is_alive: bool，是否为真⼈
         - confidence: float，置信度分数
         - message: str，描述信息
         """

        try:
            image_base64 = self.pil_to_base64(pil_image)
            request = DetectLiveFaceByBase64Request()
            request.body = LiveDetectFaceBase64Req(image_base64=image_base64)
            response = self.client.detect_live_face_by_base64(request)

            result = getattr(response, "result", None)
            if not result:
                raise RuntimeError("live-detect empty result")

            # alive/confidence 字段来⾃华为云 SDK 响应
            is_alive = bool(getattr(result, "alive", False))
            confidence = getattr(result, "confidence", 0) or 0

            message = "真⼈" if is_alive else "⾮活体攻击"
            return is_alive, float(confidence), message
        except Exception as e:
            print(f"静默活体检测失败: {e}")
            raise

    def search_face(self, pil_image, top_n=1, threshold=0.7):
        """1:N ⼈脸搜索。
         从⼈脸库中搜索与输⼊图⽚最相似的⼈脸，返回匹配结果。
         参数:
         pil_image: PIL.Image 对象
         top_n: 返回前N个最相似的结果
         threshold: 相似度阈值，低于此值的结果会被过滤
         返回:
         list[SearchFace] - 每个结果包含：
         - face_id: ⼈脸唯⼀标识
         - external_image_id: 外部ID（即员⼯编号）
         - similarity: 相似度（0~1）
         """

        if not self.face_search_enabled:
            # FaceSet 未准备好时直接返回空，避免上层误判
            return []
        try:
            request = SearchFaceByBase64Request()
            request.face_set_name = self.face_set_name
            request.body = FaceSearchBase64Req(
                image_base64=self.pil_to_base64(pil_image),
                top_n=top_n,
                threshold=threshold  # 阈值越⾼越严格
            )
            response = self.client.search_face_by_base64(request)
            return response.faces if response else []
        except exceptions.ClientRequestException as e:
            print(f"⼈脸搜索失败: {e.error_msg}")
            return []

    # face_service.py（在 FaceRecognitionService 类中新增）

    def compare_faces(self, image1, image2):
        """1:1 人脸比对。

        将两张人脸图片进行比对，返回相似度分数。
        适用于二次确认或人工复核场景。

        参数:
            image1: PIL.Image 第一张人脸图片
            image2: PIL.Image 第二张人脸图片

        返回:
            float: 相似度（0~1），1表示完全相同
        """
        try:
            request = CompareFaceByBase64Request()
            request.body = FaceCompareBase64Req(
                image1_base64=self.pil_to_base64(image1),
                image2_base64=self.pil_to_base64(image2)
            )
            response = self.client.compare_face_by_base64(request)
            return response.similarity if response else 0
        except exceptions.ClientRequestException as e:
            print(f"人脸比对失败: {e.error_msg}")
            return 0
