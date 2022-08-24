from tkinter import messagebox

import os

def video_tags(video_path, error_path, tag_path, self):

	video_list = os.listdir(video_path)

	video_list_last = []

	for video_name in video_list:
		if video_name[0] != '.':
			video_list_last.append(video_name)

	tag_bar_count = 0

	tag_bar_length = 300

	tag_bar_video_list = len(video_list_last)

	for video_name in video_list_last:

		os.system('python3 video2tag_system.py --video_name {} --video_path {} --error_path {} --tag_path {}' \
			.format(video_name, video_path, error_path, tag_path))

		tag_bar_count += 1

		self.bar['value'] = (tag_bar_count * tag_bar_length) // tag_bar_video_list
		self.page.update()

	messagebox.showerror(message='标签全部提取成功!')