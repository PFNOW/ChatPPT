import json
import os

class Config:
    def __init__(self, config_file='config.json'):
        self.config_file = config_file
        self.load_config()
    
    def load_config(self):
        # 检查 config 文件是否存在
        if not os.path.exists(self.config_file):
            raise FileNotFoundError(f"Config file '{self.config_file}' not found.")

        with open(self.config_file, 'r') as f:
            config = json.load(f)
            
            # 加载 ChatPPT 运行模式（默认文本模态）
            self.input_mode = config.get('input_mode', "text")
            
            # 加载 PPT 默认模板
            self.ppt_template = config.get('ppt_template', "templates/MasterTemplate.pptx")
            
            # 加载布局映射
            self.layout_mapping = config.get('layout_mapping', {})

            # 加载 LLM 相关配置
            llm_config = config.get('llm', {})
            self.openai_token = os.getenv("OPENAI_TOKEN", llm_config.get('openai_token'))
            self.openai_url = os.getenv("OPENAI_URL", llm_config.get('openai_url'))
            self.llm_model_type = llm_config.get('model_type', 'openai')
            self.openai_model_name = llm_config.get('openai_model_name', 'gpt-4o-mini')
            self.ollama_model_name = llm_config.get('ollama_model_name', 'llama3')
            self.ollama_api_url = llm_config.get('ollama_api_url', 'http://localhost:3000/api/chat/completions')
            self.ollama_api_key = os.getenv("OLLAMA_API_KEY", llm_config.get('ollama_api_key'))
