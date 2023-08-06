# _*_coding:utf-8_*_
import unittest

from load_m3u8 import resolve


class TestUtil(unittest.TestCase):
    def test_download(self):
        m3u8_url = "http://www.youtube.com/test.m3u8"
        m3u8_url ="D://4026ab9a5b92f4424519c7be60d2f4f5//hls//k0915hr6r1t.322012.hls//.m3u8"
        m3u8_url ="https://video-tx.huke88.com/5cf26bebvodtranscq1256517420/f736d2235285890794934977725/drm/v.f240.m3u8?rlimit=3&t=5f37ee92&sign=50cad1c3b068cdbbf2755f746e6005d0&us=1597490274"
        load_obj = resolve.Load_M3U8(m3u8_url)
        load_obj.run()