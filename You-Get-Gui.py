import tkinter as tk
import tkinter.filedialog
import tkinter.messagebox
import subprocess
import os
import re
import time
import sys
import webbrowser


class YouGetGui:

    def __init__(self, window):
        super().__init__()
        self.__version__ = '1.1'
        self.new_window_var_old = None
        self.root = window
        self.root.title(f'You-get GUI v{self.__version__}')
        self.entries_list = []
        # 下载Frame
        self.download_frame = tk.Frame(self.root)
        # 下载地址
        self.url_label = tk.Label(self.download_frame, text='下载地址：')
        self.url_label.grid(row=0, column=0)
        self.url_entry = tk.Entry(self.download_frame, width=47)
        self.url_entry.grid(row=0, column=1, columnspan=6)
        self.entries_list.append(self.url_entry)
        self.url_entry_hint = tk.Label(self.download_frame, text='')
        self.url_entry_hint.grid(row=0, column=1, columnspan=6, sticky='w')
        # 清除下载地址
        self.clean = tk.Button(self.download_frame, text='清空', width=8,
                               command=self.clean_url_entry)
        self.clean.grid(row=0, column=7)

        # 下载路径
        self.path_label = tk.Label(self.download_frame, text='下载路径：')
        self.path_label.grid(row=1, column=0)
        self.path_entry = tk.Entry(self.download_frame, width=41)
        self.entries_list.append(self.path_entry)
        self.path_entry.grid(row=1, column=1, columnspan=5)
        self.clean_path = tk.Button(self.download_frame, text='清空', width=6,
                                    command=lambda: self.path_entry.delete(0, tk.END))
        self.clean_path.grid(row=1, column=6)
        self.path_button = tk.Button(self.download_frame, text='选择路径', width=8, command=self.select_path)
        self.path_button.grid(row=1, column=7)

        # 保存文件名
        self.new_name_label = tk.Label(self.download_frame, text='新文件名：')
        self.new_name_label.grid(row=2, column=0)
        self.new_name_entry = tk.Entry(self.download_frame, width=49, justify='left')
        self.new_name_entry.grid(row=2, column=1, columnspan=6)
        self.entries_list.append(self.new_name_entry)
        self.clean_new_name = tk.Button(self.download_frame, text='清空', width=8,
                                        command=lambda: self.new_name_entry.delete(0, tk.END))
        self.clean_new_name.grid(row=2, column=7)

        self.new_name_entry_hint_frame = tk.Frame(self.download_frame)
        self.new_name_entry_hint_date_frame = tk.LabelFrame(self.new_name_entry_hint_frame, text='文件名替换规则',
                                                            fg='black')
        self.new_name_entry_hint_date_text = tk.Text(self.new_name_entry_hint_date_frame, wrap='none', fg='black',
                                                     height=5, width=65)
        self.new_name_entry_hint_date_text.insert(tk.END, ""
                                                          "{n}     - 从1开始计数（1，2，3，4……）\n"
                                                          "{Zn}    - 根据下载的数量自动用0补齐位数（例如：下载100个视频，编号会自动从001，002……开始）\n"
                                                          "{ZnM}   - 同上，不过指定从第M个开始编号（例如{Zn8}，下载的视频编号从008开始。008、009……）\n"
                                                          "{zn}    - 自动用0补齐两位数字（例如：01、02……99、100、101……）\n"
                                                          "{znM}   - 自动用0补齐两位数字，不过编号从M开始（例如{zn4}：04、05……）\n"
                                                          "{zNn}   - 自动用0补齐N+1位数字（例如{z3n}：0001……|{z4n}：00001……）\n"
                                                          "{zNnM}  - 自动用0补齐N+1位数字，并且编号从M开始（例如{z3n3}：0003、0004……|{z4n4}：00004、00005……\n"
                                                          "{a}     - 星期几的缩写（例如，'Mon' 到 'Sun'）\n"
                                                          "{A}     - 星期几的全称（例如，'Monday' 到 'Sunday'）\n"
                                                          "{b}     - 月份的缩写（例如，'Jan' 到 'Dec'）\n"
                                                          "{B}     - 月份的全称（例如，'January' 到 'December'）\n"
                                                          "{c}     - 适当的日期和时间表示（例如，'Tue Aug 16 21:30:00 1988'）\n"
                                                          "{d}     - 零填充的月份中的一天（例如，'01' 到 '31'）\n"
                                                          "{m}     - 月份（'01' 到 '12'）\n"
                                                          "{M}     - 分钟（'00' 到 '59'）\n"
                                                          "{H}     - 小时（'00' 到 '23'）\n"
                                                          "{I}     - 小时（12 小时制，'01' 到 '12'）\n"
                                                          "{p}     - 上午或下午的标识符（例如，'AM' 或 'PM'）\n"
                                                          "{S}     - 秒（'00' 到 '60'）\n"
                                                          "{u}     - 星期几（1 到 7，星期一为 1）\n"
                                                          "{w}     - 星期几（0 到 6，星期天为 0）\n"
                                                          "{x}/{D} - 适当的日期表示（例如，'08/16/88'）\n"
                                                          "{X}     - 适当的时间表示（例如，'21:30:00'）\n"
                                                          "{y}     - 没有世纪的年份（'00' 到 '99'）\n"
                                                          "{C}     - 世纪（例如，'20'）\n"
                                                          "{Y}     - 有世纪的年份（例如，'2024'）\n"
                                                          "{z}     - 时区偏移量的小时数（例如，'-0800' 表示 UTC-8）\n"
                                                          "{Z}     - 时区名称（例如，'UTC'、'PST'、'中国标准时间'）")
        self.new_name_entry_hint_date_text.config(state="disabled")
        self.new_name_entry_hint_date_scrollbar_x = tk.Scrollbar(self.new_name_entry_hint_date_frame,
                                                                 orient='horizontal',
                                                                 command=self.new_name_entry_hint_date_text.xview)
        self.new_name_entry_hint_date_scrollbar_y = tk.Scrollbar(self.new_name_entry_hint_date_frame, orient='vertical',
                                                                 command=self.new_name_entry_hint_date_text.yview)
        self.new_name_entry_hint_date_scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.new_name_entry_hint_date_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.entries_list.append(self.new_name_entry_hint_date_text)
        self.new_name_entry_hint_date_scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.new_name_entry_hint_date_text.config(xscrollcommand=self.new_name_entry_hint_date_scrollbar_x.set)
        self.new_name_entry_hint_date_text.config(yscrollcommand=self.new_name_entry_hint_date_scrollbar_y.set)
        self.new_name_entry_hint_date_frame.grid(row=2, column=0, rowspan=1, columnspan=8)
        self.new_name_entry_hint_frame.grid(row=3, column=0, columnspan=8)

        # 按键栏
        self.base_bottom_frame = tk.Frame(self.download_frame)
        # 解析更多信息
        self.print_info_frame = tk.Frame(self.base_bottom_frame)
        self.more_info_button = tk.Button(self.print_info_frame, text='解析更多信息', width=10, command=self.more_info)
        self.more_info_button.grid(row=0, column=0)
        # 用json格式打印解析的信息
        self.print_info_as_json_var = tkinter.BooleanVar()
        self.print_info_as_json_var.set(False)
        self.print_info_as_json_checkbutton = tk.Checkbutton(self.print_info_frame, text='用json格式打印',
                                                             variable=self.print_info_as_json_var)
        self.print_info_as_json_checkbutton.grid(row=0, column=1, columnspan=1, sticky=tk.W)
        self.print_info_frame.grid(row=0, column=0, columnspan=3, sticky=tk.E)
        # 解析视频真实地址
        self.real_link_button = tk.Button(self.base_bottom_frame, text='解析真实地址', width=10, command=self.real_link)
        self.real_link_button.grid(row=0, column=3)
        # 开始下载按钮
        self.download_button = tk.Button(self.base_bottom_frame, text='开始下载', width=7, command=self.lunch_download)
        self.download_button.grid(row=0, column=5)

        # 状态提示
        self.status_label = tk.Label(self.base_bottom_frame, text='')
        self.status_label.grid(row=0, column=6, columnspan=2)

        self.download_frame.grid(row=0, column=0, columnspan=8, sticky=tk.W + tk.N)
        self.base_bottom_frame.grid(row=4, column=0, columnspan=8)

        # 设置
        self.settings_frame = tk.LabelFrame(self.root, text='设置')
        # 不要下载字幕(字幕，歌词，弹幕，…)
        self.no_download_captions_var = tkinter.BooleanVar()
        self.no_download_captions_var.set(False)
        self.no_download_captions_checkbutton = tk.Checkbutton(self.settings_frame, text='不下载字幕(字幕，歌词，弹幕，…)',
                                                               variable=self.no_download_captions_var)
        self.no_download_captions_checkbutton.grid(row=0, column=0, columnspan=3, sticky=tk.W)
        # 不合并视频片段
        self.merge_video_parts_var = tkinter.BooleanVar()
        self.merge_video_parts_var.set(False)
        self.merge_video_parts_checkbutton = tk.Checkbutton(self.settings_frame, text='不合并视频片段',
                                                            variable=self.merge_video_parts_var)
        self.merge_video_parts_checkbutton.grid(row=1, column=0, columnspan=3, sticky=tk.W)
        # 使用m3u8 url下载视频
        self.download_m3u8_var = tkinter.BooleanVar()
        self.download_m3u8_var.set(False)
        self.download_m3u8_checkbutton = tk.Checkbutton(self.settings_frame, text='使用m3u8 url下载视频',
                                                        variable=self.download_m3u8_var)
        self.download_m3u8_checkbutton.grid(row=2, column=0, columnspan=3, sticky=tk.W)
        # 忽略SSL错误
        self.ignore_ssl_errors_var = tkinter.BooleanVar()
        self.ignore_ssl_errors_var.set(False)
        self.ignore_ssl_errors_checkbutton = tk.Checkbutton(self.settings_frame, text='忽略SSL错误',
                                                            variable=self.ignore_ssl_errors_var)
        self.ignore_ssl_errors_checkbutton.grid(row=3, column=0, columnspan=3, sticky=tk.W)
        # 强制重新下载
        self.forced_download_var = tkinter.BooleanVar()
        self.forced_download_var.set(False)
        self.forced_download_checkbutton = tk.Checkbutton(self.settings_frame,
                                                          text='强制重新下载（覆盖同名文件或临时文件）',
                                                          variable=self.forced_download_var)
        self.forced_download_checkbutton.grid(row=4, column=0, columnspan=3, sticky=tk.W)
        # 跳过现有文件而不检查文件大小
        self.skip_download_var = tkinter.BooleanVar()
        self.skip_download_var.set(False)
        self.skip_download_checkbutton = tk.Checkbutton(self.settings_frame, text='跳过现有文件而不检查文件大小',
                                                        variable=self.skip_download_var)
        self.skip_download_checkbutton.grid(row=5, column=0, columnspan=3, sticky=tk.W)
        # 自动重命名相同名称的不同文件
        self.auto_rename_var = tkinter.BooleanVar()
        self.auto_rename_var.set(True)
        self.auto_rename_checkbutton = tk.Checkbutton(self.settings_frame, text='自动重命名相同名称的不同文件',
                                                      variable=self.auto_rename_var)
        self.auto_rename_checkbutton.grid(row=6, column=0, columnspan=3, sticky=tk.W)
        # 视频访问密码
        self.download_video_password_frame = tk.Frame(self.settings_frame)
        self.download_video_password_var = tkinter.BooleanVar()
        self.download_video_password_var.set(False)
        self.download_video_password_checkbutton = tk.Checkbutton(self.download_video_password_frame,
                                                                  text='视频访问密码',
                                                                  variable=self.download_video_password_var,
                                                                  command=lambda: self.download_video_password_entry.config(
                                                                      state='normal' if self.download_video_password_var.get() else 'disabled')
                                                                  )
        self.download_video_password_checkbutton.grid(row=0, column=0, columnspan=1, sticky=tk.W)
        self.download_video_password_entry = tk.Entry(self.download_video_password_frame, width=20, state='disabled')
        self.download_video_password_entry.grid(row=0, column=1, columnspan=1, sticky=tk.E)
        self.entries_list.append(self.download_video_password_entry)
        self.download_video_password_frame.grid(row=7, column=0, columnspan=3, sticky=tk.W)
        # 开启调试模式
        self.debug_var = tkinter.BooleanVar()
        self.debug_var.set(False)
        self.debug_checkbutton = tk.Checkbutton(self.settings_frame, text='开启调试模式（--debug）',
                                                variable=self.debug_var)
        self.debug_checkbutton.grid(row=8, column=0, columnspan=3, sticky=tk.W)
        # 下载格式
        self.download_format_frame = tk.Frame(self.settings_frame)
        self.download_format_var = tkinter.BooleanVar()
        self.download_format_var.set(False)
        self.download_format_checkbutton = tk.Checkbutton(self.download_format_frame, text='下载选定格式（format）',
                                                          variable=self.download_format_var,
                                                          command=lambda: self.download_format_entry.config(
                                                              state='normal' if self.download_format_var.get() else 'disabled')
                                                          )
        self.download_format_checkbutton.grid(row=0, column=0, columnspan=1, sticky=tk.W)
        self.download_format_entry = tk.Entry(self.download_format_frame, width=10, state='disabled')
        self.download_format_entry.grid(row=0, column=1, columnspan=2, sticky=tk.E)
        self.entries_list.append(self.download_format_entry)
        self.download_format_frame.grid(row=9, column=0, columnspan=3, sticky=tk.W)
        # 下载标签
        self.download_itag_frame = tk.Frame(self.settings_frame)
        self.download_itag_var = tkinter.BooleanVar()
        self.download_itag_var.set(False)
        self.download_itag_checkbutton = tk.Checkbutton(self.download_itag_frame, text='下载选定标签（itag）',
                                                        variable=self.download_itag_var,
                                                        command=lambda: self.download_itag_entry.config(
                                                            state='normal' if self.download_itag_var.get() else 'disabled')
                                                        )
        self.download_itag_checkbutton.grid(row=0, column=0, columnspan=1, sticky=tk.W)
        self.download_itag_entry = tk.Entry(self.download_itag_frame, width=10, state='disabled')
        self.download_itag_entry.grid(row=0, column=1, columnspan=2, sticky=tk.E)
        self.entries_list.append(self.download_itag_entry)
        self.download_itag_frame.grid(row=9, column=2, columnspan=3, sticky=tk.E)
        # 下载播放列表
        self.download_all_frame = tk.Frame(self.settings_frame)
        self.download_all_var = tkinter.BooleanVar()
        self.download_all_var.set(False)
        self.download_all_checkbutton = tk.Checkbutton(self.download_all_frame, text='下载整个播放列表',
                                                       variable=self.download_all_var,
                                                       command=lambda: (self.download_all_start_label.config(
                                                           fg='black' if self.download_all_var.get() else 'gray'),
                                                                        self.download_all_page_entry.config(
                                                                            state='normal' if self.download_all_var.get() else 'disabled'),
                                                                        self.download_all_front_label.config(
                                                                            fg='black' if self.download_all_var.get() else 'gray'),
                                                                        self.download_all_start_entry.config(
                                                                            state='normal' if self.download_all_var.get() else 'disabled'),
                                                                        self.download_all_middle_label.config(
                                                                            fg='black' if self.download_all_var.get() else 'gray'),
                                                                        self.download_all_end_entry.config(
                                                                            state='normal' if self.download_all_var.get() else 'disabled'),
                                                                        self.download_all_end_label.config(
                                                                            fg='black' if self.download_all_var.get() else 'gray')
                                                       )
                                                       )
        self.download_all_checkbutton.grid(row=0, column=0)
        self.download_all_start_label = tk.Label(self.download_all_frame, text='下载第', fg='gray')
        self.download_all_start_label.grid(row=0, column=1)
        self.download_all_page_entry = tk.Entry(self.download_all_frame, width=5, state='disabled')
        self.download_all_page_entry.grid(row=0, column=2)
        self.entries_list.append(self.download_all_page_entry)
        self.download_all_front_label = tk.Label(self.download_all_frame, text='页的第', fg='gray')
        self.download_all_front_label.grid(row=0, column=3)
        self.download_all_start_entry = tk.Entry(self.download_all_frame, width=5, state='disabled')
        self.download_all_start_entry.grid(row=0, column=4)
        self.entries_list.append(self.download_all_start_entry)
        self.download_all_middle_label = tk.Label(self.download_all_frame, text='个至第', fg='gray')
        self.download_all_middle_label.grid(row=0, column=5)
        self.download_all_end_entry = tk.Entry(self.download_all_frame, width=5, state='disabled')
        self.download_all_end_entry.grid(row=0, column=6)
        self.entries_list.append(self.download_all_end_entry)
        self.download_all_end_label = tk.Label(self.download_all_frame, text='个视频（包括）。', fg='gray')
        self.download_all_end_label.grid(row=0, column=7)
        self.download_all_frame.grid(row=10, column=0, columnspan=8, sticky=tk.W)
        # 使用Cookies
        self.use_cookies_frame = tk.Frame(self.settings_frame)
        self.use_cookies_var = tkinter.BooleanVar()
        self.use_cookies_var.set(False)
        self.use_cookies_checkbutton = tk.Checkbutton(self.use_cookies_frame, text='使用Cookies',
                                                      variable=self.use_cookies_var,
                                                      command=lambda: (self.use_cookies_entry.config(
                                                          state='normal' if self.use_cookies_var.get() else 'disabled'),
                                                                       self.use_cookies_button.config(
                                                                           state='normal' if self.use_cookies_var.get() else 'disabled')
                                                      ))
        self.use_cookies_checkbutton.grid(row=0, column=0)
        self.use_cookies_entry = tk.Entry(self.use_cookies_frame, width=35, state='disabled')
        self.use_cookies_entry.grid(row=0, column=1)
        self.entries_list.append(self.use_cookies_entry)
        self.use_cookies_button = tk.Button(self.use_cookies_frame, text='选择Cookies文件',
                                            state='disabled',
                                            command=self.select_cookies_file)
        self.use_cookies_button.grid(row=0, column=2)
        self.use_cookies_frame.grid(row=11, column=0, columnspan=8, sticky=tk.W)
        # 播放视频/音乐
        self.play_frame = tk.Frame(self.settings_frame)
        self.play_var = tkinter.BooleanVar()
        self.play_var.set(False)
        self.play_checkbutton = tk.Checkbutton(self.play_frame, text='播放视频/音乐',
                                               variable=self.play_var,
                                               command=lambda: (self.player_entry.config(
                                                   state='normal' if self.play_var.get() else 'disabled'),
                                                                self.play_exe_argument_label.config(
                                                                    fg='black' if self.play_var.get() else 'gray'),
                                                                self.play_exe_argument_entry.config(
                                                                    state='normal' if self.play_var.get() else 'disabled'),
                                                                self.play_button.config(
                                                                    state='normal' if self.play_var.get() else 'disabled'),
                                                                self.download_button.config(
                                                                    text='播放' if self.play_var.get() else '开始下载',
                                                                    command=self.play if self.play_var.get() else self.lunch_download)
                                                                ))
        self.play_checkbutton.grid(row=0, column=0)
        self.player_entry = tk.Entry(self.play_frame, width=20, state='disabled')
        self.player_entry.grid(row=0, column=1)
        self.entries_list.append(self.player_entry)
        self.play_button = tk.Button(self.play_frame, text='选择EXE文件', command=self.select_player_file,
                                     state='disabled')
        self.play_button.grid(row=0, column=2)
        self.play_exe_argument_label = tk.Label(self.play_frame, text='参数', fg='gray')
        self.play_exe_argument_label.grid(row=0, column=3)
        self.play_exe_argument_entry = tk.Entry(self.play_frame, width=15, state='disabled')
        self.play_exe_argument_entry.grid(row=0, column=4)
        self.entries_list.append(self.play_exe_argument_entry)
        self.play_frame.grid(row=12, column=0, columnspan=8, sticky=tk.W)
        # 在新的窗口运行所有命令
        self.new_window_var = tkinter.BooleanVar()
        self.new_window_var.set(True)
        self.new_window_checkbutton = tk.Checkbutton(self.settings_frame,
                                                     text='在新的窗口运行所有命令（推荐）不建议在批量下载中取消勾选，因为没做多'
                                                          '\n线程所以只会在you-get程序执行结束后程序才会接受新的指令（俗称：卡住）',
                                                     height=2,
                                                     variable=self.new_window_var,
                                                     command=self.new_window_var_update)
        self.new_window_checkbutton.grid(row=13, column=0, columnspan=8, sticky=tk.W)
        self.new_window_var_update()

        # 代理选项
        self.proxy_setting = tk.LabelFrame(self.settings_frame, text='代理')
        self.no_proxy_var = tkinter.BooleanVar()
        self.no_proxy_var.set(False)
        self.no_proxy_checkbutton = tk.Checkbutton(self.proxy_setting, text='不使用任何代理（包括系统代理）',
                                                   variable=self.no_proxy_var, command=self.no_proxy_button_check)
        self.no_proxy_checkbutton.grid(row=0, column=0, columnspan=3, sticky=tk.W)
        self.proxy_setting_var = tkinter.BooleanVar()
        self.proxy_setting_var.set(False)
        self.proxy_setting_checkbutton = tk.Checkbutton(self.proxy_setting, text='使用自定义代理',
                                                        variable=self.proxy_setting_var,
                                                        command=self.proxy_setting_button_check)
        self.proxy_setting_checkbutton.grid(row=1, column=0, columnspan=1, sticky=tk.W)
        self.proxy_extracting_only_var = tkinter.BooleanVar()
        self.proxy_extracting_only_var.set(False)
        self.proxy_extracting_only_checkbutton = tk.Checkbutton(self.proxy_setting, text='仅用于提取',
                                                                variable=self.proxy_extracting_only_var,
                                                                state='disabled')
        self.proxy_extracting_only_checkbutton.grid(row=1, column=1, columnspan=1, sticky=tk.W)
        self.proxy_type_var = tkinter.StringVar()
        self.proxy_type_var.set('Socks5')
        self.proxy_type_socks5_radiobutton = tk.Radiobutton(self.proxy_setting, text='Socks5',
                                                            variable=self.proxy_type_var, value='Socks5',
                                                            state='disabled', command=self.proxy_type_button_check)
        self.proxy_type_socks5_radiobutton.grid(row=2, column=0, sticky=tk.W)
        self.proxy_type_http_radiobutton = tk.Radiobutton(self.proxy_setting, text='Http',
                                                          variable=self.proxy_type_var, value='Http', state='disabled',
                                                          command=self.proxy_type_button_check)
        self.proxy_type_http_radiobutton.grid(row=2, column=1, sticky=tk.W)
        self.proxy_path_label = tk.Label(self.proxy_setting, text='代理地址：', fg='gray')
        self.proxy_path_label.grid(row=3, column=0, sticky=tk.W)
        self.proxy_path_entry = tk.Entry(self.proxy_setting, width=20, state='disabled')
        self.proxy_path_entry.grid(row=3, column=0, columnspan=3, sticky=tk.E)
        self.entries_list.append(self.proxy_path_entry)
        self.proxy_login_frame = tk.LabelFrame(self.proxy_setting, text='登录', fg='gray')
        self.proxy_login_var = tkinter.BooleanVar()
        self.proxy_login_var.set(False)
        self.proxy_login_checkbutton = tk.Checkbutton(self.proxy_login_frame, text='用户名登录',
                                                      variable=self.proxy_login_var,
                                                      command=self.proxy_login_button_check, state='disabled')
        self.proxy_login_checkbutton.grid(row=0, column=0, columnspan=3, sticky=tk.W)
        self.proxy_user_name_label = tk.Label(self.proxy_login_frame, text='用户名：', fg='gray')
        self.proxy_user_name_label.grid(row=1, column=0)
        self.proxy_user_name_entry = tk.Entry(self.proxy_login_frame, width=21, state='disabled')
        self.proxy_user_name_entry.grid(row=1, column=1, columnspan=6)
        self.entries_list.append(self.proxy_user_name_entry)
        self.proxy_password_label = tk.Label(self.proxy_login_frame, text='密码：', fg='gray')
        self.proxy_password_label.grid(row=2, column=0)
        self.proxy_password_entry = tk.Entry(self.proxy_login_frame, width=21, state='disabled')
        self.proxy_password_entry.grid(row=2, column=1, columnspan=6)
        self.entries_list.append(self.proxy_password_entry)
        self.proxy_login_frame.grid(row=4, column=0, columnspan=3, sticky=tk.W)
        self.proxy_time_out_frame = tk.Frame(self.proxy_setting)
        self.proxy_time_out_var = tkinter.BooleanVar()
        self.proxy_time_out_var.set(False)
        self.proxy_time_out_checkbutton = tk.Checkbutton(self.proxy_time_out_frame, text='代理超时时间',
                                                         variable=self.proxy_time_out_var,
                                                         command=lambda: (self.proxy_time_out_entry.config(
                                                             state='normal' if self.proxy_time_out_var.get() else 'disabled'),
                                                                          self.proxy_time_out_label.config(
                                                                              fg='black' if self.proxy_time_out_label[
                                                                                                'fg'] == 'gray' else 'gray')
                                                         )
                                                         )
        self.proxy_time_out_checkbutton.grid(row=0, column=0)
        self.proxy_time_out_entry = tk.Entry(self.proxy_time_out_frame, width=10)
        self.proxy_time_out_entry.insert(0, '10')
        self.proxy_time_out_entry.config(state='disabled')
        self.proxy_time_out_entry.grid(row=0, column=1)
        self.entries_list.append(self.proxy_time_out_entry)
        self.proxy_time_out_label = tk.Label(self.proxy_time_out_frame, text='秒', fg='gray')
        self.proxy_time_out_label.grid(row=0, column=2)
        self.proxy_time_out_frame.grid(row=5, column=0, columnspan=3, sticky=tk.W)
        self.proxy_setting.grid(row=0, column=3, rowspan=9, sticky=tk.W + tk.N)
        # 批量下载
        self.batch_download_frame = tk.LabelFrame(self.settings_frame, text='批量功能')
        self.batch_download_power_var = tkinter.BooleanVar()
        self.batch_download_power_var.set(False)
        self.batch_download_power_checkbutton = tk.Checkbutton(self.batch_download_frame, text='使用批量功能',
                                                               variable=self.batch_download_power_var,
                                                               command=self.batch_download_power)
        self.batch_download_power_checkbutton.grid(row=0, column=0, columnspan=1, sticky=tk.W)
        self.batch_download_parallel_var = tkinter.BooleanVar()
        self.batch_download_parallel_var.set(True)
        self.batch_download_parallel_checkbutton = tk.Checkbutton(self.batch_download_frame, text='同时进行',
                                                                  state='disabled',
                                                                  variable=self.batch_download_parallel_var,
                                                                  command=self.batch_download_parallel)
        self.batch_download_parallel_checkbutton.grid(row=0, column=1, columnspan=1, sticky=tk.W)
        self.batch_download_from_file_frame = tk.Frame(self.batch_download_frame)
        self.batch_download_from_file_var = tkinter.BooleanVar()
        self.batch_download_from_file_var.set(False)
        self.batch_download_from_file_checkbutton = tk.Checkbutton(self.batch_download_from_file_frame,
                                                                   text='从文件中获取视频地址列表',
                                                                   state='disabled',
                                                                   variable=self.batch_download_from_file_var,
                                                                   command=self.batch_download_from_file_check)
        self.batch_download_from_file_checkbutton.grid(row=0, column=0, columnspan=1, sticky=tk.W)
        self.batch_download_from_file_select_button = tk.Button(self.batch_download_from_file_frame, text='选择文件',
                                                                state='disabled',
                                                                command=self.batch_download_from_file_select)
        self.batch_download_from_file_select_button.grid(row=0, column=1, columnspan=1)
        self.batch_download_from_file_frame.grid(row=0, column=2, columnspan=6, sticky=tk.W)

        self.batch_download_links_frame = tk.LabelFrame(self.batch_download_frame, text='下载地址列表（一行一个）',
                                                        fg='gray')
        self.batch_download_links_text = tk.Text(self.batch_download_links_frame, wrap='none', fg='gray', height=7,
                                                 width=65, state='disabled')
        self.batch_download_links_scrollbar_x = tk.Scrollbar(self.batch_download_links_frame, orient='horizontal',
                                                             command=self.batch_download_links_text.xview)
        self.batch_download_links_scrollbar_y = tk.Scrollbar(self.batch_download_links_frame, orient='vertical',
                                                             command=self.batch_download_links_text.yview)
        self.batch_download_links_scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.batch_download_links_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.entries_list.append(self.batch_download_links_text)
        self.batch_download_links_scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.batch_download_links_text.config(xscrollcommand=self.batch_download_links_scrollbar_x.set)
        self.batch_download_links_text.config(yscrollcommand=self.batch_download_links_scrollbar_y.set)
        self.batch_download_links_frame.grid(row=2, column=0, rowspan=1, columnspan=8, sticky='nw')

        self.batch_download_frame.grid(row=14, column=0, columnspan=8, sticky=tk.W)
        self.settings_frame.grid(row=1, column=0, columnspan=8, rowspan=999, sticky=tk.W + tk.N)

        # 输出
        self.output_frame = tk.LabelFrame(self.root, text='日志')
        self.output_text = tk.Text(self.output_frame, wrap=tk.WORD, height=40, width=84)
        self.output_scrollbar = tk.Scrollbar(self.output_frame, command=self.output_text.yview)
        self.output_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.entries_list.append(self.output_text)
        self.output_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.output_text.config(yscrollcommand=self.output_scrollbar.set)
        self.output_frame.grid(row=0, column=8, rowspan=20, sticky="nsew")
        self.output_text_clean = tk.Button(self.root, text='清空日志内容',
                                           command=lambda: self.output_text.delete('1.0', tk.END))
        self.output_text_clean.grid(row=0, column=8, sticky='ne')

        # 提示栏
        self.tips_label = tk.Label(self.root, justify=tk.LEFT,
                                   text='※注意：本程序只是给You-Get程序上一层GUI外壳以便于使用，并不包含You-Get程序本体。\n'
                                        '1、若无下载路径，则默认下载到软件本体所在的文件夹中。\n'
                                        '2、新文件名只要填写名称，无需填写后缀（填写了也没用）。\n'
                                        '3、若无新文件名，则程序自动保存为视频原始名称。\n'
                                        '4、代理地址必须要同时填写主机地址与端口号。（如：127.0.0.1:00000）\n'
                                        '5、"下載整个播放列表"选项后面的空都可以不填。\n'
                                        '     若只填第x页就下载x页中的全部视频，若只填从y视频开始下载就从y视频一直下载到最后一个视频。\n'
                                        '6、用于计数的文件名替换规则只能用于同时下载视频上，无法用于逐个下载（You-Get程序限制，我无法修改）。\n'
                                        '\n其余内容可以进入GitHub的Wiki界面查看，也欢迎再Issues上提交反馈')
        self.tips_label.grid(row=20, column=8, columnspan=8)

        tk.Label(self.root, text='(c)hunyanjie（魂魇桀） 2024', font=(None, 12, 'bold')).grid(row=21, column=8,
                                                                                            columnspan=8)

        self.menubar = tk.Menu(self.root)
        self.root.config(menu=self.menubar)

        self.about_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_command(label="关于", command=self.about)

        self.install_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_command(label="一键安装/更新You-Get", command=self.install_you_get)

        self.version_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_command(label="查看You-Get版本", command=self.check_you_get_version)

        self.introduce_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_command(label="功能介绍", command=lambda: webbrowser.open('https://github.com/hunyanjie/You-Get-Gui/wiki/%E6%8C%87%E5%8D%97-info#%E5%8A%9F%E8%83%BD%E4%BB%8B%E7%BB%8D', new=0))

        self.introduce_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_command(label="Issues/问题反馈", command=lambda: webbrowser.open('https://github.com/hunyanjie/You-Get-Gui/issues', new=0))

        self.bilibili_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_command(label="bilibili视频无法下载？", command=lambda: webbrowser.open('https://github.com/hunyanjie/You-Get-Gui/wiki/%E6%8C%87%E5%8D%97-info#2b%E7%AB%99%E8%A7%86%E9%A2%91%E6%97%A0%E6%B3%95%E4%B8%8B%E8%BD%BD', new=0))

        self.bilibili_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_command(label="可以检索视频信息但无法下载？", command=lambda: webbrowser.open('https://github.com/hunyanjie/You-Get-Gui/wiki/%E6%8C%87%E5%8D%97-info#1%E5%8F%AF%E4%BB%A5%E6%B5%8F%E8%A7%88%E8%A7%86%E9%A2%91%E4%BF%A1%E6%81%AF%E4%BD%86%E6%97%A0%E6%B3%95%E4%B8%8B%E8%BD%BD', new=0))

        self.exit_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_command(label="退出程序", command=self.exit_program)

        # 为所有可输入的控件添加右键菜单
        self.right_click_menu()

    def right_click_menu(self):
        for widget in self.entries_list:
            right_click_menu = tk.Menu(widget, tearoff=0)
            right_click_menu.add_command(label="复制", command=lambda w=widget: self.copy(w))
            right_click_menu.add_command(label="剪切", command=lambda w=widget: self.cut(w))
            right_click_menu.add_command(label="粘贴", command=lambda w=widget: self.paste(w))
            right_click_menu.add_separator()
            right_click_menu.add_command(label="全选", command=lambda w=widget: self.select_all(w))

            widget.bind("<Button-3>", lambda event, w=widget, m=right_click_menu: self.show_context_menu(event, w, m))

    def show_context_menu(self, event, widget, right_click_menu):
        print("[DEBUG]event.widget:", event.widget, "\t|\twidget.focus_get():", widget.focus_get())
        try:
            if event.widget != widget.focus_get():
                widget.tag_add(tk.SEL, "1.0", tk.END)
                widget.focus_set()
            widget.mark_set(tk.INSERT, "insert")  # 将光标移动到对应的控件中的正确位置
        except AttributeError:
            if event.widget != widget.focus_get():
                widget.selection_range(0, len(widget.get()))
                widget.focus_set()
            widget.icursor("insert")
        right_click_menu.post(event.x_root, event.y_root)

    def copy(self, widget):
        try:
            print("[DEBUG]Copy:", widget.selection_get())
            widget.clipboard_clear()
            widget.clipboard_append(widget.selection_get())
        except Exception:
            pass

    def cut(self, widget):
        try:
            print("[DEBUG]Cut:", widget.selection_get())
            widget.clipboard_clear()
            widget.clipboard_append(widget.selection_get())
            widget.delete(tk.SEL_FIRST, tk.SEL_LAST)
        except Exception:
            pass

    def paste(self, widget):
        try:
            widget.delete(tk.SEL_FIRST, tk.SEL_LAST)
        except Exception:
            pass
        finally:
            try:
                print("[DEBUG]Paste:", widget.clipboard_get())
                widget.insert(tk.INSERT, widget.clipboard_get())
            except Exception:
                pass

    def select_all(self, widget):
        try:
            widget.tag_add(tk.SEL, "1.0", tk.END)
            widget.mark_set(tk.INSERT, "insert")  # 将光标移动到对应的控件中的正确位置
            widget.see(tk.INSERT)
        except AttributeError:
            widget.selection_range(0, len(widget.get()))
            widget.icursor("insert")
        return 'break'

    def lunch_download(self, cmd='', download=True, play=False):
        if download:
            cmd = 'you-get'
            if self.path_entry.get() != "":
                cmd += f' --output-dir "{self.path_entry.get()}"'
            if self.new_name_entry.get() != "":
                "移动至batch_download_check函数"
                pass
            if self.download_itag_var.get():
                if ' --json' not in cmd or ' --info' not in cmd:
                    if self.download_itag_entry.get() != "":
                        cmd += f' --itag={self.download_itag_entry.get()}'
                    else:
                        print('[WARN]Please enter the itag number!!!')
                        self.status_label.config(text='未填入itag！', fg='red')
                        return
            if self.download_format_var.get():
                if ' --json' not in cmd or ' --info' not in cmd:
                    if self.download_format_entry.get() != "":
                        cmd += f' --format={self.download_format_entry.get()}'
                    else:
                        print('[WARN]Please enter the format number!!!')
                        self.status_label.config(text='未填入format！', fg='red')
                        return
            if self.no_download_captions_var.get():
                cmd += ' --no-caption'
            if self.merge_video_parts_var.get():
                cmd += ' --no-merge'
            if self.download_m3u8_var.get():
                cmd += ' --m3u8'
            if self.ignore_ssl_errors_var.get():
                cmd += ' --insecure'
            if self.forced_download_var.get():
                cmd += ' --force'
            if self.skip_download_var.get():
                cmd += ' --skip-existing-file-size-check'
            if self.auto_rename_var.get():
                cmd += ' --auto-rename'
            if self.download_all_var.get():
                cmd += ' --playlist'
                if self.download_all_page_entry.get() != '':
                    if self.download_all_page_entry.get().isdigit():
                        cmd += f' --page-size {self.download_all_page_entry.get()}'
                    else:
                        print('[WARN]Please fill in a non-negative integer!!!')
                        self.status_label.config(text='请在下载的特定页数处填上非负整数！', fg='red')
                        return
                if self.download_all_start_entry.get() != '':
                    if self.download_all_start_entry.get().isdigit():
                        cmd += f' --first {self.download_all_start_entry.get()}'
                    else:
                        print('[WARN]Please fill in a non-negative integer!!!')
                        self.status_label.config(text='请在开始下载的视频编号处填上非负整数！', fg='red')
                        return
                if self.download_all_end_entry.get() != '':
                    if self.download_all_end_entry.get().isdigit():
                        cmd += f' --last {self.download_all_end_entry.get()}'
                    else:
                        print('[WARN]Please fill in a non-negative integer!!!')
                        self.status_label.config(text='请在结束下载的视频编号处填上非负整数！', fg='red')
                        return
        if self.debug_var.get():
            cmd += ' --debug'
        if self.use_cookies_var.get():
            if self.use_cookies_entry.get() != '':
                cmd += f' --cookies "{self.use_cookies_entry.get()}"'
            else:
                print('[WARN]Please fill in the Cookies path!!!')
                self.status_label.config(text='未填入Cookies路径！', fg='red')
                return
        if self.download_video_password_var.get():
            if self.download_video_password_entry.get() != '':
                cmd += f' --password "{self.download_video_password_entry.get()}"'
            else:
                print('[WARN]Please enter the video password!!!')
                self.status_label.config(text='未填入视频密码！', fg='red')
                return
        if self.no_proxy_var.get():
            cmd += ' --no-proxy'
        else:
            if self.proxy_setting_var.get():
                if self.proxy_path_entry.get() != '':
                    print('[DEBUG]proxy type:', self.proxy_type_var.get())
                    if self.proxy_type_var.get() == 'Socks5':
                        if self.proxy_login_var.get():
                            if self.proxy_user_name_entry.get() != '' and self.proxy_password_entry.get() != '':
                                cmd += (f' --socks-proxy {self.proxy_user_name_entry.get()}:'
                                        f'{self.proxy_password_entry.get()}@{self.proxy_path_entry.get()}')
                            else:
                                print('[WARN]Please enter the login username and password of the agent host!!!')
                                self.status_label.config(text='请输入代理主机的登入用户名与密码！！！', fg='red')
                                return
                        else:
                            cmd += f' --socks-proxy {self.proxy_path_entry.get()}'
                    else:
                        if self.proxy_extracting_only_var.get():
                            cmd += f' --extractor-proxy {self.proxy_path_entry.get()}'
                        else:
                            cmd += f' --http-proxy {self.proxy_path_entry.get()}'
                else:
                    print('[WARN]Please enter the proxy host address and port number!!!')
                    self.status_label.config(text='请输入代理主机地址与端口号!!', fg='red')
                    return
            if self.proxy_time_out_var.get():
                if self.proxy_time_out_entry.get() != '':
                    cmd += f' --timeout {self.proxy_time_out_entry.get()}'
                else:
                    print('[WARN]Please enter a proxy timeout period!!!')
                    self.status_label.config(text='请输入代理超时时间!!', fg='red')
                    return
        if play:
            self.downloading(cmd)
        else:
            self.batch_download_check(cmd)

    def batch_download_check(self, cmd):  # 批量下载检查
        # 如果使用批量功能
        if self.batch_download_power_var.get():
            # 如果从文件中获取下载连接
            if self.batch_download_from_file_var.get():
                # 检测文件连接是否存在
                if self.url_entry.get() != '':
                    # 如果勾选同时下载
                    if self.batch_download_parallel_var.get():
                        try:
                            with open(f'{self.url_entry.get()}', "r") as file:
                                line_numbers = 0
                                line_number = 0
                                for line in file:
                                    if line.strip() != '':
                                        line_numbers += 1
                                print("[INFO]Total download:", line_numbers)
                                for line in file:
                                    if line.strip() != '':
                                        line_number += 1
                                        print(f"[INFO]Now download:{line_number}/{line_numbers}")
                                        cmd_tmp = self.new_name_change(cmd, (line_numbers, line_number))
                                        self.downloading(f'{cmd_tmp} "{line.strip()}"')
                        except FileNotFoundError:
                            print('[WARN]File does not exist!!!')
                            self.status_label.config(text='文件不存在！', fg='red')
                            return
                    else:
                        cmd_tmp = self.new_name_change(cmd, (1, 1), False)
                        self.downloading(f'{cmd_tmp} --input-file "{self.url_entry.get()}"')
                else:
                    print('[WARN]Please enter the download URL collection file address!!!')
                    self.status_label.config(text='未填入下载网址集合文件地址！', fg='red')
                    return
            else:
                text = self.batch_download_links_text.get("1.0", tk.END)
                if text.strip() != '':
                    # 如果同时下载
                    if self.batch_download_parallel_var.get():
                        line_numbers = 0
                        line_number = 0
                        for line in text.split('\n'):
                            if line.strip() != '':
                                line_numbers += 1
                        print("[INFO]Total download:", line_numbers)
                        for line in text.split('\n'):
                            if line.strip() != '':
                                line_number += 1
                                print(f"[INFO]Now download:{line_number}/{line_numbers}")
                                cmd_tmp = self.new_name_change(cmd, (line_numbers, line_number))
                                self.downloading(f'{cmd_tmp} "{line.strip()}"')
                    else:
                        tmp_file_path = os.environ.get('temp')
                        with open(f"{tmp_file_path}\\YouGetGuiTmpData.txt", "w") as file:
                            for line in text.split('\n'):
                                if line.strip() != '':
                                    file.write(line + "\n")
                        cmd_tmp = self.new_name_change(cmd, (1, 1), False)
                        self.downloading(f'{cmd_tmp} --input-file "{tmp_file_path}\\YouGetGuiTmpData.txt"')
                else:
                    print('[WARN]Please enter the download URL or file path!!!')
                    self.status_label.config(text='未填入下载地址或下载网址集合文件地址！', fg='red')
                    return
        else:
            if self.url_entry.get() == '':
                print('[WARN]Please enter the download URL!!!')
                self.status_label.config(text='未填入下载地址！', fg='red')
                return
            else:
                cmd += f' "{self.url_entry.get()}"'
                cmd_tmp = self.new_name_change(cmd, (1, 1), False)
                self.downloading(cmd_tmp)

    def downloading(self, cmd):
        print('[INDO]Starting......')
        self.status_label.config(text='已发送请求！请等待......', fg='blue')
        if self.new_window_var.get():
            cmd = 'start cmd /k ' + cmd
            print('[INFO]输入:\n', cmd)
            output_info = f'输入:\n{cmd}\n'
            self.output_text.insert(tk.END, output_info)
            subprocess.Popen(cmd, shell=True)
        else:
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            out, error = process.communicate()
            out = out.decode('utf-8')
            error = error.decode('utf-8')
            print('[INFO]输出:\n', out)
            print('[INFO]错误:\n', error)
            output_info = f'输入:\n{cmd}\n输出:\n{out}\n错误:\n{error}\n-------------------------------------\n'
            self.output_text.insert(tk.END, output_info)

    def new_name_change(self, cmd, number=(1, 1), batch_download=True):
        if self.new_name_entry.get() != "":
            date_keys = ["%a", "%A", "%b", "%B", "%c", "%C", "%d", '%m', "%M", "%H", "%I", "%p", "%S", "%u", "%w", "%x",
                         "%X", "%y", "%Y", "%z", "%Z"]
            keys = {}
            other_keys = {"{n}": number[1]}  # 解决{n}
            keys.update(other_keys)

            new_name_data = self.new_name_entry.get()
            # new_name_data = "time is: {Y}-{m}-{d} {H}:{M}:{S},{12345678} No.{n}/{Zn}/{{z5n}}  {zzzzzzzz}|{Zzzzn}|{Zn8}|dfghjk|{z3n1}|{{z2z}}|{zzzzz}|{zn1}|{z2cn}|{z3n}|{zn}|dsfg"

            # 解决{Zn(...)}
            pattern_Znd = r"\{Zn(?:\d+)?\}"
            matches_Znd = re.findall(pattern_Znd, new_name_data)
            for match in matches_Znd:
                # 提取数字部分，如果有的话
                match_number = match.replace("{Zn", "").replace("}", "")
                if match_number:
                    # if match_number.isdigit():
                    # 如果有数字，将 number[1] 转换为相应位数的字符串，并拼接数字
                    keys[match] = f"{number[1] + int(match_number):0{len(str(number[0]))}d}"
                else:
                    # 如果没有数字，直接将 number[1] 作为值
                    if batch_download:
                        keys[match] = f"{number[1]:0{len(str(number[0]))}d}"
                    else:
                        keys[match] = "1"

            # 解决{z(...)n(...)}
            # 处理 {z数字n数字} 形式的字符串
            pattern_zdnd = r"\{z(\d+)n(\d+)\}"
            matches_zdnd = re.findall(pattern_zdnd, new_name_data)
            for match in matches_zdnd:
                z_count = int(match[0])
                n_digit = int(match[1])
                value = str(number[1] + n_digit).zfill(z_count + 1)
                key = match  # 使用完整的匹配字符串作为键
                keys["{z" + key[0] + "n" + key[1] + "}"] = value
            # 处理 {zn数字} 形式的字符串
            pattern_znd = r"\{zn(\d+)\}"
            matches_znd = re.findall(pattern_znd, new_name_data)
            for match in matches_znd:
                n_digit = int(match)
                value = str(number[1] + n_digit)  # 从 number[1] 开始累加
                key = match  # 使用完整的匹配字符串作为键
                keys["{zn" + key + "}"] = value.zfill(n_digit + 1)  # 用0补齐到正确的位数
            # 处理 {z数字n} 形式的字符串
            pattern_zn = r"\{z(\d+)n\}"
            matches_zn = re.findall(pattern_zn, new_name_data)
            for match in matches_zn:
                z_count = int(match)  # 去掉 'n' 后提取数字
                value = str(number[1]).zfill(z_count + 1)  # 使用当前累加值
                key = match  # 使用完整的匹配字符串作为键
                keys["{z" + key[0] + "n}"] = value
            # 处理 {zn} 形式的字符串
            pattern_zn = r"\{zn\}"
            matches_zn = re.findall(pattern_zn, new_name_data)
            keys["{zn}"] = str(number[1]).zfill(2)
            print(f"[DEBUG]Replace keys:", keys)
            for date_key in date_keys:
                keys["{" + date_key.replace("%", "") + "}"] = time.strftime(date_key, time.localtime())
            for key, var in keys.items():
                new_name_data = new_name_data.replace(key, str(var))
            cmd += f' --output-filename "{new_name_data}"'
        return cmd

    def clean_url_entry(self):
        if self.batch_download_power_var.get() is False and self.batch_download_from_file_checkbutton.cget(
                "state") != 'normal':
            self.url_label.config(text='下载地址：')
        self.url_entry.delete(0, tk.END)

    def select_path(self):
        path = tk.filedialog.askdirectory()
        print("[DEBUG]Save Path:", path)
        if path != '':
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, path)

    def more_info(self):
        if self.print_info_as_json_var.get():
            cmd = f'you-get --json'
        else:
            cmd = f'you-get --info'
        print("[INFO]", cmd)
        self.lunch_download(cmd, False)

    def real_link(self):
        cmd = f'you-get --url'
        if self.download_itag_var.get():
            if self.download_itag_entry.get() != "":
                cmd += f' --itag={self.download_itag_entry.get()}'
            else:
                print('[WARN]Please enter the itag number!!!')
                self.status_label.config(text='未填入itag！', fg='red')
                return
        if self.download_format_var.get():
            if self.download_format_entry.get() != "":
                cmd += f' --format={self.download_format_entry.get()}'
            else:
                print('[WARN]Please enter the format number!!!')
                self.status_label.config(text='未填入format！', fg='red')
                return
        print("[INFO]", cmd)
        self.lunch_download(cmd, False)

    def no_proxy_button_check(self):
        if self.no_proxy_var.get():
            self.proxy_setting_checkbutton.config(fg='gray', state='disabled')
            self.proxy_extracting_only_checkbutton.config(state='disabled')
            self.proxy_type_socks5_radiobutton.config(state='disabled')
            self.proxy_type_http_radiobutton.config(state='disabled')
            self.proxy_path_label.config(fg='gray')
            self.proxy_path_entry.config(state='disabled')
            self.proxy_login_frame.config(fg='gray')
            self.proxy_login_checkbutton.config(state='disabled')
            self.proxy_user_name_label.config(fg='gray')
            self.proxy_user_name_entry.config(state='disabled')
            self.proxy_password_label.config(fg='gray')
            self.proxy_password_entry.config(state='disabled')
            self.proxy_time_out_checkbutton.config(state='disabled')
            self.proxy_time_out_entry.config(state='disabled')
            self.proxy_time_out_label.config(fg='gray')
        else:
            self.proxy_setting_checkbutton.config(fg='black', state='normal')
            if self.proxy_setting_var.get():
                self.proxy_type_socks5_radiobutton.config(state='normal')
                self.proxy_type_http_radiobutton.config(state='normal')
                self.proxy_path_label.config(fg='black')
                self.proxy_path_entry.config(state='normal')
                if self.proxy_type_var.get() == 'Socks5':
                    self.proxy_extracting_only_checkbutton.config(state='disabled')
                    self.proxy_login_frame.config(fg='black')
                    self.proxy_login_checkbutton.config(state='normal')
                    if self.proxy_login_var.get():
                        self.proxy_user_name_label.config(fg='black')
                        self.proxy_user_name_entry.config(state='normal')
                        self.proxy_password_label.config(fg='black')
                        self.proxy_password_entry.config(state='normal')
                    else:
                        self.proxy_user_name_label.config(fg='gray')
                        self.proxy_user_name_entry.config(state='disabled')
                        self.proxy_password_label.config(fg='gray')
                        self.proxy_password_entry.config(state='disabled')
                elif self.proxy_type_var.get() == 'Http':
                    self.proxy_extracting_only_checkbutton.config(state='normal')
                    self.proxy_login_frame.config(fg='gray')
                    self.proxy_login_checkbutton.config(state='disabled')
                    self.proxy_user_name_label.config(fg='gray')
                    self.proxy_user_name_entry.config(state='disabled')
                    self.proxy_password_label.config(fg='gray')
                    self.proxy_password_entry.config(state='disabled')
            else:
                self.proxy_extracting_only_checkbutton.config(state='disabled')
                self.proxy_type_socks5_radiobutton.config(state='disabled')
                self.proxy_type_http_radiobutton.config(state='disabled')
                self.proxy_path_label.config(fg='gray')
                self.proxy_path_entry.config(state='disabled')
                self.proxy_login_frame.config(fg='gray')
                self.proxy_login_checkbutton.config(state='disabled')
                self.proxy_user_name_label.config(fg='gray')
                self.proxy_user_name_entry.config(state='disabled')
                self.proxy_password_label.config(fg='gray')
                self.proxy_password_entry.config(state='disabled')
            self.proxy_time_out_checkbutton.config(state='normal')
            if self.proxy_time_out_var.get():
                self.proxy_time_out_entry.config(state='normal')
                self.proxy_time_out_label.config(fg='black')

    def proxy_setting_button_check(self):
        if self.proxy_setting_var.get():
            self.proxy_type_socks5_radiobutton.config(state='normal')
            self.proxy_type_http_radiobutton.config(state='normal')
            self.proxy_path_label.config(fg='black')
            self.proxy_path_entry.config(state='normal')
            if self.proxy_type_var.get() == 'Socks5':
                self.proxy_extracting_only_checkbutton.config(state='disabled')
                self.proxy_login_frame.config(fg='black')
                self.proxy_login_checkbutton.config(state='normal')
                if self.proxy_login_var.get():
                    self.proxy_user_name_label.config(fg='black')
                    self.proxy_user_name_entry.config(state='normal')
                    self.proxy_password_label.config(fg='black')
                    self.proxy_password_entry.config(state='normal')
                else:
                    self.proxy_user_name_label.config(fg='gray')
                    self.proxy_user_name_entry.config(state='disabled')
                    self.proxy_password_label.config(fg='gray')
                    self.proxy_password_entry.config(state='disabled')
            elif self.proxy_type_var.get() == 'Http':
                self.proxy_extracting_only_checkbutton.config(state='normal')
                self.proxy_login_frame.config(fg='gray')
                self.proxy_login_checkbutton.config(state='disabled')
                self.proxy_user_name_label.config(fg='gray')
                self.proxy_user_name_entry.config(state='disabled')
                self.proxy_password_label.config(fg='gray')
                self.proxy_password_entry.config(state='disabled')
        else:
            self.proxy_extracting_only_checkbutton.config(state='disabled')
            self.proxy_path_label.config(fg='gray')
            self.proxy_path_entry.config(state='disabled')
            self.proxy_login_frame.config(fg='gray')
            self.proxy_login_checkbutton.config(state='disabled')
            self.proxy_user_name_label.config(fg='gray')
            self.proxy_user_name_entry.config(state='disabled')
            self.proxy_password_label.config(fg='gray')
            self.proxy_password_entry.config(state='disabled')
            self.proxy_type_socks5_radiobutton.config(state='disabled')
            self.proxy_type_http_radiobutton.config(state='disabled')

    def proxy_type_button_check(self):
        if self.proxy_type_var.get() == 'Socks5':
            self.proxy_extracting_only_checkbutton.config(state='disabled')
            self.proxy_login_frame.config(fg='black')
            self.proxy_login_checkbutton.config(state='normal')
            if self.proxy_login_var.get():
                self.proxy_user_name_label.config(fg='black')
                self.proxy_user_name_entry.config(state='normal')
                self.proxy_password_label.config(fg='black')
                self.proxy_password_entry.config(state='normal')
            else:
                self.proxy_user_name_label.config(fg='gray')
                self.proxy_user_name_entry.config(state='disabled')
                self.proxy_password_label.config(fg='gray')
                self.proxy_password_entry.config(state='disabled')
        elif self.proxy_type_var.get() == 'Http':
            self.proxy_extracting_only_checkbutton.config(state='normal')
            self.proxy_login_frame.config(fg='gray')
            self.proxy_login_checkbutton.config(state='disabled')
            self.proxy_user_name_label.config(fg='gray')
            self.proxy_user_name_entry.config(state='disabled')
            self.proxy_password_label.config(fg='gray')
            self.proxy_password_entry.config(state='disabled')

    def proxy_login_button_check(self):
        if self.proxy_login_var.get():
            self.proxy_user_name_label.config(fg='black')
            self.proxy_user_name_entry.config(state='normal')
            self.proxy_password_label.config(fg='black')
            self.proxy_password_entry.config(state='normal')
        else:
            self.proxy_user_name_label.config(fg='gray')
            self.proxy_user_name_entry.config(state='disabled')
            self.proxy_password_label.config(fg='gray')
            self.proxy_password_entry.config(state='disabled')

    def select_player_file(self):
        path = tk.filedialog.askopenfilename(filetypes=[('播放器EXE文件', ['*.exe']), ('所有文件', '.*')])
        if path != '':
            self.player_entry.delete(0, tk.END)
            self.player_entry.insert(0, path)

    def play(self):
        if self.url_entry.get() != '':
            if self.player_entry.get():
                player_data = f"'{self.player_entry.get()}' {self.play_exe_argument_entry.get()}"
                cmd = f'you-get --player "{player_data}" "{self.url_entry.get()}"'
            else:
                print('[WARN]The player executable file path was not filled!!!')
                self.status_label.config(text='未填入播放器可执行程序文件路径！', fg='red')
                return
        else:
            print('[WARN]The video file path is not entered!!!')
            self.status_label.config(text='未填入视频文件路径！', fg='red')
            return
        print("[INFO]", cmd)
        self.lunch_download(cmd, download=False, play=True)

    def select_cookies_file(self):
        path = tk.filedialog.askopenfilename(filetypes=[('Cookies文件', ['*.txt', '*.sqlite']), ('所有文件', '.*')])
        if path != '':
            self.use_cookies_entry.delete(0, tk.END)
            self.use_cookies_entry.insert(0, path)

    def new_window_var_update(self):
        self.new_window_var_old = self.new_window_var.get()

    def batch_download_power(self):
        if self.batch_download_power_var.get():
            self.batch_download_parallel_checkbutton.config(state='normal')
            self.batch_download_from_file_checkbutton.config(state='normal')
            self.batch_download_parallel()
            if self.batch_download_from_file_var.get():
                self.url_entry_hint.config(text='')
                self.url_label.config(text='文件地址：', fg='black')
                self.url_entry.config(state='normal')
                self.batch_download_from_file_select_button.config(state='normal')
            else:
                self.url_entry_hint.config(text='请在下方【下载地址列表】中添加下载地址')
                self.url_label.config(text='下载地址：', fg='gray')
                self.url_entry.config(state='disabled')
                self.batch_download_links_frame.config(fg='black')
                self.batch_download_links_text.config(fg='black', state='normal')
        else:
            self.url_entry_hint.config(text='')
            self.url_label.config(text='下载地址：', fg='black')
            self.url_entry.config(state='normal')
            self.batch_download_from_file_checkbutton.config(state='disabled')
            self.batch_download_from_file_select_button.config(state='disabled')
            self.batch_download_parallel_checkbutton.config(state='disabled')
            self.batch_download_parallel()
            self.batch_download_links_frame.config(fg='gray')
            self.batch_download_links_text.config(fg='gray', state='disabled')

    def batch_download_from_file_check(self):
        if self.batch_download_from_file_var.get():
            self.url_entry_hint.config(text='')
            self.url_label.config(text='文件地址：', fg='black')
            self.url_entry.config(state='normal')
            self.batch_download_from_file_select_button.config(state='normal')
            self.batch_download_links_frame.config(fg='gray')
            self.batch_download_links_text.config(fg='gray', state='disabled')
        else:
            self.url_entry_hint.config(text='请在下方【下载地址列表】中添加下载地址')
            self.url_label.config(text='下载地址：', fg='gray')
            self.url_entry.config(state='disabled')
            self.batch_download_from_file_select_button.config(state='disabled')
            self.batch_download_links_frame.config(fg='black')
            self.batch_download_links_text.config(fg='black', state='normal')

    def batch_download_parallel(self):
        if self.batch_download_parallel_var.get() and self.batch_download_power_var.get():
            self.new_window_var_old = self.new_window_var.get()
            self.new_window_var.set(True)
            self.new_window_checkbutton.config(fg='gray', state='disabled')
        else:
            self.new_window_var.set(self.new_window_var_old)
            self.new_window_checkbutton.config(fg='black', state='normal')

    def batch_download_from_file_select(self):
        path = tk.filedialog.askopenfilename(filetypes=[('网址集合文件', ['*.txt']), ('所有文件', '.*')])
        if path != '':
            self.url_entry_hint.config(text='')
            self.url_entry.delete(0, tk.END)
            self.url_entry.insert(0, path)
        else:
            self.url_entry_hint.config(text='请在下方【下载地址列表】中添加下载地址')

    def about(self):
        about_page = tk.Tk()
        about_page.title(f'关于 You-Get GUI v{self.__version__}')
        tk.Label(about_page, text='关于', font=(None, 25, 'bold')).pack()
        tk.Label(about_page, text='').pack()
        tk.Label(about_page, text='注意事项', font=(None, 18, 'bold')).pack()
        tk.Label(about_page, justify=tk.LEFT,
                 text='1、本程序只是给You-Get程序上一层GUI外壳以便于使用，并不包含You-Get程序本体。\n'
                      '2、若出现报错，请检查你的网络以及填入的参数是否正确并且符合you-get的要求。\n'
                      '3、有的时候软件看上去是卡住了，但其实是在等待you-get程序的反馈，耐心等待即可。\n'
                      '4、若下载时中断，可从重新填入相同的视频地址点击开始下载按键即可继续下载。\n').pack()
        tk.Label(about_page, text='').pack()
        tk.Label(about_page, text='v' + self.__version__ + '更新内容', font=(None, 18, 'bold')).pack()
        tk.Label(about_page, justify=tk.LEFT,
                 text='1、 【新增】自定义批量下载重命名编号规则\n'
                      '2、 【新增】右键菜单\n'
                      '3、 【新增】视频访问密码填写功能\n'
                      '4、 【新增】添加http代理选项\n'
                      '5、 【新增】添加“仅用于提取”的代理选项\n'
                      '6、 【新增】添加代理超时秒数设置\n'
                      '7、 【新增】添加“跳过现有文件而不检查文件大小”选项\n'
                      '8、 【新增】检测更新功能\n'
                      '9、 【新增】视频列表详细功能\n'
                      '10、【新增】You-Get版本查询等快捷按键\n'
                      '11、【优化】优化部分代码逻辑\n'
                      '12、【修复】修复上一版本的视频播放反人类操作\n').pack()
        tk.Button(about_page, text='检测更新', command=self.update_program, width=30).pack()
        tk.Label(about_page, text='').pack()
        tk.Label(about_page, text='版权', font=(None, 18, 'bold')).pack()
        tk.Label(about_page, text='(c)hunyanjie（魂魇桀） 2024').pack()
        tk.Label(about_page, text='').pack()
        tk.Label(about_page, text='链接', font=(None, 18, 'bold')).pack()
        link_frame = tk.Frame(about_page)
        tk.Label(link_frame, text='GitHub').grid(row=0, column=0)
        project_page_link_show = tk.Entry(link_frame, width=40)
        project_page_link_show.grid(row=0, column=1)
        project_page_link_show.delete(0, tk.END)
        project_page_link_show.insert(tk.END, 'https://github.com/hunyanjie/You-Get-Gui')
        project_page_link_show.config(state='readonly')
        url = tk.Button(link_frame, text='点击跳转', command=lambda: webbrowser.open('https://github.com/hunyanjie/You-Get-Gui', new=0))
        url.grid(row=0, column=2)
        wiki = tk.Button(link_frame, text='Wiki', command=lambda: webbrowser.open('https://github.com/hunyanjie/You-Get-Gui/wiki', new=0))
        wiki.grid(row=0, column=3)
        link_frame.pack()

    def update_program(self):
        class update_program_class:
            def __init__(self, window, __version__):
                self.__version__ = __version__
                self.root = window
                self.root.title('检查更新')
                self.check_hint = tk.Label(self.root, text='检查更新中...', font=(None, 16, 'bold'))
                self.check_hint.grid(row=0, columnspan=2)
                self.local_vision = tk.Label(self.root, text=f'当前版本：v{self.__version__}')
                self.local_vision.grid(row=1, columnspan=1, sticky='w')
                self.cloud_version = tk.Label(self.root, text='云端版本：获取中……')
                self.cloud_version.grid(row=2, columnspan=1, sticky='w')
                self.update_log = tk.LabelFrame(self.root, text='更新日志')
                self.update_log_text = tk.Text(self.update_log, wrap='none', exportselection=True, state='disabled',
                                               height=20, width=60)
                self.update_log_scrollbar_x = tk.Scrollbar(self.update_log,
                                                           orient='horizontal',
                                                           command=self.update_log_text.xview)
                self.update_log_scrollbar_y = tk.Scrollbar(self.update_log, orient='vertical',
                                                           command=self.update_log_text.yview)
                self.update_log_scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
                self.update_log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
                self.update_log_scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
                self.update_log_text.config(xscrollcommand=self.update_log_scrollbar_x.set)
                self.update_log_text.config(yscrollcommand=self.update_log_scrollbar_y.set)
                self.update_log.grid(row=3, column=0, rowspan=1, columnspan=8, sticky='nw')
                self.update_log_text.insert(tk.END, '获取中……')

                self.update_button = tk.Button(self.root, text='打开下载页面', state='disabled', width=15)
                self.update_button.grid(row=4, column=0)
                self.update_check()
                self.recheck_update_button = tk.Button(self.root, text='检查更新', state='normal', width=15,
                                                       command=self.update_check)
                self.recheck_update_button.grid(row=4, column=1)

            def update_check(self):
                try:
                    import urllib.request
                    response = urllib.request.urlopen('https://hunyanjie.github.io/file/project/You-Get-GUI/update.txt')
                    content = response.read().decode('utf-8')
                    print("[DEBUG]", content)
                except Exception as error_type:
                    self.check_hint.config(text=f'检查更新失败！\n原因：{error_type}', fg='orange')
                    self.cloud_version.config(text='云端版本：获取失败！')
                    self.update_log_text.config(state='normal')
                    self.update_log_text.delete('1.0', tk.END)
                    self.update_log_text.insert(tk.END, '获取失败！')
                    self.update_log_text.config(state='disabled')
                    self.update_button.config(state='disabled')
                    return

                show = content.split("\n")
                if float(self.__version__) >= float(re.search(r'v(\d+\.\d+)', show[0]).group(1)):
                    self.check_hint.config(text='当前版本已是最新版本', fg='green')
                    self.cloud_version.config(text=f'云端版本：{show[0]}')
                    self.update_log_text.config(state='normal')
                    self.update_log_text.delete('1.0', tk.END)
                    self.update_log_text.insert(tk.END, '\n'.join(show[0:]))
                    self.update_log_text.config(state='disabled')
                    self.update_button.config(state='normal', command=lambda: self.open_update_page(float(re.search(r'v(\d+\.\d+)', show[0]).group(1))))
                else:
                    if float(re.search(r'v(\d+\.\d+)', show[0]).group(1)) - float(self.__version__) >= 1:
                        self.check_hint.config(text='版本过旧，是否更新？', fg='red')
                    else:
                        self.check_hint.config(text='发现新版本，是否更新？', fg='orange')
                    self.cloud_version.config(text=f'云端版本：{show[0]}')
                    self.update_log_text.config(state='normal')
                    self.update_log_text.delete('1.0', tk.END)
                    self.update_log_text.insert(tk.END, '\n'.join(show[0:]))
                    self.update_log_text.config(state='disabled')
                    self.update_button.config(state='normal', command=lambda: self.open_update_page(float(re.search(r'v(\d+\.\d+)', show[0]).group(1))))

            @staticmethod
            def open_update_page(ver):
                webbrowser.open(f'https://github.com/hunyanjie/You-Get-Gui/releases/tag/v{ver}')

        update_window = tk.Tk()
        update_program_class(update_window, self.__version__)

    @staticmethod
    def install_you_get():
        os.system("start cmd /k pip install --upgrade you-get")
        tk.messagebox.showinfo("提示",
                               "已调起You-Get安装程序，请稍等...\n若出现报错，请尝试手动安装You-Get或者在网络上搜索解决方案。")

    @staticmethod
    def check_you_get_version():
        process = subprocess.Popen("you-get --version", stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, shell=True)
        print("[DEBUG]", process.communicate())
        if process.communicate()[1].startswith("you-get: version"):
            you_get_version = process.communicate()[1].split(",")[0].replace("you-get: version ", "")
            tk.messagebox.showinfo("You-Get 版本检查", "You-Get 版本：" + you_get_version)
        elif process.communicate()[1].replace("\n", "") == "'you-get' 不是内部或外部命令，也不是可运行的程序或批处理文件。":
            tk.messagebox.showwarning("错误", f"You-Get版本获取失败！请确保You-Get已安装")
        else:
            tk.messagebox.showerror("错误", f"未知错误！\n{process.communicate()[1]}")

    def exit_program(self):
        if tk.messagebox.askyesno("提示", "是否退出程序？"):
            self.root.destroy()
            sys.exit()


def window_close_handle():
    # 监听到关闭窗体的后，弹出提示信息框，提示是否真的要关闭，若是的话，则关闭
    if tkinter.messagebox.askyesno("提示", "是否退出程序？"):
        root.destroy()
        sys.exit()


root = tk.Tk()
YouGetGui(root)
root.protocol('WM_DELETE_WINDOW', window_close_handle)
root.mainloop()
