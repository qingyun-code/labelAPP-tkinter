from tkinter import messagebox
import time
import cv2

def capture_video_one(video_path, result_video_path, result_video, start_time, end_time):
	"""
	功能：截取短视频
	参数：
		video_path：需要截取的视频路径
		result_video_path：截取后的视频存放的路径
		result_video：截取了的视频的名称（不带后缀）
		start_time：截取开始时间（单位s）
		end_time：截取结束时间（单位s）
	"""

	# 读取视屏
	cap = cv2.VideoCapture(video_path)

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
		# raise Exception('Frame number error: ' + result_video[0:-4])
		messagebox.showerror(message='帧数错误!' + '\n' + '错误视频为' + str(result_video[0:-4]))
		return 'error'

	else:
		return 'true'


def capture_video_more(video_path, result_video_path, input_string, self):
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
			# raise Exception('Length error: ' + one_video_string + '; The desired length: ' \
			# 	+ str(one_video_string_length) + '; The real length is: ' + str(len(one_video_string)))
			messagebox.showerror(message='字符串长度错误!' + '\n' + '错误字符串为：' + str(one_video_string))
			return 'error'

		# 检测字符串中的非数字字符是否出错
		if (one_video_string[1] != ':') or (one_video_string[6] != ':') or \
			(one_video_string[4] != '-') or (one_video_string[9] != '(') or (one_video_string[16] != ')'):
			# raise Exception('Char error: ' + one_video_string)
			messagebox.showerror(message='非数字部分错误!' + '\n' + '错误字符串为：' + str(one_video_string))
			return 'error'

		# 检测字符串中数字是否符合规范
		for index in number_index_list:
			if (one_video_string[index] >= '0') and (one_video_string[index] <= '9'):
				pass
			else:
				# raise Exception('Number error: ' + one_video_string)
				messagebox.showerror(message='数字部分错误!' + '\n' + '错误字符串为：' + str(one_video_string))
				return 'error'

		# 初始化截取的视频的起始和结束时间
		start_time_seconds = int(one_video_string[0]) * 60 + int(one_video_string[2]) * 10 + int(one_video_string[3])
		end_time_seconds = int(one_video_string[5]) * 60 + int(one_video_string[7]) * 10 + int(one_video_string[8])

		# 检测时间是否出错
		if (end_time_seconds - start_time_seconds) != 5:
			# raise Exception('Time error: ' + one_video_string)
			messagebox.showerror(message='时间错误!' + '\n' + '错误字符串为：' + str(one_video_string))
			return 'error'

	# 检测是否有相同的视频名
	if video_string_list_length != 1:
		for one_index in range(video_string_list_length - 1):
			one_video_string_one = video_string_list[one_index]

			for two_index in range(video_string_list_length - one_index - 1):
				one_video_string_two = video_string_list[two_index + one_index + 1]

				if one_video_string_one[10:16] == one_video_string_two[10:16]:
					# raise Exception('Name of video error: ' + one_video_string_one + ' and ' + one_video_string_two)
					messagebox.showerror(message='相同名称错误!' + '\n' + '错误字符串为：' + str(one_video_string_one))
					return 'error'

	print("Start processing video!")

	bar_count = 0

	bar_length = 300

	bar_video_list = len(video_string_list)

	for one_video_string in video_string_list:

		# 设置截取视频的开始结尾时间
		start_time = int(one_video_string[0]) * 60 + int(one_video_string[2]) * 10 + int(one_video_string[3])
		end_time = int(one_video_string[5]) * 60 + int(one_video_string[7]) * 10 + int(one_video_string[8])

		# 设置返回结果的视频的名称
		result_video = one_video_string[10:16] + '.mp4'

		capture_video_result = capture_video_one(video_path, result_video_path, result_video, start_time, end_time)

		if capture_video_result == 'error':
			return 'error'

		bar_count += 1

		self.bar['value'] = (bar_count * bar_length) // bar_video_list
		self.page.update()
		# print('bar_count=' + str(bar_count) + ';' + 'bar_video_list=' + str(bar_video_list) + ';' + 'value=' + str((bar_count * bar_length) // bar_video_list))
		# time.sleep(0.05)

		print(one_video_string[10:16] + 'is successful!')

	print("All are successful!")

	messagebox.showinfo(message='全部剪切成功!')

if __name__ == '__main__':
	video_path = "/Users/yun/Desktop/body_posture_code/my_2s-AGCN/data_videos/long_videos/sit_all/"
	result_video_path = "short_videos/all_data/up_data/"
	video = "sit_all_2.mp4"
	input_string = '0:10-0:15(800057)+0:11-0:16(800058)+0:12-0:17(800059)+0:13-0:18(800060)+0:25-0:30(800061)+0:26-0:31(800062)+0:27-0:32(800063)+0:45-0:50(800064)+0:46-0:51(800065)+0:47-0:52(800066)+0:48-0:53(800067)+1:14-1:19(800068)+1:15-1:20(800069)+1:16-1:21(800070)+1:17-1:22(800071)+1:33-1:38(800072)+1:34-1:39(800073)+1:35-1:40(800074)+1:36-1:41(800075)+1:47-1:52(800076)+1:48-1:53(800077)+1:49-1:54(800078)+1:50-1:55(800079)+2:01-2:06(800080)+2:02-2:07(800081)+2:03-2:08(800082)+2:04-2:09(800083)+2:20-2:25(800084)+2:21-2:26(800085)+2:22-2:27(800086)+2:23-2:28(800087)+2:39-2:44(800088)+2:40-2:45(800089)+2:41-2:46(800090)+2:42-2:47(800091)+2:53-2:58(800092)+2:54-2:59(800093)+2:55-3:00(800094)+3:06-3:11(800095)+3:07-3:12(800096)+3:08-3:13(800097)+3:26-3:31(800098)+3:27-3:32(800099)+3:28-3:33(800100)+3:29-3:34(800101)+3:40-3:45(800102)+3:41-3:46(800103)+3:42-3:47(800104)+3:54-3:59(800105)+3:55-4:00(800106)+3:56-4:01(800107)+4:06-4:11(800108)+4:07-4:12(800109)+4:08-4:13(800110)+4:22-4:27(800111)+4:23-4:28(800112)+4:24-4:29(800113)+4:25-4:30(800114)+4:35-4:40(800115)+4:36-4:41(800116)+4:37-4:42(800117)+4:38-4:43(800118)+4:50-4:55(800119)+4:51-4:56(800120)+4:52-4:57(800121)'
	capture_video_more(video_path, result_video_path, video, input_string)