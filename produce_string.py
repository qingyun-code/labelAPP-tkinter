from tkinter import messagebox

def produce_string(input_string, video_name):

	long_string_length = 19

	short_string_length = 9

	input_string_list = input_string.split('+')

	if len(input_string_list[0]) == long_string_length:
		return produce_string_long(input_string, video_name)
	elif len(input_string_list[0]) == short_string_length:
		return produce_string_short(input_string, video_name)
	else:
		messagebox.showerror(message='时间段错误!' + '\n' + '您输入的时间段字符数为：' + str(len(input_string_list[0])))
		return 'error'


def produce_string_long(input_string_long, video_name):

	one_long_string_length = 19

	long_number_index_list = [0, 2, 3, 5, 7, 8, 10, 12, 13, 15, 17, 18]

	input_string_long_list = input_string_long.split('+')

	# 定义要把每段时间范围连起来的总的字符串
	all_string = ''

	# print(input_string_long_list)
	for input_string_long_one in input_string_long_list:

		# 如果名字字符长度不等于19就检测出错误
		if len(input_string_long_one) != one_long_string_length:
			# raise Exception('Length error: ' + input_string_long_one + '; The desired length: ' \
			# 	+ str(one_long_string_length) + '; The real length is: ' + str(len(input_string_long_one)))
			messagebox.showerror(message='字符串长度错误!' + '\n' + '错误字符串为：' + str(input_string_long_one))
			return 'error'

		# 检测字符串中的非数字字符是否出错
		if (input_string_long_one[1] != ':') or (input_string_long_one[6] != ':') or \
			(input_string_long_one[11] != ':') or (input_string_long_one[16] != ':') or \
			(input_string_long_one[4] != '-') or (input_string_long_one[9] != '-') or (input_string_long_one[14] != '-'):
			# raise Exception('Char error: ' + input_string_long_one)
			messagebox.showerror(message='字符错误!' + '\n' + '错误字符串为：' + str(input_string_long_one))
			return 'error'

		# 检测字符串中数字是否符合规范
		for index in long_number_index_list:
			if (input_string_long_one[index] >= '0') and (input_string_long_one[index] <= '9'):
				pass
			else:
				# raise Exception('Number error: ' + input_string_long_one)
				messagebox.showerror(message='数字不规范错误!' + '\n' + '错误字符串为：' + str(input_string_long_one))
				return 'error'

		# 初始化各阶段的时间，单位为s
		t1 = int(input_string_long_one[0]) * 60 + int(input_string_long_one[2]) * 10 + int(input_string_long_one[3])
		t2 = int(input_string_long_one[5]) * 60 + int(input_string_long_one[7]) * 10 + int(input_string_long_one[8])
		t3 = int(input_string_long_one[10]) * 60 + int(input_string_long_one[12]) * 10 + int(input_string_long_one[13])
		t4 = int(input_string_long_one[15]) * 60 + int(input_string_long_one[17]) * 10 + int(input_string_long_one[18])

		# 检测时间是否出错
		if ((t3 - t2) > 5) or ((t4 - t1) < 5) or (t1 > t2) or (t2 > t3) or (t3 > t4):
			# raise Exception('Time error: ' + input_string_long_one)
			messagebox.showerror(message='时间错误!' + '\n' + '错误字符串为：' + str(input_string_long_one))
			return 'error'

		# 初始化起始时间
		if (t3 - 5) < t1:
			start_time = t1
		else:
			start_time = t3 - 5

		# 初始化结束时间
		if (t2 + 5) > t4:
			end_time = t4
		else:
			end_time = t2 + 5

		# print(input_string_long_one + ':')

		# 打印要得到的字符
		while (start_time + 5) <= end_time:

			# 初始化输出字符
			output_string = str(start_time // 60) + ':'

			# 添加分和秒位数字
			if (start_time % 60) > 9:
				output_string += str(start_time % 60)
			else:
				output_string += ('0' + str(start_time % 60))

			# 添加起始和结束的连接符
			output_string += '-'

			# 初始化这次的结束时间
			one_end_time = start_time + 5

			# 拼接结束时间的字符串
			output_string += str(one_end_time // 60) + ':'

			if (one_end_time % 60) > 9:
				output_string += str(one_end_time % 60)
			else:
				output_string += ('0' + str(one_end_time % 60))

			# 拼接视频名字的字符串
			output_string += ('(' + video_name + ')')

			# 判断是否要换行
			# if (one_end_time + 1) <= end_time:
			# 	print(output_string + '+',end='')
			# else:
			# 	print(output_string + '\n')

			# 把要输出的文件名和时间范围连起来
			all_string += (output_string + '+')

			# 开始时间加一
			start_time += 1

			# 视频名字加一
			video_name = str(int(video_name) + 1)

	# 打印出最后要输出的总的字符串
	# print('All string is:')
	# print(all_string[0:-1])
	return str(all_string[0:-1])

def produce_string_short(input_string_short, video_name):

	one_short_string_length = 9

	short_number_index_list = [0, 2, 3, 5, 7, 8]

	input_string_short_list = input_string_short.split('+')

	# 定义要把每段时间范围连起来的总的字符串
	all_string = ''

	# print(input_string_short_list)
	for input_string_short_one in input_string_short_list:

		# 如果名字字符长度不等于9就检测出错误
		if len(input_string_short_one) != one_short_string_length:
			# raise Exception('Length error: ' + input_string_short_one + '; The desired length: ' \
			# 	+ str(one_long_string_length) + '; The real length is: ' + str(len(input_string_short_one)))
			messagebox.showerror(message='字符串长度错误!' + '\n' + '错误字符串为：' + str(input_string_short_one))
			return 'error'

		# 检测字符串中的非数字字符是否出错
		if (input_string_short_one[1] != ':') or (input_string_short_one[6] != ':') or \
			(input_string_short_one[4] != '-'):
			# raise Exception('Char error: ' + input_string_short_one)
			messagebox.showerror(message='字符错误!' + '\n' + '错误字符串为：' + str(input_string_short_one))
			return 'error'

		# 检测字符串中数字是否符合规范
		for index in short_number_index_list:
			if (input_string_short_one[index] >= '0') and (input_string_short_one[index] <= '9'):
				pass
			else:
				# raise Exception('Number error: ' + input_string_short_one)
				messagebox.showerror(message='数字不规范错误!' + '\n' + '错误字符串为：' + str(input_string_short_one))
				return 'error'

		# 初始起始和结束时间，单位为s
		start_time = int(input_string_short_one[0]) * 60 + int(input_string_short_one[2]) * 10 + int(input_string_short_one[3])
		end_time = int(input_string_short_one[5]) * 60 + int(input_string_short_one[7]) * 10 + int(input_string_short_one[8])

		# print(input_string_short_one + ':')

		# 打印要得到的字符
		while (start_time + 5) <= end_time:

			# 初始化输出字符
			output_string = str(start_time // 60) + ':'

			# 添加分和秒位数字
			if (start_time % 60) > 9:
				output_string += str(start_time % 60)
			else:
				output_string += ('0' + str(start_time % 60))

			# 添加起始和结束的连接符
			output_string += '-'

			# 初始化这次的结束时间
			one_end_time = start_time + 5

			# 拼接结束时间的字符串
			output_string += str(one_end_time // 60) + ':'

			if (one_end_time % 60) > 9:
				output_string += str(one_end_time % 60)
			else:
				output_string += ('0' + str(one_end_time % 60))

			# 拼接视频名字的字符串
			output_string += ('(' + video_name + ')')

			# 判断是否要换行
			# if (one_end_time + 1) <= end_time:
			# 	print(output_string + '+',end='')
			# else:
			# 	print(output_string + '\n')

			# 把要输出的文件名和时间范围连起来
			all_string += (output_string + '+')

			# 开始时间加一
			start_time += 1

			# 视频名字加一
			video_name = str(int(video_name) + 1)

	# 打印出最后要输出的总的字符串
	# print('All string is:')
	# print(all_string[0:-1])
	return str(all_string[0:-1])

if __name__ == '__main__':

	# input_string_long = '0:10-0:13-0:15-0:19+0:25-0:27-0:29-0:33+0:45-0:48-0:50-0:53+1:13-1:17-1:19-1:22+1:33-1:36-1:38-1:42+1:47-1:50-1:52-1:55+2:00-2:04-2:06-2:10+2:18-2:23-2:25-2:28+2:39-2:42-2:44-2:47+2:53-2:55-2:57-3:01+3:05-3:09-3:11-3:13+3:26-3:29-3:31-3:35+3:40-3:42-3:44-3:47+3:53-3:57-3:59-4:01+4:06-4:08-4:10-4:13+4:22-4:25-4:27-4:30+4:35-4:38-4:40-4:44+4:48-4:53-4:55-4:57'
	# video_name = '800057'
	# produce_string_long(input_string_long, video_name)

	# input_string_short = '2:17-3:31+3:39-4:18+4:30-5:00'
	# input_string_short = '2:17-3:31'
	# video_name = '300119'
	# produce_string_short(input_string_short, video_name)

	input_string = '0:10-0:13-0:15-0:19+0:25-0:27-0:29-0:33'
	video_name = '300119'
	produce_string(input_string, video_name)
