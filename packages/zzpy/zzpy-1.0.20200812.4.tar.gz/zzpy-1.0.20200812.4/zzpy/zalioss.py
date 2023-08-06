class OssConfig:
    def __init__(self, access_key_id='', access_key_secret='', bucket='', endpoint=''):
        self.access_key_id = access_key_id
        self.access_key_secret = access_key_secret
        self.bucket = bucket
        self.endpoint = endpoint


class OssFile:
    def __init__(self, config=None):
        import oss2
        if not config:
            from .zconfig import get_param
            config = OssConfig()
            config.access_key_id = get_param("OSS_ACCESS_KEY_ID", default='')
            config.access_key_secret = get_param(
                "OSS_ACCESS_KEY_SECRET", default='')
            config.bucket = get_param("OSS_BUCKET", default='')
            config.endpoint = get_param("OSS_ENDPOINT", default='')
        self.bucket = oss2.Bucket(
            oss2.Auth(config.access_key_id, config.access_key_secret), config.endpoint, config.bucket)

    def download(self, key, file_path):
        """下载文件"""
        return self.bucket.get_object_to_file(key, file_path)

    def upload(self, key, file_path, infrequent_access_flag=True):
        """上传文件，infrequent_access_flag低频标识"""
        import oss2
        headers = {
            'x-oss-storage-class': oss2.BUCKET_STORAGE_CLASS_IA} if infrequent_access_flag else None
        return self.bucket.put_object_from_file(key, file_path)

    def delete(self, prefix):
        key_list = [it.key for it in self.bucket.list_objects(
            prefix=prefix).object_list]
        if len(key_list) > 0:
            return self.bucket.batch_delete_objects(key_list=key_list)
        return None

    def exist(self, key):
        """判断文件是否已存在"""
        return self.bucket.object_exists(key)

    def not_exist(self, key):
        """判断文件是否不存在"""
        return not self.exist(key)

    def meta(self, key):
        """获取文件元信息"""
        return self.bucket.get_object_meta(key)
