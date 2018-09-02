from utils import *


def is_valid(url, path):
	if url is '':
		print('请输入视频链接...')
		gui.GUIOperate.write_scrolled_text('请输入视频链接...\n')
		return None
	else:
		url_pattern = re.compile('[a-zA-z]+://[^\s]*', re.S)
		result = re.search(url_pattern, url)
		if result is None:
			print('错误的视频链接，请重新输入...')
			gui.GUIOperate.write_scrolled_text('错误的视频链接，请重新输入...\n')
			return None
		else:
			if path is '':
				print('请输入视频保存路径...')
				gui.GUIOperate.write_scrolled_text('请输入视频保存路径...\n')
				return None
			else:
				path_pattern = re.compile('(^[a-zA-Z]:/[.-0-9a-zA-Z_]+(/[.-0-9a-zA-Z_]+)*$)|(^[a-zA-Z]:/[.-0-9a-zA-Z_]*$)', re.S)
				result = re.search(path_pattern, path)
				if result is None:
					print('错误的文件路径，请重新输入...')
					gui.GUIOperate.write_scrolled_text('错误的文件路径，请重新输入...\n')
					return None
				else:
					return True


# http://www.vipjiexi.com/tong.php?url=[播放地址或视频id]
def get_m3u8_url_route_1(url):
	real_url = 'http://www.wq114.org/tong.php?url=' + url
	html = get_page(real_url)
	if html:
		pattern = re.compile('<iframe.*?src=.*?url=(.*?)\".*?</iframe>', re.S)
		m3u8_url = re.search(pattern, html)
		if m3u8_url:
			return m3u8_url.group(1)
		else:
			print('未找到视频...')
			gui.GUIOperate.write_scrolled_text('未找到视频...\n')
			return None
	return None


# http://www.wmxz.wang/video.php?url=[播放地址或视频id]
def get_m3u8_url_route_2(url):
	real_url = 'http://www.82190555.com/index.php?url=' + url
	html_index = get_page(real_url)
	if html_index:
		pat_index = re.compile('<iframe.*?src=\"(.*?url=.*?)\".*?</iframe>', re.S)
		m3u8_index = re.search(pat_index, html_index)
		if m3u8_index:
			m3u8_index = m3u8_index.group(1)
			html_m3u8_index = get_page(m3u8_index, real_url)
			if html_m3u8_index:
				pat_m3u8_index = re.compile('(https://.*?index.m3u8)', re.S)
				m3u8_index_url = re.search(pat_m3u8_index, html_m3u8_index)
				if m3u8_index_url:
					m3u8_index_url = m3u8_index_url.group(1)
					html_m3u8_url = get_m3u8_content(m3u8_index_url)
					file_line = html_m3u8_url.split('\n')
					for index, line in enumerate(file_line):
						if "EXT-X-STREAM-INF" in line:
							m3u8_content = str(file_line[index + 1])
							return m3u8_index_url.replace('index.m3u8', m3u8_content)
					print('未找到视频...')
					gui.GUIOperate.write_scrolled_text('未找到视频...\n')
					return None
				return None
			return None
		return None
	return None
	

def run(url, path, name):
	if is_valid(url, path):  # 判断有效性
		gui.GUIOperate.change_entry_fg('#F5F5F5')
		m3u8_url = get_m3u8_url_route_2(url)
		if m3u8_url:
			download_m3u8(m3u8_url, path, name)
		else:
			m3u8_url = get_m3u8_url_route_1(url)
			if m3u8_url:
				download_m3u8(m3u8_url, path, name)


if __name__ == '__main__':
	_url = 'http://www.iqiyi.com/v_19rr839kro.html'
	_path = 'E:/PycharmProjects/Video_Crack/video'
	_name = 'movie'
	run(_url, _path, _name)
