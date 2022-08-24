# -*- coding: UTF-8 -*-
import os
import cv2

import argparse

# 导入mediapipe人工智能工具包
import mediapipe as mp

def parse_args():

	parser = argparse.ArgumentParser("Evaluation Parameters")

	parser.add_argument(
		'--video_name',
		type=str,
		default='aaaaaa',
		help='the directory of test images')

	parser.add_argument(
		'--video_path',
		type=str,
		default='aaaaaa',
		help='the directory of test images')

	parser.add_argument(
		'--error_path',
		type=str,
		default='aaaaaa',
		help='the directory of test images')

	parser.add_argument(
		'--tag_path',
		type=str,
		default='aaaaaa',
		help='the directory of test images')

	parser.add_argument(
		"--digit",
		type=int,
		default=123,
		help="输入数字")

	args = parser.parse_args()

	return args

args = parse_args()

# 导入solution
mp_pose = mp.solutions.pose

# 导入模型
pose = mp_pose.Pose(static_image_mode=False,      # 是静态图片还是连续视频帧
					model_complexity=1,           # 选择人体姿态关键点检测模型，0性能差但快，2性能好但慢，1介于两者之间
					smooth_landmarks=True,        # 是否平滑关键点
					enable_segmentation=True,     # 是否人体抠图
					min_detection_confidence=0.5, # 置信度阈值
					min_tracking_confidence=0.5)  # 追踪阈值
video_path = args.video_path

error_path = args.error_path

tag_path = args.tag_path

false_tag = 0

# 创建对应的出错文件
# with open('/Users/mac/Desktop/temp/test/error.txt', 'a') as error_file:
with open(error_path + 'error.txt', 'a') as error_file:

	# 创建对应的标签文件
	# with open('/Users/mac/Desktop/temp/test/' + args.video_name.split('.')[0] + '.txt', 'w') as tag_file:
	with open(tag_path + args.video_name.split('.')[0] + '.txt', 'w') as tag_file:
		cap = cv2.VideoCapture(video_path + args.video_name)

		count_frame = 0

		# 无限循环，直到break被触发
		while cap.isOpened():

			# 获取画面
			success, frame = cap.read()

			if not success:
				if count_frame == 150:
					print(args.video_name.split('.')[0] + ' ' + 'write success !')
					break
				else:
					print('Error:' + args.video_name.split('.')[0] + ' is not success!!!')

					false_tag = 1

					break

			count_frame += 1

			# 得到原始图像的高和宽
			h = frame.shape[0]
			w = frame.shape[1]

			# BGR转RGB
			img_RGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

			# 将RGB图像输入模型，获取预测结果
			results = pose.process(img_RGB)

			# 需要显示的关节点列表
			all_joint = [15, 13, 11, 23, 25, 27, 12, 24, 26, 28, 14, 16, 0, 7, 8, 2, 5, 33]
			# 分别对应的openpose中的各个关节点：
			#             0    1   2   3   4   5   6   7   8   9  10  11 12 13 14 15 16  17

			if results.pose_landmarks:

				for joint_num in all_joint:

					# 33号关键点blasepose中没有，所以加上
					if joint_num == 33:

						# 选择骨骼两端中置信度最小的关节的置信度为33号关节点的置信度
						if results.pose_landmarks.landmark[11].visibility < \
							results.pose_landmarks.landmark[12].visibility:
							visibility = results.pose_landmarks.landmark[11].visibility
						else:
							visibility = results.pose_landmarks.landmark[12].visibility

						# 赋值归一化后的横纵坐标值
						x = (results.pose_landmarks.landmark[11].x + \
								  results.pose_landmarks.landmark[12].x) / 2.
						y = (results.pose_landmarks.landmark[11].y+ \
								  results.pose_landmarks.landmark[12].y) / 2.

						tag_file.write(str(x) + '_' + str(y) + '_' + str(visibility))

					else:
						# 赋值归一化后的横纵坐标值还有置信度
						x = results.pose_landmarks.landmark[joint_num].x
						y = results.pose_landmarks.landmark[joint_num].y
						visibility = results.pose_landmarks.landmark[joint_num].visibility

						tag_file.write(str(x) + '_' + str(y) + '_' + str(visibility) + '+')

				tag_file.write('\n')
			else:
				print('Error:pose_landmarks is NULL!!!')
				print(args.video_name + ' is error!!!')
				error_file.write(args.video_name + '\n')

				false_tag = 1

				break

	if false_tag == 1:

		# 移除错误标签
		os.remove(tag_path + args.video_name.split('.')[0] + '.txt')

		# 标签回归到原来状态
		false_tag = 0
