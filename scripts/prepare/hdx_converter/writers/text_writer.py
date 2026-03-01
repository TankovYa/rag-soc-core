from pathlib import Path
import logging
from typing import Optional, Dict, Any
from ..writers.file_writer import FileWriter

class TextWriter:
    def __init__(self, config):
        self.config = config
        self.file_writer = FileWriter(config)
    
    def format_text_content(self, title: str, content: str, navigation: str = "") -> str:
        """Форматирование текстового контента"""
        lines = content.split('\n')
        cleaned_lines = []
        for line in lines:
            if line.strip().startswith('# ') and title in line:
                continue
            cleaned_lines.append(line)
        
        cleaned_content = '\n'.join(cleaned_lines)
        return f"Title: {title}\n\n{cleaned_content}{navigation}"
    
    def save_text_file(self, content: str, base_filename: str, 
                      output_dir: Path, title: str = "") -> Optional[Path]:
        """Сохранение текстового файла"""
        # Убираем .md если есть в конце
        if base_filename.lower().endswith('.md'):
            base_filename = base_filename[:-3]

        # Убираем .txt если уже есть (на всякий случай)
        if base_filename.lower().endswith('.txt'):
            base_filename = base_filename[:-4]

        # Добавляем .txt
        filename = f"{base_filename}.txt"

        return self.file_writer.save_file(content, filename, "", output_dir, title)

    def format_structured_content(self, structured_data: Dict[str, Any], navigation: str) -> str:
        """Форматирование структурированных данных в текст - ИСПРАВЛЕННАЯ ВЕРСИЯ"""
        logger = logging.getLogger('HDXConverter')
        logger.debug("=== ФОРМАТИРОВАНИЕ STRUCTURED_DATA В ТЕКСТ ===")

        text_parts = []

        # Добавляем заголовок статьи
        article_title = structured_data.get("metadata", {}).get("article_title", "")
        if article_title:
            text_parts.append(f"# {article_title}\n")
            logger.debug(f"Добавлен заголовок: {article_title}")

        # Рекурсивная обработка контента
        def process_element(element, indent=0):
            if isinstance(element, dict):
                element_type = element.get("type")

                if element_type == "section":
                    title = element.get("title", "")
                    content = element.get("content", [])
                    if title:
                        text_parts.append(f"\n{'=' * (50 if indent == 0 else 40)}")
                        text_parts.append(f"{'  ' * indent}{title.upper()}")
                        text_parts.append(f"{'=' * (50 if indent == 0 else 40)}\n")
                    for item in content:
                        process_element(item, indent + 1)

                elif element_type == "navigation":
                    # === ИСПРАВЛЕНИЕ: Обработка навигации из structured_data ===
                    content = element.get("content", "")
                    if content:
                        text_parts.append("\n" + "="*50 + "\n")
                        text_parts.append("NAVIGATION\n")
                        text_parts.append("="*50 + "\n")
                        text_parts.append(content + "\n")
                    # === КОНЕЦ ИСПРАВЛЕНИЯ ===

                elif element_type == "paragraph":
                    content_data = element.get("content", "")
                    if isinstance(content_data, str):
                        text_parts.append(f"{'  ' * indent}{content_data}\n")
                    elif isinstance(content_data, list):
                        for item in content_data:
                            process_element(item, indent)
                        text_parts.append("\n")

                elif element_type == "list":
                    items = element.get("items", [])
                    for i, item in enumerate(items):
                        process_element(item, indent)

                elif element_type == "list_item":
                    content = element.get("content", [])
                    text = element.get("text", "")
                    if text:
                        text_parts.append(f"{'  ' * indent}* {text}\n")
                    elif content:
                        text_parts.append(f"{'  ' * indent}* ")
                        for item in content:
                            process_element(item, indent)
                        text_parts.append("\n")

                elif element_type == "link":
                    text = element.get("text", "")
                    href = element.get("href", "")
                    text_parts.append(f"[{text}]")

                elif element_type == "code_block":
                    content = element.get("content", "")
                    text_parts.append(f"\n{'  ' * indent}```\n")
                    text_parts.append(f"{content}\n")
                    text_parts.append(f"{'  ' * indent}```\n\n")

            elif isinstance(element, list):
                for item in element:
                    process_element(item, indent)

        # Обрабатываем весь контент
        for content_item in structured_data.get("content", []):
            process_element(content_item)

        # === ИСПРАВЛЕНИЕ ПРОБЛЕМЫ 8: Убрано добавление навигации из параметра navigation ===
        # Навигация уже обработана из structured_data
        # === КОНЕЦ ИСПРАВЛЕНИЯ ===

        logger.debug(f"=== ЗАВЕРШЕНО ФОРМАТИРОВАНИЕ STRUCTURED_DATA ===")
        logger.debug(f"Размер текстового контента: {len(''.join(text_parts))} символов")

        return ''.join(text_parts)