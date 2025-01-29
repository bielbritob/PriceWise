from pathlib import Path
from typing import Optional
import streamlit.components.v1 as components
from jinja2 import Environment, FileSystemLoader
import os

# Diretório dos templates
frontend_dir = (Path(__file__).parent / "frontend").absolute()
_component_func = components.declare_component(
    "st_drag_drop", path=str(frontend_dir)
)

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
env = Environment(loader=FileSystemLoader(template_dir))


def render_drag_drop_template(draggable_items, droppable_items, extra_items):
    """Renderiza o template Jinja2 com itens arrastáveis, zonas de drop e itens extras."""
    template = env.get_template('drag_drop_template.html')
    return template.render(
        draggable_items=draggable_items,
        droppable_items=droppable_items,
        extra_items=extra_items
    )


def st_drag_drop(
        draggable_items,
        droppable_items,
        extra_items=None,  # Adicionando suporte para itens extras
        key: Optional[str] = None
):
    """Função principal para usar o componente de drag-and-drop no Streamlit."""

    # Se extra_items não for fornecido, define como um dicionário vazio
    if extra_items is None:
        extra_items = {}

    # Renderiza o HTML
    rendered_html = render_drag_drop_template(draggable_items, droppable_items, extra_items)

    # Passa o HTML renderizado para o frontend
    component_value = _component_func(html_content=rendered_html, key=key, default={})

    return component_value