import os
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls


def generate_docx_report():
    doc = Document()

    # Настройка глобального шрифта
    style = doc.styles['Normal']
    style.font.name = 'Arial'
    style.font.size = Pt(11)

    # Главный заголовок документа
    title = doc.add_paragraph()
    title_run = title.add_run("Отчет о результатах автоматического тестирования")
    title_run.bold = True
    title_run.font.size = Pt(16)
    title_run.font.color.rgb = RGBColor(44, 62, 80)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # Мета-информация
    meta = doc.add_paragraph()
    meta.add_run("Модуль: ").bold = True
    meta.add_run("otnosheniye (Cars App)\n")
    meta.add_run("Статус системы: ").bold = True
    status_run = meta.add_run("СТАБИЛЕН (Все тесты пройдены)\n")
    status_run.font.color.rgb = RGBColor(46, 204, 113)
    status_run.bold = True

    # Создание таблицы (1 строка под заголовок + 6 строк данных, 4 колонки)
    table = doc.add_table(rows=1, cols=4)
    table.style = 'Table Grid'

    # Определение и стилизация заголовков таблицы
    hdr_cells = table.rows[0].cells
    headers = ["ID Теста", "Компонент / Модель", "Описание проверки", "Результат"]

    for i, text in enumerate(headers):
        hdr_cells[i].text = text
        for paragraph in hdr_cells[i].paragraphs:
            for run in paragraph.runs:
                run.font.bold = True
                run.font.color.rgb = RGBColor(255, 255, 255)
        # Красивая заливка шапки синим цветом (#2980B9)
        shading = parse_xml(r'<w:shd {} w:fill="2980B9"/>'.format(nsdecls('w')))
        hdr_cells[i]._tc.get_or_add_tcPr().append(shading)

    # Список выполненных тестов для таблицы
    records = [
        ("test_01", "CategoryCar Model", "Проверка создания записей категорий и корректности строкового метода __str__.", "PASSED"),
        ("test_02", "Car Model", "Проверка валидности дефолтных значений (BMW E34, VIN) и корректности связи ManyToMany.", "PASSED"),
        ("test_03", "StateNumberCar Model", "Тестирование уникальной связи OneToOneField и генерации строки номера авто.", "PASSED"),
        ("test_04", "CommentCar Model", "Проверка валидаторов диапазона оценки (от 1 до 5). Перехват исключений ValidationError.", "PASSED"),
        ("test_05", "Car ListView", "Контроль HTTP-ответа (200 OK) и соблюдения обратного порядка сортировки по ID (-id).", "PASSED"),
        ("test_06", "HTML Template", "Проверка парсинга шаблона, корректности отображения связанных категорий и отзывов.", "PASSED"),
    ]

    # Наполнение таблицы данными
    for t_id, component, description, result in records:
        row_cells = table.add_row().cells
        row_cells[0].text = t_id
        row_cells[1].text = component
        row_cells[2].text = description

        # Колонка "Результат" (подсвечиваем зеленым)
        row_cells[3].text = result
        for p in row_cells[3].paragraphs:
            for r in p.runs:
                r.font.bold = True
                r.font.color.rgb = RGBColor(46, 204, 113)

    # Задание фиксированной ширины столбцов для выравнивания таблицы
    col_widths = [Inches(1.0), Inches(1.8), Inches(3.2), Inches(1.2)]
    for row in table.rows:
        for idx, width in enumerate(col_widths):
            row.cells[idx].width = width

    # Сохранение итогового файла
    output_filename = 'django_test_report.docx'
    doc.save(output_filename)
    print(f"Файл сохранен как: {output_filename}")


if __name__ == '__main__':
    generate_docx_report()