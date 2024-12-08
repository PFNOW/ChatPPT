from data_structures import SlideContent, Slide
from layout_manager import LayoutManager

# SlideBuilder 类用于构建单张幻灯片并通过 LayoutManager 自动分配布局
class SlideBuilder:
    def __init__(self, layout_manager: LayoutManager):
        self.layout_manager = layout_manager  # 布局管理器实例
        self.title = ""  # 幻灯片标题
        self.bullet_points = []  # 幻灯片要点列表
        self.image_path = None  # 幻灯片图片路径
        self.table_path = None  # 幻灯片表格路径
        self.chart_path = None  # 幻灯片图表路径
        self.media_path = None  # 幻灯片媒体路径
        self.layout_id = None  # 布局ID
        self.layout_name = None  # 布局名称

    def set_title(self, title: str):
        self.title = title  # 设置幻灯片的标题

    def add_bullet_point(self, bullet: str):
        self.bullet_points.append(bullet)  # 添加要点

    def set_image(self, image_path: str):
        self.image_path = image_path  # 设置图片路径

    def set_table(self, table_path: str):
        self.table_path = table_path  # 设置表格路径

    def set_media(self, media_path: str):
        self.media_path = media_path  # 设置媒体路径

    def set_chart(self, chart_path: str):
        self.chart_path = chart_path  # 设置图表路径

    def finalize(self) -> Slide:
        """
        组装并返回最终的 Slide 对象，调用 LayoutManager 自动分配布局。
        """
        # 创建 SlideContent 对象
        content = SlideContent(
            title=self.title,
            bullet_points=self.bullet_points,
            image_path=self.image_path,
            table_path=self.table_path,
            chart_path=self.chart_path,
            media_path=self.media_path
        )

        # 调用 LayoutManager 分配布局
        self.layout_id, self.layout_name = self.layout_manager.assign_layout(content)

        # 返回最终的 Slide 对象
        return Slide(layout_id=self.layout_id, layout_name=self.layout_name, content=content)
