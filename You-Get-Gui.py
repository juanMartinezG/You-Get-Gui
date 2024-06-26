"""
author: hunyanjie（魂魇桀）
state: MIT License
"""

import json
import os
import re
import subprocess
import sys
import threading
import time
import tkinter as tk
import tkinter.filedialog
import tkinter.messagebox
import webbrowser
from tkinter import ttk


class YouGetGui:
    def __init__(self):
        super().__init__()
        self.__version__ = '2.0'
        self.new_window_var_old = None
        self.root = tk.Tk()
        self.root.title(f'You-Get GUI v{self.__version__}')
        self.top_windows = False
        self.entries_list = []
        self.new_settings = {"auto_save_download_setting": {}}
        # 隐藏窗口等待加载完成
        self.root.withdraw()
        self.default_settings = {
            "default_setting": {
                "language": "zh-cn",
                "window_type": "0",
                "exit_with_hint": True,
                "show_change_name_format": True,
                "show_hover_tip": True,
                "auto_save_download_setting": {
                    "power": False,
                    "url": False,
                    "save_path": False,
                    "save_name": False,
                    "print_with_json": False,
                    "download_captions": False,
                    "merge_video_parts": False,
                    "download_m3u8_video": False,
                    "ignore_ssl_errors": False,
                    "forced_download": False,
                    "skip_downloaded_video": False,
                    "auto_rename": False,
                    "download_video_password_power": False,
                    "download_video_password_value": False,
                    "debug": False,
                    "download_format_power": False,
                    "download_format_value": False,
                    "download_itag_power": False,
                    "download_itag_value": False,
                    "download_list_power": False,
                    "download_list_page": False,
                    "download_list_start": False,
                    "download_list_end": False,
                    "use_cookies_power": False,
                    "use_cookies_path": False,
                    "player_power": False,
                    "player_path": False,
                    "player_argument": False,
                    "run_in_new_window": True,
                    "proxy_power": False,
                    "proxy_no_proxy": False,
                    "proxy_extracting_only": False,
                    "proxy_type": False,
                    "proxy_host": False,
                    "proxy_login_power": False,
                    "proxy_login_username": False,
                    "proxy_login_password": False,
                    "proxy_timeout_time_power": False,
                    "proxy_timeout_time_value": False,
                    "batch_download_power": False,
                    "batch_download_parallel": False,
                    "batch_download_download_from_file_power": False,
                    "batch_download_download_from_file_path": False,
                    "batch_download_urls": False,
                }
            },
            "download_setting": {
                "url": "",
                "save_path": "",
                "save_name": "",
                "print_with_json": False,
                "download_captions": True,
                "merge_video_parts": True,
                "download_m3u8_video": False,
                "ignore_ssl_errors": False,
                "forced_download": False,
                "skip_downloaded_video": False,
                "auto_rename": True,
                "download_video_password": {
                    "power": False,
                    "value": ""
                },
                "debug": False,
                "download_format": {
                    "power": False,
                    "value": ""
                },
                "download_itag": {
                    "power": False,
                    "value": ""
                },
                "download_list": {
                    "power": False,
                    "page": "",
                    "start": "",
                    "end": ""
                },
                "use_cookies": {
                    "power": False,
                    "path": ""
                },
                "player": {
                    "power": False,
                    "path": "",
                    "argument": ""
                },
                "run_in_new_window": True,
                "proxy": {
                    "power": False,
                    "no_proxy": False,
                    "extracting_only": False,
                    "type": "Socks5",
                    "host": "",
                    "login": {
                        "power": False,
                        "username": "",
                        "password": ""
                    },
                    "timeout_time": {
                        "power": False,
                        "value": "10"
                    }
                },
                "batch_download": {
                    "power": False,
                    "parallel": True,
                    "download_from_file": {
                        "power": False,
                        "path": ""
                    },
                    "urls": []
                }
            },
            "languages": {
                "zh-cn": {
                    "show_name": "简体中文",
                    "clear": "清空",
                    "url": "下载地址",
                    "file_path": "文件地址",
                    "save_path": "下載路径",
                    "save_path_choose": "选择路径",
                    "save_name": "新文件名",
                    "new_name_entry_hint_date_title": "文件名替换规则",
                    "new_name_entry_hint_date_text": "{n}     - 从1开始计数（1，2，3，4……）\n"
                                                     "{Zn}    - 根据下载的数量自动用0补齐位数（例如：下载100个视频，编号会自动从001，002……开始）\n"
                                                     "{ZnM}   - 同上，不过指定从第M个开始编号（例如{Zn8}，下载的视频编号从008开始。008、009……）\n"
                                                     "{zn}    - 自动用0补齐两位数字（例如：01、02……99、100、101……）\n"
                                                     "{znM}   - 自动用0补齐两位数字，不过编号从M开始（例如{zn4}：04、05……）\n"
                                                     "{zNn}   - 自动用0补齐N+1位数字（例如{z3n}：0001……|{z4n}：00001……）\n"
                                                     "{zNnM}  - 自动用0补齐N+1位数字，并且编号从M开始（例如{z3n3}：0003、0004……|{z4n4}：00004、00005……）\n"
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
                                                     "{Z}     - 时区名称（例如，'UTC'、'PST'、'中国标准时间'）",
                    "more_info": "解析更多信息",
                    "print_with_json": "用json格式打印",
                    "real_link": "解析真实地址",
                    "start_download": "开始下载",
                    "start_play": "播放",
                    "download_settings_window": "下载设置窗口",
                    "download_settings": "下载设置",
                    "download_captions": "下载字幕（字幕，歌词，弹幕，…）",
                    "download_captions_show": "下载字幕",
                    "merge_video_parts": "合并视频片段",
                    "download_m3u8_video": "使用m3u8 url下载视频",
                    "ignore_ssl_errors": "忽略SSL错误",
                    "forced_download": "强制重新下载（覆盖同名文件或临时文件）",
                    "forced_download_show": "强制重新下载",
                    "skip_downloaded_video": "跳过现有文件而不检查文件大小",
                    "auto_rename": "自动重命名相同名称的不同文件",
                    "download_video_password_power": "视频访问密码",
                    "download_video_password_value": "密码值",
                    "debug": "开启调试模式（--debug）",
                    "debug_show": "开启调试模式",
                    "download_format_power": "下載选定格式（format）",
                    "download_format_value": "具体格式值",
                    "download_itag_power": "下载选定标签（itag）",
                    "download_itag_value": "具体标签值",
                    "download_list_power": "下載整个播放列表",
                    "download_list_start_label": "下载第",
                    "download_list_page": "页数",
                    "download_list_front_label": "页的第",
                    "download_list_start": "开始值",
                    "download_list_middle_label": "个至第",
                    "download_list_end": "结束值",
                    "download_list_end_label": "个视频（包括）。",
                    "use_cookies_power": "使用 Cookies",
                    "use_cookies_path": "Cookies 路径",
                    "use_cookies_choose": "选择 Cookies 文件",
                    "player_power": "播放视频/音乐",
                    "player_path": "播放器路径",
                    "player_path_choose": "选择EXE文件",
                    "play_exe_argument": "参数",
                    "player_argument": "播放器参数",
                    "run_in_new_window": "在新的窗口运行所有命令（推荐）",
                    "run_in_new_window_show": "在新的窗口运行所有命令",
                    "proxy": "代理",
                    "proxy_power": "使用自定义代理",
                    "proxy_no_proxy": "不使用任何代理（包括系统代理）",
                    "proxy_extracting_only": "仅用于提取",
                    "proxy_type": "代理类型",
                    "proxy_host": "代理地址",
                    "proxy_login": "登录",
                    "proxy_login_power": "用户名登录",
                    "proxy_login_username": "用户名",
                    "proxy_login_password": "密码",
                    "proxy_timeout_time_power": "代理超时时间",
                    "proxy_timeout_time_value": "时间",
                    "proxy_timeout_time_hint": "秒",
                    "batch_download": "批量功能",
                    "batch_download_power": "批量功能总开关",
                    "batch_download_parallel": "同时进行",
                    "batch_download_download_from_file_power": "从文件中获取视频地址列表",
                    "batch_download_download_from_file_path": "文件路径",
                    "batch_download_download_from_file_path_choose": "选择文件",
                    "batch_download_urls": "下载地址列表（一行一个）",
                    "batch_download_urls_show": "下载地址列表",
                    "batch_download_urls_hint": "请在下方【下载地址列表】中添加下载地址",
                    "download_log_window": "下载日志窗口",
                    "download_log": "下载日志",
                    "download_log_clean": "清空日志内容",
                    "download_hint": "※注意：本程序只是给You-Get程序上一层GUI外壳以便于使用，并不包含You-Get程序本体。\n"
                                     "1、若无下载路径，则默认下载到软件本体所在的文件夹中。\n"
                                     "2、新文件名只要填写名称，无需填写后缀（填写了也没用）。\n"
                                     "3、若无新文件名，则程序自动保存为视频原始名称。\n"
                                     "4、代理地址必须要同时填写主机地址与端口号。（如：127.0.0.1:00000）\n"
                                     "5、\"下載整个播放列表\"选项后面的空都可以不填。\n"
                                     "     若只填第x页就下载x页中的全部视频，若只填从y视频开始下载就从y视频一直下载到最后一个视频。\n"
                                     "6、用于计数的文件名替换规则只能用于同时下载视频上，无法用于逐个下载（You-Get程序限制，我无法修改）。\n"
                                     "\n其余内容可以进入GitHub的Wiki界面查看，也欢迎再Issues上提交反馈",
                    "program": "程序",
                    "about": "关于",
                    "setting_window": "设置窗口",
                    "setting": "设置",
                    "top_window": "置顶本窗口",
                    "about_you_get": "You-get相关",
                    "install_update_you_get": "一键安装/更新You-Get",
                    "install_update_you_get_hint": "已调起You-Get安装程序，请稍等...\n若出现报错，请尝试手动安装You-Get或者在网络上搜索解决方案。",
                    "show_you_get_version": "查看You-Get版本",
                    "you_get_version_check_title": "You-Get 版本检查",
                    "you_get_version": "You-Get 版本：",
                    "windows": "窗口",
                    "help": "帮助",
                    "function_introduction": "功能介绍",
                    "issues": "Issues/问题反馈",
                    "cannot_download_bilibili_video": "bilibili视频无法下载？",
                    "can_find_video_but_cannot_download": "可以检索视频信息但无法下载？",
                    "exit": "退出程序",
                    "copy": "复制",
                    "cut": "剪切",
                    "paste": "粘贴",
                    "status_hint_cannot_find_itag": "未填入itag！",
                    "status_hint_cannot_find_format": "未填入format！",
                    "status_hint_list_page_not_digit": "请在下载的特定页数处填上非负整数！",
                    "status_hint_list_start_not_digit": "请在开始下载的视频编号处填上非负整数！",
                    "status_hint_list_end_not_digit": "请在结束下载的视频编号处填上非负整数！",
                    "status_hint_cannot_find_cookies_file": "未填入Cookies路径！",
                    "status_hint_cannot_find_video_password": "未填入视频密码！",
                    "status_hint_cannot_find_proxy_user_and_passwd": "请输入代理主机的登入用户名与密码！！！",
                    "status_hint_cannot_find_proxy_host_port": "请输入代理主机地址与端口号！！",
                    "status_hint_cannot_find_timeout_time": "请输入代理超时时间！！",
                    "status_hint_cannot_find_file": "文件不存在！",
                    "status_hint_cannot_find_url_collection_file": "未填入下载网址集合文件地址！",
                    "status_hint_cannot_find_download_path": "未填入下载地址或下载网址集合文件地址！",
                    "status_hint_cannot_find_download_url": "未填入下载地址！",
                    "status_hint_cannot_find_player_path": "未填入播放器可执行程序文件路径！",
                    "status_hint_cannot_find_video_file": "未填入视频文件路径！",
                    "status_hint_lunched": "已发送请求！请等待......",
                    "log_input": "输入：",
                    "log_output": "输出：",
                    "log_error": "错误：",
                    "player_exe_file": "播放器EXE文件",
                    "cookies_file": "Cookies文件",
                    "urls_collection_file": "网址集合文件",
                    "all_type_file": "所有文件",
                    "about_window_hint_title": "注意事项",
                    "about_window_hint": "1、本程序只是给You-Get程序上一层GUI外壳以便于使用，并不包含You-Get程序本体。\n"
                                         "2、若出现报错，请检查你的网络以及填入的参数是否正确并且符合you-get的要求。\n"
                                         "3、有的时候软件看上去是卡住了，但其实是在等待you-get程序的反馈，耐心等待即可。\n"
                                         "4、若下载时中断，可从重新填入相同的视频地址点击开始下载按键即可继续下载。",
                    "upgrade": "更新",
                    "checking_upgrade": "正在联网检查更新......",
                    "check_upgrade": "检查更新",
                    "current_version": "当前版本",
                    "cloud_version": "云端版本",
                    "copyright": "版权",
                    "link": "链接",
                    "click_to_jump": "点击跳转",
                    "wiki": "Wiki",
                    "getting_version_info": "获取中......",
                    "fail_to_get_upgrade": "获取失败！",
                    "fail_to_check_upgrade": "检查更新失败！",
                    "already_new_version": "当前版本已是最新版本",
                    "old_version": "版本过旧，需要更新",
                    "find_new_version": "发现新版本",
                    "upgrade_log": "更新日志",
                    "open_download_new_version_page": "打开下载页面",
                    "reason": "原因：",
                    "hint": "提示",
                    "error": "错误",
                    "whether_save_settings": "是否保存设置？",
                    "restart_program": "请重启程序以应用新设置！",
                    "fail_to_read_file": "配置文件读取失败！",
                    "define_setting": "基础设置",
                    "program_style": "程序风格",
                    "program_style_hint": "说明：\n      0：完整界面\n      1：无日志界面\n      2：极简界面（日志和下载设置分成不同的窗口显示）",
                    "show_change_name_format": "显示【文件名替换规则】",
                    "exit_with_hint": "在退出程序时提示",
                    "show_hover_tip": "显示悬浮提示",
                    "auto_save_download_setting": "自动保留设置（下次打开程序的时候会恢复成上一次关闭程序前的状态）",
                    "auto_save_download_power": "总开关",
                    "select_all": "全选",
                    "unselect_all": "全不选",
                    "reverse_select": "反选",
                    "auto_save_download_setting_detail": "勾选你要保留的设置",
                    "restore_default_settings": "恢复默认设置",
                    "accept": "保存设置",
                    "cancel": "取消保存",
                    "whether_exit": "是否退出程序？",
                    "tip_not_required": "非必填",
                    "tip_file_path": "默认下载到程序所在的文件夹内",
                    "tip_proxy_Http_only": "仅在Http代理模式下可用",
                    "tip_proxy_socks5_only": "仅在Socks5代理模式下可用",
                    "tip_proxy_host": "必须同时填写主机地址与端口号",
                    "tip_need_restart": "若是更改则需要重启应用程序",
                },
                "en": {
                    "show_name": "English",
                    "clear": "Clear",
                    "url": "Url",
                    "file_path": "File path",
                    "save_path": "Save path",
                    "save_path_choose": "Choose",
                    "save_name": "New file name",
                    "new_name_entry_hint_date_title": "Filename replacement rules",
                    "new_name_entry_hint_date_text": "{n}     - Start counting at 1 (1，2，3，4......)\n"
                                                     "{Zn}    - Automatically fill in the digits with zeros based on the number of downloads (e.g., if you download 100 videos, the numbers will automatically start from 001,002... Start)\n"
                                                     "{ZnM}   - Same as above, but with numbering starting at the MTH (for example, {Zn8}, and 008 for downloaded videos). 008, 009...)\n"
                                                     "{zn}    - Automatically fills in two digits with zeros (e.g. 01, 02... 99, 100, 101...)\n"
                                                     "{znM}   - Automatically fills two digits with 0, but numbering starts with M (e.g. {zn4} : 04, 05...)\n"
                                                     "{zNn}   - Automatically padding N+1 digits with zeros (e.g. {z3n} : 0001... |{z4n} : 00001......)\n"
                                                     "{zNnM}  - Automatically fills N+1 digits with zeros, and numbering starts with M (e.g. {z3n3} : 0003, 0004... |{z4n4} : 00004, 00005......)\n"
                                                     "{a}     - Abbreviation for day of the week (e.g., 'Mon' to 'Sun')\n"
                                                     "{A}     - Full name of the day of the week (for example, 'Monday' through 'Sunday')\n"
                                                     "{b}     - Month abbreviation (e.g., 'Jan' to 'Dec')\n"
                                                     "{B}     - Full name of month (e.g., 'January' to 'December')\n"
                                                     "{c}     - Appropriate date and time representation (e.g., 'Tue Aug 16 21:30:00 1988')\n"
                                                     "{d}     - Day of the month with zero padding (for example, '01' to '31')\n"
                                                     "{m}     - Month ('01' to '12')\n"
                                                     "{M}     - Minute ('00' to '59')\n"
                                                     "{H}     - Hour (24-hour system, '00' to '23') \n"
                                                     "{I}     - Hour (12-hour system, '01' to '12')\n"
                                                     "{p}     - Identifier for morning or afternoon (e.g., 'AM' or 'PM')\n"
                                                     "{S}     - Seconds ('00' to '60')\n"
                                                     "{u}     - Day of the week (1 to 7, Monday being 1)\n"
                                                     "{w}     - Day of the week (0 to 6, Sunday is 0)\n"
                                                     "{x}/{D} - Appropriate date representation (e.g., '08/16/88')\n"
                                                     "{X}     - Appropriate time representation (e.g., '21:30:00')\n"
                                                     "{y}     - Year del_class without century ('00' to '99')\n"
                                                     "{C}     - Century (for example, '20')\n"
                                                     "{Y}     - Year with century (for example, '2024')\n"
                                                     "{z}     - Hour of time zone offset (e.g., '-0800' for UTC-8)\n"
                                                     "{Z}     - Time zone name (e.g., 'UTC', 'PST', 'China Standard Time')",
                    "more_info": "Parse more info",
                    "print_with_json": "Print in json",
                    "real_link": "Resolve real address",
                    "start_download": "Download",
                    "start_play": "Play",
                    "download_settings_window": "Download Settings window",
                    "download_settings": "Download Settings",
                    "download_captions": "Download subtitles (subtitles, lyrics, danmaku,...)",
                    "download_captions_show": "Download subtitles",
                    "merge_video_parts": "Merge video parts",
                    "download_m3u8_video": "Download video using m3u8 url",
                    "ignore_ssl_errors": "Ignore SSL errors",
                    "forced_download": "Force a re-download\n(overwriting a file of same name or a temp file)",
                    "forced_download_show": "Force re-download",
                    "skip_downloaded_video": "Skip existing files without checking file size",
                    "auto_rename": "Auto rename different files with the same name",
                    "download_video_password_power": "Video access password",
                    "download_video_password_value": "Password value",
                    "debug": "Enable debug mode (--debug)",
                    "debug_show": "Enable debug mode",
                    "download_format_power": "Download selected format",
                    "download_format_value": "Format value",
                    "download_itag_power": "Download selected tags (itag)",
                    "download_itag_value": "Tag value",
                    "download_list_power": "Download whole playlist",
                    "download_list_start_label": "Page",
                    "download_list_page": "Page",
                    "download_list_front_label": "Start from",
                    "download_list_start": "Start value",
                    "download_list_middle_label": "to",
                    "download_list_end": "End value",
                    "download_list_end_label": "video(s).",
                    "use_cookies_power": "Use Cookies",
                    "use_cookies_path": "Cookies path",
                    "use_cookies_choose": "Choose",
                    "player_power": "Play video/music",
                    "player_path": "Player path",
                    "player_path_choose": "Choose",
                    "play_exe_argument": "Argument",
                    "player_argument": "Player argument",
                    "run_in_new_window": "Run all commands in a new window (Recommended)",
                    "run_in_new_window_show": "Run all commands in a new window",
                    "proxy": "Proxy",
                    "proxy_power": "Use custom proxy",
                    "proxy_no_proxy": "Do not use any proxy\n(include system proxies)",
                    "proxy_extracting_only": "For extraction only",
                    "proxy_type": "Proxy type",
                    "proxy_host": "Proxy host",
                    "proxy_login": "Login",
                    "proxy_login_power": "Login",
                    "proxy_login_username": "Username",
                    "proxy_login_password": "Password",
                    "proxy_timeout_time_power": "Timeout",
                    "proxy_timeout_time_value": "Time",
                    "proxy_timeout_time_hint": "s",
                    "batch_download": "Batch download",
                    "batch_download_power": "Master switch",
                    "batch_download_parallel": "Parallel",
                    "batch_download_download_from_file_power": "Get video urls from file",
                    "batch_download_download_from_file_path": "File path",
                    "batch_download_download_from_file_path_choose": "Choose",
                    "batch_download_urls": "Video urls list (one per line)",
                    "batch_download_urls_show": "List of video urls",
                    "batch_download_urls_hint": "Please add the download address in the following [Video urls list]",
                    "download_log_window": "Download log window",
                    "download_log": "Download log",
                    "download_log_clean": "Clear all log",
                    "download_hint": "※ Note: This program simply provides a user-friendly GUI shell for You-Get and does not include the You-Get program itself.\n"
                                     "1. If no download path is specified, the software will be downloaded to its default storage folder.\n"
                                     "2. The suffix doesn't need to be filled in if the new file name includes the name.\n"
                                     "3. If there's no new file name, the program saves automatically to the original video name.\n"
                                     "4. The proxy address should be filled with both the host address and port number simultaneously. (e.g. 127.0.0.1:00000)\n"
                                     "5. You can leave the blanks after the \"Download whole playlist\" option empty.\n"
                                     "    If you only fill in page x, all videos on that page will be downloaded;\n"
                                     "    if you only fill in video y, download from video y to the last one.\n"
                                     "6. The file name replacement rule for counting is only applicable to simultaneous video downloads, not individual ones\n"
                                     "    (due to You-Get program restrictions that I can't modify).\n"
                                     "\nThe rest of the content can be viewed on GitHub's Wiki interface, and feedback on Issues is also welcome.",
                    "program": "Program",
                    "about": "About",
                    "setting_window": "Settings window",
                    "setting": "Settings",
                    "top_window": "Top this window",
                    "about_you_get": "You-get related",
                    "install_update_you_get": "One-click install / update You-Get",
                    "install_update_you_get_hint": "The You-Get installer has been started, please wait...\nIf You Get an error, try manually installing you-get or searching for a solution on the web.",
                    "show_you_get_version": "View the You-Get version",
                    "you_get_version_check_title": "You-Get version check",
                    "you_get_version": "You-Get version: ",
                    "windows": "Window",
                    "help": "Help",
                    "function_introduction": "Function introduction",
                    "issues": "Issues",
                    "cannot_download_bilibili_video": "The bilibili video cannot be downloaded?",
                    "can_find_video_but_cannot_download": "Can retrieve video information but cannot download it?",
                    "exit": "Exit",
                    "copy": "Copy",
                    "cut": "Cut",
                    "paste": "Paste",
                    "status_hint_cannot_find_itag": "No itag!",
                    "status_hint_cannot_find_format": "No format!",
                    "status_hint_list_page_not_digit": "Please fill in the specific number of pages downloaded with a non-negative integer!",
                    "status_hint_list_start_not_digit": "Please fill in the number of the video you started downloading with a non-negative integer!",
                    "status_hint_list_end_not_digit": "Please fill in a non-negative integer at the end of the video download number!",
                    "status_hint_cannot_find_cookies_file": "No cookie path filled!",
                    "status_hint_cannot_find_video_password": "No video password!",
                    "status_hint_cannot_find_proxy_user_and_passwd": "Please enter the login username and password of the proxy host!!",
                    "status_hint_cannot_find_proxy_host_port": "Please enter the proxy host address and port number!!",
                    "status_hint_cannot_find_timeout_time": "Please enter the proxy timeout time!!",
                    "status_hint_cannot_find_file": "File does not exist!",
                    "status_hint_cannot_find_url_collection_file": "Did not fill the download URL collection file address!",
                    "status_hint_cannot_find_download_path": "No download address or download URL collection file address!",
                    "status_hint_cannot_find_download_url": "No download address!",
                    "status_hint_cannot_find_player_path": "Player executable file path not filled!",
                    "status_hint_cannot_find_video_file": "Did not fill the video file path!",
                    "status_hint_lunched": "Request sent! Please wait ......",
                    "log_input": "Input: ",
                    "log_output": "Output: ",
                    "log_error": "Error: ",
                    "player_exe_file": "Player EXE file",
                    "cookies_file": "Cookie file",
                    "urls_collection_file": "URL collection file",
                    "all_type_file": "All files",
                    "about_window_hint_title": "Precautions",
                    "about_window_hint": "1. This program provides a GUI shell for easy use of You-Get, but does not include the You-Get program ontology.\n"
                                         "2. If an error occurs, verify that your network and entered parameters meet You-Get's requirements.\n"
                                         "3. Sometimes the software appears stuck, but it's actually waiting for your feedback on the You-Get program. Just be patient.\n"
                                         "4. If the download is interrupted, simply re-enter the video address and click Download to resume.",
                    "upgrade": "Update",
                    "checking_upgrade": "Networking to check for updates......",
                    "check_upgrade": "Check for updates",
                    "current_version": "Current version",
                    "cloud_version": "Cloud version",
                    "copyright": "Copyright",
                    "link": "Link",
                    "click_to_jump": "Click to jump",
                    "wiki": "Wiki",
                    "getting_version_info": "Getting......",
                    "fail_to_get_upgrade": "Failed to obtain!",
                    "fail_to_check_upgrade": "Check the update failed!",
                    "already_new_version": "The current version is the latest version.",
                    "old_version": "The version is old and needs to be updated.",
                    "find_new_version": "Discover new version",
                    "upgrade_log": "Upgrade log",
                    "open_download_new_version_page": "Open the download page.",
                    "reason": "Reason: ",
                    "hint": "Hint",
                    "error": "Error",
                    "whether_save_settings": "Do you want to save Settings?",
                    "restart_program": "Restart the program to apply the new Settings!",
                    "fail_to_read_file": "Configuration file read failed!",
                    "define_setting": "Define setting",
                    "program_style": "Program style",
                    "program_style_hint": "Description:\n      0: Full interface\n      1: No log interface\n      2: Minimal interface (log and download Settings are displayed in different Windows)",
                    "show_change_name_format": "Display [Filename replacement rules]",
                    "exit_with_hint": "Hint when exiting the program",
                    "show_hover_tip": "Display hover tips",
                    "auto_save_download_setting": "Automatically retain the setting (the next time you open the program will be restored to the state before the last shutdown)",
                    "auto_save_download_power": "Main switch",
                    "select_all": "Select all",
                    "unselect_all": "Select none",
                    "reverse_select": "Reverse select",
                    "auto_save_download_setting_detail": "Check the Settings you want to keep",
                    "restore_default_settings": "Restore default Settings",
                    "accept": "Save Settings",
                    "cancel": "Cancel save",
                    "whether_exit": "Do you want to exit the program?",
                    "tip_not_required": "Not required",
                    "tip_file_path": "Default download to the folder where the program is located",
                    "tip_proxy_Http_only": "Only work in Http proxy",
                    "tip_proxy_socks5_only": "Only work in Socks5 proxy",
                    "tip_proxy_host": "Both host address and port must be specified",
                    "tip_need_restart": "If changed, need to restart the application",
                }
            }
        }
        self.user_settings = {}
        self.final_settings = {}
        self.check_define()
        self.root.deiconify()
        # 定义颜色样式
        ttk.Style().configure('gray.TCheckbutton', foreground='gray')

        # 只是为了方便我翻代码的
        if True:
            # 下载Frame
            self.download_frame = ttk.Frame(self.root)
            # 下载地址
            self.url_label = ttk.Label(self.download_frame, text=self.final_settings["language"]["url"])
            self.url_label.grid(row=0, column=0)
            self.url_path = tk.StringVar()
            self.url_entry = ttk.Entry(self.download_frame, width=47, textvariable=self.url_path)
            self.url_entry.grid(row=0, column=1, columnspan=6)
            self.entries_list.append(self.url_entry)
            self.url_entry_hint = ttk.Label(self.download_frame, text='')
            self.url_entry_hint.grid(row=0, column=1, columnspan=6, sticky='w')
            # 清除下载地址
            self.clean = ttk.Button(self.download_frame, text=self.final_settings["language"]["clear"], width=8,
                                    command=self.clean_url_entry)
            self.clean.grid(row=0, column=7)

            # 下载路径
            self.path_label = ttk.Label(self.download_frame, text=self.final_settings["language"]["save_path"])
            self.path_label.grid(row=1, column=0)
            self.path_entry = ttk.Entry(self.download_frame, width=41)
            self.EnhancedTooltip(self, self.path_entry, self.final_settings["language"]["tip_file_path"])
            self.entries_list.append(self.path_entry)
            self.path_entry.grid(row=1, column=1, columnspan=5)
            self.clean_path = ttk.Button(self.download_frame, text=self.final_settings["language"]["save_path_choose"],
                                         width=8, command=self.select_path)
            self.clean_path.grid(row=1, column=6)
            self.path_button = ttk.Button(self.download_frame, text=self.final_settings["language"]["clear"], width=8,
                                          command=lambda: self.path_entry.delete(0, tk.END))
            self.path_button.grid(row=1, column=7)

            # 保存文件名
            self.new_name_label = ttk.Label(self.download_frame, text=self.final_settings["language"]["save_name"])
            self.new_name_label.grid(row=2, column=0)
            self.new_name_entry = ttk.Entry(self.download_frame, width=49, justify='left')
            self.new_name_entry.grid(row=2, column=1, columnspan=6)
            self.entries_list.append(self.new_name_entry)
            self.clean_new_name = ttk.Button(self.download_frame, text=self.final_settings["language"]["clear"],
                                             width=8,
                                             command=lambda: self.new_name_entry.delete(0, tk.END))
            self.clean_new_name.grid(row=2, column=7)
            self.EnhancedTooltip(self, self.new_name_entry, self.final_settings["language"]["tip_not_required"])
            # 保存文件名规则
            self.new_name_entry_hint_frame = ttk.Frame(self.download_frame)
            self.new_name_entry_hint_date_frame = tk.LabelFrame(self.new_name_entry_hint_frame,
                                                                text=self.final_settings["language"][
                                                                    "new_name_entry_hint_date_title"])
            self.new_name_entry_hint_date_text = tk.Text(self.new_name_entry_hint_date_frame, wrap='none',
                                                         foreground='black',
                                                         height=5, width=70)
            self.new_name_entry_hint_date_text.insert(tk.END,
                                                      self.final_settings["language"]["new_name_entry_hint_date_text"])
            self.new_name_entry_hint_date_text.config(state="disabled")
            self.new_name_entry_hint_date_scrollbar_x = ttk.Scrollbar(self.new_name_entry_hint_date_frame,
                                                                      orient='horizontal',
                                                                      command=self.new_name_entry_hint_date_text.xview)
            self.new_name_entry_hint_date_scrollbar_y = ttk.Scrollbar(self.new_name_entry_hint_date_frame,
                                                                      orient='vertical',
                                                                      command=self.new_name_entry_hint_date_text.yview)
            self.new_name_entry_hint_date_scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
            self.new_name_entry_hint_date_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            self.entries_list.append(self.new_name_entry_hint_date_text)
            self.new_name_entry_hint_date_scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
            self.new_name_entry_hint_date_text.config(xscrollcommand=self.new_name_entry_hint_date_scrollbar_x.set)
            self.new_name_entry_hint_date_text.config(yscrollcommand=self.new_name_entry_hint_date_scrollbar_y.set)
            self.new_name_entry_hint_date_frame.grid(row=2, column=0, rowspan=1, columnspan=8)
            if self.final_settings['default_setting']['show_change_name_format']:
                self.new_name_entry_hint_frame.grid(row=3, column=0, columnspan=8)

            # 按键栏
            self.base_bottom_frame = ttk.Frame(self.download_frame)
            # 解析更多信息
            self.print_info_frame = ttk.Frame(self.base_bottom_frame)
            self.more_info_button = ttk.Button(self.print_info_frame, text=self.final_settings["language"]["more_info"],
                                               command=self.more_info)
            self.more_info_button.grid(row=0, column=0)
            # 用json格式打印解析的信息
            self.print_info_as_json_var = tkinter.BooleanVar()
            self.print_info_as_json_var.set(False)
            self.print_info_as_json_checkbutton = ttk.Checkbutton(self.print_info_frame,
                                                                  text=self.final_settings["language"][
                                                                      "print_with_json"],
                                                                  variable=self.print_info_as_json_var)
            self.print_info_as_json_checkbutton.grid(row=0, column=1, columnspan=1, sticky=tk.W)
            self.print_info_frame.grid(row=0, column=0, columnspan=3, sticky=tk.E)
            # 解析视频真实地址
            self.real_link_button = ttk.Button(self.base_bottom_frame,
                                               text=self.final_settings["language"]["real_link"],
                                               command=self.real_link)
            self.real_link_button.grid(row=0, column=3)
            # 开始下载按钮
            self.download_button = ttk.Button(self.base_bottom_frame,
                                              text=self.final_settings["language"]["start_download"],
                                              command=self.lunch_download)
            self.download_button.grid(row=0, column=5)

            # 状态提示
            self.status_label = ttk.Label(self.base_bottom_frame, text='')
            self.status_label.grid(row=0, column=6, columnspan=2)

            self.base_bottom_frame.grid(row=4, column=0, columnspan=8, sticky=tk.W + tk.N)
            self.download_frame.grid(row=0, column=0, columnspan=8, sticky=tk.W + tk.N)

        if str(self.final_settings['default_setting']['window_type']) == '2':
            self.download_settings_window = tk.Toplevel()
            self.download_settings_window.title(self.final_settings["language"]["download_settings_window"])
            # 设置
            self.settings_frame = ttk.Frame(self.download_settings_window)
            # 不要下载字幕(字幕，歌词，弹幕，…)
            self.download_captions_var = tkinter.BooleanVar()
            self.download_captions_var.set(True)
            self.download_captions_checkbutton = ttk.Checkbutton(self.settings_frame,
                                                                 text=self.final_settings["language"][
                                                                     "download_captions"],
                                                                 variable=self.download_captions_var)
            self.download_captions_checkbutton.grid(row=0, column=0, columnspan=3, sticky=tk.W)
            # 不合并视频片段
            self.merge_video_parts_var = tkinter.BooleanVar()
            self.merge_video_parts_var.set(True)
            self.merge_video_parts_checkbutton = ttk.Checkbutton(self.settings_frame,
                                                                 text=self.final_settings["language"][
                                                                     "merge_video_parts"],
                                                                 variable=self.merge_video_parts_var)
            self.merge_video_parts_checkbutton.grid(row=1, column=0, columnspan=3, sticky=tk.W)
            # 使用m3u8 url下载视频
            self.download_m3u8_video_var = tkinter.BooleanVar()
            self.download_m3u8_video_var.set(False)
            self.download_m3u8_video_checkbutton = ttk.Checkbutton(self.settings_frame,
                                                                   text=self.final_settings["language"][
                                                                       "download_m3u8_video"],
                                                                   variable=self.download_m3u8_video_var)
            self.download_m3u8_video_checkbutton.grid(row=2, column=0, columnspan=3, sticky=tk.W)
            # 忽略SSL错误
            self.ignore_ssl_errors_var = tkinter.BooleanVar()
            self.ignore_ssl_errors_var.set(False)
            self.ignore_ssl_errors_checkbutton = ttk.Checkbutton(self.settings_frame,
                                                                 text=self.final_settings["language"][
                                                                     "ignore_ssl_errors"],
                                                                 variable=self.ignore_ssl_errors_var)
            self.ignore_ssl_errors_checkbutton.grid(row=3, column=0, columnspan=3, sticky=tk.W)
            # 强制重新下载
            self.forced_download_var = tkinter.BooleanVar()
            self.forced_download_var.set(False)
            self.forced_download_checkbutton = ttk.Checkbutton(self.settings_frame,
                                                               text=self.final_settings["language"]["forced_download"],
                                                               variable=self.forced_download_var)
            self.forced_download_checkbutton.grid(row=4, column=0, columnspan=3, sticky=tk.W)
            # 跳过现有文件而不检查文件大小
            self.skip_downloaded_video_var = tkinter.BooleanVar()
            self.skip_downloaded_video_var.set(False)
            self.skip_downloaded_video_checkbutton = ttk.Checkbutton(self.settings_frame,
                                                                     text=self.final_settings["language"][
                                                                         "skip_downloaded_video"],
                                                                     variable=self.skip_downloaded_video_var)
            self.skip_downloaded_video_checkbutton.grid(row=5, column=0, columnspan=3, sticky=tk.W)
            # 自动重命名相同名称的不同文件
            self.auto_rename_var = tkinter.BooleanVar()
            self.auto_rename_var.set(True)
            self.auto_rename_checkbutton = ttk.Checkbutton(self.settings_frame,
                                                           text=self.final_settings["language"]["auto_rename"],
                                                           variable=self.auto_rename_var)
            self.auto_rename_checkbutton.grid(row=6, column=0, columnspan=3, sticky=tk.W)
            # 视频访问密码
            self.download_video_password_frame = ttk.Frame(self.settings_frame)
            self.download_video_password_var = tkinter.BooleanVar()
            self.download_video_password_var.set(False)
            self.download_video_password_checkbutton = ttk.Checkbutton(self.download_video_password_frame,
                                                                       text=self.final_settings["language"][
                                                                           "download_video_password_power"],
                                                                       variable=self.download_video_password_var,
                                                                       command=lambda: self.download_video_password_entry.config(
                                                                           state='normal' if self.download_video_password_var.get() else 'disabled')
                                                                       )
            self.download_video_password_checkbutton.grid(row=0, column=0, columnspan=1, sticky=tk.W)
            self.download_video_password_entry = ttk.Entry(self.download_video_password_frame, width=20,
                                                           state='disabled')
            self.download_video_password_entry.grid(row=0, column=1, columnspan=1, sticky=tk.E)
            self.entries_list.append(self.download_video_password_entry)
            self.download_video_password_frame.grid(row=7, column=0, columnspan=3, sticky=tk.W)
            # 开启调试模式
            self.debug_var = tkinter.BooleanVar()
            self.debug_var.set(False)
            self.debug_checkbutton = ttk.Checkbutton(self.settings_frame, text=self.final_settings["language"]["debug"],
                                                     variable=self.debug_var)
            self.debug_checkbutton.grid(row=8, column=0, columnspan=3, sticky=tk.W)
            # 下载格式
            self.download_format_frame = ttk.Frame(self.settings_frame)
            self.download_format_var = tkinter.BooleanVar()
            self.download_format_var.set(False)
            self.download_format_checkbutton = ttk.Checkbutton(self.download_format_frame,
                                                               text=self.final_settings["language"][
                                                                   "download_format_power"],
                                                               variable=self.download_format_var,
                                                               command=lambda: self.download_format_entry.config(
                                                                   state='normal' if self.download_format_var.get() else 'disabled')
                                                               )
            self.download_format_checkbutton.grid(row=0, column=0, columnspan=1, sticky=tk.W)
            self.download_format_entry = ttk.Entry(self.download_format_frame, width=10, state='disabled')
            self.download_format_entry.grid(row=0, column=1, columnspan=2, sticky=tk.E)
            self.entries_list.append(self.download_format_entry)
            self.download_format_frame.grid(row=9, column=0, columnspan=3, sticky=tk.W)
            # 下载标签
            self.download_itag_frame = ttk.Frame(self.settings_frame)
            self.download_itag_var = tkinter.BooleanVar()
            self.download_itag_var.set(False)
            self.download_itag_checkbutton = ttk.Checkbutton(self.download_itag_frame,
                                                             text=self.final_settings["language"][
                                                                 "download_itag_power"],
                                                             variable=self.download_itag_var,
                                                             command=lambda: self.download_itag_entry.config(
                                                                 state='normal' if self.download_itag_var.get() else 'disabled')
                                                             )
            self.download_itag_checkbutton.grid(row=0, column=0, columnspan=1, sticky=tk.W)
            self.download_itag_entry = ttk.Entry(self.download_itag_frame, width=10, state='disabled')
            self.download_itag_entry.grid(row=0, column=1, columnspan=2, sticky=tk.E)
            self.entries_list.append(self.download_itag_entry)
            self.download_itag_frame.grid(row=9, column=2, columnspan=3, sticky=tk.E)
            # 下载播放列表
            self.download_all_frame = ttk.Frame(self.settings_frame)
            self.download_all_var = tkinter.BooleanVar()
            self.download_all_var.set(False)
            self.download_all_checkbutton = ttk.Checkbutton(self.download_all_frame,
                                                            text=self.final_settings["language"]["download_list_power"],
                                                            variable=self.download_all_var,
                                                            command=lambda: (
                                                                self.download_all_start_label.config(
                                                                    foreground='black' if self.download_all_var.get() else 'gray'),
                                                                self.download_all_page_entry.config(
                                                                    state='normal' if self.download_all_var.get() else 'disabled'),
                                                                self.download_all_front_label.config(
                                                                    foreground='black' if self.download_all_var.get() else 'gray'),
                                                                self.download_all_start_entry.config(
                                                                    state='normal' if self.download_all_var.get() else 'disabled'),
                                                                self.download_all_middle_label.config(
                                                                    foreground='black' if self.download_all_var.get() else 'gray'),
                                                                self.download_all_end_entry.config(
                                                                    state='normal' if self.download_all_var.get() else 'disabled'),
                                                                self.download_all_end_label.config(
                                                                    foreground='black' if self.download_all_var.get() else 'gray')))
            self.download_all_checkbutton.grid(row=0, column=0)
            self.download_all_start_label = ttk.Label(self.download_all_frame,
                                                      text=self.final_settings["language"]["download_list_start_label"],
                                                      foreground='gray')
            self.download_all_start_label.grid(row=0, column=1)
            self.download_all_page_entry = ttk.Entry(self.download_all_frame, width=5, state='disabled')
            self.download_all_page_entry.grid(row=0, column=2)
            self.EnhancedTooltip(self, self.download_all_page_entry,
                                 self.final_settings["language"]["tip_not_required"])
            self.entries_list.append(self.download_all_page_entry)
            self.download_all_front_label = ttk.Label(self.download_all_frame,
                                                      text=self.final_settings["language"]["download_list_front_label"],
                                                      foreground='gray')
            self.download_all_front_label.grid(row=0, column=3)
            self.download_all_start_entry = ttk.Entry(self.download_all_frame, width=5, state='disabled')
            self.download_all_start_entry.grid(row=0, column=4)
            self.EnhancedTooltip(self, self.download_all_start_entry,
                                 self.final_settings["language"]["tip_not_required"])
            self.entries_list.append(self.download_all_start_entry)
            self.download_all_middle_label = ttk.Label(self.download_all_frame, text=self.final_settings["language"][
                "download_list_middle_label"], foreground='gray')
            self.download_all_middle_label.grid(row=0, column=5)
            self.download_all_end_entry = ttk.Entry(self.download_all_frame, width=5, state='disabled')
            self.download_all_end_entry.grid(row=0, column=6)
            self.EnhancedTooltip(self, self.download_all_end_entry, self.final_settings["language"]["tip_not_required"])
            self.entries_list.append(self.download_all_end_entry)
            self.download_all_end_label = ttk.Label(self.download_all_frame,
                                                    text=self.final_settings["language"]["download_list_end_label"],
                                                    foreground='gray')
            self.download_all_end_label.grid(row=0, column=7)
            self.download_all_frame.grid(row=10, column=0, columnspan=8, sticky=tk.W)
            # 使用Cookies
            self.use_cookies_frame = ttk.Frame(self.settings_frame)
            self.use_cookies_var = tkinter.BooleanVar()
            self.use_cookies_var.set(False)
            self.use_cookies_checkbutton = ttk.Checkbutton(self.use_cookies_frame,
                                                           text=self.final_settings["language"]["use_cookies_power"],
                                                           variable=self.use_cookies_var,
                                                           command=lambda: (self.use_cookies_entry.config(
                                                               state='normal' if self.use_cookies_var.get() else 'disabled'),
                                                                            self.use_cookies_button.config(
                                                                                state='normal' if self.use_cookies_var.get() else 'disabled')
                                                           ))
            self.use_cookies_checkbutton.grid(row=0, column=0)
            self.use_cookies_entry = ttk.Entry(self.use_cookies_frame, width=35, state='disabled')
            self.use_cookies_entry.grid(row=0, column=1)
            self.entries_list.append(self.use_cookies_entry)
            self.use_cookies_button = ttk.Button(self.use_cookies_frame,
                                                 text=self.final_settings["language"]["use_cookies_choose"],
                                                 state='disabled',
                                                 command=self.select_cookies_file)
            self.use_cookies_button.grid(row=0, column=2)
            self.use_cookies_frame.grid(row=11, column=0, columnspan=8, sticky=tk.W)
            # 播放视频/音乐
            self.play_frame = ttk.Frame(self.settings_frame)
            self.play_var = tkinter.BooleanVar()
            self.play_var.set(False)
            self.play_checkbutton = ttk.Checkbutton(self.play_frame,
                                                    text=self.final_settings["language"]["player_power"],
                                                    variable=self.play_var,
                                                    command=lambda: (self.player_entry.config(
                                                        state='normal' if self.play_var.get() else 'disabled'),
                                                                     self.play_exe_argument_label.config(
                                                                         foreground='black' if self.play_var.get() else 'gray'),
                                                                     self.play_exe_argument_entry.config(
                                                                         state='normal' if self.play_var.get() else 'disabled'),
                                                                     self.play_button.config(
                                                                         state='normal' if self.play_var.get() else 'disabled'),
                                                                     self.download_button.config(
                                                                         text='播放' if self.play_var.get() else '开始下载',
                                                                         command=self.play if self.play_var.get() else self.lunch_download)
                                                    ))
            self.play_checkbutton.grid(row=0, column=0)
            self.player_entry = ttk.Entry(self.play_frame, width=20, state='disabled')
            self.player_entry.grid(row=0, column=1)
            self.entries_list.append(self.player_entry)
            self.play_button = ttk.Button(self.play_frame, text=self.final_settings["language"]["player_path_choose"],
                                          command=self.select_player_file,
                                          state='disabled')
            self.play_button.grid(row=0, column=2)
            self.play_exe_argument_label = ttk.Label(self.play_frame,
                                                     text=self.final_settings["language"]["play_exe_argument"],
                                                     foreground='gray')
            self.play_exe_argument_label.grid(row=0, column=3)
            self.play_exe_argument_entry = ttk.Entry(self.play_frame, width=15, state='disabled')
            self.play_exe_argument_entry.grid(row=0, column=4)
            self.EnhancedTooltip(self, self.play_exe_argument_entry,
                                 self.final_settings["language"]["tip_not_required"])
            self.entries_list.append(self.play_exe_argument_entry)
            self.play_frame.grid(row=12, column=0, columnspan=8, sticky=tk.W)
            # 在新的窗口运行所有命令
            self.new_window_var = tkinter.BooleanVar()
            self.new_window_var.set(True)
            self.new_window_checkbutton = ttk.Checkbutton(self.settings_frame,
                                                          text=self.final_settings["language"]["run_in_new_window"],
                                                          variable=self.new_window_var,
                                                          command=self.new_window_var_update)
            self.new_window_checkbutton.grid(row=13, column=0, columnspan=8, sticky=tk.W)
            self.new_window_var_update()

            # 代理选项
            self.proxy_setting = tk.LabelFrame(self.settings_frame, text=self.final_settings["language"]["proxy"])
            self.no_proxy_var = tkinter.BooleanVar()
            self.no_proxy_var.set(False)
            self.no_proxy_checkbutton = ttk.Checkbutton(self.proxy_setting,
                                                        text=self.final_settings["language"]["proxy_no_proxy"],
                                                        variable=self.no_proxy_var, command=self.no_proxy_button_check)
            self.no_proxy_checkbutton.grid(row=0, column=0, columnspan=3, sticky=tk.W)
            self.proxy_setting_var = tkinter.BooleanVar()
            self.proxy_setting_var.set(False)
            self.proxy_setting_checkbutton = ttk.Checkbutton(self.proxy_setting,
                                                             text=self.final_settings["language"]["proxy_power"],
                                                             variable=self.proxy_setting_var,
                                                             command=self.proxy_setting_button_check)
            self.proxy_setting_checkbutton.grid(row=1, column=0, columnspan=1, sticky=tk.W)
            self.proxy_extracting_only_var = tkinter.BooleanVar()
            self.proxy_extracting_only_var.set(False)
            self.proxy_extracting_only_checkbutton = ttk.Checkbutton(self.proxy_setting,
                                                                     text=self.final_settings["language"][
                                                                         "proxy_extracting_only"],
                                                                     variable=self.proxy_extracting_only_var,
                                                                     state='disabled')
            self.EnhancedTooltip(self, self.proxy_extracting_only_checkbutton, self.final_settings["language"]["tip_proxy_Http_only"])
            self.proxy_extracting_only_checkbutton.grid(row=1, column=1, columnspan=1, sticky=tk.W)
            self.proxy_type_var = tkinter.StringVar()
            self.proxy_type_var.set('Socks5')
            self.proxy_type_socks5_radiobutton = ttk.Radiobutton(self.proxy_setting, text='Socks5',
                                                                 variable=self.proxy_type_var, value='Socks5',
                                                                 state='disabled', command=self.proxy_type_button_check)
            self.proxy_type_socks5_radiobutton.grid(row=2, column=0, sticky=tk.W)
            self.proxy_type_http_radiobutton = ttk.Radiobutton(self.proxy_setting, text='Http',
                                                               variable=self.proxy_type_var, value='Http',
                                                               state='disabled',
                                                               command=self.proxy_type_button_check)
            self.proxy_type_http_radiobutton.grid(row=2, column=1, sticky=tk.W)
            self.proxy_path_label = ttk.Label(self.proxy_setting, text=self.final_settings["language"]["proxy_host"],
                                              foreground='gray')
            self.proxy_path_label.grid(row=3, column=0, sticky=tk.W)
            self.proxy_path_entry = ttk.Entry(self.proxy_setting, width=20, state='disabled')
            self.proxy_path_entry.grid(row=3, column=0, columnspan=3, sticky=tk.E)
            self.entries_list.append(self.proxy_path_entry)
            self.proxy_login_frame = tk.LabelFrame(self.proxy_setting,
                                                   text=self.final_settings["language"]["proxy_login"],
                                                   foreground='gray')
            self.EnhancedTooltip(self, self.proxy_login_frame, self.final_settings["language"]["tip_proxy_socks5_only"])
            self.proxy_login_var = tkinter.BooleanVar()
            self.proxy_login_var.set(False)
            self.proxy_login_checkbutton = ttk.Checkbutton(self.proxy_login_frame,
                                                           text=self.final_settings["language"]["proxy_login_power"],
                                                           variable=self.proxy_login_var,
                                                           command=self.proxy_login_button_check, state='disabled')
            self.proxy_login_checkbutton.grid(row=0, column=0, columnspan=3, sticky=tk.W)
            self.proxy_user_name_label = ttk.Label(self.proxy_login_frame,
                                                   text=self.final_settings["language"]["proxy_login_username"],
                                                   foreground='gray')
            self.proxy_user_name_label.grid(row=1, column=0)
            self.proxy_user_name_entry = ttk.Entry(self.proxy_login_frame, width=21, state='disabled')
            self.proxy_user_name_entry.grid(row=1, column=1, columnspan=6)
            self.entries_list.append(self.proxy_user_name_entry)
            self.proxy_password_label = ttk.Label(self.proxy_login_frame,
                                                  text=self.final_settings["language"]["proxy_login_password"],
                                                  foreground='gray')
            self.proxy_password_label.grid(row=2, column=0)
            self.proxy_password_entry = ttk.Entry(self.proxy_login_frame, width=21, state='disabled')
            self.proxy_password_entry.grid(row=2, column=1, columnspan=6)
            self.entries_list.append(self.proxy_password_entry)
            self.proxy_login_frame.grid(row=4, column=0, columnspan=3, sticky=tk.W)
            self.proxy_time_out_frame = ttk.Frame(self.proxy_setting)
            self.proxy_time_out_var = tkinter.BooleanVar()
            self.proxy_time_out_var.set(False)
            self.proxy_time_out_checkbutton = ttk.Checkbutton(self.proxy_time_out_frame,
                                                              text=self.final_settings["language"][
                                                                  "proxy_timeout_time_power"],
                                                              variable=self.proxy_time_out_var,
                                                              command=lambda: [self.proxy_time_out_entry.config(
                                                                  state='normal' if self.proxy_time_out_var.get() else 'disabled'),
                                                                  self.proxy_time_out_label.config(
                                                                      foreground='black' if self.proxy_time_out_var.get() else 'gray')
                                                              ]
                                                              )
            self.proxy_time_out_checkbutton.grid(row=0, column=0)
            self.proxy_time_out_entry = ttk.Entry(self.proxy_time_out_frame, width=10)
            self.proxy_time_out_entry.insert(0, '10')
            self.proxy_time_out_entry.config(state='disabled')
            self.proxy_time_out_entry.grid(row=0, column=1)
            self.entries_list.append(self.proxy_time_out_entry)
            self.proxy_time_out_label = ttk.Label(self.proxy_time_out_frame,
                                                  text=self.final_settings["language"]["proxy_timeout_time_hint"],
                                                  foreground='gray')
            self.proxy_time_out_label.grid(row=0, column=2)
            self.proxy_time_out_frame.grid(row=5, column=0, columnspan=3, sticky=tk.W)
            self.proxy_setting.grid(row=0, column=3, rowspan=9, sticky=tk.W + tk.N)
            # 批量下载
            self.batch_download_frame = tk.LabelFrame(self.settings_frame,
                                                      text=self.final_settings["language"]["batch_download"])
            self.batch_download_power_var = tkinter.BooleanVar()
            self.batch_download_power_var.set(False)
            self.batch_download_power_checkbutton = ttk.Checkbutton(self.batch_download_frame,
                                                                    text=self.final_settings["language"][
                                                                        "batch_download_power"],
                                                                    variable=self.batch_download_power_var,
                                                                    command=self.batch_download_power)
            self.batch_download_power_checkbutton.grid(row=0, column=0, columnspan=1, sticky=tk.W)
            self.batch_download_parallel_var = tkinter.BooleanVar()
            self.batch_download_parallel_var.set(True)
            self.batch_download_parallel_checkbutton = ttk.Checkbutton(self.batch_download_frame,
                                                                       text=self.final_settings["language"][
                                                                           "batch_download_parallel"],
                                                                       state='disabled',
                                                                       variable=self.batch_download_parallel_var,
                                                                       command=self.batch_download_parallel)
            self.batch_download_parallel_checkbutton.grid(row=0, column=1, columnspan=1, sticky=tk.W)
            self.batch_download_from_file_frame = ttk.Frame(self.batch_download_frame)
            self.batch_download_from_file_var = tkinter.BooleanVar()
            self.batch_download_from_file_var.set(False)
            self.batch_download_file_path = tk.StringVar()
            self.batch_download_from_file_checkbutton = ttk.Checkbutton(self.batch_download_from_file_frame,
                                                                        text=self.final_settings["language"][
                                                                            "batch_download_download_from_file_power"],
                                                                        state='disabled',
                                                                        variable=self.batch_download_from_file_var,
                                                                        command=self.batch_download_from_file_check)
            self.batch_download_from_file_checkbutton.grid(row=0, column=0, columnspan=1, sticky=tk.W)
            self.batch_download_from_file_select_button = ttk.Button(self.batch_download_from_file_frame,
                                                                     text=self.final_settings["language"][
                                                                         "batch_download_download_from_file_path_choose"],
                                                                     state='disabled',
                                                                     command=self.batch_download_from_file_select)
            self.batch_download_from_file_select_button.grid(row=0, column=1, columnspan=1)
            self.batch_download_from_file_frame.grid(row=0, column=2, columnspan=6, sticky=tk.W)

            self.batch_download_links_frame = tk.LabelFrame(self.batch_download_frame,
                                                            text=self.final_settings["language"]["batch_download_urls"],
                                                            foreground='gray')
            self.batch_download_links_text = tk.Text(self.batch_download_links_frame, wrap='none', foreground='gray',
                                                     height=7, width=70, state='disabled')
            self.batch_download_links_scrollbar_x = ttk.Scrollbar(self.batch_download_links_frame, orient='horizontal',
                                                                  command=self.batch_download_links_text.xview)
            self.batch_download_links_scrollbar_y = ttk.Scrollbar(self.batch_download_links_frame, orient='vertical',
                                                                  command=self.batch_download_links_text.yview)
            self.batch_download_links_scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
            self.batch_download_links_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            self.entries_list.append(self.batch_download_links_text)
            self.batch_download_links_scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
            self.batch_download_links_text.config(xscrollcommand=self.batch_download_links_scrollbar_x.set)
            self.batch_download_links_text.config(yscrollcommand=self.batch_download_links_scrollbar_y.set)
            self.batch_download_links_frame.grid(row=2, column=0, rowspan=1, columnspan=8, sticky='nw')

            self.batch_download_frame.grid(row=14, column=0, columnspan=8, sticky=tk.W)
            self.settings_frame.grid(row=1, column=0, columnspan=8, rowspan=20, sticky=tk.W + tk.N)
            self.download_log_window = tk.Toplevel()
            self.download_log_window.title(self.final_settings["language"]["download_log_window"])
            # 输出
            self.output_frame = ttk.Frame(self.download_log_window)
            self.output_text = tk.Text(self.output_frame, wrap=tk.WORD, height=40, width=84)
            self.output_scrollbar = ttk.Scrollbar(self.output_frame, command=self.output_text.yview)
            self.output_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            self.entries_list.append(self.output_text)
            self.output_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            self.output_text.config(yscrollcommand=self.output_scrollbar.set)
            self.output_frame.grid(row=0, column=8, rowspan=20, sticky="nsew")
            self.output_text_clean = ttk.Button(self.download_log_window,
                                                text=self.final_settings["language"]["download_log_clean"],
                                                command=lambda: self.output_text.delete('1.0', tk.END))
            self.output_text_clean.grid(row=0, column=8, sticky='ne')
            # 提示栏
            self.tips_label = ttk.Label(self.download_log_window, justify=tk.LEFT,
                                        text=self.final_settings["language"]["download_hint"])
            self.tips_label.grid(row=20, column=8, columnspan=8)
        else:
            # 设置
            self.settings_frame = tk.LabelFrame(self.root, text=self.final_settings["language"]["download_settings"])
            # 不要下载字幕(字幕，歌词，弹幕，…)
            self.download_captions_var = tkinter.BooleanVar()
            self.download_captions_var.set(True)
            self.download_captions_checkbutton = ttk.Checkbutton(self.settings_frame,
                                                                 text=self.final_settings["language"][
                                                                     "download_captions"],
                                                                 variable=self.download_captions_var)
            self.download_captions_checkbutton.grid(row=0, column=0, columnspan=3, sticky=tk.W)
            # 不合并视频片段
            self.merge_video_parts_var = tkinter.BooleanVar()
            self.merge_video_parts_var.set(True)
            self.merge_video_parts_checkbutton = ttk.Checkbutton(self.settings_frame,
                                                                 text=self.final_settings["language"][
                                                                     "merge_video_parts"],
                                                                 variable=self.merge_video_parts_var)
            self.merge_video_parts_checkbutton.grid(row=1, column=0, columnspan=3, sticky=tk.W)
            # 使用m3u8 url下载视频
            self.download_m3u8_video_var = tkinter.BooleanVar()
            self.download_m3u8_video_var.set(False)
            self.download_m3u8_video_checkbutton = ttk.Checkbutton(self.settings_frame,
                                                                   text=self.final_settings["language"][
                                                                       "download_m3u8_video"],
                                                                   variable=self.download_m3u8_video_var)
            self.download_m3u8_video_checkbutton.grid(row=2, column=0, columnspan=3, sticky=tk.W)
            # 忽略SSL错误
            self.ignore_ssl_errors_var = tkinter.BooleanVar()
            self.ignore_ssl_errors_var.set(False)
            self.ignore_ssl_errors_checkbutton = ttk.Checkbutton(self.settings_frame,
                                                                 text=self.final_settings["language"][
                                                                     "ignore_ssl_errors"],
                                                                 variable=self.ignore_ssl_errors_var)
            self.ignore_ssl_errors_checkbutton.grid(row=3, column=0, columnspan=3, sticky=tk.W)
            # 强制重新下载
            self.forced_download_var = tkinter.BooleanVar()
            self.forced_download_var.set(False)
            self.forced_download_checkbutton = ttk.Checkbutton(self.settings_frame,
                                                               text=self.final_settings["language"]["forced_download"],
                                                               variable=self.forced_download_var)
            self.forced_download_checkbutton.grid(row=4, column=0, columnspan=3, sticky=tk.W)
            # 跳过现有文件而不检查文件大小
            self.skip_downloaded_video_var = tkinter.BooleanVar()
            self.skip_downloaded_video_var.set(False)
            self.skip_downloaded_video_checkbutton = ttk.Checkbutton(self.settings_frame,
                                                                     text=self.final_settings["language"][
                                                                         "skip_downloaded_video"],
                                                                     variable=self.skip_downloaded_video_var)
            self.skip_downloaded_video_checkbutton.grid(row=5, column=0, columnspan=3, sticky=tk.W)
            # 自动重命名相同名称的不同文件
            self.auto_rename_var = tkinter.BooleanVar()
            self.auto_rename_var.set(True)
            self.auto_rename_checkbutton = ttk.Checkbutton(self.settings_frame,
                                                           text=self.final_settings["language"]["auto_rename"],
                                                           variable=self.auto_rename_var)
            self.auto_rename_checkbutton.grid(row=6, column=0, columnspan=3, sticky=tk.W)
            # 视频访问密码
            self.download_video_password_frame = ttk.Frame(self.settings_frame)
            self.download_video_password_var = tkinter.BooleanVar()
            self.download_video_password_var.set(False)
            self.download_video_password_checkbutton = ttk.Checkbutton(self.download_video_password_frame,
                                                                       text=self.final_settings["language"][
                                                                           "download_video_password_power"],
                                                                       variable=self.download_video_password_var,
                                                                       command=lambda: self.download_video_password_entry.config(
                                                                           state='normal' if self.download_video_password_var.get() else 'disabled')
                                                                       )
            self.download_video_password_checkbutton.grid(row=0, column=0, columnspan=1, sticky=tk.W)
            self.download_video_password_entry = ttk.Entry(self.download_video_password_frame, width=20,
                                                           state='disabled')
            self.download_video_password_entry.grid(row=0, column=1, columnspan=1, sticky=tk.E)
            self.entries_list.append(self.download_video_password_entry)
            self.download_video_password_frame.grid(row=7, column=0, columnspan=3, sticky=tk.W)
            # 开启调试模式
            self.debug_var = tkinter.BooleanVar()
            self.debug_var.set(False)
            self.debug_checkbutton = ttk.Checkbutton(self.settings_frame, text=self.final_settings["language"]["debug"],
                                                     variable=self.debug_var)
            self.debug_checkbutton.grid(row=8, column=0, columnspan=3, sticky=tk.W)
            # 下载格式
            self.download_format_frame = ttk.Frame(self.settings_frame)
            self.download_format_var = tkinter.BooleanVar()
            self.download_format_var.set(False)
            self.download_format_checkbutton = ttk.Checkbutton(self.download_format_frame,
                                                               text=self.final_settings["language"][
                                                                   "download_format_power"],
                                                               variable=self.download_format_var,
                                                               command=lambda: self.download_format_entry.config(
                                                                   state='normal' if self.download_format_var.get() else 'disabled')
                                                               )
            self.download_format_checkbutton.grid(row=0, column=0, columnspan=1, sticky=tk.W)
            self.download_format_entry = ttk.Entry(self.download_format_frame, width=10, state='disabled')
            self.download_format_entry.grid(row=0, column=1, columnspan=2, sticky=tk.E)
            self.entries_list.append(self.download_format_entry)
            self.download_format_frame.grid(row=9, column=0, columnspan=3, sticky=tk.W)
            # 下载标签
            self.download_itag_frame = ttk.Frame(self.settings_frame)
            self.download_itag_var = tkinter.BooleanVar()
            self.download_itag_var.set(False)
            self.download_itag_checkbutton = ttk.Checkbutton(self.download_itag_frame,
                                                             text=self.final_settings["language"][
                                                                 "download_itag_power"],
                                                             variable=self.download_itag_var,
                                                             command=lambda: self.download_itag_entry.config(
                                                                 state='normal' if self.download_itag_var.get() else 'disabled')
                                                             )
            self.download_itag_checkbutton.grid(row=0, column=0, columnspan=1, sticky=tk.W)
            self.download_itag_entry = ttk.Entry(self.download_itag_frame, width=10, state='disabled')
            self.download_itag_entry.grid(row=0, column=1, columnspan=2, sticky=tk.E)
            self.entries_list.append(self.download_itag_entry)
            self.download_itag_frame.grid(row=9, column=2, columnspan=3, sticky=tk.E)
            # 下载播放列表
            self.download_all_frame = ttk.Frame(self.settings_frame)
            self.download_all_var = tkinter.BooleanVar()
            self.download_all_var.set(False)
            self.download_all_checkbutton = ttk.Checkbutton(self.download_all_frame,
                                                            text=self.final_settings["language"]["download_list_power"],
                                                            variable=self.download_all_var,
                                                            command=lambda: (self.download_all_start_label.config(
                                                                foreground='black' if self.download_all_var.get() else 'gray'),
                                                                             self.download_all_page_entry.config(
                                                                                 state='normal' if self.download_all_var.get() else 'disabled'),
                                                                             self.download_all_front_label.config(
                                                                                 foreground='black' if self.download_all_var.get() else 'gray'),
                                                                             self.download_all_start_entry.config(
                                                                                 state='normal' if self.download_all_var.get() else 'disabled'),
                                                                             self.download_all_middle_label.config(
                                                                                 foreground='black' if self.download_all_var.get() else 'gray'),
                                                                             self.download_all_end_entry.config(
                                                                                 state='normal' if self.download_all_var.get() else 'disabled'),
                                                                             self.download_all_end_label.config(
                                                                                 foreground='black' if self.download_all_var.get() else 'gray')
                                                            )
                                                            )
            self.download_all_checkbutton.grid(row=0, column=0)
            self.download_all_start_label = ttk.Label(self.download_all_frame,
                                                      text=self.final_settings["language"]["download_list_start_label"],
                                                      foreground='gray')
            self.download_all_start_label.grid(row=0, column=1)
            self.download_all_page_entry = ttk.Entry(self.download_all_frame, width=5, state='disabled')
            self.download_all_page_entry.grid(row=0, column=2)
            self.entries_list.append(self.download_all_page_entry)
            self.download_all_front_label = ttk.Label(self.download_all_frame,
                                                      text=self.final_settings["language"]["download_list_front_label"],
                                                      foreground='gray')
            self.download_all_front_label.grid(row=0, column=3)
            self.download_all_start_entry = ttk.Entry(self.download_all_frame, width=5, state='disabled')
            self.download_all_start_entry.grid(row=0, column=4)
            self.entries_list.append(self.download_all_start_entry)
            self.download_all_middle_label = ttk.Label(self.download_all_frame, text=self.final_settings["language"][
                "download_list_middle_label"], foreground='gray')
            self.download_all_middle_label.grid(row=0, column=5)
            self.download_all_end_entry = ttk.Entry(self.download_all_frame, width=5, state='disabled')
            self.download_all_end_entry.grid(row=0, column=6)
            self.entries_list.append(self.download_all_end_entry)
            self.download_all_end_label = ttk.Label(self.download_all_frame,
                                                    text=self.final_settings["language"]["download_list_end_label"],
                                                    foreground='gray')
            self.download_all_end_label.grid(row=0, column=7)
            self.download_all_frame.grid(row=10, column=0, columnspan=8, sticky=tk.W)
            # 使用Cookies
            self.use_cookies_frame = ttk.Frame(self.settings_frame)
            self.use_cookies_var = tkinter.BooleanVar()
            self.use_cookies_var.set(False)
            self.use_cookies_checkbutton = ttk.Checkbutton(self.use_cookies_frame,
                                                           text=self.final_settings["language"]["use_cookies_power"],
                                                           variable=self.use_cookies_var,
                                                           command=lambda: (self.use_cookies_entry.config(
                                                               state='normal' if self.use_cookies_var.get() else 'disabled'),
                                                                            self.use_cookies_button.config(
                                                                                state='normal' if self.use_cookies_var.get() else 'disabled')
                                                           ))
            self.use_cookies_checkbutton.grid(row=0, column=0)
            self.use_cookies_entry = ttk.Entry(self.use_cookies_frame, width=35, state='disabled')
            self.use_cookies_entry.grid(row=0, column=1)
            self.entries_list.append(self.use_cookies_entry)
            self.use_cookies_button = ttk.Button(self.use_cookies_frame,
                                                 text=self.final_settings["language"]["use_cookies_choose"],
                                                 state='disabled',
                                                 command=self.select_cookies_file)
            self.use_cookies_button.grid(row=0, column=2)
            self.use_cookies_frame.grid(row=11, column=0, columnspan=8, sticky=tk.W)
            # 播放视频/音乐
            self.play_frame = ttk.Frame(self.settings_frame)
            self.play_var = tkinter.BooleanVar()
            self.play_var.set(False)
            self.play_checkbutton = ttk.Checkbutton(self.play_frame,
                                                    text=self.final_settings["language"]["player_power"],
                                                    variable=self.play_var,
                                                    command=lambda: (self.player_entry.config(
                                                        state='normal' if self.play_var.get() else 'disabled'),
                                                                     self.play_exe_argument_label.config(
                                                                         foreground='black' if self.play_var.get() else 'gray'),
                                                                     self.play_exe_argument_entry.config(
                                                                         state='normal' if self.play_var.get() else 'disabled'),
                                                                     self.play_button.config(
                                                                         state='normal' if self.play_var.get() else 'disabled'),
                                                                     self.download_button.config(
                                                                         text='播放' if self.play_var.get() else '开始下载',
                                                                         command=self.play if self.play_var.get() else self.lunch_download)
                                                    ))
            self.play_checkbutton.grid(row=0, column=0)
            self.player_entry = ttk.Entry(self.play_frame, width=20, state='disabled')
            self.player_entry.grid(row=0, column=1)
            self.entries_list.append(self.player_entry)
            self.play_button = ttk.Button(self.play_frame, text=self.final_settings["language"]["player_path_choose"],
                                          command=self.select_player_file,
                                          state='disabled')
            self.play_button.grid(row=0, column=2)
            self.play_exe_argument_label = ttk.Label(self.play_frame,
                                                     text=self.final_settings["language"]["play_exe_argument"],
                                                     foreground='gray')
            self.play_exe_argument_label.grid(row=0, column=3)
            self.play_exe_argument_entry = ttk.Entry(self.play_frame, width=15, state='disabled')
            self.EnhancedTooltip(self, self.play_exe_argument_entry,
                                 self.final_settings["language"]["tip_not_required"])
            self.play_exe_argument_entry.grid(row=0, column=4)
            self.entries_list.append(self.play_exe_argument_entry)
            self.play_frame.grid(row=12, column=0, columnspan=8, sticky=tk.W)
            # 在新的窗口运行所有命令
            self.new_window_var = tkinter.BooleanVar()
            self.new_window_var.set(True)
            self.new_window_checkbutton = ttk.Checkbutton(self.settings_frame,
                                                          text=self.final_settings["language"]["run_in_new_window"],
                                                          variable=self.new_window_var,
                                                          command=self.new_window_var_update)
            self.new_window_checkbutton.grid(row=13, column=0, columnspan=8, sticky=tk.W)
            self.new_window_var_update()

            # 代理选项
            self.proxy_setting = tk.LabelFrame(self.settings_frame, text=self.final_settings["language"]["proxy"])
            self.no_proxy_var = tkinter.BooleanVar()
            self.no_proxy_var.set(False)
            self.no_proxy_checkbutton = ttk.Checkbutton(self.proxy_setting,
                                                        text=self.final_settings["language"]["proxy_no_proxy"],
                                                        variable=self.no_proxy_var, command=self.no_proxy_button_check)
            self.no_proxy_checkbutton.grid(row=0, column=0, columnspan=3, sticky=tk.W)
            self.proxy_setting_var = tkinter.BooleanVar()
            self.proxy_setting_var.set(False)
            self.proxy_setting_checkbutton = ttk.Checkbutton(self.proxy_setting,
                                                             text=self.final_settings["language"]["proxy_power"],
                                                             variable=self.proxy_setting_var,
                                                             command=self.proxy_setting_button_check)
            self.proxy_setting_checkbutton.grid(row=1, column=0, columnspan=1, sticky=tk.W)
            self.proxy_extracting_only_var = tkinter.BooleanVar()
            self.proxy_extracting_only_var.set(False)
            self.proxy_extracting_only_checkbutton = ttk.Checkbutton(self.proxy_setting,
                                                                     text=self.final_settings["language"][
                                                                         "proxy_extracting_only"],
                                                                     variable=self.proxy_extracting_only_var,
                                                                     state='disabled')
            self.EnhancedTooltip(self, self.proxy_extracting_only_checkbutton, self.final_settings["language"]["tip_proxy_Http_only"])
            self.proxy_extracting_only_checkbutton.grid(row=1, column=1, columnspan=1, sticky=tk.W)
            self.proxy_type_var = tkinter.StringVar()
            self.proxy_type_var.set('Socks5')
            self.proxy_type_socks5_radiobutton = ttk.Radiobutton(self.proxy_setting, text='Socks5',
                                                                 variable=self.proxy_type_var, value='Socks5',
                                                                 state='disabled', command=self.proxy_type_button_check)
            self.proxy_type_socks5_radiobutton.grid(row=2, column=0, sticky=tk.W)
            self.proxy_type_http_radiobutton = ttk.Radiobutton(self.proxy_setting, text='Http',
                                                               variable=self.proxy_type_var, value='Http',
                                                               state='disabled',
                                                               command=self.proxy_type_button_check)
            self.proxy_type_http_radiobutton.grid(row=2, column=1, sticky=tk.W)
            self.proxy_path_label = ttk.Label(self.proxy_setting, text=self.final_settings["language"]["proxy_host"],
                                              foreground='gray')
            self.proxy_path_label.grid(row=3, column=0, sticky=tk.W)
            self.proxy_path_entry = ttk.Entry(self.proxy_setting, width=20, state='disabled')
            self.EnhancedTooltip(self, self.proxy_path_entry, self.final_settings["language"]["tip_proxy_host"])
            self.proxy_path_entry.grid(row=3, column=0, columnspan=3, sticky=tk.E)
            self.entries_list.append(self.proxy_path_entry)
            self.proxy_login_frame = tk.LabelFrame(self.proxy_setting,
                                                   text=self.final_settings["language"]["proxy_login"],
                                                   foreground='gray')
            self.EnhancedTooltip(self, self.proxy_login_frame, self.final_settings["language"]["tip_proxy_socks5_only"])
            self.proxy_login_var = tkinter.BooleanVar()
            self.proxy_login_var.set(False)
            self.proxy_login_checkbutton = ttk.Checkbutton(self.proxy_login_frame,
                                                           text=self.final_settings["language"]["proxy_login_power"],
                                                           variable=self.proxy_login_var,
                                                           command=self.proxy_login_button_check, state='disabled')
            self.proxy_login_checkbutton.grid(row=0, column=0, columnspan=3, sticky=tk.W)
            self.proxy_user_name_label = ttk.Label(self.proxy_login_frame,
                                                   text=self.final_settings["language"]["proxy_login_username"],
                                                   foreground='gray')
            self.proxy_user_name_label.grid(row=1, column=0)
            self.proxy_user_name_entry = ttk.Entry(self.proxy_login_frame, width=21, state='disabled')
            self.proxy_user_name_entry.grid(row=1, column=1, columnspan=6)
            self.entries_list.append(self.proxy_user_name_entry)
            self.proxy_password_label = ttk.Label(self.proxy_login_frame,
                                                  text=self.final_settings["language"]["proxy_login_password"],
                                                  foreground='gray')
            self.proxy_password_label.grid(row=2, column=0)
            self.proxy_password_entry = ttk.Entry(self.proxy_login_frame, width=21, state='disabled')
            self.proxy_password_entry.grid(row=2, column=1, columnspan=6)
            self.entries_list.append(self.proxy_password_entry)
            self.proxy_login_frame.grid(row=4, column=0, columnspan=3, sticky=tk.W)
            self.proxy_time_out_frame = ttk.Frame(self.proxy_setting)
            self.proxy_time_out_var = tkinter.BooleanVar()
            self.proxy_time_out_var.set(False)
            self.proxy_time_out_checkbutton = ttk.Checkbutton(self.proxy_time_out_frame,
                                                              text=self.final_settings["language"][
                                                                  "proxy_timeout_time_power"],
                                                              variable=self.proxy_time_out_var,
                                                              command=lambda: [self.proxy_time_out_entry.config(
                                                                  state='normal' if self.proxy_time_out_var.get() else 'disabled'),
                                                                  self.proxy_time_out_label.config(
                                                                      foreground='black' if self.proxy_time_out_var.get() else 'gray')
                                                              ]
                                                              )
            self.proxy_time_out_checkbutton.grid(row=0, column=0)
            self.proxy_time_out_entry = ttk.Entry(self.proxy_time_out_frame, width=10)
            self.proxy_time_out_entry.insert(0, '10')
            self.proxy_time_out_entry.config(state='disabled')
            self.proxy_time_out_entry.grid(row=0, column=1)
            self.entries_list.append(self.proxy_time_out_entry)
            self.proxy_time_out_label = ttk.Label(self.proxy_time_out_frame,
                                                  text=self.final_settings["language"]["proxy_timeout_time_hint"],
                                                  foreground='gray')
            self.proxy_time_out_label.grid(row=0, column=2)
            self.proxy_time_out_frame.grid(row=5, column=0, columnspan=3, sticky=tk.W)
            self.proxy_setting.grid(row=0, column=3, rowspan=9, sticky=tk.W + tk.N)
            # 批量下载
            self.batch_download_frame = tk.LabelFrame(self.settings_frame,
                                                      text=self.final_settings["language"]["batch_download"])
            self.batch_download_power_var = tkinter.BooleanVar()
            self.batch_download_power_var.set(False)
            self.batch_download_power_checkbutton = ttk.Checkbutton(self.batch_download_frame,
                                                                    text=self.final_settings["language"][
                                                                        "batch_download_power"],
                                                                    variable=self.batch_download_power_var,
                                                                    command=self.batch_download_power)
            self.batch_download_power_checkbutton.grid(row=0, column=0, columnspan=1, sticky=tk.W)
            self.batch_download_parallel_var = tkinter.BooleanVar()
            self.batch_download_parallel_var.set(True)
            self.batch_download_parallel_checkbutton = ttk.Checkbutton(self.batch_download_frame,
                                                                       text=self.final_settings["language"][
                                                                           "batch_download_parallel"],
                                                                       state='disabled',
                                                                       variable=self.batch_download_parallel_var,
                                                                       command=self.batch_download_parallel)
            self.batch_download_parallel_checkbutton.grid(row=0, column=1, columnspan=1, sticky=tk.W)
            self.batch_download_from_file_frame = ttk.Frame(self.batch_download_frame)
            self.batch_download_from_file_var = tkinter.BooleanVar()
            self.batch_download_from_file_var.set(False)
            self.batch_download_file_path = tk.StringVar()
            self.batch_download_from_file_checkbutton = ttk.Checkbutton(self.batch_download_from_file_frame,
                                                                        text=self.final_settings["language"][
                                                                            "batch_download_download_from_file_power"],
                                                                        state='disabled',
                                                                        variable=self.batch_download_from_file_var,
                                                                        command=self.batch_download_from_file_check)
            self.batch_download_from_file_checkbutton.grid(row=0, column=0, columnspan=1, sticky=tk.W)
            self.batch_download_from_file_select_button = ttk.Button(self.batch_download_from_file_frame,
                                                                     text=self.final_settings["language"][
                                                                         "batch_download_download_from_file_path_choose"],
                                                                     state='disabled',
                                                                     command=self.batch_download_from_file_select)
            self.batch_download_from_file_select_button.grid(row=0, column=1, columnspan=1)
            self.batch_download_from_file_path = tkinter.StringVar()
            self.batch_download_from_file_frame.grid(row=0, column=2, columnspan=6, sticky=tk.W)

            self.batch_download_links_frame = tk.LabelFrame(self.batch_download_frame,
                                                            text=self.final_settings["language"]["batch_download_urls"],
                                                            foreground='gray')
            self.batch_download_links_text = tk.Text(self.batch_download_links_frame, wrap='none', foreground='gray',
                                                     height=7, width=70, state='disabled')
            self.batch_download_links_scrollbar_x = ttk.Scrollbar(self.batch_download_links_frame, orient='horizontal',
                                                                  command=self.batch_download_links_text.xview)
            self.batch_download_links_scrollbar_y = ttk.Scrollbar(self.batch_download_links_frame, orient='vertical',
                                                                  command=self.batch_download_links_text.yview)
            self.batch_download_links_scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
            self.batch_download_links_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            self.entries_list.append(self.batch_download_links_text)
            self.batch_download_links_scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
            self.batch_download_links_text.config(xscrollcommand=self.batch_download_links_scrollbar_x.set)
            self.batch_download_links_text.config(yscrollcommand=self.batch_download_links_scrollbar_y.set)
            self.batch_download_links_frame.grid(row=2, column=0, rowspan=1, columnspan=8, sticky='nw')

            self.batch_download_frame.grid(row=14, column=0, columnspan=8, sticky=tk.W)
            self.settings_frame.grid(row=1, column=0, columnspan=8, rowspan=20, sticky=tk.W + tk.N)

            # 输出
            self.output_frame = tk.LabelFrame(self.root, text=self.final_settings["language"]["download_log"])
            self.output_text = tk.Text(self.output_frame, wrap=tk.WORD, height=40, width=84)
            self.output_scrollbar = ttk.Scrollbar(self.output_frame, command=self.output_text.yview)
            self.output_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            self.entries_list.append(self.output_text)
            self.output_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            self.output_text.config(yscrollcommand=self.output_scrollbar.set)
            if str(self.final_settings['default_setting']['window_type']) == '0':
                self.output_frame.grid(row=0, column=8, rowspan=20, sticky="nsew")
            self.output_text_clean = ttk.Button(self.root, text=self.final_settings["language"]["download_log_clean"],
                                                command=lambda: self.output_text.delete('1.0', tk.END))
            if str(self.final_settings['default_setting']['window_type']) == '0':
                self.output_text_clean.grid(row=0, column=8, sticky='ne')
            # 提示栏
            self.tips_label = ttk.Label(self.root, justify=tk.LEFT,
                                        text=self.final_settings["language"]["download_hint"])
            if str(self.final_settings['default_setting']['window_type']) == '0':
                self.tips_label.grid(row=20, column=8, columnspan=8)

        ttk.Label(self.root, text='(c)hunyanjie（魂魇桀） 2024', font=(None, 12, 'bold')).grid(row=21, column=0,
                                                                                             columnspan=16)

        self.menubar = tk.Menu(self.root)
        self.root.config(menu=self.menubar)

        program_menu = tk.Menu(self.menubar, tearoff=False)
        self.menubar.add_cascade(label=self.final_settings["language"]["program"], menu=program_menu)
        program_menu.add_command(label=self.final_settings["language"]["about"], command=self.about)
        program_menu.add_separator()
        program_menu.add_command(label=self.final_settings["language"]["setting"],
                                 command=lambda: [self.settings(), self.settings_window.lift()])
        program_menu.add_separator()
        program_menu.add_checkbutton(label=self.final_settings["language"]["top_window"], command=lambda: [
            self.root.attributes('-topmost', not self.root.attributes('-topmost'))])

        you_get_menu = tk.Menu(self.menubar, tearoff=False)
        self.menubar.add_cascade(label=self.final_settings["language"]["about_you_get"], menu=you_get_menu)
        you_get_menu.add_command(label=self.final_settings["language"]["install_update_you_get"],
                                 command=self.install_you_get)
        you_get_menu.add_command(label=self.final_settings["language"]["show_you_get_version"],
                                 command=self.check_you_get_version)

        if str(self.final_settings['default_setting']['window_type']) == '2':
            windows_menu = tk.Menu(self.menubar, tearoff=False)
            self.menubar.add_cascade(label=self.final_settings["language"]["windows"], menu=windows_menu)
            windows_menu.add_command(label=self.final_settings["language"]["download_settings_window"],
                                     command=lambda: [self.download_settings_window.deiconify(),
                                                      self.download_settings_window.lift()])
            windows_menu.add_command(label=self.final_settings["language"]["download_log_window"],
                                     command=lambda: [self.download_log_window.deiconify(),
                                                      self.download_log_window.lift()])

        help_menu = tk.Menu(self.menubar, tearoff=False)
        self.menubar.add_cascade(label=self.final_settings["language"]["help"], menu=help_menu)
        help_menu.add_command(label=self.final_settings["language"]["function_introduction"],
                              command=lambda: webbrowser.open(
                                  'https://github.com/hunyanjie/You-Get-Gui/wiki/%E6%8C%87%E5%8D%97-info#%E5%8A%9F%E8%83%BD%E4%BB%8B%E7%BB%8D',
                                  new=0))
        help_menu.add_command(label=self.final_settings["language"]["issues"],
                              command=lambda: webbrowser.open('https://github.com/hunyanjie/You-Get-Gui/issues', new=0))
        help_menu.add_separator()
        help_menu.add_command(label=self.final_settings["language"]["cannot_download_bilibili_video"],
                              command=lambda: webbrowser.open(
                                  'https://github.com/hunyanjie/You-Get-Gui/wiki/%E6%8C%87%E5%8D%97-info#2b%E7%AB%99%E8%A7%86%E9%A2%91%E6%97%A0%E6%B3%95%E4%B8%8B%E8%BD%BD',
                                  new=0))
        help_menu.add_command(label=self.final_settings["language"]["can_find_video_but_cannot_download"],
                              command=lambda: webbrowser.open(
                                  'https://github.com/hunyanjie/You-Get-Gui/wiki/%E6%8C%87%E5%8D%97-info#1%E5%8F%AF%E4%BB%A5%E6%B5%8F%E8%A7%88%E8%A7%86%E9%A2%91%E4%BF%A1%E6%81%AF%E4%BD%86%E6%97%A0%E6%B3%95%E4%B8%8B%E8%BD%BD',
                                  new=0))

        self.exit_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_command(label=self.final_settings["language"]["exit"], command=self.exit_program)

        # 为所有可输入的控件添加右键菜单
        self.right_click_menu()

        self.check_define(step=1)

    def right_click_menu(self):
        for widget in self.entries_list:
            right_click_menu = tk.Menu(widget, tearoff=0)
            right_click_menu.add_command(label=self.final_settings["language"]["copy"],
                                         command=lambda w=widget: self.copy(w))
            right_click_menu.add_command(label=self.final_settings["language"]["cut"],
                                         command=lambda w=widget: self.cut(w))
            right_click_menu.add_command(label=self.final_settings["language"]["paste"],
                                         command=lambda w=widget: self.paste(w))
            right_click_menu.add_separator()
            right_click_menu.add_command(label=self.final_settings["language"]["select_all"],
                                         command=lambda w=widget: self.select_all(w))

            widget.bind("<Button-3>", lambda event, w=widget, m=right_click_menu: self.show_context_menu(event, w, m))

    def show_context_menu(self, event, widget, right_click_menu):
        print('[DEBUG] event.widget:', event.widget, '\t|\twidget.focus_get():', widget.focus_get())
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
            print('[DEBUG] Copy:', widget.selection_get())
            widget.clipboard_clear()
            widget.clipboard_append(widget.selection_get())
        except Exception:
            pass

    def cut(self, widget):
        try:
            print('[DEBUG] Cut:', widget.selection_get())
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
                print('[DEBUG] Paste:', widget.clipboard_get())
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
                        print('[WARN] Please enter the itag number!!!')
                        self.status_label.config(text=self.final_settings["language"]["status_hint_cannot_find_itag"],
                                                 foreground='red')
                        return
            if self.download_format_var.get():
                if ' --json' not in cmd or ' --info' not in cmd:
                    if self.download_format_entry.get() != "":
                        cmd += f' --format={self.download_format_entry.get()}'
                    else:
                        print('[WARN] Please enter the format number!!!')
                        self.status_label.config(text=self.final_settings["language"]["status_hint_cannot_find_format"],
                                                 foreground='red')
                        return
            if not self.download_captions_var.get():
                cmd += ' --no-caption'
            if not self.merge_video_parts_var.get():
                cmd += ' --no-merge'
            if self.download_m3u8_video_var.get():
                cmd += ' --m3u8'
            if self.ignore_ssl_errors_var.get():
                cmd += ' --insecure'
            if self.forced_download_var.get():
                cmd += ' --force'
            if self.skip_downloaded_video_var.get():
                cmd += ' --skip-existing-file-size-check'
            if self.auto_rename_var.get():
                cmd += ' --auto-rename'
            if self.download_all_var.get():
                cmd += ' --playlist'
                if self.download_all_page_entry.get() != '':
                    if self.download_all_page_entry.get().isdigit():
                        cmd += f' --page-size {self.download_all_page_entry.get()}'
                    else:
                        print('[WARN] Please fill in a non-negative integer!!!')
                        self.status_label.config(
                            text=self.final_settings["language"]["status_hint_list_page_not_digit"], foreground='red')
                        return
                if self.download_all_start_entry.get() != '':
                    if self.download_all_start_entry.get().isdigit():
                        cmd += f' --first {self.download_all_start_entry.get()}'
                    else:
                        print('[WARN] Please fill in a non-negative integer!!!')
                        self.status_label.config(
                            text=self.final_settings["language"]["status_hint_list_start_not_digit"], foreground='red')
                        return
                if self.download_all_end_entry.get() != '':
                    if self.download_all_end_entry.get().isdigit():
                        cmd += f' --last {self.download_all_end_entry.get()}'
                    else:
                        print('[WARN] Please fill in a non-negative integer!!!')
                        self.status_label.config(text=self.final_settings["language"]["status_hint_list_end_not_digit"],
                                                 foreground='red')
                        return
        if self.debug_var.get():
            cmd += ' --debug'
        if self.use_cookies_var.get():
            if self.use_cookies_entry.get() != '':
                cmd += f' --cookies "{self.use_cookies_entry.get()}"'
            else:
                print('[WARN] Please fill in the Cookies path!!!')
                self.status_label.config(text=self.final_settings["language"]["status_hint_cannot_find_cookies_file"],
                                         foreground='red')
                return
        if self.download_video_password_var.get():
            if self.download_video_password_entry.get() != '':
                cmd += f' --password "{self.download_video_password_entry.get()}"'
            else:
                print('[WARN] Please enter the video password!!!')
                self.status_label.config(text=self.final_settings["language"]["status_hint_cannot_find_video_password"],
                                         foreground='red')
                return
        if self.no_proxy_var.get():
            cmd += ' --no-proxy'
        else:
            if self.proxy_setting_var.get():
                if self.proxy_path_entry.get() != '':
                    print('[DEBUG] Proxy type:', self.proxy_type_var.get())
                    if self.proxy_type_var.get() == 'Socks5':
                        if self.proxy_login_var.get():
                            if self.proxy_user_name_entry.get() != '' and self.proxy_password_entry.get() != '':
                                cmd += (f' --socks-proxy {self.proxy_user_name_entry.get()}:'
                                        f'{self.proxy_password_entry.get()}@{self.proxy_path_entry.get()}')
                            else:
                                print('[WARN] Please enter the login username and password of the agent host!!!')
                                self.status_label.config(text=self.final_settings["language"][
                                    "status_hint_cannot_find_proxy_user_and_passwd"], foreground='red')
                                return
                        else:
                            cmd += f' --socks-proxy {self.proxy_path_entry.get()}'
                    else:
                        if self.proxy_extracting_only_var.get():
                            cmd += f' --extractor-proxy {self.proxy_path_entry.get()}'
                        else:
                            cmd += f' --http-proxy {self.proxy_path_entry.get()}'
                else:
                    print('[WARN] Please enter the proxy host address and port number!!!')
                    self.status_label.config(
                        text=self.final_settings["language"]["status_hint_cannot_find_proxy_host_port"],
                        foreground='red')
                    return
            if self.proxy_time_out_var.get():
                if self.proxy_time_out_entry.get() != '':
                    cmd += f' --timeout {self.proxy_time_out_entry.get()}'
                else:
                    print('[WARN] Please enter a proxy timeout period!!!')
                    self.status_label.config(
                        text=self.final_settings["language"]["status_hint_cannot_find_timeout_time"], foreground='red')
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
                # 检测文件链接是否存在
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
                                print('[INFO] Total download:', line_numbers)
                                for line in file:
                                    if line.strip() != '':
                                        line_number += 1
                                        print(f'[INFO] Now download:{line_number}/{line_numbers}')
                                        cmd_tmp = self.new_name_change(cmd, (line_numbers, line_number))
                                        self.downloading(f'{cmd_tmp} "{line.strip()}"')
                        except FileNotFoundError:
                            print('[WARN] File does not exist!!!')
                            self.status_label.config(
                                text=self.final_settings["language"]["status_hint_cannot_find_file"], foreground='red')
                            return
                    else:
                        cmd_tmp = self.new_name_change(cmd, (1, 1), False)
                        self.downloading(f'{cmd_tmp} --input-file "{self.url_entry.get()}"')
                else:
                    print('[WARN] Please enter the download URL collection file address!!!')
                    self.status_label.config(
                        text=self.final_settings["language"]["status_hint_cannot_find_url_collection_file"],
                        foreground='red')
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
                        print('[INFO] Total download:', line_numbers)
                        for line in text.split('\n'):
                            if line.strip() != '':
                                line_number += 1
                                print(f'[INFO] Now download:{line_number}/{line_numbers}')
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
                    print('[WARN] Please enter the download URL or file path!!!')
                    self.status_label.config(
                        text=self.final_settings["language"]["status_hint_cannot_find_download_path"], foreground='red')
                    return
        else:
            if self.url_entry.get() == '':
                print('[WARN] Please enter the download URL!!!')
                self.status_label.config(text=self.final_settings["language"]["status_hint_cannot_find_download_url"],
                                         foreground='red')
                return
            else:
                cmd += f' "{self.url_entry.get()}"'
                cmd_tmp = self.new_name_change(cmd, (1, 1), False)
                self.downloading(cmd_tmp)

    def downloading(self, cmd):
        print('[INDO] Starting......')
        self.status_label.config(text=self.final_settings["language"]["status_hint_lunched"], foreground='blue')
        if self.new_window_var.get():
            cmd = 'start cmd /k ' + cmd
            print('[INFO] Input:\n', cmd)
            output_info = f'{self.final_settings["language"]["log_input"]}\n{cmd}\n'
            self.output_text.insert(tk.END, output_info)
            self.output_text.see('end-1c')
            subprocess.Popen(cmd, shell=True)
        else:
            threading.Thread(target=self.single_threaded_download, args=(cmd,)).start()

    def single_threaded_download(self, cmd):
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        out, error = process.communicate()
        out = out.decode('utf-8')
        error = error.decode('utf-8')
        print('[INFO] Output:\n', out)
        print('[INFO] Error:\n', error)
        output_info = f'{self.final_settings["language"]["log_input"]}\n{cmd}\n{self.final_settings["language"]["log_output"]}\n{out}\n{self.final_settings["language"]["log_error"]}\n{error}\n-------------------------------------\n'
        self.output_text.insert(tk.END, output_info)
        self.output_text.see('end-1c')

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
            print(f'[DEBUG]Replace keys:', keys)
            for date_key in date_keys:
                keys["{" + date_key.replace("%", "") + "}"] = time.strftime(date_key, time.localtime())
            for key, var in keys.items():
                new_name_data = new_name_data.replace(key, str(var))
            cmd += f' --output-filename "{new_name_data}"'
        return cmd

    def clean_url_entry(self):
        if self.batch_download_power_var.get() is False and self.batch_download_from_file_checkbutton.cget("state") != 'normal':
            self.url_label.config(text=self.final_settings["language"]["url"])
        self.url_entry.delete(0, tk.END)

    def select_path(self):
        path = tk.filedialog.askdirectory()
        print('[DEBUG] Save Path:', path)
        if path != '':
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, path)

    def more_info(self):
        if self.print_info_as_json_var.get():
            cmd = f'you-get --json'
        else:
            cmd = f'you-get --info'
        print('[INFO]', cmd)
        self.lunch_download(cmd, False)

    def real_link(self):
        cmd = f'you-get --url'
        if self.download_itag_var.get():
            if self.download_itag_entry.get() != "":
                cmd += f' --itag={self.download_itag_entry.get()}'
            else:
                print('[WARN] Please enter the itag number!!!')
                self.status_label.config(text=self.final_settings["language"]["status_hint_cannot_find_itag"],
                                         foreground='red')
                return
        if self.download_format_var.get():
            if self.download_format_entry.get() != "":
                cmd += f' --format={self.download_format_entry.get()}'
            else:
                print('[WARN] Please enter the format number!!!')
                self.status_label.config(text=self.final_settings["language"]["status_hint_cannot_find_format"],
                                         foreground='red')
                return
        print('[INFO]', cmd)
        self.lunch_download(cmd, False)

    def no_proxy_button_check(self):
        if self.no_proxy_var.get():
            self.proxy_setting_checkbutton.config(style='gray.TCheckbutton', state='disabled')
            self.proxy_extracting_only_checkbutton.config(state='disabled')
            self.proxy_type_socks5_radiobutton.config(state='disabled')
            self.proxy_type_http_radiobutton.config(state='disabled')
            self.proxy_path_label.config(foreground='gray')
            self.proxy_path_entry.config(state='disabled')
            self.proxy_login_frame.config(foreground='gray')
            self.proxy_login_checkbutton.config(state='disabled')
            self.proxy_user_name_label.config(foreground='gray')
            self.proxy_user_name_entry.config(state='disabled')
            self.proxy_password_label.config(foreground='gray')
            self.proxy_password_entry.config(state='disabled')
            self.proxy_time_out_checkbutton.config(state='disabled')
            self.proxy_time_out_entry.config(state='disabled')
            self.proxy_time_out_label.config(foreground='gray')
        else:
            self.proxy_setting_checkbutton.config(style='TCheckbutton', state='normal')
            if self.proxy_setting_var.get():
                self.proxy_type_socks5_radiobutton.config(state='normal')
                self.proxy_type_http_radiobutton.config(state='normal')
                self.proxy_path_label.config(foreground='black')
                self.proxy_path_entry.config(state='normal')
                if self.proxy_type_var.get() == 'Socks5':
                    self.proxy_extracting_only_checkbutton.config(state='disabled')
                    self.proxy_login_frame.config(foreground='black')
                    self.proxy_login_checkbutton.config(state='normal')
                    if self.proxy_login_var.get():
                        self.proxy_user_name_label.config(foreground='black')
                        self.proxy_user_name_entry.config(state='normal')
                        self.proxy_password_label.config(foreground='black')
                        self.proxy_password_entry.config(state='normal')
                    else:
                        self.proxy_user_name_label.config(foreground='gray')
                        self.proxy_user_name_entry.config(state='disabled')
                        self.proxy_password_label.config(foreground='gray')
                        self.proxy_password_entry.config(state='disabled')
                elif self.proxy_type_var.get() == 'Http':
                    self.proxy_extracting_only_checkbutton.config(state='normal')
                    self.proxy_login_frame.config(foreground='gray')
                    self.proxy_login_checkbutton.config(state='disabled')
                    self.proxy_user_name_label.config(foreground='gray')
                    self.proxy_user_name_entry.config(state='disabled')
                    self.proxy_password_label.config(foreground='gray')
                    self.proxy_password_entry.config(state='disabled')
            else:
                self.proxy_extracting_only_checkbutton.config(state='disabled')
                self.proxy_type_socks5_radiobutton.config(state='disabled')
                self.proxy_type_http_radiobutton.config(state='disabled')
                self.proxy_path_label.config(foreground='gray')
                self.proxy_path_entry.config(state='disabled')
                self.proxy_login_frame.config(foreground='gray')
                self.proxy_login_checkbutton.config(state='disabled')
                self.proxy_user_name_label.config(foreground='gray')
                self.proxy_user_name_entry.config(state='disabled')
                self.proxy_password_label.config(foreground='gray')
                self.proxy_password_entry.config(state='disabled')
            self.proxy_time_out_checkbutton.config(state='normal')
            if self.proxy_time_out_var.get():
                self.proxy_time_out_entry.config(state='normal')
                self.proxy_time_out_label.config(foreground='black')

    def proxy_setting_button_check(self):
        if self.proxy_setting_var.get():
            self.proxy_type_socks5_radiobutton.config(state='normal')
            self.proxy_type_http_radiobutton.config(state='normal')
            self.proxy_path_label.config(foreground='black')
            self.proxy_path_entry.config(state='normal')
            if self.proxy_type_var.get() == 'Socks5':
                self.proxy_extracting_only_checkbutton.config(state='disabled')
                self.proxy_login_frame.config(foreground='black')
                self.proxy_login_checkbutton.config(state='normal')
                if self.proxy_login_var.get():
                    self.proxy_user_name_label.config(foreground='black')
                    self.proxy_user_name_entry.config(state='normal')
                    self.proxy_password_label.config(foreground='black')
                    self.proxy_password_entry.config(state='normal')
                else:
                    self.proxy_user_name_label.config(foreground='gray')
                    self.proxy_user_name_entry.config(state='disabled')
                    self.proxy_password_label.config(foreground='gray')
                    self.proxy_password_entry.config(state='disabled')
            elif self.proxy_type_var.get() == 'Http':
                self.proxy_extracting_only_checkbutton.config(state='normal')
                self.proxy_login_frame.config(foreground='gray')
                self.proxy_login_checkbutton.config(state='disabled')
                self.proxy_user_name_label.config(foreground='gray')
                self.proxy_user_name_entry.config(state='disabled')
                self.proxy_password_label.config(foreground='gray')
                self.proxy_password_entry.config(state='disabled')
        else:
            self.proxy_extracting_only_checkbutton.config(state='disabled')
            self.proxy_path_label.config(foreground='gray')
            self.proxy_path_entry.config(state='disabled')
            self.proxy_login_frame.config(foreground='gray')
            self.proxy_login_checkbutton.config(state='disabled')
            self.proxy_user_name_label.config(foreground='gray')
            self.proxy_user_name_entry.config(state='disabled')
            self.proxy_password_label.config(foreground='gray')
            self.proxy_password_entry.config(state='disabled')
            self.proxy_type_socks5_radiobutton.config(state='disabled')
            self.proxy_type_http_radiobutton.config(state='disabled')

    def proxy_type_button_check(self):
        if self.proxy_type_var.get() == 'Socks5':
            self.proxy_extracting_only_checkbutton.config(state='disabled')
            self.proxy_login_frame.config(foreground='black')
            self.proxy_login_checkbutton.config(state='normal')
            if self.proxy_login_var.get():
                self.proxy_user_name_label.config(foreground='black')
                self.proxy_user_name_entry.config(state='normal')
                self.proxy_password_label.config(foreground='black')
                self.proxy_password_entry.config(state='normal')
            else:
                self.proxy_user_name_label.config(foreground='gray')
                self.proxy_user_name_entry.config(state='disabled')
                self.proxy_password_label.config(foreground='gray')
                self.proxy_password_entry.config(state='disabled')
        elif self.proxy_type_var.get() == 'Http':
            self.proxy_extracting_only_checkbutton.config(state='normal')
            self.proxy_login_frame.config(foreground='gray')
            self.proxy_login_checkbutton.config(state='disabled')
            self.proxy_user_name_label.config(foreground='gray')
            self.proxy_user_name_entry.config(state='disabled')
            self.proxy_password_label.config(foreground='gray')
            self.proxy_password_entry.config(state='disabled')

    def proxy_login_button_check(self):
        if self.proxy_login_var.get():
            self.proxy_user_name_label.config(foreground='black')
            self.proxy_user_name_entry.config(state='normal')
            self.proxy_password_label.config(foreground='black')
            self.proxy_password_entry.config(state='normal')
        else:
            self.proxy_user_name_label.config(foreground='gray')
            self.proxy_user_name_entry.config(state='disabled')
            self.proxy_password_label.config(foreground='gray')
            self.proxy_password_entry.config(state='disabled')

    def select_player_file(self):
        path = tk.filedialog.askopenfilename(filetypes=[(self.final_settings["language"]["player_exe_file"], ['*.exe']),
                                                        (self.final_settings["language"]["all_type_file"], '.*')])
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
                self.status_label.config(text=self.final_settings["language"]["status_hint_cannot_find_player_path"],
                                         foreground='red')
                return
        else:
            print('[WARN]The video file path is not entered!!!')
            self.status_label.config(text=self.final_settings["language"]["status_hint_cannot_find_video_file"],
                                     foreground='red')
            return
        print('[INFO]', cmd)
        self.lunch_download(cmd, download=False, play=True)

    def select_cookies_file(self):
        path = tk.filedialog.askopenfilename(
            filetypes=[(self.final_settings["language"]["cookies_file"], ['*.txt', '*.sqlite']),
                       (self.final_settings["language"]["all_type_file"], '.*')])
        if path != '':
            self.use_cookies_entry.delete(0, tk.END)
            self.use_cookies_entry.insert(0, path)

    def new_window_var_update(self):
        self.new_window_var_old = self.new_window_var.get()

    def batch_download_power(self, step=0):
        if self.batch_download_power_var.get():
            self.batch_download_parallel_checkbutton.config(state='normal')
            self.batch_download_from_file_checkbutton.config(state='normal')
            self.batch_download_parallel(step=step)
            if self.batch_download_from_file_var.get():
                self.url_entry_hint.config(text='')
                self.url_label.config(text=self.final_settings["language"]["file_path"], foreground='black')
                self.url_entry.config(state='normal', textvariable=self.batch_download_file_path)
                self.batch_download_from_file_select_button.config(state='normal')
            else:
                self.url_entry_hint.config(text=self.final_settings["language"]["batch_download_urls_hint"])
                self.url_label.config(text=self.final_settings["language"]["url"], foreground='gray')
                self.url_entry.config(state='disabled', textvariable=self.url_path)
                self.batch_download_links_frame.config(foreground='black')
                self.batch_download_links_text.config(foreground='black', state='normal')
        else:
            self.url_entry_hint.config(text='')
            self.url_label.config(text=self.final_settings["language"]["url"], foreground='black')
            self.url_entry.config(state='normal', textvariable=self.url_path)
            self.batch_download_from_file_checkbutton.config(state='disabled')
            self.batch_download_from_file_select_button.config(state='disabled')
            self.batch_download_parallel_checkbutton.config(state='disabled')
            self.batch_download_parallel()
            self.batch_download_links_frame.config(foreground='gray')
            self.batch_download_links_text.config(foreground='gray', state='disabled')

    def batch_download_from_file_check(self):
        if self.batch_download_from_file_var.get():
            self.url_entry_hint.config(text='')
            self.url_label.config(text=self.final_settings["language"]["file_path"], foreground='black')
            self.url_entry.config(state='normal', textvariable=self.batch_download_file_path)
            self.batch_download_from_file_select_button.config(state='normal')
            self.batch_download_links_frame.config(foreground='gray')
            self.batch_download_links_text.config(foreground='gray', state='disabled')
        else:
            self.url_entry_hint.config(text=self.final_settings["language"]["batch_download_urls_hint"])
            self.url_label.config(text=self.final_settings["language"]["url"], foreground='gray')
            self.url_entry.config(state='disabled', textvariable=self.url_path)
            self.batch_download_from_file_select_button.config(state='disabled')
            self.batch_download_links_frame.config(foreground='black')
            self.batch_download_links_text.config(foreground='black', state='normal')

    def batch_download_parallel(self, step=0):
        if self.batch_download_parallel_var.get() and self.batch_download_power_var.get():
            if step == 0:
                self.new_window_var_old = self.new_window_var.get()
            self.new_window_var.set(True)
            self.new_window_checkbutton.config(style='gray.TCheckbutton', state='disabled')
        else:
            self.new_window_var.set(self.new_window_var_old)
            self.new_window_checkbutton.config(style='TCheckbutton', state='normal')

    def batch_download_from_file_select(self):
        path = tk.filedialog.askopenfilename(
            filetypes=[(self.final_settings["language"]["urls_collection_file"], ['*.txt']),
                       (self.final_settings["language"]["all_type_file"], '.*')])
        if path != '':
            self.url_entry_hint.config(text='')
            self.url_entry.delete(0, tk.END)
            self.url_entry.insert(0, path)
        else:
            self.url_entry_hint.config(text=self.final_settings["language"]["batch_download_urls_hint"])

    def about(self):
        def about_page_check_upgrade():
            try:
                import urllib.request
                response = urllib.request.urlopen('https://hunyanjie.github.io/file/project/You-Get-GUI/update.txt')
                content = response.read().decode('utf-8')
                print('[DEBUG] version info get:\n', content)
            except Exception:
                new_version_show.config(text=self.final_settings["language"]["fail_to_get_upgrade"])
                return

            show = content.split("\n")
            if float(self.__version__) >= float(re.search(r'v(\d+\.\d+)', show[0]).group(1)):
                new_version_show.config(text=self.final_settings["language"]["already_new_version"], foreground='green')
            else:
                if float(re.search(r'v(\d+\.\d+)', show[0]).group(1)) - float(self.__version__) >= 1:
                    new_version_show.config(text=self.final_settings["language"]["old_version"], foreground='red')
                else:
                    new_version_show.config(text=self.final_settings["language"]["find_new_version"], foreground='orange')

        about_page = tk.Toplevel()
        about_page.title(f'{self.final_settings["language"]["about"]} You-Get GUI v{self.__version__}')
        ttk.Label(about_page, text=self.final_settings["language"]["about"] + ' v' + self.__version__,
                  font=(None, 25, 'bold')).pack()
        ttk.Label(about_page, text='').pack()
        ttk.Label(about_page, text=self.final_settings["language"]["about_window_hint_title"],
                  font=(None, 18, 'bold')).pack()
        ttk.Label(about_page, justify=tk.LEFT,
                  text=self.final_settings["language"]["about_window_hint"]).pack()
        ttk.Label(about_page, text='').pack()
        ttk.Label(about_page, text=self.final_settings["language"]["upgrade"], font=(None, 18, 'bold')).pack()
        new_version_show = ttk.Label(about_page, text=self.final_settings["language"]["checking_upgrade"])
        new_version_show.pack()
        threading.Thread(target=about_page_check_upgrade, args=()).start()
        ttk.Button(about_page, text=self.final_settings["language"]["check_upgrade"], command=self.upgrade_program,
                   width=30).pack()
        ttk.Label(about_page, text='').pack()
        ttk.Label(about_page, text=self.final_settings["language"]["copyright"], font=(None, 18, 'bold')).pack()
        ttk.Label(about_page, text='(c)hunyanjie（魂魇桀） 2024').pack()
        ttk.Label(about_page, text='').pack()
        ttk.Label(about_page, text='声明 / Statement', font=(None, 18, 'bold')).pack()
        ttk.Label(about_page, text="如果您使用本程序，则默认视为您同意我们的【免责声明】和【隐私政策】。\nIf you use this program, you are deemed to have agreed to our Disclaimer and Privacy Policy.\n【免责声明】和【隐私政策】可以在本项目的Github主页查看\n[Disclaimer] and [Privacy Policy] can be viewed on the project's Github home page\n").pack()
        ttk.Label(about_page, text=self.final_settings["language"]["link"], font=(None, 18, 'bold')).pack()
        link_frame = ttk.Frame(about_page)
        ttk.Label(link_frame, text='GitHub').grid(row=0, column=0)
        project_page_link_show = ttk.Entry(link_frame, width=40)
        project_page_link_show.grid(row=0, column=1)
        project_page_link_show.delete(0, tk.END)
        project_page_link_show.insert(tk.END, 'https://github.com/hunyanjie/You-Get-Gui')
        project_page_link_show.config(state='readonly')
        url = ttk.Button(link_frame, text=self.final_settings["language"]["click_to_jump"],
                         command=lambda: webbrowser.open('https://github.com/hunyanjie/You-Get-Gui', new=0))
        url.grid(row=0, column=2)
        wiki = ttk.Button(link_frame, text=self.final_settings["language"]["wiki"],
                          command=lambda: webbrowser.open('https://github.com/hunyanjie/You-Get-Gui/wiki', new=0))
        wiki.grid(row=0, column=3)
        link_frame.pack()

    def upgrade_program(self):
        def upgrade_check():
            try:
                import urllib.request
                response = urllib.request.urlopen('https://hunyanjie.github.io/file/project/You-Get-GUI/update.txt')
                content = response.read().decode('utf-8')
                print('[DEBUG] version info get:\n', content)
            except Exception as error_type:
                check_hint.config(
                    text=f'{self.final_settings["language"]["fail_to_check_upgrade"]}\n{self.final_settings["language"]["reason"]}{error_type}',
                    foreground='orange')
                cloud_version.config(text='云端版本：获取失败！')
                upgrade_log_text.config(state='normal')
                upgrade_log_text.delete('1.0', tk.END)
                upgrade_log_text.insert(tk.END, self.final_settings["language"]["fail_to_get_upgrade"])
                upgrade_log_text.config(state='disabled')
                upgrade_button.config(state='disabled')
                return

            show = content.split("\n")
            if float(self.__version__) >= float(re.search(r'v(\d+\.\d+)', show[0]).group(1)):
                check_hint.config(text=self.final_settings["language"]["already_new_version"], foreground='green')
                cloud_version.config(text=f'{self.final_settings["language"]["cloud_version"]}: {show[0]}')
                upgrade_log_text.config(state='normal')
                upgrade_log_text.delete('1.0', tk.END)
                upgrade_log_text.insert(tk.END, '\n'.join(show[0:]))
                upgrade_log_text.config(state='disabled')
                upgrade_button.config(state='normal', command=lambda: open_upgrade_page(
                    float(re.search(r'v(\d+\.\d+)', show[0]).group(1))))
            else:
                if float(re.search(r'v(\d+\.\d+)', show[0]).group(1)) - float(self.__version__) >= 1:
                    check_hint.config(text=self.final_settings["language"]["old_version"], foreground='red')
                else:
                    check_hint.config(text=self.final_settings["language"]["find_new_version"], foreground='orange')
                cloud_version.config(text=f'{self.final_settings["language"]["cloud_version"]}: {show[0]}')
                upgrade_log_text.config(state='normal')
                upgrade_log_text.delete('1.0', tk.END)
                upgrade_log_text.insert(tk.END, '\n'.join(show[0:]))
                upgrade_log_text.config(state='disabled')
                upgrade_button.config(state='normal', command=lambda: open_upgrade_page(
                    float(re.search(r'v(\d+\.\d+)', show[0]).group(1))))

        def open_upgrade_page(ver):
            webbrowser.open(f'https://github.com/hunyanjie/You-Get-Gui/releases/tag/v{ver}')

        upgrade_window = tk.Toplevel()
        upgrade_window.title(self.final_settings["language"]["check_upgrade"])

        check_hint = ttk.Label(upgrade_window, text=self.final_settings["language"]["checking_upgrade"],
                               font=(None, 16, 'bold'))
        check_hint.grid(row=0, columnspan=2)
        local_version = ttk.Label(upgrade_window,
                                 text=f'{self.final_settings["language"]["current_version"]}: v{self.__version__}')
        local_version.grid(row=1, columnspan=1, sticky='w')
        cloud_version = ttk.Label(upgrade_window,
                                  text=f'{self.final_settings["language"]["cloud_version"]}: {self.final_settings["language"]["getting_version_info"]}')
        cloud_version.grid(row=2, columnspan=1, sticky='w')
        upgrade_log = tk.LabelFrame(upgrade_window, text=self.final_settings["language"]["upgrade_log"])
        upgrade_log_text = tk.Text(upgrade_log, wrap='none', exportselection=True, state='disabled',
                                   height=20, width=60)
        upgrade_log_scrollbar_x = ttk.Scrollbar(upgrade_log,
                                                orient='horizontal',
                                                command=upgrade_log_text.xview)
        upgrade_log_scrollbar_y = ttk.Scrollbar(upgrade_log, orient='vertical',
                                                command=upgrade_log_text.yview)
        upgrade_log_scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        upgrade_log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        upgrade_log_scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        upgrade_log_text.config(xscrollcommand=upgrade_log_scrollbar_x.set)
        upgrade_log_text.config(yscrollcommand=upgrade_log_scrollbar_y.set)
        upgrade_log.grid(row=3, column=0, rowspan=1, columnspan=8, sticky='nw')
        upgrade_log_text.insert(tk.END, self.final_settings["language"]["getting_version_info"])

        upgrade_button = ttk.Button(upgrade_window,
                                    text=self.final_settings["language"]["open_download_new_version_page"],
                                    state='disabled', width=15)
        upgrade_button.grid(row=4, column=0)
        threading.Thread(target=upgrade_check, args=()).start()
        recheck_upgrade_button = ttk.Button(upgrade_window, text=self.final_settings["language"]["check_upgrade"],
                                            state='normal', width=15, command=lambda: [
                check_hint.config(text='检查更新中...', font=(None, 16, 'bold'), foreground='black'),
                threading.Thread(target=upgrade_check, args=()).start()])
        recheck_upgrade_button.grid(row=4, column=1)

    def settings(self):
        # 确保每次调用settings时，都重新读取配置文件，并且确保多次调用时如果窗体已经存在，则直接激活窗体，否则重新创建窗体
        self.settings_window = tk.Toplevel()
        self.settings_window.title(f'You-Get GUI {self.final_settings["language"]["setting"]}')
        self.auto_save_download_settings = []
        self.is_change_settings = False
        self.need_to_restart = False
        self.new_settings = {"auto_save_download_setting": {}}
        self.old_settings = {}
        for key, value in self.final_settings.items():
            self.old_settings[key] = value

        def settings_set(input_settings):
            self.program_language_combobox.current(next((index for index, lang in enumerate(
                [f"{k} / {v['show_name']}" for k, v in self.final_settings['languages'].items()]) if lang.startswith(
                self.final_settings['default_setting']['language'] + ' / ')), None))
            self.program_style_combobox.current(int(input_settings["default_setting"]["window_type"]))
            self.show_change_name_format_var.set(input_settings["default_setting"]["show_change_name_format"])
            self.exit_with_hint_var.set(input_settings["default_setting"]["exit_with_hint"])
            self.show_hover_tip_var.set(input_settings["default_setting"]["show_hover_tip"])

            self.auto_save_download_setting_power_var.set(
                input_settings["default_setting"]["auto_save_download_setting"]["power"])
            self.auto_save_download_setting_url_var.set(
                input_settings["default_setting"]["auto_save_download_setting"]["url"])
            self.auto_save_download_setting_save_path_var.set(
                input_settings["default_setting"]["auto_save_download_setting"]["save_path"])
            self.auto_save_download_setting_save_name_var.set(
                input_settings["default_setting"]["auto_save_download_setting"]["save_name"])
            self.auto_save_download_setting_print_with_json_var.set(
                input_settings["default_setting"]["auto_save_download_setting"]["print_with_json"])
            self.auto_save_download_setting_download_captions_var.set(
                input_settings["default_setting"]["auto_save_download_setting"]["download_captions"])
            self.auto_save_download_setting_merge_video_parts_var.set(
                input_settings["default_setting"]["auto_save_download_setting"]["merge_video_parts"])
            self.auto_save_download_setting_download_m3u8_video_var.set(
                input_settings["default_setting"]["auto_save_download_setting"]["download_m3u8_video"])
            self.auto_save_download_setting_ignore_ssl_errors_var.set(
                input_settings["default_setting"]["auto_save_download_setting"]["ignore_ssl_errors"])
            self.auto_save_download_setting_forced_download_var.set(
                input_settings["default_setting"]["auto_save_download_setting"]["forced_download"])
            self.auto_save_download_setting_skip_downloaded_video_var.set(
                input_settings["default_setting"]["auto_save_download_setting"]["skip_downloaded_video"])
            self.auto_save_download_setting_auto_rename_var.set(
                input_settings["default_setting"]["auto_save_download_setting"]["auto_rename"])
            self.auto_save_download_setting_download_video_password_power_var.set(
                input_settings["default_setting"]["auto_save_download_setting"]["download_video_password_power"])
            self.auto_save_download_setting_download_video_password_value_var.set(
                input_settings["default_setting"]["auto_save_download_setting"]["download_video_password_value"])
            self.auto_save_download_setting_download_format_power_var.set(
                input_settings["default_setting"]["auto_save_download_setting"]["download_format_power"])
            self.auto_save_download_setting_download_format_value_var.set(
                input_settings["default_setting"]["auto_save_download_setting"]["download_format_value"])
            self.auto_save_download_setting_download_itag_power_var.set(
                input_settings["default_setting"]["auto_save_download_setting"]["download_itag_power"])
            self.auto_save_download_setting_download_itag_value_var.set(
                input_settings["default_setting"]["auto_save_download_setting"]["download_itag_value"])
            self.auto_save_download_setting_download_list_power_var.set(
                input_settings["default_setting"]["auto_save_download_setting"]["download_list_power"])
            self.auto_save_download_setting_download_list_page_var.set(
                input_settings["default_setting"]["auto_save_download_setting"]["download_list_page"])
            self.auto_save_download_setting_download_list_start_var.set(
                input_settings["default_setting"]["auto_save_download_setting"]["download_list_start"])
            self.auto_save_download_setting_download_list_end_var.set(
                input_settings["default_setting"]["auto_save_download_setting"]["download_list_end"])
            self.auto_save_download_setting_run_in_new_window_var.set(
                input_settings["default_setting"]["auto_save_download_setting"]["run_in_new_window"])
            self.auto_save_download_setting_debug_var.set(
                input_settings["default_setting"]["auto_save_download_setting"]["debug"])
            self.auto_save_download_setting_use_cookies_power_var.set(
                input_settings["default_setting"]["auto_save_download_setting"]["use_cookies_power"])
            self.auto_save_download_setting_use_cookies_path_var.set(
                input_settings["default_setting"]["auto_save_download_setting"]["use_cookies_path"])
            self.auto_save_download_setting_player_power_var.set(
                input_settings["default_setting"]["auto_save_download_setting"]["player_power"])
            self.auto_save_download_setting_player_path_var.set(
                input_settings["default_setting"]["auto_save_download_setting"]["player_path"])
            self.auto_save_download_setting_player_argument_var.set(
                input_settings["default_setting"]["auto_save_download_setting"]["player_argument"])
            self.auto_save_download_setting_proxy_power_var.set(
                input_settings["default_setting"]["auto_save_download_setting"]["proxy_power"])
            self.auto_save_download_setting_proxy_no_proxy_var.set(
                input_settings["default_setting"]["auto_save_download_setting"]["proxy_no_proxy"])
            self.auto_save_download_setting_proxy_extracting_only_var.set(
                input_settings["default_setting"]["auto_save_download_setting"]["proxy_extracting_only"])
            self.auto_save_download_setting_proxy_type_var.set(
                input_settings["default_setting"]["auto_save_download_setting"]["proxy_type"])
            self.auto_save_download_setting_proxy_url_var.set(
                input_settings["default_setting"]["auto_save_download_setting"]["proxy_host"])
            self.auto_save_download_setting_proxy_login_power_var.set(
                input_settings["default_setting"]["auto_save_download_setting"]["proxy_login_power"])
            self.auto_save_download_setting_proxy_login_username_var.set(
                input_settings["default_setting"]["auto_save_download_setting"]["proxy_login_username"])
            self.auto_save_download_setting_proxy_login_password_var.set(
                input_settings["default_setting"]["auto_save_download_setting"]["proxy_login_password"])
            self.auto_save_download_setting_proxy_timeout_time_power_var.set(
                input_settings["default_setting"]["auto_save_download_setting"]["proxy_timeout_time_power"])
            self.auto_save_download_setting_proxy_timeout_time_value_var.set(
                input_settings["default_setting"]["auto_save_download_setting"]["proxy_timeout_time_value"])
            self.auto_save_download_setting_batch_download_power_var.set(
                input_settings["default_setting"]["auto_save_download_setting"]["batch_download_power"])
            self.auto_save_download_setting_batch_download_parallel_var.set(
                input_settings["default_setting"]["auto_save_download_setting"]["batch_download_parallel"])
            self.auto_save_download_setting_batch_download_from_file_power_var.set(
                input_settings["default_setting"]["auto_save_download_setting"][
                    "batch_download_download_from_file_power"])
            self.auto_save_download_setting_batch_download_from_file_path_var.set(
                input_settings["default_setting"]["auto_save_download_setting"][
                    "batch_download_download_from_file_path"])
            self.auto_save_download_setting_batch_urls_var.set(
                input_settings["default_setting"]["auto_save_download_setting"]["batch_download_urls"])

        def check_settings_change(event=None):
            self.new_settings = {"auto_save_download_setting": {}}
            self.new_settings["language"] = [k for k, v in self.final_settings['languages'].items()][
                [f"{k} / {v['show_name']}" for k, v in self.final_settings['languages'].items()].index(
                    self.program_language_combobox.get())]
            self.new_settings["window_type"] = self.program_style_combobox.get()
            self.new_settings["exit_with_hint"] = self.exit_with_hint_var.get()
            self.new_settings["show_hover_tip"] = self.show_hover_tip_var.get()
            self.new_settings["show_change_name_format"] = self.show_change_name_format_var.get()
            self.new_settings["auto_save_download_setting"]["power"] = self.auto_save_download_setting_power_var.get()
            self.new_settings["auto_save_download_setting"]["url"] = self.auto_save_download_setting_url_var.get()
            self.new_settings["auto_save_download_setting"][
                "save_path"] = self.auto_save_download_setting_save_path_var.get()
            self.new_settings["auto_save_download_setting"][
                "save_name"] = self.auto_save_download_setting_save_name_var.get()
            self.new_settings["auto_save_download_setting"][
                "print_with_json"] = self.auto_save_download_setting_print_with_json_var.get()
            self.new_settings["auto_save_download_setting"][
                "download_captions"] = self.auto_save_download_setting_download_captions_var.get()
            self.new_settings["auto_save_download_setting"][
                "merge_video_parts"] = self.auto_save_download_setting_merge_video_parts_var.get()
            self.new_settings["auto_save_download_setting"][
                "download_m3u8_video"] = self.auto_save_download_setting_download_m3u8_video_var.get()
            self.new_settings["auto_save_download_setting"][
                "ignore_ssl_errors"] = self.auto_save_download_setting_ignore_ssl_errors_var.get()
            self.new_settings["auto_save_download_setting"][
                "forced_download"] = self.auto_save_download_setting_forced_download_var.get()
            self.new_settings["auto_save_download_setting"][
                "skip_downloaded_video"] = self.auto_save_download_setting_skip_downloaded_video_var.get()
            self.new_settings["auto_save_download_setting"][
                "auto_rename"] = self.auto_save_download_setting_auto_rename_var.get()
            self.new_settings["auto_save_download_setting"][
                "download_video_password_power"] = self.auto_save_download_setting_download_video_password_power_var.get()
            self.new_settings["auto_save_download_setting"][
                "download_video_password_value"] = self.auto_save_download_setting_download_video_password_value_var.get()
            self.new_settings["auto_save_download_setting"][
                "download_format_power"] = self.auto_save_download_setting_download_format_power_var.get()
            self.new_settings["auto_save_download_setting"][
                "download_format_value"] = self.auto_save_download_setting_download_format_value_var.get()
            self.new_settings["auto_save_download_setting"][
                "download_itag_power"] = self.auto_save_download_setting_download_itag_power_var.get()
            self.new_settings["auto_save_download_setting"][
                "download_itag_value"] = self.auto_save_download_setting_download_itag_value_var.get()
            self.new_settings["auto_save_download_setting"][
                "download_list_power"] = self.auto_save_download_setting_download_list_power_var.get()
            self.new_settings["auto_save_download_setting"][
                "download_list_page"] = self.auto_save_download_setting_download_list_page_var.get()
            self.new_settings["auto_save_download_setting"][
                "download_list_start"] = self.auto_save_download_setting_download_list_start_var.get()
            self.new_settings["auto_save_download_setting"][
                "download_list_end"] = self.auto_save_download_setting_download_list_end_var.get()
            self.new_settings["auto_save_download_setting"][
                "run_in_new_window"] = self.auto_save_download_setting_run_in_new_window_var.get()
            self.new_settings["auto_save_download_setting"]["debug"] = self.auto_save_download_setting_debug_var.get()
            self.new_settings["auto_save_download_setting"][
                "use_cookies_power"] = self.auto_save_download_setting_use_cookies_power_var.get()
            self.new_settings["auto_save_download_setting"][
                "use_cookies_path"] = self.auto_save_download_setting_use_cookies_path_var.get()
            self.new_settings["auto_save_download_setting"][
                "player_power"] = self.auto_save_download_setting_player_power_var.get()
            self.new_settings["auto_save_download_setting"][
                "player_path"] = self.auto_save_download_setting_player_path_var.get()
            self.new_settings["auto_save_download_setting"][
                "player_argument"] = self.auto_save_download_setting_player_argument_var.get()
            self.new_settings["auto_save_download_setting"][
                "proxy_power"] = self.auto_save_download_setting_proxy_power_var.get()
            self.new_settings["auto_save_download_setting"][
                "proxy_no_proxy"] = self.auto_save_download_setting_proxy_no_proxy_var.get()
            self.new_settings["auto_save_download_setting"][
                "proxy_extracting_only"] = self.auto_save_download_setting_proxy_extracting_only_var.get()
            self.new_settings["auto_save_download_setting"][
                "proxy_type"] = self.auto_save_download_setting_proxy_type_var.get()
            self.new_settings["auto_save_download_setting"][
                "proxy_host"] = self.auto_save_download_setting_proxy_url_var.get()
            self.new_settings["auto_save_download_setting"][
                "proxy_login_power"] = self.auto_save_download_setting_proxy_login_power_var.get()
            self.new_settings["auto_save_download_setting"][
                "proxy_login_username"] = self.auto_save_download_setting_proxy_login_username_var.get()
            self.new_settings["auto_save_download_setting"][
                "proxy_login_password"] = self.auto_save_download_setting_proxy_login_password_var.get()
            self.new_settings["auto_save_download_setting"][
                "proxy_timeout_time_power"] = self.auto_save_download_setting_proxy_timeout_time_power_var.get()
            self.new_settings["auto_save_download_setting"][
                "proxy_timeout_time_value"] = self.auto_save_download_setting_proxy_timeout_time_value_var.get()
            self.new_settings["auto_save_download_setting"][
                "batch_download_power"] = self.auto_save_download_setting_batch_download_power_var.get()
            self.new_settings["auto_save_download_setting"][
                "batch_download_parallel"] = self.auto_save_download_setting_batch_download_parallel_var.get()
            self.new_settings["auto_save_download_setting"][
                "batch_download_download_from_file_power"] = self.auto_save_download_setting_batch_download_from_file_power_var.get()
            self.new_settings["auto_save_download_setting"][
                "batch_download_download_from_file_path"] = self.auto_save_download_setting_batch_download_from_file_path_var.get()
            self.new_settings["auto_save_download_setting"][
                "batch_download_urls"] = self.auto_save_download_setting_batch_urls_var.get()

            if self.new_settings != self.final_settings["default_setting"]:
                self.is_change_settings = True
            else:
                self.is_change_settings = False

            if self.new_settings["language"] != self.old_settings["default_setting"]["language"] or self.new_settings[
                "window_type"] != self.old_settings["default_setting"]["window_type"] or self.new_settings[
                "show_change_name_format"] != self.old_settings["default_setting"]["show_change_name_format"]:
                self.need_to_restart = True
            else:
                self.need_to_restart = False

        def close_settings_window():
            check_settings_change()
            if self.is_change_settings:
                self.settings_window.attributes("-disabled", 1)
                try:
                    hide_askyesnocancel = tk.messagebox.askyesnocancel(self.final_settings["languages"][self.new_settings["language"]]["hint"], self.final_settings["languages"][self.new_settings["language"]]["whether_save_settings"])
                except:
                    hide_askyesnocancel = tk.messagebox.askyesnocancel(self.final_settings["language"]["hint"], self.final_settings["language"]["whether_save_settings"])
                self.settings_window.lift()
                self.settings_window.attributes("-disabled", 0)
                if hide_askyesnocancel:
                    check_settings_change()
                    self.save_settings()
                    if self.need_to_restart:
                        try:
                            tk.messagebox.showinfo(self.final_settings["languages"][self.final_settings["default_setting"]["language"]]["hint"], self.final_settings["languages"][self.final_settings["default_setting"]["language"]]["restart_program"])
                        except:
                            tk.messagebox.showinfo(self.final_settings["language"]["hint"], self.final_settings["language"]["restart_program"])
                    self.settings_window.destroy()
                elif hide_askyesnocancel is False:
                    self.settings_window.destroy()
                elif hide_askyesnocancel is None:
                    return
            else:
                if self.need_to_restart:
                    tk.messagebox.showinfo(self.final_settings["language"]["hint"],
                                           self.final_settings["language"]["restart_program"])
                self.settings_window.destroy()

        # 基础设置
        # 就是方便我翻代码的。（本人实力有限，感谢理解！）
        if True:
            self.program_define_setting_lableframe = tk.LabelFrame(self.settings_window,
                                                                   text=self.final_settings["language"][
                                                                       "define_setting"])
            self.program_style_top_frame = ttk.Frame(self.program_define_setting_lableframe)
            self.program_style_frame = ttk.Frame(self.program_style_top_frame)
            self.program_style_label = ttk.Label(self.program_style_frame,
                                                 text=self.final_settings["language"]["program_style"])
            self.EnhancedTooltip(self, self.program_style_label, self.final_settings["language"]["tip_need_restart"])
            self.program_style_label.grid(row=0, column=0, rowspan=4, sticky=tk.W + tk.N)
            self.program_style_combobox = ttk.Combobox(self.program_style_frame, values=['0', '1', '2'], width=5)
            self.EnhancedTooltip(self, self.program_style_combobox, self.final_settings["language"]["tip_need_restart"])
            self.program_style_combobox.grid(row=0, column=1, sticky=tk.W)
            self.program_style_combobox.current(int(self.final_settings['default_setting']['window_type'] if int(
                self.final_settings['default_setting']['window_type']) <= 2 else 0))
            self.program_style_combobox.bind("<<ComboboxSelected>>", check_settings_change)
            self.program_style_frame.grid(row=0, column=0, sticky=tk.W)
            self.program_style_hint_label = ttk.Label(self.program_style_top_frame, justify=tk.LEFT,
                                                      text=self.final_settings["language"]["program_style_hint"])
            self.program_style_hint_label.grid(row=0, column=1, rowspan=4, ipadx=20, ipady=5, sticky=tk.W)
            self.program_style_top_frame.grid(row=0, column=0, columnspan=3)

            self.program_language_frame = ttk.Frame(self.program_define_setting_lableframe)
            self.program_language_label = ttk.Label(self.program_language_frame, text="语言 / Language:")
            self.program_language_label.grid(row=0, column=0, sticky=tk.W)
            self.program_language_combobox = ttk.Combobox(self.program_language_frame,
                                                          values=[f"{k} / {v['show_name']}" for k, v in
                                                                  self.final_settings['languages'].items()])
            self.EnhancedTooltip(self, self.program_language_combobox, self.final_settings["language"]["tip_need_restart"])
            self.program_language_combobox.grid(row=0, column=1, sticky=tk.W)
            self.program_language_combobox.current(next((index for index, lang in enumerate(
                [f"{k} / {v['show_name']}" for k, v in self.final_settings['languages'].items()]) if lang.startswith(
                self.final_settings['default_setting']['language'] + ' / ')), None))
            self.program_language_combobox.bind("<<ComboboxSelected>>", check_settings_change)
            self.program_language_frame.grid(row=1, column=0, columnspan=3, sticky=tk.W)

            self.show_change_name_format_var = tk.BooleanVar()
            self.show_change_name_format_var.set(
                bool(self.final_settings['default_setting']['show_change_name_format']))
            self.show_change_name_format_checkbutton = ttk.Checkbutton(self.program_define_setting_lableframe,
                                                                       text=self.final_settings["language"][
                                                                           "show_change_name_format"],
                                                                       variable=self.show_change_name_format_var,
                                                                       command=check_settings_change)
            self.EnhancedTooltip(self, self.show_change_name_format_checkbutton,self.final_settings["language"]["tip_need_restart"])
            self.show_change_name_format_checkbutton.grid(row=3, column=0)
            self.exit_with_hint_var = tk.BooleanVar()
            self.exit_with_hint_var.set(bool(self.final_settings['default_setting']['exit_with_hint']))
            self.exit_with_hint_checkbutton = ttk.Checkbutton(self.program_define_setting_lableframe,
                                                              text=self.final_settings["language"]["exit_with_hint"],
                                                              variable=self.exit_with_hint_var,
                                                              command=check_settings_change)
            self.exit_with_hint_checkbutton.grid(row=3, column=1)
            self.show_hover_tip_var = tk.BooleanVar()
            self.show_hover_tip_var.set(bool(self.final_settings['default_setting']['show_hover_tip']))
            self.show_hover_tip_checkbutton = ttk.Checkbutton(self.program_define_setting_lableframe,
                                                              text=self.final_settings["language"]["show_hover_tip"],
                                                              variable=self.show_hover_tip_var,
                                                              command=check_settings_change)
            self.show_hover_tip_checkbutton.grid(row=3, column=2)
            self.program_define_setting_lableframe.grid(row=0, column=0, sticky=tk.W)

        # 保留设置
        self.auto_save_download_setting_labelframe = tk.LabelFrame(self.settings_window,
                                                                   text=self.final_settings["language"][
                                                                       "auto_save_download_setting"])
        self.auto_save_download_setting_power_var = tk.BooleanVar()
        self.auto_save_download_setting_power_var.set(
            bool(self.final_settings['default_setting']['auto_save_download_setting']['power']))
        self.auto_save_download_setting_power_checkbutton = ttk.Checkbutton(self.auto_save_download_setting_labelframe,
                                                                            text=self.final_settings["language"][
                                                                                "auto_save_download_power"],
                                                                            variable=self.auto_save_download_setting_power_var,
                                                                            command=check_settings_change)
        self.auto_save_download_setting_power_checkbutton.grid(row=0, column=0, sticky=tk.W + tk.N)
        # 设置快捷按键
        self.auto_save_download_setting_select_all_button = ttk.Button(self.auto_save_download_setting_labelframe,
                                                                       text=self.final_settings["language"][
                                                                           "select_all"], command=lambda: [
                [auto_save_download_setting.set(True) for auto_save_download_setting in
                 self.auto_save_download_settings], check_settings_change()])
        self.auto_save_download_setting_select_all_button.grid(row=0, column=1)
        self.auto_save_download_setting_unselect_all_button = ttk.Button(self.auto_save_download_setting_labelframe,
                                                                         text=self.final_settings["language"][
                                                                             "unselect_all"], command=lambda: [
                [auto_save_download_setting.set(False) for auto_save_download_setting in
                 self.auto_save_download_settings], check_settings_change()])
        self.auto_save_download_setting_unselect_all_button.grid(row=0, column=2)
        self.auto_save_download_setting_reverse_select_button = ttk.Button(self.auto_save_download_setting_labelframe,
                                                                           text=self.final_settings["language"][
                                                                               "reverse_select"], command=lambda: [
                [auto_save_download_setting.set(not auto_save_download_setting.get()) for auto_save_download_setting in
                 self.auto_save_download_settings], check_settings_change()])
        self.auto_save_download_setting_reverse_select_button.grid(row=0, column=3)

        self.auto_save_download_setting_detail_labelframe = tk.LabelFrame(self.auto_save_download_setting_labelframe,
                                                                          text=self.final_settings["language"][
                                                                              "auto_save_download_setting_detail"])

        # 下载设置保留设置
        if True:
            self.auto_save_download_setting_default_setting_frame = ttk.Frame(
                self.auto_save_download_setting_detail_labelframe)
            self.auto_save_download_setting_url_var = tk.BooleanVar()
            self.auto_save_download_settings.append(self.auto_save_download_setting_url_var)
            self.auto_save_download_setting_url_var.set(
                bool(self.final_settings['default_setting']['auto_save_download_setting']['url']))
            self.auto_save_download_setting_url_checkbutton = ttk.Checkbutton(
                self.auto_save_download_setting_default_setting_frame, text=self.final_settings["language"]["url"],
                variable=self.auto_save_download_setting_url_var, command=check_settings_change)
            self.auto_save_download_setting_url_checkbutton.grid(row=0, column=0)
            self.auto_save_download_setting_save_path_var = tk.BooleanVar()
            self.auto_save_download_settings.append(self.auto_save_download_setting_save_path_var)
            self.auto_save_download_setting_save_path_var.set(
                bool(self.final_settings['default_setting']['auto_save_download_setting']['save_path']))
            self.auto_save_download_setting_save_path_checkbutton = ttk.Checkbutton(
                self.auto_save_download_setting_default_setting_frame,
                text=self.final_settings["language"]["save_path"],
                variable=self.auto_save_download_setting_save_path_var, command=check_settings_change)
            self.auto_save_download_setting_save_path_checkbutton.grid(row=0, column=1)
            self.auto_save_download_setting_save_name_var = tk.BooleanVar()
            self.auto_save_download_settings.append(self.auto_save_download_setting_save_name_var)
            self.auto_save_download_setting_save_name_var.set(
                bool(self.final_settings['default_setting']['auto_save_download_setting']['save_name']))
            self.auto_save_download_setting_save_name_checkbutton = ttk.Checkbutton(
                self.auto_save_download_setting_default_setting_frame,
                text=self.final_settings["language"]["save_name"],
                variable=self.auto_save_download_setting_save_name_var, command=check_settings_change)
            self.auto_save_download_setting_save_name_checkbutton.grid(row=0, column=2)
            self.auto_save_download_setting_print_with_json_var = tk.BooleanVar()
            self.auto_save_download_settings.append(self.auto_save_download_setting_print_with_json_var)
            self.auto_save_download_setting_print_with_json_var.set(
                bool(self.final_settings['default_setting']['auto_save_download_setting']['print_with_json']))
            self.auto_save_download_setting_print_with_json_checkbutton = ttk.Checkbutton(
                self.auto_save_download_setting_default_setting_frame,
                text=self.final_settings["language"]["print_with_json"],
                variable=self.auto_save_download_setting_print_with_json_var, command=check_settings_change)
            self.auto_save_download_setting_print_with_json_checkbutton.grid(row=0, column=3)
            self.auto_save_download_setting_default_setting_frame.grid(row=0, column=0, columnspan=9,
                                                                       sticky=tk.W + tk.N)

            self.auto_save_download_setting_part_frame = ttk.Frame(self.auto_save_download_setting_detail_labelframe)

            self.auto_save_download_setting_part_frame_label_one = ttk.Label(self.auto_save_download_setting_part_frame)
            self.auto_save_download_setting_download_captions_var = tk.BooleanVar()
            self.auto_save_download_settings.append(self.auto_save_download_setting_download_captions_var)
            self.auto_save_download_setting_download_captions_var.set(
                bool(self.final_settings['default_setting']['auto_save_download_setting']['download_captions']))
            self.auto_save_download_setting_download_captions_checkbutton = ttk.Checkbutton(
                self.auto_save_download_setting_part_frame_label_one,
                text=self.final_settings["language"]["download_captions_show"],
                variable=self.auto_save_download_setting_download_captions_var, command=check_settings_change)
            self.auto_save_download_setting_download_captions_checkbutton.grid(row=0, column=0, sticky=tk.W + tk.N)
            self.auto_save_download_setting_merge_video_parts_var = tk.BooleanVar()
            self.auto_save_download_settings.append(self.auto_save_download_setting_merge_video_parts_var)
            self.auto_save_download_setting_merge_video_parts_var.set(
                bool(self.final_settings['default_setting']['auto_save_download_setting']['merge_video_parts']))
            self.auto_save_download_setting_merge_video_parts_checkbutton = ttk.Checkbutton(
                self.auto_save_download_setting_part_frame_label_one,
                text=self.final_settings["language"]["merge_video_parts"],
                variable=self.auto_save_download_setting_merge_video_parts_var, command=check_settings_change)
            self.auto_save_download_setting_merge_video_parts_checkbutton.grid(row=0, column=1, sticky=tk.W + tk.N)
            self.auto_save_download_setting_download_m3u8_video_var = tk.BooleanVar()
            self.auto_save_download_settings.append(self.auto_save_download_setting_download_m3u8_video_var)
            self.auto_save_download_setting_download_m3u8_video_var.set(
                bool(self.final_settings['default_setting']['auto_save_download_setting']['download_m3u8_video']))
            self.auto_save_download_setting_download_m3u8_video_checkbutton = ttk.Checkbutton(
                self.auto_save_download_setting_part_frame_label_one,
                text=self.final_settings["language"]["download_m3u8_video"],
                variable=self.auto_save_download_setting_download_m3u8_video_var, command=check_settings_change)
            self.auto_save_download_setting_download_m3u8_video_checkbutton.grid(row=0, column=2, sticky=tk.W + tk.N)
            self.auto_save_download_setting_ignore_ssl_errors_var = tk.BooleanVar()
            self.auto_save_download_settings.append(self.auto_save_download_setting_ignore_ssl_errors_var)
            self.auto_save_download_setting_ignore_ssl_errors_var.set(
                bool(self.final_settings['default_setting']['auto_save_download_setting']['ignore_ssl_errors']))
            self.auto_save_download_setting_ignore_ssl_errors_checkbutton = ttk.Checkbutton(
                self.auto_save_download_setting_part_frame_label_one,
                text=self.final_settings["language"]["ignore_ssl_errors"],
                variable=self.auto_save_download_setting_ignore_ssl_errors_var, command=check_settings_change)
            self.auto_save_download_setting_ignore_ssl_errors_checkbutton.grid(row=0, column=3, sticky=tk.W + tk.N)
            self.auto_save_download_setting_forced_download_var = tk.BooleanVar()
            self.auto_save_download_settings.append(self.auto_save_download_setting_forced_download_var)
            self.auto_save_download_setting_forced_download_var.set(
                bool(self.final_settings['default_setting']['auto_save_download_setting']['forced_download']))
            self.auto_save_download_setting_forced_download_checkbutton = ttk.Checkbutton(
                self.auto_save_download_setting_part_frame_label_one,
                text=self.final_settings["language"]["forced_download_show"],
                variable=self.auto_save_download_setting_forced_download_var, command=check_settings_change)
            self.auto_save_download_setting_forced_download_checkbutton.grid(row=0, column=4, sticky=tk.W + tk.N)
            self.auto_save_download_setting_part_frame_label_one.grid(row=0, column=0, columnspan=9, sticky=tk.W + tk.N)

            self.auto_save_download_setting_part_frame_label_two = ttk.Label(self.auto_save_download_setting_part_frame)
            self.auto_save_download_setting_skip_downloaded_video_var = tk.BooleanVar()
            self.auto_save_download_settings.append(self.auto_save_download_setting_skip_downloaded_video_var)
            self.auto_save_download_setting_skip_downloaded_video_var.set(
                bool(self.final_settings['default_setting']['auto_save_download_setting']['skip_downloaded_video']))
            self.auto_save_download_setting_skip_downloaded_video_checkbutton = ttk.Checkbutton(
                self.auto_save_download_setting_part_frame_label_two,
                text=self.final_settings["language"]["skip_downloaded_video"],
                variable=self.auto_save_download_setting_skip_downloaded_video_var, command=check_settings_change)
            self.auto_save_download_setting_skip_downloaded_video_checkbutton.grid(row=0, column=0, sticky=tk.W + tk.N)
            self.auto_save_download_setting_auto_rename_var = tk.BooleanVar()
            self.auto_save_download_settings.append(self.auto_save_download_setting_auto_rename_var)
            self.auto_save_download_setting_auto_rename_var.set(
                bool(self.final_settings['default_setting']['auto_save_download_setting']['auto_rename']))
            self.auto_save_download_setting_auto_rename_checkbutton = ttk.Checkbutton(
                self.auto_save_download_setting_part_frame_label_two,
                text=self.final_settings["language"]["auto_rename"],
                variable=self.auto_save_download_setting_auto_rename_var, command=check_settings_change)
            self.auto_save_download_setting_auto_rename_checkbutton.grid(row=0, column=1, sticky=tk.W + tk.N)
            # -------------------------
            self.auto_save_download_setting_download_video_password_frame = tk.LabelFrame(
                self.auto_save_download_setting_part_frame_label_two)
            self.auto_save_download_setting_download_video_password_power_var = tk.BooleanVar()
            self.auto_save_download_settings.append(self.auto_save_download_setting_download_video_password_power_var)
            self.auto_save_download_setting_download_video_password_power_var.set(bool(
                self.final_settings['default_setting']['auto_save_download_setting']['download_video_password_power']))
            self.auto_save_download_setting_download_video_password_power_checkbutton = ttk.Checkbutton(
                self.auto_save_download_setting_download_video_password_frame,
                text=self.final_settings["language"]["download_video_password_power"],
                variable=self.auto_save_download_setting_download_video_password_power_var,
                command=check_settings_change)
            self.auto_save_download_setting_download_video_password_power_checkbutton.grid(row=0, column=0,
                                                                                           sticky=tk.W + tk.N)
            self.auto_save_download_setting_download_video_password_value_var = tk.BooleanVar()
            self.auto_save_download_settings.append(self.auto_save_download_setting_download_video_password_value_var)
            self.auto_save_download_setting_download_video_password_value_var.set(bool(
                self.final_settings['default_setting']['auto_save_download_setting']['download_video_password_value']))
            self.auto_save_download_setting_download_video_password_value_checkbutton = ttk.Checkbutton(
                self.auto_save_download_setting_download_video_password_frame,
                text=self.final_settings["language"]["download_video_password_value"],
                variable=self.auto_save_download_setting_download_video_password_value_var,
                command=check_settings_change)
            self.auto_save_download_setting_download_video_password_value_checkbutton.grid(row=0, column=1,
                                                                                           sticky=tk.W + tk.N)
            self.auto_save_download_setting_download_video_password_frame.grid(row=0, column=2, columnspan=2,
                                                                               sticky=tk.W)
            self.auto_save_download_setting_part_frame_label_two.grid(row=1, column=0, columnspan=9, sticky=tk.W + tk.N)

            self.auto_save_download_setting_part_frame_label_three = ttk.Label(
                self.auto_save_download_setting_part_frame)
            self.auto_save_download_setting_download_format_frame = tk.LabelFrame(
                self.auto_save_download_setting_part_frame_label_three)
            self.auto_save_download_setting_download_format_power_var = tk.BooleanVar()
            self.auto_save_download_settings.append(self.auto_save_download_setting_download_format_power_var)
            self.auto_save_download_setting_download_format_power_var.set(
                bool(self.final_settings['default_setting']['auto_save_download_setting']['download_format_power']))
            self.auto_save_download_setting_download_format_power_checkbutton = ttk.Checkbutton(
                self.auto_save_download_setting_download_format_frame,
                text=self.final_settings["language"]["download_format_power"],
                variable=self.auto_save_download_setting_download_format_power_var, command=check_settings_change)
            self.auto_save_download_setting_download_format_power_checkbutton.grid(row=0, column=0, sticky=tk.W + tk.N)
            self.auto_save_download_setting_download_format_value_var = tk.BooleanVar()
            self.auto_save_download_settings.append(self.auto_save_download_setting_download_format_value_var)
            self.auto_save_download_setting_download_format_value_var.set(
                bool(self.final_settings['default_setting']['auto_save_download_setting']['download_format_value']))
            self.auto_save_download_setting_download_format_value_checkbutton = ttk.Checkbutton(
                self.auto_save_download_setting_download_format_frame,
                text=self.final_settings["language"]["download_format_value"],
                variable=self.auto_save_download_setting_download_format_value_var, command=check_settings_change)
            self.auto_save_download_setting_download_format_value_checkbutton.grid(row=0, column=1, sticky=tk.W + tk.N)
            self.auto_save_download_setting_download_format_frame.grid(row=0, column=0, columnspan=2, sticky=tk.W)
            # -------------------------
            self.auto_save_download_setting_download_itag_frame = tk.LabelFrame(
                self.auto_save_download_setting_part_frame_label_three)
            self.auto_save_download_setting_download_itag_power_var = tk.BooleanVar()
            self.auto_save_download_settings.append(self.auto_save_download_setting_download_itag_power_var)
            self.auto_save_download_setting_download_itag_power_var.set(
                bool(self.final_settings['default_setting']['auto_save_download_setting']['download_itag_power']))
            self.auto_save_download_setting_download_itag_power_checkbutton = ttk.Checkbutton(
                self.auto_save_download_setting_download_itag_frame,
                text=self.final_settings["language"]["download_itag_power"],
                variable=self.auto_save_download_setting_download_itag_power_var, command=check_settings_change)
            self.auto_save_download_setting_download_itag_power_checkbutton.grid(row=0, column=0, sticky=tk.W + tk.N)
            self.auto_save_download_setting_download_itag_value_var = tk.BooleanVar()
            self.auto_save_download_settings.append(self.auto_save_download_setting_download_itag_value_var)
            self.auto_save_download_setting_download_itag_value_var.set(
                bool(self.final_settings['default_setting']['auto_save_download_setting']['download_itag_value']))
            self.auto_save_download_setting_download_itag_value_checkbutton = ttk.Checkbutton(
                self.auto_save_download_setting_download_itag_frame,
                text=self.final_settings["language"]["download_itag_value"],
                variable=self.auto_save_download_setting_download_itag_value_var, command=check_settings_change)
            self.auto_save_download_setting_download_itag_value_checkbutton.grid(row=0, column=1, sticky=tk.W + tk.N)
            self.auto_save_download_setting_download_itag_frame.grid(row=0, column=2, columnspan=2, sticky=tk.W)
            self.auto_save_download_setting_part_frame_label_three.grid(row=2, column=0, columnspan=9,
                                                                        sticky=tk.W + tk.N)

            self.auto_save_download_setting_part_frame_label_four = ttk.Label(
                self.auto_save_download_setting_part_frame)
            self.auto_save_download_setting_download_list_frame = tk.LabelFrame(
                self.auto_save_download_setting_part_frame_label_four)
            self.auto_save_download_setting_download_list_power_var = tk.BooleanVar()
            self.auto_save_download_settings.append(self.auto_save_download_setting_download_list_power_var)
            self.auto_save_download_setting_download_list_power_var.set(
                bool(self.final_settings['default_setting']['auto_save_download_setting']['download_list_power']))
            self.auto_save_download_setting_download_list_power_checkbutton = ttk.Checkbutton(
                self.auto_save_download_setting_download_list_frame,
                text=self.final_settings["language"]["download_list_power"],
                variable=self.auto_save_download_setting_download_list_power_var, command=check_settings_change)
            self.auto_save_download_setting_download_list_power_checkbutton.grid(row=0, column=0, sticky=tk.W + tk.N)
            self.auto_save_download_setting_download_list_page_var = tk.BooleanVar()
            self.auto_save_download_settings.append(self.auto_save_download_setting_download_list_page_var)
            self.auto_save_download_setting_download_list_page_var.set(
                bool(self.final_settings['default_setting']['auto_save_download_setting']['download_list_page']))
            self.auto_save_download_setting_download_list_page_checkbutton = ttk.Checkbutton(
                self.auto_save_download_setting_download_list_frame,
                text=self.final_settings["language"]["download_list_page"],
                variable=self.auto_save_download_setting_download_list_page_var, command=check_settings_change)
            self.auto_save_download_setting_download_list_page_checkbutton.grid(row=0, column=1, sticky=tk.W + tk.N)
            self.auto_save_download_setting_download_list_start_var = tk.BooleanVar()
            self.auto_save_download_settings.append(self.auto_save_download_setting_download_list_start_var)
            self.auto_save_download_setting_download_list_start_var.set(
                bool(self.final_settings['default_setting']['auto_save_download_setting']['download_list_start']))
            self.auto_save_download_setting_download_list_start_checkbutton = ttk.Checkbutton(
                self.auto_save_download_setting_download_list_frame,
                text=self.final_settings["language"]["download_list_start"],
                variable=self.auto_save_download_setting_download_list_start_var, command=check_settings_change)
            self.auto_save_download_setting_download_list_start_checkbutton.grid(row=0, column=2, sticky=tk.W + tk.N)
            self.auto_save_download_setting_download_list_end_var = tk.BooleanVar()
            self.auto_save_download_settings.append(self.auto_save_download_setting_download_list_end_var)
            self.auto_save_download_setting_download_list_end_var.set(
                bool(self.final_settings['default_setting']['auto_save_download_setting']['download_list_end']))
            self.auto_save_download_setting_download_list_end_checkbutton = ttk.Checkbutton(
                self.auto_save_download_setting_download_list_frame,
                text=self.final_settings["language"]["download_list_end"],
                variable=self.auto_save_download_setting_download_list_end_var, command=check_settings_change)
            self.auto_save_download_setting_download_list_end_checkbutton.grid(row=0, column=3, sticky=tk.W + tk.N)
            self.auto_save_download_setting_download_list_frame.grid(row=0, column=0, columnspan=4, sticky=tk.W + tk.N)
            # -------------------------
            self.auto_save_download_setting_run_in_new_window_var = tk.BooleanVar()
            self.auto_save_download_settings.append(self.auto_save_download_setting_run_in_new_window_var)
            self.auto_save_download_setting_run_in_new_window_var.set(
                bool(self.final_settings['default_setting']['auto_save_download_setting']['run_in_new_window']))
            self.auto_save_download_setting_run_in_new_window_checkbutton = ttk.Checkbutton(
                self.auto_save_download_setting_part_frame_label_four,
                text=self.final_settings["language"]["run_in_new_window_show"],
                variable=self.auto_save_download_setting_run_in_new_window_var, command=check_settings_change)
            self.auto_save_download_setting_run_in_new_window_checkbutton.grid(row=0, column=4, sticky=tk.W + tk.N)
            # -------------------------
            self.auto_save_download_setting_debug_var = tk.BooleanVar()
            self.auto_save_download_settings.append(self.auto_save_download_setting_debug_var)
            self.auto_save_download_setting_debug_var.set(
                bool(self.final_settings['default_setting']['auto_save_download_setting']['debug']))
            self.auto_save_download_setting_debug_checkbutton = ttk.Checkbutton(
                self.auto_save_download_setting_part_frame_label_four,
                text=self.final_settings["language"]["debug_show"], variable=self.auto_save_download_setting_debug_var,
                command=check_settings_change)
            self.auto_save_download_setting_debug_checkbutton.grid(row=0, column=5, sticky=tk.W + tk.N)
            self.auto_save_download_setting_part_frame_label_four.grid(row=3, column=0, columnspan=9,
                                                                       sticky=tk.W + tk.N)

            self.auto_save_download_setting_part_frame_label_five = ttk.Frame(
                self.auto_save_download_setting_part_frame)
            self.auto_save_download_setting_use_cookies_frame = tk.LabelFrame(
                self.auto_save_download_setting_part_frame_label_five)
            self.auto_save_download_setting_use_cookies_power_var = tk.BooleanVar()
            self.auto_save_download_settings.append(self.auto_save_download_setting_use_cookies_power_var)
            self.auto_save_download_setting_use_cookies_power_var.set(
                bool(self.final_settings['default_setting']['auto_save_download_setting']['use_cookies_power']))
            self.auto_save_download_setting_use_cookies_power_checkbutton = ttk.Checkbutton(
                self.auto_save_download_setting_use_cookies_frame,
                text=self.final_settings["language"]["use_cookies_power"],
                variable=self.auto_save_download_setting_use_cookies_power_var, command=check_settings_change)
            self.auto_save_download_setting_use_cookies_power_checkbutton.grid(row=0, column=0, sticky=tk.W + tk.N)
            self.auto_save_download_setting_use_cookies_path_var = tk.BooleanVar()
            self.auto_save_download_settings.append(self.auto_save_download_setting_use_cookies_path_var)
            self.auto_save_download_setting_use_cookies_path_var.set(
                bool(self.final_settings['default_setting']['auto_save_download_setting']['use_cookies_path']))
            self.auto_save_download_setting_use_cookies_path_checkbutton = ttk.Checkbutton(
                self.auto_save_download_setting_use_cookies_frame,
                text=self.final_settings["language"]["use_cookies_path"],
                variable=self.auto_save_download_setting_use_cookies_path_var, command=check_settings_change)
            self.auto_save_download_setting_use_cookies_path_checkbutton.grid(row=0, column=1, sticky=tk.W + tk.N)
            self.auto_save_download_setting_use_cookies_frame.grid(row=0, column=0, columnspan=2)
            # -------------------------
            self.auto_save_download_setting_player_frame = tk.LabelFrame(
                self.auto_save_download_setting_part_frame_label_five)
            self.auto_save_download_setting_player_power_var = tk.BooleanVar()
            self.auto_save_download_settings.append(self.auto_save_download_setting_player_power_var)
            self.auto_save_download_setting_player_power_var.set(
                bool(self.final_settings['default_setting']['auto_save_download_setting']['player_power']))
            self.auto_save_download_setting_player_power_checkbutton = ttk.Checkbutton(
                self.auto_save_download_setting_player_frame, text=self.final_settings["language"]["player_power"],
                variable=self.auto_save_download_setting_player_power_var, command=check_settings_change)
            self.auto_save_download_setting_player_power_checkbutton.grid(row=0, column=0, sticky=tk.W + tk.N)
            self.auto_save_download_setting_player_path_var = tk.BooleanVar()
            self.auto_save_download_settings.append(self.auto_save_download_setting_player_path_var)
            self.auto_save_download_setting_player_path_var.set(
                bool(self.final_settings['default_setting']['auto_save_download_setting']['player_path']))
            self.auto_save_download_setting_player_path_checkbutton = ttk.Checkbutton(
                self.auto_save_download_setting_player_frame, text=self.final_settings["language"]["player_path"],
                variable=self.auto_save_download_setting_player_path_var, command=check_settings_change)
            self.auto_save_download_setting_player_path_checkbutton.grid(row=0, column=1, sticky=tk.W + tk.N)
            self.auto_save_download_setting_player_argument_var = tk.BooleanVar()
            self.auto_save_download_settings.append(self.auto_save_download_setting_player_argument_var)
            self.auto_save_download_setting_player_argument_var.set(
                bool(self.final_settings['default_setting']['auto_save_download_setting']['player_argument']))
            self.auto_save_download_setting_player_argument_checkbutton = ttk.Checkbutton(
                self.auto_save_download_setting_player_frame, text=self.final_settings["language"]["player_argument"],
                variable=self.auto_save_download_setting_player_argument_var, command=check_settings_change)
            self.auto_save_download_setting_player_argument_checkbutton.grid(row=0, column=2, sticky=tk.W + tk.N)
            self.auto_save_download_setting_player_frame.grid(row=0, column=2, columnspan=3)
            self.auto_save_download_setting_part_frame_label_five.grid(row=4, column=0, columnspan=9,
                                                                       sticky=tk.W + tk.N)

            self.auto_save_download_setting_part_frame.grid(row=1, column=0, columnspan=9, sticky=tk.W + tk.N)

            self.auto_save_download_setting_proxy_frame = tk.LabelFrame(
                self.auto_save_download_setting_detail_labelframe)

            self.auto_save_download_setting_proxy_frame_label_one = ttk.Frame(
                self.auto_save_download_setting_proxy_frame)
            self.auto_save_download_setting_proxy_power_var = tk.BooleanVar()
            self.auto_save_download_settings.append(self.auto_save_download_setting_proxy_power_var)
            self.auto_save_download_setting_proxy_power_var.set(
                bool(self.final_settings['default_setting']['auto_save_download_setting']['proxy_power']))
            self.auto_save_download_setting_proxy_power_checkbutton = ttk.Checkbutton(
                self.auto_save_download_setting_proxy_frame_label_one,
                text=self.final_settings["language"]["proxy_power"],
                variable=self.auto_save_download_setting_proxy_power_var, command=check_settings_change)
            self.auto_save_download_setting_proxy_power_checkbutton.grid(row=0, column=0, sticky=tk.W + tk.N)
            self.auto_save_download_setting_proxy_no_proxy_var = tk.BooleanVar()
            self.auto_save_download_settings.append(self.auto_save_download_setting_proxy_no_proxy_var)
            self.auto_save_download_setting_proxy_no_proxy_var.set(
                bool(self.final_settings['default_setting']['auto_save_download_setting']['proxy_no_proxy']))
            self.auto_save_download_setting_proxy_no_proxy_checkbutton = ttk.Checkbutton(
                self.auto_save_download_setting_proxy_frame_label_one,
                text=self.final_settings["language"]["proxy_no_proxy"],
                variable=self.auto_save_download_setting_proxy_no_proxy_var, command=check_settings_change)
            self.auto_save_download_setting_proxy_no_proxy_checkbutton.grid(row=0, column=1, sticky=tk.W + tk.N)
            self.auto_save_download_setting_proxy_extracting_only_var = tk.BooleanVar()
            self.auto_save_download_settings.append(self.auto_save_download_setting_proxy_extracting_only_var)
            self.auto_save_download_setting_proxy_extracting_only_var.set(
                bool(self.final_settings['default_setting']['auto_save_download_setting']['proxy_extracting_only']))
            self.auto_save_download_setting_proxy_extracting_only_checkbutton = ttk.Checkbutton(
                self.auto_save_download_setting_proxy_frame_label_one,
                text=self.final_settings["language"]["proxy_extracting_only"],
                variable=self.auto_save_download_setting_proxy_extracting_only_var, command=check_settings_change)
            self.auto_save_download_setting_proxy_extracting_only_checkbutton.grid(row=0, column=2, sticky=tk.W + tk.N)
            self.auto_save_download_setting_proxy_type_var = tk.BooleanVar()
            self.auto_save_download_settings.append(self.auto_save_download_setting_proxy_type_var)
            self.auto_save_download_setting_proxy_type_var.set(
                bool(self.final_settings['default_setting']['auto_save_download_setting']['proxy_type']))
            self.auto_save_download_setting_proxy_type_checkbutton = ttk.Checkbutton(
                self.auto_save_download_setting_proxy_frame_label_one,
                text=self.final_settings["language"]["proxy_type"],
                variable=self.auto_save_download_setting_proxy_type_var, command=check_settings_change)
            self.auto_save_download_setting_proxy_type_checkbutton.grid(row=0, column=3, sticky=tk.W + tk.N)
            self.auto_save_download_setting_proxy_url_var = tk.BooleanVar()
            self.auto_save_download_settings.append(self.auto_save_download_setting_proxy_url_var)
            self.auto_save_download_setting_proxy_url_var.set(
                bool(self.final_settings['default_setting']['auto_save_download_setting']['proxy_host']))
            self.auto_save_download_setting_proxy_url_checkbutton = ttk.Checkbutton(
                self.auto_save_download_setting_proxy_frame_label_one,
                text=self.final_settings["language"]["proxy_host"],
                variable=self.auto_save_download_setting_proxy_url_var, command=check_settings_change)
            self.auto_save_download_setting_proxy_url_checkbutton.grid(row=0, column=4, sticky=tk.W + tk.N)
            self.auto_save_download_setting_proxy_frame_label_one.grid(row=0, column=0, columnspan=9,
                                                                       sticky=tk.W + tk.N)

            self.auto_save_download_setting_proxy_frame_label_two = ttk.Frame(
                self.auto_save_download_setting_proxy_frame)
            self.auto_save_download_setting_proxy_login_frame = tk.LabelFrame(
                self.auto_save_download_setting_proxy_frame_label_two)
            self.auto_save_download_setting_proxy_login_power_var = tk.BooleanVar()
            self.auto_save_download_settings.append(self.auto_save_download_setting_proxy_login_power_var)
            self.auto_save_download_setting_proxy_login_power_var.set(
                bool(self.final_settings['default_setting']['auto_save_download_setting']['proxy_login_power']))
            self.auto_save_download_setting_proxy_login_power_checkbutton = ttk.Checkbutton(
                self.auto_save_download_setting_proxy_login_frame,
                text=self.final_settings["language"]["proxy_login_power"],
                variable=self.auto_save_download_setting_proxy_login_power_var, command=check_settings_change)
            self.auto_save_download_setting_proxy_login_power_checkbutton.grid(row=0, column=0, sticky=tk.W + tk.N)
            self.auto_save_download_setting_proxy_login_username_var = tk.BooleanVar()
            self.auto_save_download_settings.append(self.auto_save_download_setting_proxy_login_username_var)
            self.auto_save_download_setting_proxy_login_username_var.set(
                bool(self.final_settings['default_setting']['auto_save_download_setting']['proxy_login_username']))
            self.auto_save_download_setting_proxy_login_username_checkbutton = ttk.Checkbutton(
                self.auto_save_download_setting_proxy_login_frame,
                text=self.final_settings["language"]["proxy_login_username"],
                variable=self.auto_save_download_setting_proxy_login_username_var, command=check_settings_change)
            self.auto_save_download_setting_proxy_login_username_checkbutton.grid(row=0, column=1, sticky=tk.W + tk.N)
            self.auto_save_download_setting_proxy_login_password_var = tk.BooleanVar()
            self.auto_save_download_settings.append(self.auto_save_download_setting_proxy_login_password_var)
            self.auto_save_download_setting_proxy_login_password_var.set(
                bool(self.final_settings['default_setting']['auto_save_download_setting']['proxy_login_password']))
            self.auto_save_download_setting_proxy_login_password_checkbutton = ttk.Checkbutton(
                self.auto_save_download_setting_proxy_login_frame,
                text=self.final_settings["language"]["proxy_login_password"],
                variable=self.auto_save_download_setting_proxy_login_password_var, command=check_settings_change)
            self.auto_save_download_setting_proxy_login_password_checkbutton.grid(row=0, column=2, sticky=tk.W + tk.N)
            self.auto_save_download_setting_proxy_login_frame.grid(row=0, column=0, columnspan=3, sticky=tk.W + tk.N)
            # -------------------------
            self.auto_save_download_setting_proxy_timeout_time_power_var = tk.BooleanVar()
            self.auto_save_download_settings.append(self.auto_save_download_setting_proxy_timeout_time_power_var)
            self.auto_save_download_setting_proxy_timeout_time_power_var.set(
                bool(self.final_settings['default_setting']['auto_save_download_setting']['proxy_timeout_time_power']))
            self.auto_save_download_setting_proxy_timeout_time_power_checkbutton = ttk.Checkbutton(
                self.auto_save_download_setting_proxy_frame_label_two,
                text=self.final_settings["language"]["proxy_timeout_time_power"],
                variable=self.auto_save_download_setting_proxy_timeout_time_power_var, command=check_settings_change)
            self.auto_save_download_setting_proxy_timeout_time_power_checkbutton.grid(row=0, column=3,
                                                                                      sticky=tk.W + tk.N)
            self.auto_save_download_setting_proxy_timeout_time_value_var = tk.BooleanVar()
            self.auto_save_download_settings.append(self.auto_save_download_setting_proxy_timeout_time_value_var)
            self.auto_save_download_setting_proxy_timeout_time_value_var.set(
                bool(self.final_settings['default_setting']['auto_save_download_setting']['proxy_timeout_time_value']))
            self.auto_save_download_setting_proxy_timeout_time_value_checkbutton = ttk.Checkbutton(
                self.auto_save_download_setting_proxy_frame_label_two,
                text=self.final_settings["language"]["proxy_timeout_time_value"],
                variable=self.auto_save_download_setting_proxy_timeout_time_value_var, command=check_settings_change)
            self.auto_save_download_setting_proxy_timeout_time_value_checkbutton.grid(row=0, column=4,
                                                                                      sticky=tk.W + tk.N)
            self.auto_save_download_setting_proxy_frame_label_two.grid(row=1, column=0, columnspan=9,
                                                                       sticky=tk.W + tk.N)

            self.auto_save_download_setting_proxy_frame.grid(row=2, column=0, columnspan=9, sticky=tk.W + tk.N)

            self.auto_save_download_setting_batch_download_frame = tk.LabelFrame(
                self.auto_save_download_setting_detail_labelframe)
            self.auto_save_download_setting_batch_download_power_var = tk.BooleanVar()
            self.auto_save_download_settings.append(self.auto_save_download_setting_batch_download_power_var)
            self.auto_save_download_setting_batch_download_power_var.set(
                bool(self.final_settings['default_setting']['auto_save_download_setting']['batch_download_power']))
            self.auto_save_download_setting_batch_download_power_checkbutton = ttk.Checkbutton(
                self.auto_save_download_setting_batch_download_frame,
                text=self.final_settings["language"]["batch_download_power"],
                variable=self.auto_save_download_setting_batch_download_power_var, command=check_settings_change)
            self.auto_save_download_setting_batch_download_power_checkbutton.grid(row=0, column=0, sticky=tk.W + tk.N)
            self.auto_save_download_setting_batch_download_parallel_var = tk.BooleanVar()
            self.auto_save_download_settings.append(self.auto_save_download_setting_batch_download_parallel_var)
            self.auto_save_download_setting_batch_download_parallel_var.set(
                bool(self.final_settings['default_setting']['auto_save_download_setting']['batch_download_parallel']))
            self.auto_save_download_setting_batch_download_parallel_checkbutton = ttk.Checkbutton(
                self.auto_save_download_setting_batch_download_frame,
                text=self.final_settings["language"]["batch_download_parallel"],
                variable=self.auto_save_download_setting_batch_download_parallel_var, command=check_settings_change)
            self.auto_save_download_setting_batch_download_parallel_checkbutton.grid(row=0, column=1,
                                                                                     sticky=tk.W + tk.N)
            self.auto_save_download_setting_batch_download_from_file_power_var = tk.BooleanVar()
            self.auto_save_download_settings.append(self.auto_save_download_setting_batch_download_from_file_power_var)
            self.auto_save_download_setting_batch_download_from_file_power_var.set(bool(
                self.final_settings['default_setting']['auto_save_download_setting'][
                    'batch_download_download_from_file_power']))
            self.auto_save_download_setting_batch_download_from_file_power_checkbutton = ttk.Checkbutton(
                self.auto_save_download_setting_batch_download_frame,
                text=self.final_settings["language"]["batch_download_download_from_file_power"],
                variable=self.auto_save_download_setting_batch_download_from_file_power_var,
                command=check_settings_change)
            self.auto_save_download_setting_batch_download_from_file_power_checkbutton.grid(row=0, column=2,
                                                                                            sticky=tk.W + tk.N)
            self.auto_save_download_setting_batch_download_from_file_path_var = tk.BooleanVar()
            self.auto_save_download_settings.append(self.auto_save_download_setting_batch_download_from_file_path_var)
            self.auto_save_download_setting_batch_download_from_file_path_var.set(bool(
                self.final_settings['default_setting']['auto_save_download_setting'][
                    'batch_download_download_from_file_path']))
            self.auto_save_download_setting_batch_download_from_file_path_checkbutton = ttk.Checkbutton(
                self.auto_save_download_setting_batch_download_frame,
                text=self.final_settings["language"]["batch_download_download_from_file_path"],
                variable=self.auto_save_download_setting_batch_download_from_file_path_var,
                command=check_settings_change)
            self.auto_save_download_setting_batch_download_from_file_path_checkbutton.grid(row=0, column=3,
                                                                                           sticky=tk.W + tk.N)
            self.auto_save_download_setting_batch_urls_var = tk.BooleanVar()
            self.auto_save_download_settings.append(self.auto_save_download_setting_batch_urls_var)
            self.auto_save_download_setting_batch_urls_var.set(
                bool(self.final_settings['default_setting']['auto_save_download_setting']['batch_download_urls']))
            self.auto_save_download_setting_batch_urls_checkbutton = ttk.Checkbutton(
                self.auto_save_download_setting_batch_download_frame,
                text=self.final_settings["language"]["batch_download_urls_show"],
                variable=self.auto_save_download_setting_batch_urls_var, command=check_settings_change)
            self.auto_save_download_setting_batch_urls_checkbutton.grid(row=0, column=4, sticky=tk.W + tk.N)
            self.auto_save_download_setting_batch_download_frame.grid(row=3, column=0, columnspan=9, sticky=tk.W + tk.N)

        self.auto_save_download_setting_detail_labelframe.grid(row=1, column=0, columnspan=9, sticky=tk.W + tk.N)
        self.auto_save_download_setting_labelframe.grid(row=2, column=0, columnspan=9, sticky=tk.W)

        self.settings_window_status_frame = tk.Frame(self.settings_window)
        # 按键栏
        self.settings_window_restore_default_settings_botton = ttk.Button(self.settings_window_status_frame,
                                                                          text=self.final_settings["language"][
                                                                              "restore_default_settings"],
                                                                          command=lambda: settings_set(
                                                                              self.default_settings))
        self.settings_window_restore_default_settings_botton.grid(row=0, column=1, sticky=tk.W)
        self.settings_window_accept_botton = ttk.Button(self.settings_window_status_frame,
                                                        text=self.final_settings["language"]["accept"],
                                                        command=lambda: [check_settings_change(), self.save_settings()])
        self.settings_window_accept_botton.grid(row=0, column=7, sticky=tk.E)
        self.settings_window_cancel_botton = ttk.Button(self.settings_window_status_frame,
                                                        text=self.final_settings["language"]["cancel"],
                                                        command=close_settings_window)
        self.settings_window_cancel_botton.grid(row=0, column=8, sticky=tk.E)

        self.settings_window_status_frame.grid(row=3, column=0, columnspan=9, sticky=tk.W)

        self.settings_window.protocol('WM_DELETE_WINDOW', lambda: close_settings_window())

    def save_settings(self):
        print('[INFO] Settings saving......')
        self.final_settings["default_setting"] = self.new_settings
        self.output_settings = {}
        for k, v in self.final_settings.items():
            if k != "language":
                self.output_settings[k] = v
        with open("you-get-gui.config", "w", encoding='utf-8') as f:
            json.dump(self.output_settings, f, ensure_ascii=False, sort_keys=False, indent=4,
                      separators=(',', ': '))
        print('[DEBUG]', self.final_settings)
        print('[INFO] Settings saved!')

    def save_download_settings(self):
        if self.final_settings["default_setting"]["auto_save_download_setting"]["power"]:
            print('[INFO] Download settings saving ......')
            if self.final_settings["default_setting"]["auto_save_download_setting"]["url"]:
                self.final_settings["download_setting"]["url"] = self.url_path.get()
            if self.final_settings["default_setting"]["auto_save_download_setting"]["save_path"]:
                self.final_settings["download_setting"]["save_path"] = self.path_entry.get()
            if self.final_settings["default_setting"]["auto_save_download_setting"]["save_name"]:
                self.final_settings["download_setting"]["save_name"] = self.new_name_entry.get()
            if self.final_settings["default_setting"]["auto_save_download_setting"]["print_with_json"]:
                self.final_settings["download_setting"]["print_with_json"] = self.print_info_as_json_var.get()
            if self.final_settings["default_setting"]["auto_save_download_setting"]["download_captions"]:
                self.final_settings["download_setting"]["download_captions"] = self.download_captions_var.get()
            if self.final_settings["default_setting"]["auto_save_download_setting"]["merge_video_parts"]:
                self.final_settings["download_setting"]["merge_video_parts"] = self.merge_video_parts_var.get()
            if self.final_settings["default_setting"]["auto_save_download_setting"]["download_m3u8_video"]:
                self.final_settings["download_setting"]["download_m3u8_video"] = self.download_m3u8_video_var.get()
            if self.final_settings["default_setting"]["auto_save_download_setting"]["ignore_ssl_errors"]:
                self.final_settings["download_setting"]["ignore_ssl_errors"] = self.ignore_ssl_errors_var.get()
            if self.final_settings["default_setting"]["auto_save_download_setting"]["forced_download"]:
                self.final_settings["download_setting"]["forced_download"] = self.forced_download_var.get()
            if self.final_settings["default_setting"]["auto_save_download_setting"]["skip_downloaded_video"]:
                self.final_settings["download_setting"]["skip_downloaded_video"] = self.skip_downloaded_video_var.get()
            if self.final_settings["default_setting"]["auto_save_download_setting"]["auto_rename"]:
                self.final_settings["download_setting"]["auto_rename"] = self.auto_rename_var.get()
            if self.final_settings["default_setting"]["auto_save_download_setting"]["download_video_password_power"]:
                self.final_settings["download_setting"]["download_video_password"][
                    "power"] = self.download_video_password_var.get()
            if self.final_settings["default_setting"]["auto_save_download_setting"]["download_video_password_value"]:
                self.final_settings["download_setting"]["download_video_password"][
                    "value"] = self.download_video_password_entry.get()
            if self.final_settings["default_setting"]["auto_save_download_setting"]["debug"]:
                self.final_settings["download_setting"]["debug"] = self.debug_var.get()
            if self.final_settings["default_setting"]["auto_save_download_setting"]["download_format_power"]:
                self.final_settings["download_setting"]["download_format"]["power"] = self.download_format_var.get()
            if self.final_settings["default_setting"]["auto_save_download_setting"]["download_format_value"]:
                self.final_settings["download_setting"]["download_format"]["value"] = self.download_format_entry.get()
            if self.final_settings["default_setting"]["auto_save_download_setting"]["download_itag_power"]:
                self.final_settings["download_setting"]["download_itag"]["power"] = self.download_itag_var.get()
            if self.final_settings["default_setting"]["auto_save_download_setting"]["download_itag_value"]:
                self.final_settings["download_setting"]["download_itag"]["value"] = self.download_itag_entry.get()
            if self.final_settings["default_setting"]["auto_save_download_setting"]["download_list_power"]:
                self.final_settings["download_setting"]["download_list"]["power"] = self.download_all_var.get()
            if self.final_settings["default_setting"]["auto_save_download_setting"]["download_list_page"]:
                self.final_settings["download_setting"]["download_list"]["page"] = self.download_all_page_entry.get()
            if self.final_settings["default_setting"]["auto_save_download_setting"]["download_list_start"]:
                self.final_settings["download_setting"]["download_list"]["start"] = self.download_all_start_entry.get()
            if self.final_settings["default_setting"]["auto_save_download_setting"]["download_list_end"]:
                self.final_settings["download_setting"]["download_list"]["end"] = self.download_all_end_entry.get()
            if self.final_settings["default_setting"]["auto_save_download_setting"]["use_cookies_power"]:
                self.final_settings["download_setting"]["use_cookies"]["power"] = self.use_cookies_var.get()
            if self.final_settings["default_setting"]["auto_save_download_setting"]["use_cookies_path"]:
                self.final_settings["download_setting"]["use_cookies"]["path"] = self.use_cookies_entry.get()
            if self.final_settings["default_setting"]["auto_save_download_setting"]["player_power"]:
                self.final_settings["download_setting"]["player"]["power"] = self.play_var.get()
            if self.final_settings["default_setting"]["auto_save_download_setting"]["player_path"]:
                self.final_settings["download_setting"]["player"]["path"] = self.player_entry.get()
            if self.final_settings["default_setting"]["auto_save_download_setting"]["player_argument"]:
                self.final_settings["download_setting"]["player"]["argument"] = self.play_exe_argument_entry.get()
            if self.final_settings["default_setting"]["auto_save_download_setting"]["run_in_new_window"]:
                if self.batch_download_parallel_var.get() and self.batch_download_power_var.get():
                    self.final_settings["download_setting"]["run_in_new_window"] = self.new_window_var_old
                else:
                    self.final_settings["download_setting"]["run_in_new_window"] = self.new_window_var.get()
            if self.final_settings["default_setting"]["auto_save_download_setting"]["proxy_power"]:
                self.final_settings["download_setting"]["proxy"]["power"] = self.proxy_setting_var.get()
            if self.final_settings["default_setting"]["auto_save_download_setting"]["proxy_no_proxy"]:
                self.final_settings["download_setting"]["proxy"]["no_proxy"] = self.no_proxy_var.get()
            if self.final_settings["default_setting"]["auto_save_download_setting"]["proxy_extracting_only"]:
                self.final_settings["download_setting"]["proxy"][
                    "extracting_only"] = self.proxy_extracting_only_var.get()
            if self.final_settings["default_setting"]["auto_save_download_setting"]["proxy_type"]:
                self.final_settings["download_setting"]["proxy"]["type"] = self.proxy_type_var.get()
            if self.final_settings["default_setting"]["auto_save_download_setting"]["proxy_host"]:
                self.final_settings["download_setting"]["proxy"]["host"] = self.proxy_path_entry.get()
            if self.final_settings["default_setting"]["auto_save_download_setting"]["proxy_login_power"]:
                self.final_settings["download_setting"]["proxy"]["login"]["power"] = self.proxy_login_var.get()
            if self.final_settings["default_setting"]["auto_save_download_setting"]["proxy_login_username"]:
                self.final_settings["download_setting"]["proxy"]["login"]["username"] = self.proxy_user_name_entry.get()
            if self.final_settings["default_setting"]["auto_save_download_setting"]["proxy_login_password"]:
                self.final_settings["download_setting"]["proxy"]["login"]["password"] = self.proxy_password_entry.get()
            if self.final_settings["default_setting"]["auto_save_download_setting"]["proxy_timeout_time_power"]:
                self.final_settings["download_setting"]["proxy"]["timeout_time"][
                    "power"] = self.proxy_time_out_var.get()
            if self.final_settings["default_setting"]["auto_save_download_setting"]["proxy_timeout_time_value"]:
                self.final_settings["download_setting"]["proxy"]["timeout_time"][
                    "value"] = self.proxy_time_out_entry.get()
            if self.final_settings["default_setting"]["auto_save_download_setting"]["batch_download_power"]:
                self.final_settings["download_setting"]["batch_download"]["power"] = self.batch_download_power_var.get()
            if self.final_settings["default_setting"]["auto_save_download_setting"]["batch_download_parallel"]:
                self.final_settings["download_setting"]["batch_download"][
                    "parallel"] = self.batch_download_parallel_var.get()
            if self.final_settings["default_setting"]["auto_save_download_setting"][
                "batch_download_download_from_file_power"]:
                self.final_settings["download_setting"]["batch_download"]["download_from_file"][
                    "power"] = self.batch_download_from_file_var.get()
            if self.final_settings["default_setting"]["auto_save_download_setting"][
                "batch_download_download_from_file_path"]:
                self.final_settings["download_setting"]["batch_download"]["download_from_file"][
                    "path"] = self.batch_download_file_path.get()
            if self.final_settings["default_setting"]["auto_save_download_setting"]["batch_download_urls"]:
                self.final_settings["download_setting"]["batch_download"]["urls"] = self.batch_download_links_text.get(
                    0.0, tk.END).splitlines()
            self.save_settings()
            print('[INFO] Download settings saved!')

    def install_you_get(self):
        os.system("start cmd /k pip install --upgrade you-get")
        tk.messagebox.showinfo(self.final_settings["language"]["hint"],
                               self.final_settings["language"]["install_update_you_get_hint"])

    def check_you_get_version(self):
        process = subprocess.Popen("you-get --version", stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   universal_newlines=True, shell=True)
        print('[DEBUG]', process.communicate())
        if process.communicate()[1].startswith("you-get: version"):
            you_get_version = process.communicate()[1].split(",")[0].replace("you-get: version ", "")
            tk.messagebox.showinfo(self.final_settings["language"]["you_get_version_check_title"],
                                   self.final_settings["language"]["you_get_version"] + you_get_version)
        else:
            tk.messagebox.showerror(self.final_settings["language"]["error"], process.communicate()[1])

    def check_define(self, step=0):

        def merge_settings(default_settings, user_settings):
            result = {}
            for key, value in default_settings.items():
                if key in user_settings:
                    if isinstance(value, dict) and isinstance(user_settings[key], dict):
                        result[key] = merge_settings(value, user_settings[key])
                        for k in user_settings[key]:
                            if k not in result[key]:
                                result[key][k] = user_settings[key][k]
                    elif isinstance(value, list) and isinstance(user_settings[key], list):
                        # 如果两个值都是列表，则将它们合并
                        result[key] = value + user_settings[key]
                    else:
                        result[key] = user_settings[key]
                else:
                    result[key] = value
            return result

        def merge_language_settings(default_settings, user_settings):
            # 确定程序界面语言设置
            program_language = user_settings["default_setting"]["language"]

            # 获取默认语言设置和用户语言设置
            default_language_settings = default_settings["languages"][program_language]
            user_language_settings = user_settings["languages"].get(program_language, {})

            # 创建一个新的字典来存储合并后的语言设置
            merged_language_settings = {}

            # 遍历默认语言设置中的所有项
            # for key, value in default_language_settings.items():
            #     # 如果用户设置中存在该项，则使用用户设置，否则使用默认设置
            #     merged_language_settings[key] = user_language_settings.get(key, value)
            for key, value in default_language_settings.items():
                merged_language_settings[key] = value

            merged_language_settings.update(user_language_settings)

            # 将合并后的语言设置赋值给final_settings
            self.final_settings["language"] = merged_language_settings

        """
        step=0: 检测并读取配置文件【you-get-gui.config】
        step=1: 根据【you-get-gui.config】中的内容设置各个控件的值
        """

        self.first_time_start = False

        if step == 0:
            if not os.path.isfile("you-get-gui.config"):
                with open("you-get-gui.config", "w", encoding='utf-8') as f:
                    json.dump(self.default_settings, f, ensure_ascii=False, sort_keys=False, indent=4,
                              separators=(',', ': '))
                self.first_time_start = True
            try:
                self.user_settings = json.load(open("you-get-gui.config", "r", encoding='utf-8'))
            except json.decoder.JSONDecodeError as error_type:
                print('[ERROR] Read [you-get-gui.config] error:', error_type)
                error_place = re.findall(r'\b(\d+)\b', str(error_type))
                tk.messagebox.showerror("错误！ Warning!",
                                        f"配置文件读取失败！Configuration file read failed!\n原因：文件【./you-get-gui.config】第 {error_place[0]} 行，第 {error_place[1]} 列（总第{error_place[2]}个字符）处出现问题！\n详情 Detail：{error_type}")
                self.user_settings = {"default_setting": {}, "download_setting": {}, "languages": {}}
            except Exception as error_type:
                tk.messagebox.showerror("错误！ Error!",
                                        f"配置文件读取失败！Configuration file read failed!\n原因：内部错误，请联系开发者！\nCause: Internal error, please contact developer!\n详情 Detail：{error_type}")
                self.user_settings = {"default_setting": {}, "download_setting": {}, "languages": {}}
            self.final_settings = merge_settings(self.default_settings, self.user_settings)
            self.new_window_var_old = self.final_settings['download_setting']['run_in_new_window']
            merge_language_settings(self.default_settings, self.user_settings)

            if self.first_time_start:
                self.about()
        elif step == 1:
            self.url_path.set(str(self.final_settings['download_setting']['url']))
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(tk.END, str(self.final_settings['download_setting']['save_path']))
            self.new_name_entry.delete(0, tk.END)
            self.new_name_entry.insert(tk.END, str(self.final_settings['download_setting']['save_name']))

            self.print_info_as_json_var.set(bool(self.final_settings['download_setting']['print_with_json']))
            self.download_captions_var.set(bool(self.final_settings['download_setting']['download_captions']))
            self.merge_video_parts_var.set(bool(self.final_settings['download_setting']['merge_video_parts']))

            self.download_m3u8_video_var.set(bool(self.final_settings['download_setting']['download_m3u8_video']))
            self.ignore_ssl_errors_var.set(bool(self.final_settings['download_setting']['ignore_ssl_errors']))
            self.forced_download_var.set(bool(self.final_settings['download_setting']['forced_download']))
            self.skip_downloaded_video_var.set(bool(self.final_settings['download_setting']['skip_downloaded_video']))
            self.auto_rename_var.set(bool(self.final_settings['download_setting']['auto_rename']))

            self.download_video_password_var.set(
                bool(self.final_settings['download_setting']['download_video_password']['power']))
            self.download_video_password_entry.config(state=tk.NORMAL)
            self.download_video_password_entry.delete(0, tk.END)
            self.download_video_password_entry.insert(tk.END, str(
                self.final_settings['download_setting']['download_video_password']['value']))
            self.download_video_password_entry.config(
                state="normal" if self.download_video_password_var.get() else "disabled")

            self.debug_var.set(bool(self.final_settings['download_setting']['debug']))

            self.download_format_var.set(bool(self.final_settings['download_setting']['download_format']['power']))
            self.download_format_entry.config(state=tk.NORMAL)
            self.download_format_entry.delete(0, tk.END)
            self.download_format_entry.insert(tk.END,
                                              str(self.final_settings['download_setting']['download_format']['value']))
            self.download_format_entry.config(state="normal" if self.download_format_var.get() else "disabled")

            self.download_itag_var.set(bool(self.final_settings['download_setting']['download_itag']['power']))
            self.download_itag_entry.config(state=tk.NORMAL)
            self.download_itag_entry.delete(0, tk.END)
            self.download_itag_entry.insert(tk.END,
                                            str(self.final_settings['download_setting']['download_itag']['value']))
            self.download_itag_entry.config(state="normal" if self.download_itag_var.get() else "disabled")

            self.download_all_var.set(bool(self.final_settings['download_setting']['download_list']['power']))
            self.download_all_page_entry.config(state=tk.NORMAL)
            self.download_all_page_entry.delete(0, tk.END)
            self.download_all_page_entry.insert(tk.END,
                                                str(self.final_settings['download_setting']['download_list']['page']))
            self.download_all_start_entry.config(state=tk.NORMAL)
            self.download_all_start_entry.delete(0, tk.END)
            self.download_all_start_entry.insert(tk.END,
                                                 str(self.final_settings['download_setting']['download_list']['start']))
            self.download_all_end_entry.config(state=tk.NORMAL)
            self.download_all_end_entry.delete(0, tk.END)
            self.download_all_end_entry.insert(tk.END,
                                               str(self.final_settings['download_setting']['download_list']['end']))
            self.download_all_start_label.config(foreground='black' if self.download_all_var.get() else 'gray'),
            self.download_all_page_entry.config(state='normal' if self.download_all_var.get() else 'disabled'),
            self.download_all_front_label.config(foreground='black' if self.download_all_var.get() else 'gray'),
            self.download_all_start_entry.config(state='normal' if self.download_all_var.get() else 'disabled'),
            self.download_all_middle_label.config(foreground='black' if self.download_all_var.get() else 'gray'),
            self.download_all_end_entry.config(state='normal' if self.download_all_var.get() else 'disabled'),
            self.download_all_end_label.config(foreground='black' if self.download_all_var.get() else 'gray')

            self.use_cookies_var.set(bool(self.final_settings['download_setting']['use_cookies']['power']))
            self.use_cookies_entry.config(state=tk.NORMAL)
            self.use_cookies_entry.delete(0, tk.END)
            self.use_cookies_entry.insert(tk.END, str(self.final_settings['download_setting']['use_cookies']['path']))
            self.use_cookies_entry.config(state='normal' if self.use_cookies_var.get() else 'disabled'),
            self.use_cookies_button.config(state='normal' if self.use_cookies_var.get() else 'disabled')

            self.play_var.set(bool(self.final_settings['download_setting']['player']['power']))
            self.player_entry.config(state=tk.NORMAL)
            self.player_entry.delete(0, tk.END)
            self.player_entry.insert(tk.END, str(self.final_settings['download_setting']['player']['path']))
            self.play_exe_argument_entry.config(state=tk.NORMAL)
            self.play_exe_argument_entry.delete(0, tk.END)
            self.play_exe_argument_entry.insert(tk.END,
                                                str(self.final_settings['download_setting']['player']['argument']))

            self.player_entry.config(state='normal' if self.play_var.get() else 'disabled'),
            self.play_exe_argument_label.config(foreground='black' if self.play_var.get() else 'gray'),
            self.play_exe_argument_entry.config(state='normal' if self.play_var.get() else 'disabled'),
            self.play_button.config(state='normal' if self.play_var.get() else 'disabled'),
            self.download_button.config(text=self.final_settings["language"]["start_play"] if self.play_var.get() else
            self.final_settings["language"]["start_download"],
                                        command=self.play if self.play_var.get() else self.lunch_download)

            self.new_window_var.set(bool(self.final_settings['download_setting']['run_in_new_window']))
            self.new_window_var_old = bool(self.final_settings['download_setting']['run_in_new_window'])

            self.no_proxy_var.set(bool(self.final_settings['download_setting']['proxy']['no_proxy']))
            self.proxy_setting_var.set(bool(self.final_settings['download_setting']['proxy']['power']))
            self.proxy_extracting_only_var.set(
                bool(self.final_settings['download_setting']['proxy']['extracting_only']))
            self.proxy_type_var.set(str(self.final_settings['download_setting']['proxy']['type']))
            self.proxy_path_entry.config(state=tk.NORMAL)
            self.proxy_path_entry.delete(0, tk.END)
            self.proxy_path_entry.insert(tk.END, str(self.final_settings['download_setting']['proxy']['host']))
            self.proxy_path_entry.config(state="normal" if self.proxy_type_var.get() else "disabled")
            self.proxy_login_var.set(bool(self.final_settings['download_setting']['proxy']['login']['power']))
            self.proxy_user_name_entry.config(state=tk.NORMAL)
            self.proxy_user_name_entry.delete(0, tk.END)
            self.proxy_user_name_entry.insert(tk.END, str(
                self.final_settings['download_setting']['proxy']['login']['username']))
            self.proxy_password_entry.config(state=tk.NORMAL)
            self.proxy_password_entry.delete(0, tk.END)
            self.proxy_password_entry.insert(tk.END,
                                             str(self.final_settings['download_setting']['proxy']['login']['password']))
            self.proxy_user_name_entry.config(state="normal" if self.proxy_login_var.get() else "disabled")
            self.proxy_password_entry.config(state="normal" if self.proxy_login_var.get() else "disabled")
            self.proxy_time_out_var.set(bool(self.final_settings['download_setting']['proxy']['timeout_time']['power']))
            self.proxy_time_out_entry.config(state=tk.NORMAL)
            self.proxy_time_out_entry.delete(0, tk.END)
            self.proxy_time_out_entry.insert(tk.END, str(
                self.final_settings['download_setting']['proxy']['timeout_time']['value']))
            self.proxy_time_out_entry.config(state="normal" if self.proxy_time_out_var.get() else "disabled")
            self.no_proxy_button_check()

            self.batch_download_power_var.set(bool(self.final_settings['download_setting']['batch_download']['power']))
            self.batch_download_parallel_var.set(
                bool(self.final_settings['download_setting']['batch_download']['parallel']))
            self.batch_download_parallel(step=1)
            self.batch_download_from_file_var.set(
                bool(self.final_settings['download_setting']['batch_download']['download_from_file']['power']))
            self.batch_download_file_path.set(
                str(self.final_settings["download_setting"]["batch_download"]["download_from_file"]["path"]))
            self.batch_download_links_text.config(state=tk.NORMAL)
            self.batch_download_links_text.delete(0.0, tk.END)
            for link in list(self.final_settings['download_setting']['batch_download']['urls']):
                self.batch_download_links_text.insert(tk.END, str(link) + '\n')
            self.batch_download_links_text.config(
                state="normal" if not self.batch_download_from_file_var.get() and self.batch_download_power_var.get() else "disabled")
            self.batch_download_power(step=1)

    def mainloop(self):
        self.root.protocol('WM_DELETE_WINDOW', self.exit_program)
        if str(self.final_settings['default_setting']['window_type']) == '2':
            self.download_log_window.withdraw()
            self.download_settings_window.withdraw()
            self.download_log_window.protocol('WM_DELETE_WINDOW', lambda: self.download_log_window.withdraw())
            self.download_settings_window.protocol('WM_DELETE_WINDOW', lambda: self.download_settings_window.withdraw())
        # self.settings()
        self.root.lift()
        self.root.mainloop()

    def exit_program(self):
        if self.final_settings['default_setting']['exit_with_hint']:
            # 监听到关闭窗体的后，弹出提示信息框，提示是否真的要关闭，若是的话，则关闭
            if tk.messagebox.askyesno(self.final_settings["language"]["hint"],
                                      self.final_settings["language"]["whether_exit"]):
                self.save_download_settings()
                sys.exit()
        else:
            self.save_download_settings()
            sys.exit()

    class EnhancedTooltip:
        def __init__(self, outer_instance, widget, text="", del_class=False, **kwargs):
            self.final_settings = outer_instance.final_settings
            if not self.final_settings['default_setting']['show_hover_tip'] or text == "":
                return
            self.del_class = del_class
            self.widget = widget
            self.tip_window = None
            # 设置提示框相对于鼠标指针的偏移量
            self.offset = (10, 5)
            # 存储默认样式参数，如果用户未指定则使用这些参数
            self.default_style = {
                'background': 'white',
                'relief': 'solid',
                'borderwidth': 1,
                'font': (None, 10)
            }
            # 更新默认样式参数，包括用户自定义的参数
            self.style_params = {**self.default_style, **kwargs}
            self.text = text
            # 绑定鼠标进入和离开事件
            self.bind_events()

        def bind_events(self):
            # 当鼠标悬停时调用显示提示的函数
            self.widget.bind("<Enter>", self.show_tip)
            # 当鼠标离开时调用隐藏提示的函数
            self.widget.bind("<Leave>", self.hide_tip)

        def show_tip(self, event=None):
            if not self.final_settings['default_setting']['show_hover_tip'] or self.del_class:
                self.hide_tip()
                return

            """显示提示信息，使用当前绑定的文本和样式参数。"""
            if self.tip_window:
                self.tip_window.destroy()
            # 获取鼠标指针的当前位置
            x, y = self.widget.winfo_pointerxy()
            # 应用偏移量
            x, y = x + self.offset[0], y + self.offset[1]
            # 创建并显示提示窗口
            self.tip_window = self.create_tip_window(x, y, self.text, self.style_params)

        def hide_tip(self, event=None):
            """隐藏提示信息，如果提示窗口存在则销毁它。"""
            if self.tip_window:
                self.tip_window.destroy()
                self.tip_window = None

        def create_tip_window(self, x, y, text, style_params):
            """根据指定的文本、位置和样式参数创建提示窗口。"""
            # 创建顶层窗口，不显示窗口边框
            tip = tk.Toplevel(self.widget, borderwidth=0)
            tip.overrideredirect(True)
            tip.geometry(f"+{x}+{y}")  # 设置窗口位置

            # 创建标签并设置文本和样式
            label = ttk.Label(tip, text=text, **style_params)
            label.pack(ipadx=1, ipady=1, fill="both", expand=True)  # 设置标签填充方式

            return tip


import sys

try:
    YouGet = YouGetGui()
    YouGet.mainloop()
except Exception as e:
    # 将错误信息保存至文件
    if sys.argv[1] == "debug":
        with open("error.log", "a+") as f:
            f.write('-------------------------------------------------------------------\n' + str(e) + '\n')
