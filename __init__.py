# MIT License
# Copyright (c) 2025 EveGlow
#region 导入模块
from PySide6.QtCore import QFile, Qt, QTimer
from PySide6.QtWidgets import *

from . import settings

from SRACore.util import system as WindowsProcess
from SRACore.util.logger import logger
from SRACore.util.logger import log_emitter
from SRACore.util.plugin import PluginBase
from SRACore.util.operator import Operator
from SRACore.util.config import ConfigManager as SRACoreConfigManager

from ctypes import windll
import json
import os
import psutil
import subprocess
import threading
import time
#endregion


#region 配置管理
class PluginConfigManager:
    def __init__(self):
        super().__init__()
        with open("plugins/StarRailAssistant-Plugin-Project-RA-X/config.json", "r") as f:
            self.config = json.load(f)
        self.showLog = self.config["showLog"]
        self.check_task = self.config["check_task"]
        if self.check_task:
            global check_task_inside
            check_task_inside = True
        self.check_delay = self.config["check_delay"]
        self.lang = self.config["lang"]

    def reload_config(self):
        self.showLog = self.config["showLog"]
        self.check_task = self.config["check_task"]
        if self.check_task:
            global check_task_inside
            check_task_inside = True
        self.check_delay = self.config["check_delay"]
        self.lang = self.config["lang"]

    def change_config(self, key, value):
        self.config[key] = value
        json.dump(self.config, open("plugins/StarRailAssistant-Plugin-Project-RA-X/config.json", "w"))
#endregion


#region 变量
check_task_inside = False
daily_task_completed = False
starting_check = False
cfgw = None
cfgm = PluginConfigManager()
operator = Operator()
task_checker_thread = None  # 任务检测线程实例
log_listener_connected = False  # 日志监听器连接状态
# runt = Main()
# 逻辑：重构该类实现方式
#endregion


#region 透明日志窗口
class TransparentLogWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("日志窗口")
        self.setGeometry(100, 100, 500, 200)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)  # 设置窗口背景透明
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Tool)  # 无边框窗口，保持最前显示，隐藏任务栏图标
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)  # 设置鼠标事件穿透
        # self.move(QApplication.primaryScreen().geometry().bottomLeft() - self.rect().bottomLeft() + QPoint(0, -300))  # 定位窗口到屏幕底部任务栏上方
        # 设置窗口无边框样式
        self.setStyleSheet("background-color: transparent; border: none;")

        # 初始化日志显示文本框
        self.log_view = QTextEdit(self)
        self.log_view.setStyleSheet("background-color: transparent; color: white;")  # 透明背景，白色文字
        self.log_view.setReadOnly(True)  # 只读模式
        self.log_view.setLineWrapMode(QTextEdit.LineWrapMode.WidgetWidth)  # 按窗口宽度自动换行
        self.log_view.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)  # 禁用水平滚动条
        self.log_view.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)  # 禁用垂直滚动条
        self.log_view.setFocusPolicy(Qt.FocusPolicy.NoFocus)  # 禁止文本框获取焦点
        self.log_view.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)  # 禁用右键菜单

        # 初始化自动定位定时器
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.update_location)
        self.timer.start()

        layout = QVBoxLayout(self)
        layout.addWidget(self.log_view)

        # 设置窗口不能进行点击操作
        hwnd = int(self.winId())
        ex_style = windll.user32.GetWindowLongW(hwnd, -20)
        windll.user32.SetWindowLongW(hwnd, -20, ex_style | 0x80000 | 0x20)

    def scroll_to_bottom(self):
        """自动滚动到文本框底部"""
        self.log_view.verticalScrollBar().setValue(self.log_view.verticalScrollBar().maximum())

    def update_log(self, msg):
        """
        更新日志显示内容

        参数:
            msg: 日志消息对象，包含level和message等信息
        """
        color_map = {
            "INFO": "#90EE90",
            "WARNING": "yellow",
            "ERROR": "red",
            "SUCCESS": "green",
            # "DEBUG": "lightblue" 测试可用
        }
        _, time, level, *message = msg.split(" ")
        if level.upper() not in ["INFO", "WARNING", "ERROR", "SUCCESS"]:
            return

        color = color_map.get(level.upper(), "white")
        # 构建带有阴影效果和颜色的HTML格式日志文本
        font_family = "Microsoft YaHei Mono, Consolas, monospace"
        html_text = (
            f'<div style="font-size:14px; font-weight:bold; font-family:\'{font_family}\'; '
            f'padding: 2px 6px;">'
            f'<span style="color:#D8BFD8">{time}</span> <span style="color:{color}">[{level}] </span> <span style="color:#7B68EE"> {"".join(message)}</span>'
            f'</div>'
        )
        self.log_view.append(html_text)
        self.scroll_to_bottom()

    def update_location(self):
        self.setVisible(WindowsProcess.is_process_running("StarRail.exe"))  # 检查游戏窗口是否激活
        region = operator.get_win_region()
        if region:
            top = region.top / operator.zoom
            left = region.left / operator.zoom
            self.setGeometry(int(left), int(top + 450), 500, 200)

    def closeEvent(self, event):
        """
        窗口关闭事件处理

        参数:
            event: 关闭事件对象
        """
        print("窗口关闭，退出程序")
        event.accept()  # 接受关闭事件



#region 任务执行器
class TaskExecutor:
    """任务重新执行器"""
    
    def __init__(self):
        self.main_instance = None
        self.is_executing = False
    
    def set_main_instance(self, main_instance):
        """设置SRA主实例引用"""
        self.main_instance = main_instance
    
    def execute_task(self, config_name=None):
        """
        执行任务

        Args:
            config_name: 配置方案名称，如果为None则使用当前配置
        """
        if self.is_executing:
            logger.warning("任务正在执行中，请等待完成后再试")
            return False

        if self.main_instance is None:
            logger.error("未找到SRA主实例，无法执行任务")
            return False

        if self.main_instance.task_thread.isRunning():
            logger.warning("SRA主程序正在运行任务，请等待完成后再试")
            return False

        try:
            self.is_executing = True
            logger.info("ProjectRAX: 开始执行任务")

            if config_name:
                # 使用指定配置执行 - 设置全局配置管理器
                from SRACore.util.config import GlobalConfigManager
                gcm = GlobalConfigManager()
                gcm.set('current_config', config_name)
                logger.info(f"ProjectRAX: 切换到配置 {config_name}")
            else:
                # 确保使用当前配置
                pass

            # 启动任务线程
            self.main_instance.task_thread.start()

            return True

        except Exception as e:
            logger.error(f"执行任务时发生错误: {e}")
            return False
        finally:
            self.is_executing = False
    
    def stop_task(self):
        """停止当前任务"""
        if self.main_instance and self.main_instance.task_thread.isRunning():
            self.main_instance.task_thread.stop()
            logger.info("ProjectRAX: 已请求停止任务")
            return True
        return False
    
    def get_available_configs(self):
        """获取可用的配置方案列表"""
        try:
            from SRACore.util.config import GlobalConfigManager
            gcm = GlobalConfigManager()
            return gcm.get('config_list', ['default'])
        except Exception as e:
            logger.error(f"获取配置列表失败: {e}")
            return ['default']

# 全局任务执行器实例
task_executor = TaskExecutor()


#region 日志监听器
def log_message_listener(msg):
    """
    监听日志消息，检测任务完成状态

    Args:
        msg: 日志消息字符串
    """
    global daily_task_completed, starting_check

    if "任务全部完成" in msg:
        logger.info("ProjectRAX: 检测到任务全部完成信号")
        daily_task_completed = True
        starting_check = True  # 开始检测周期

def connect_log_listener():
    """连接日志监听器"""
    global log_listener_connected
    if not log_listener_connected:
        log_emitter.log_signal.connect(log_message_listener)
        log_listener_connected = True
        logger.info("ProjectRAX: 日志监听器已连接")
#endregion



#region 检测任务
class TaskCheckerThread(threading.Thread):
    def __init__(self):
        super().__init__()
        cfgm.reload_config()
        self.delay = cfgm.check_delay
        self.check_task = cfgm.check_task
        self.running = True

    def stop(self):
        """停止检测线程"""
        self.running = False

    def run(self):
        global daily_task_completed, starting_check

        logger.info("ProjectRAX: 任务检测线程已启动")

        while self.running and self.check_task:
            cfgm.reload_config()
            if not self.check_task:
                break

            # 检查是否需要执行每日任务
            if not daily_task_completed:
                logger.info("ProjectRAX: 检测到每日任务未完成，开始执行")
                if task_executor.execute_task():
                    logger.info("ProjectRAX: 任务执行已开始，等待完成信号")
                    # 设置starting_check为True，等待任务完成信号
                    starting_check = True
                else:
                    logger.error("ProjectRAX: 任务执行失败，将在下个周期重试")
            else:
                logger.debug("ProjectRAX: 每日任务已完成")

            # 等待指定时间后再次检查
            time.sleep(cfgm.check_delay * 60)




#region 设置窗口
class ConfigWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = settings.Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.checkbox_display.stateChanged.connect(self.changecfg_static)
        self.ui.spinBox.valueChanged.connect(self.changecfg_static)
        self.ui.btn_enable_taskflag.clicked.connect(self.enable_taskcheck)
        self.ui.button_enable_processprotect.clicked.connect(self.enable_processprotect)
        
        # 添加手动执行任务按钮
        self.manual_execute_button = QPushButton("手动执行任务", self)
        self.manual_execute_button.clicked.connect(self.manual_execute_task)
        # 将按钮添加到界面（需要根据实际UI布局调整）
        
        # 添加配置选择下拉框
        self.config_combo = QComboBox(self)
        self.refresh_config_list()

    def refresh_config_list(self):
        """刷新配置列表"""
        configs = task_executor.get_available_configs()
        self.config_combo.clear()
        self.config_combo.addItem("使用当前配置", None)
        for config in configs:
            self.config_combo.addItem(config, config)

    def manual_execute_task(self):
        """手动执行任务"""
        selected_config = self.config_combo.currentData()
        if task_executor.execute_task(selected_config):
            logger.info("ProjectRAX: 手动任务执行已开始")
        else:
            logger.error("ProjectRAX: 手动任务执行失败")

    def changecfg_static(self):
        showLog = self.ui.checkbox_display.isChecked()
        check_delay = self.ui.spinBox.value()
        
        cfgm.change_config("showLog", showLog)
        cfgm.change_config("check_delay", check_delay)
    
    def enable_taskcheck(self):
        global check_task_inside, task_checker_thread, daily_task_completed

        if not check_task_inside:
            check_task_inside = True
            cfgm.change_config("check_task", True)
            # 重置每日任务状态，准备重新检测
            daily_task_completed = False
            # 连接日志监听器
            connect_log_listener()
            # 启动任务检测线程
            if task_checker_thread is None or not task_checker_thread.is_alive():
                task_checker_thread = TaskCheckerThread()
                task_checker_thread.daemon = True
                task_checker_thread.start()
            logger.info("ProjectRAX: 任务检测已启用")
        else:
            logger.warning("ProjectRAX: 任务检测已开启")
    
    def enable_processprotect(self):
        global check_task_inside, task_checker_thread
        cfgm.reload_config()
        for proc in psutil.process_iter(["name"]):
            try:
                if proc.info["name"] == "ProcessProtector.exe":
                    logger.error("ProjectRAX: 已经启用了进程守护，不能再次启动！")
                    return
            except (psutil.NoSuchProcess, psutil.ZombieProcess):
                pass

        # 启动进程保护器
        subprocess.Popen([os.path.join(os.getcwd(),"plugins","StarRailAssistant-Plugin-Project-RA-X","process_protector","protector.exe")])

        # 如果任务检测未启用，启用并启动
        if not check_task_inside:
            check_task_inside = True
            cfgm.change_config("check_task", True)
            connect_log_listener()
            if task_checker_thread is None or not task_checker_thread.is_alive():
                task_checker_thread = TaskCheckerThread()
                task_checker_thread.daemon = True
                task_checker_thread.start()

        logger.info("ProjectRAX: 进程保护已启用")
        os._exit(0)



#region 插件主入口
class MainEntrance(PluginBase):
    """插件主入口类"""

    def __init__(self):
        """初始化插件"""
        super().__init__(self.__class__.__name__)
        self.window = None  # 日志窗口实例

    def show_window(self):
        """显示日志窗口"""
        self.window = TransparentLogWindow()
        self.window.show()
        logger.info("插件启动成功。")  # 记录启动日志



#region 入口
# 全局变量用于存储主实例引用
main_instance_ref = None

def set_main_instance(main_instance):
    """设置SRA主实例引用（由主程序调用）"""
    global main_instance_ref
    main_instance_ref = main_instance
    task_executor.set_main_instance(main_instance)
    logger.info("ProjectRAX: 已获取SRA主实例引用")

if __name__ != "__main__":
    """作为插件运行时注册插件"""
    cfg = PluginConfigManager()
    cfg.reload_config()
    if cfg.showLog:
        log_window = TransparentLogWindow()
        log_window.show()
        log_emitter.log_signal.connect(log_window.update_log)

    # 如果启用了任务检测，启动相关组件
    if cfg.check_task:
        connect_log_listener()
        if task_checker_thread is None or not task_checker_thread.is_alive():
            task_checker_thread = TaskCheckerThread()
            task_checker_thread.daemon = True
            task_checker_thread.start()
        logger.info("ProjectRAX: 任务检测已自动启用")

    logger.info("插件启动成功。")  # 记录启动日志

def run():
    global cfgw
    cfgw = ConfigWindow()
    cfgw.show()


if __name__ == "__main__":
    """直接运行时的提示信息"""
    input("还没想好如何实现主窗口，但你可以键入'Enter'退出程序喵~")

