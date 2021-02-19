from abc import ABC
from abc import abstractmethod


class ImageHosting(ABC):
    """图床服务基类

    Attributes:
        url: 图床服务地址
    """
    def __init__(self):
        self.url = None

    @abstractmethod
    def upload(self, img_path):
        
        """上传图片
        Args:
            img_path: 本地图片文件路径
        Return:
            图片网络地址
        """
        ...


class SMMSImageHosting(ImageHosting):
    
    def __init__(self):
        self.url = "https://sm.ms/api/upload"
    
    def upload(self, img_path):
    
