import cv2

def capture_video_one(video_path, result_video_path, video, result_video, start_time, end_time):
	"""
	功能：截取短视频
	参数：
		video_path：需要截取的视频路径
		result_video_path：截取后的视频存放的路径
		video：需要截取的视频的名称（不带后缀）
		result_video：截取了的视频的名称（不带后缀）
		start_time：截取开始时间（单位s）
		end_time：截取结束时间（单位s）
	"""

	# 读取视屏
	cap = cv2.VideoCapture(video_path + video)

	# 读取视屏帧率
	fps_video = cap.get(cv2.CAP_PROP_FPS)

	# 设置写入视屏的编码格式
	fourcc = cv2.VideoWriter_fourcc(*"mp4v")

	# 获取视屏宽度和高度
	frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
	frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

	# 设置写视屏的对象
	videoWriter = cv2.VideoWriter(result_video_path + result_video, fourcc, fps_video, (frame_width, frame_height))

	# 初始化一个计数器
	acount = 0

	# 初始化帧数
	frame_number = 0

	while (cap.isOpened()):

		# 读取视屏里的图片
		ret, frame = cap.read()

		# 如果视屏没有读取结束
		if ret == True:

			# 计数器加一
			acount += 1

			# 截取相应时间内的视频信息
			if(acount > (start_time * fps_video) and acount <= (end_time * fps_video)):

				# 帧数加1
				frame_number += 1

				# 将图片写入视屏
				videoWriter.write(frame)

			if(acount == (end_time * fps_video)):
				break

		else:
			# 写入视屏结束
			videoWriter.release()
			break

	if frame_number != 150:
		raise Exception('Frame number error: ' + result_video[0:-4])


def capture_video_more(video_path, result_video_path, video, input_string):
	video_string_list = input_string.split('+')
	one_video_string_length = 17

	# 获取要处理的视频的个数
	video_string_list_length = len(video_string_list)

	# 存放字符串中有数字字符的索引
	number_index_list = [0, 2, 3, 5, 7, 8, 10, 11, 12, 13, 14, 15]

	# 检测字符串是否有错误
	for one_video_string in video_string_list:

		# 如果名字字符长度不等于17就检测出错误
		if len(one_video_string) != one_video_string_length:
			raise Exception('Length error: ' + one_video_string + '; The desired length: ' \
				+ str(one_video_string_length) + '; The real length is: ' + str(len(one_video_string)))

		# 检测字符串中的非数字字符是否出错
		if (one_video_string[1] != ':') or (one_video_string[6] != ':') or \
			(one_video_string[4] != '-') or (one_video_string[9] != '(') or (one_video_string[16] != ')'):
			raise Exception('Char error: ' + one_video_string)

		# 检测字符串中数字是否符合规范
		for index in number_index_list:
			if (one_video_string[index] >= '0') and (one_video_string[index] <= '9'):
				pass
			else:
				raise Exception('Number error: ' + one_video_string)

		# 初始化截取的视频的起始和结束时间
		start_time_seconds = int(one_video_string[0]) * 60 + int(one_video_string[2]) * 10 + int(one_video_string[3])
		end_time_seconds = int(one_video_string[5]) * 60 + int(one_video_string[7]) * 10 + int(one_video_string[8])

		# 检测时间是否出错
		if (end_time_seconds - start_time_seconds) != 5:
			raise Exception('Time error: ' + one_video_string)

	# 检测是否有相同的视频名
	if video_string_list_length != 1:
		for one_index in range(video_string_list_length - 1):
			one_video_string_one = video_string_list[one_index]

			for two_index in range(video_string_list_length - one_index - 1):
				one_video_string_two = video_string_list[two_index + one_index + 1]

				if one_video_string_one[10:16] == one_video_string_two[10:16]:
					raise Exception('Name of video error: ' + one_video_string_one + ' and ' + one_video_string_two)

	print("Start processing video!")

	print("Start capturing the video!")

	for one_video_string in video_string_list:

		# 设置截取视频的开始结尾时间
		start_time = int(one_video_string[0]) * 60 + int(one_video_string[2]) * 10 + int(one_video_string[3])
		end_time = int(one_video_string[5]) * 60 + int(one_video_string[7]) * 10 + int(one_video_string[8])

		# 设置返回结果的视频的名称
		result_video = one_video_string[10:16] + '.mp4'

		print(one_video_string[10:16] + 'is successful!')


if __name__ == '__main__':
	video_path = "/Users/yun/Desktop/body_posture_code/my_2s-AGCN/data_videos/long_videos/sleep_all/"
	result_video_path = "short_videos/specific_data/test/"
	video = "sleep_all_1.mp4"
	input_string = '0:19-0:24(500000)+0:20-0:25(500001)'
	capture_video_more(video_path, result_video_path, video, input_string)