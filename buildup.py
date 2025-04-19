import subprocess
import platform
import sys
import codecs
import os


sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

PLATFORM = platform.system()
ARCHITECTURE = platform.machine()
# 针对i386架构，由于AMD64架构的宿主机下，i386容器不会通过QEMU全虚拟化，因此会错误地获取到amd64架构
# 此修正仅适用于宿主机为AMD64架构的情况
print(platform.architecture()[0])
if (ARCHITECTURE == "x86_64") & (platform.architecture()[0] == "32bit"):
    ARCHITECTURE = "i386"
APP_NAME = "lrcapi"
APP_VERSION = "1.0.0"
PACK_NAME = f"{APP_NAME}-{APP_VERSION}-{PLATFORM}-{ARCHITECTURE}{'.exe' if PLATFORM == 'Windows' else ''}"

# 打包
def generate_add_data_options(root_dir):
    options = []
    for root, dirs, files in os.walk(root_dir):
        if files:
            # 将目录路径转换为 PyInstaller 可接受的格式
            formatted_path = root.replace("\\", "/")
            separator = ";" if PLATFORM == "Windows" else ":"
            options.append(f'--add-data "{formatted_path}/*{separator}{formatted_path}/"')
    return " ".join(options)


options = generate_add_data_options("/")
command = f"pyinstaller -F -i logo.png {options} app.py -n {PACK_NAME}"
subprocess.run(command, shell=True)
