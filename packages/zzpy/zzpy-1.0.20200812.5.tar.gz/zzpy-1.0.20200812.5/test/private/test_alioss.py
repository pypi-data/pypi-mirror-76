import zzpy as z
import os
import unittest
import warnings


class TestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        warnings.simplefilter('ignore', ResourceWarning)

    def setUp(self):
        import os
        super().setUp()
        self.root_dir = os.path.join("test", "file")
        from zzpy import init_dir
        init_dir(self.root_dir)

    def tearDown(self):
        from zzpy import remove_dir
        super().tearDown()
        remove_dir(self.root_dir)

    def test_alioss(self):
        config = z.OssConfig(access_key_id="LTAI4Fr9r2aYm6nLxGGzfWU9", access_key_secret="alEzYCJdyqBHLIobHjFHkZXstvxMEn",
                             bucket="data-3rd", endpoint="https://oss-cn-zhangjiakou.aliyuncs.com")
        oss = z.OssFile(config)
        a_path = "setup.py"
        b_path = os.path.join(self.root_dir, "b.py")
        oss.upload("test/setup.py", a_path)
        oss.download("test/setup.py", b_path)
        a = z.read_file(a_path)
        b = z.read_file(b_path)
        self.assertEqual(a, b)
        
    def test_alioss_with_config_file(self):
        oss = z.OssFile()
        a_path = "setup.py"
        b_path = os.path.join(self.root_dir, "b.py")
        oss.upload(key="test/setup1.py", file_path=a_path)
        oss.download(key="test/setup1.py", file_path=b_path)
        a = z.read_file(a_path)
        b = z.read_file(b_path)
        self.assertEqual(a, b)
