from typing import Optional, List
from dataclasses import dataclass, field

# 定义 SlideContent 数据类，表示幻灯片的内容，包括标题、要点列表、图片路径。
@dataclass
class SlideContent:
    title: str  # 幻灯片的标题
    bullet_points: List[str] = field(default_factory=list)  # 幻灯片中的要点列表，默认为空列表
    image_path: Optional[str] = None  # 幻灯片中的图片路径，默认为 None
    table_path: Optional[str] = None  # 幻灯片中的表格路径，默认为 None
    chart_path: Optional[str] = None  # 幻灯片中的图表路径，默认为 None
    media_path: Optional[str] = None  # 幻灯片中的视频路径，默认为 None

# 定义 Slide 数据类，表示每张幻灯片，包括布局 ID、布局名称以及幻灯片内容。
@dataclass
class Slide:
    layout_id: int  # 布局 ID，对应 PowerPoint 模板中的布局
    layout_name: str  # 布局名称
    content: SlideContent  # 幻灯片的内容，类型为 SlideContent

# 定义 PowerPoint 数据类，表示整个 PowerPoint 演示文稿，包括标题和幻灯片列表。
@dataclass
class PowerPoint:
    title: str  # PowerPoint 演示文稿的标题
    slides: List[Slide] = field(default_factory=list)  # 幻灯片列表，默认为空列表

    # 定义 __str__ 方法，用于打印演示文稿的详细信息
    def __str__(self):
        result = [f"PowerPoint Presentation: {self.title}"]  # 打印 PowerPoint 的标题
        for idx, slide in enumerate(self.slides, start=1):
            result.append(f"\nSlide {idx}:")
            result.append(f"  Title: {slide.content.title}")  # 打印每张幻灯片的标题
            result.append(f"  Layout: {slide.layout_name} (ID: {slide.layout_id})")  # 打印布局名称和 ID
            if slide.content.bullet_points:
                result.append(f"  Bullet Points: {', '.join(slide.content.bullet_points)}")  # 打印要点列表
            if slide.content.image_path:
                result.append(f"  Image: {slide.content.image_path}")  # 打印图片路径
        return "\n".join(result)