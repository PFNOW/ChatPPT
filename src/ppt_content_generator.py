import os
import re

from logger import LOG  # 引入日志模块
from llm import LLM  # 引入LLM模块

class PPTContentGenerator:
    def __init__(self, llm: LLM):
        self.llm = llm  # 初始化时接受一个LLM实例，用于后续生成内容

    # 读取Markdown文件并使用LLM生成pptx文稿
    def generate_pptx_md(self, markdown_file_path):
        with open(markdown_file_path, 'r', encoding='utf-8') as file:
            markdown_content = file.read()
        report = self.llm.generate_pptx_md(markdown_content)  # 调用LLM生成
        title = "NewPPT"  # 获取内容标题
        lines = report.splitlines()
        for line in lines:
            print(line)
            if line.startswith('# '):  # 检查是否以"# "开头，表示一级标题
                title = re.sub(r'[<>:"/\\|?*]', '', line[2:])  # 返回第一个找到的一级标题，去掉"# "前缀和多余的空格
        pptx_md_path = "inputs/" + title + ".md"  # 保存生成的pptx文稿
        with open(pptx_md_path, 'w+') as report_file:
            report_file.write(report)  # 写入生成的内容
        LOG.info(f"pptx文稿已保存到 {pptx_md_path}")
        return report, pptx_md_path

    # 切换API，用于测试不同API的效果
    def switch_api(self, api_name):
        # 切换LLM使用的API
        self.llm.switch_api(api_name)


if __name__ == '__main__':
    from config import Config  # 导入配置管理类
    config = Config()
    llm = LLM(config)
    ppt_content_generator = PPTContentGenerator(llm)

    markdown_content="inputs/test.txt"

    report = ppt_content_generator.generate_pptx_md(markdown_content)
    print(report)