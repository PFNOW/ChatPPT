import json
import requests
from openai import OpenAI  # 导入OpenAI库用于访问GPT模型
from logger import LOG  # 导入日志模块

class LLM:
    def __init__(self, config):
        """
        初始化 LLM 类，根据配置选择使用的模型（OpenAI 或 Ollama）。

        :param config: 配置对象，包含所有的模型配置参数。
        """
        self.config = config
        self.model = config.llm_model_type.lower()  # 获取模型类型并转换为小写
        self.conversation_history = []  # 全局变量，用于存储对话历史记录
        if self.model == "openai":
            from openai import OpenAI  # 导入OpenAI库用于访问GPT模型
            self.client = OpenAI(base_url=self.config.openai_url, api_key=self.config.openai_token)  # 创建OpenAI客户端实例
        elif self.model == "ollama":
            self.api_url = self.config.ollama_api_url  # 设置Ollama API的URL
        else:
            raise ValueError(f"Unsupported model type: {self.model}")  # 如果模型类型不支持，抛出错误

        # 从TXT文件加载系统提示信息
        with open("prompts/formatter.txt", "r", encoding='utf-8') as file:
            self.system_prompt = file.read()

    def generate_pptx_md(self, markdown_content, dry_run=False):
        """
        生成pptx文稿，根据配置选择不同的模型来处理请求。

        :param markdown_content: 用户提供的Markdown内容。
        :param dry_run: 如果为True，提示信息将保存到文件而不实际调用模型。
        :return: 生成的内容或"DRY RUN"字符串。
        """
        # 准备消息列表，包含系统提示和用户内容
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": markdown_content},
        ]

        if dry_run:
            # 如果启用了dry_run模式，将不会调用模型，而是将提示信息保存到文件中
            LOG.info("Dry run mode enabled. Saving prompt to file.")
            with open("prompts/prompt.txt", "w+") as f:
                json.dump(messages, f, indent=4, ensure_ascii=False)  # 将消息保存为JSON格式
            LOG.debug("Prompt已保存到 prompts/prompt.txt")
            return "DRY RUN"

        # 根据选择的模型调用相应的生成报告方法
        if self.model == "openai":
            self.client = OpenAI(base_url=self.config.openai_url, api_key=self.config.openai_token)  # 创建OpenAI客户端实例
            return self._generate_report_openai(messages)
        elif self.model == "ollama":
            self.api_url = self.config.ollama_api_url  # 设置Ollama API的URL
            return self._generate_report_ollama(messages)
        else:
            raise ValueError(f"Unsupported model type: {self.model}")

    def chat_with_gpt(self,user_input, system_prompt=None):
        """
        使用 LLM 聊天。

        :param user_input: 包含用户内容的消息列表。
        :param system_prompt: 系统提示信息。
        :return: 生成的报告内容
        """
        # 与 OpenAI 接口交互函数
        self.client = OpenAI(base_url=self.config.openai_url, api_key=self.config.openai_token)  # 创建OpenAI客户端实例
        # 使用默认的 system prompt 如果用户没有输入
        if system_prompt:
            self.system_prompt = system_prompt
        # 构造完整的消息列表
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": user_input}
        ]
        # 调用 API
        LOG.info("使用 OpenAI GPT 模型开始生成。")
        try:
            response = self.client.chat.completions.create(
                model=self.config.openai_model_name,
                messages=messages
            )
            LOG.debug("GPT response: {}", response)
            assistant_reply = response.choices[0].message.content
        except Exception as e:
            assistant_reply = f"Error: {e}"
        # 更新对话上下文
        self.conversation_history.append({"role": "user", "content": user_input})
        # 将回复添加到对话历史中
        self.conversation_history.append({"role": "assistant", "content": assistant_reply})
        # 控制对话上下文长度（保留最近 10 条）
        if len(self.conversation_history) > 10:
            self.conversation_history = self.conversation_history[-10:]
        return assistant_reply

    def _generate_report_openai(self, messages):
        """
        使用 OpenAI GPT 模型生成报告。
        
        :param messages: 包含系统提示和用户内容的消息列表。
        :return: 生成的报告内容。
        """
        LOG.info("使用 OpenAI GPT 模型开始生成。")
        try:
            response = self.client.chat.completions.create(
                model=self.config.openai_model_name,  # 使用配置中的OpenAI模型名称
                messages=messages
            )
            LOG.debug("GPT response: {}", response)
            return response.choices[0].message.content  # 返回生成的报告内容
        except Exception as e:
            LOG.error(f"生成时发生错误：{e}")
            raise

    def _generate_report_ollama(self, messages):
        """
        使用 Ollama LLaMA 模型生成报告。

        :param messages: 包含系统提示和用户内容的消息列表。
        :return: 生成的报告内容。
        """
        headers = {
            "Authorization": f"Bearer {self.config.ollama_api_key}",  # 使用配置中的Ollama API密钥
            "Content-Type": "application/json"
            }
        LOG.info("使用 Ollama 托管模型服务开始生成。")
        try:
            payload = {
                "model": self.config.ollama_model_name,  # 使用配置中的Ollama模型名称
                "messages": messages
            }
            response = requests.post(self.api_url,headers=headers, json=payload)  # 发送POST请求到Ollama API
            response_data = response.json()

            # 调试输出查看完整的响应结构
            LOG.debug("Ollama response: {}", response_data)

            # 直接从响应数据中获取 content
            message_content = response_data['choices'][0]['message']['content']
            if message_content:
                return message_content  # 返回生成的报告内容
            else:
                LOG.error("无法从响应中提取内容。")
                raise ValueError("Invalid response structure from Ollama API")
        except Exception as e:
            LOG.error(f"生成时发生错误：{e}")
            raise

    def switch_api(self, api_name):
        self.model = api_name.lower()



if __name__ == '__main__':
    from config import Config  # 导入配置管理类
    config = Config()
    llm = LLM(config)

    markdown_content="""
第五次作业
1.使用 python-pptx 自动生成 PowerPoint 文件，内容包括文本、图片、表格和图表 。
2.使用 Gradio 搭建一个 ChatBot 作为图形化用户界面（GUI），支持将用户输入转换为 ChatPPT PowerPoint 标准输入格式（Markdown），并最终生成 PowerPoint 文件。
2.1ChatBot System Prompt 可使用 ChatPPT v0.2 prompts/formatter.txt 文件，鼓励自行创作和优化。
2.2【可选】将 ChatBot 生成 Markdown 和 ChatPPT v0.2 的主流程整合，支持聊天输入，自动生成 PowerPoint 文件作为输出。
3.作业提交方式：将修改后的代码文件链接复制粘贴至下方评论框内并点击提交按钮即可。
"""

    report = llm.chat_with_gpt(markdown_content)
    print(report)
