import unittest

from django.test import TestCase, Client
from django.test.runner import DiscoverRunner
from django.urls import reverse
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH

from blog.models import Blog


# ---------- Инфраструктура для честного статуса ----------

class ReportingTestResult(unittest.TextTestResult):
    """Запоминает id упавших/ошибочных тестов, чтобы tearDown мог их увидеть."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.failed_tests = set()

    def addFailure(self, test, err):
        super().addFailure(test, err)
        self.failed_tests.add(test.id())

    def addError(self, test, err):
        super().addError(test, err)
        self.failed_tests.add(test.id())


class ReportingRunner(DiscoverRunner):
    """Подключает ReportingTestResult к стандартному runner Django."""

    def get_resultclass(self):
        return ReportingTestResult


# ---------- Тесты ----------

class BlogTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.report_path = 'Test_Report2.docx'

        doc = Document()

        title = doc.add_paragraph()
        title_run = title.add_run("Отчет об автоматическом тестировании")
        title_run.font.name = 'Arial'
        title_run.font.size = Pt(18)
        title_run.font.bold = True
        title.alignment = WD_ALIGN_PARAGRAPH.CENTER

        doc.add_paragraph(
            "Проект DjangoBlog Application (статус генерации: автоматический)"
        )

        table = doc.add_table(rows=1, cols=2)
        table.style = 'Table Grid'
        hdr_cells = table.rows[0].cells
        hdr_cells[0].text = 'Название выполненного теста'
        hdr_cells[1].text = 'Результат'

        for cell in hdr_cells:
            for paragraph in cell.paragraphs:
                for run in paragraph.runs:
                    run.font.bold = True
                    run.font.name = 'Arial'

        doc.save(cls.report_path)

    def setUp(self):
        self.client = Client()
        self.blog = Blog.objects.create(
            title='Тестовый заголовок',
            description='Тестовое описание',
            image='test_image.jpg',
            author='Ivanov',
        )

    def tearDown(self):
        # Смотрим, попал ли текущий тест в failed_tests нашего ReportingTestResult.
        result = getattr(self._outcome, 'result', None)
        failed = result is not None and self.id() in getattr(
            result, 'failed_tests', set()
        )
        status_text = 'Ошибка' if failed else 'GOOD'

        doc = Document(self.report_path)
        table = doc.tables[0]

        row_cells = table.add_row().cells
        row_cells[0].text = self._testMethodName
        row_cells[1].text = status_text

        for cell in row_cells:
            for paragraph in cell.paragraphs:
                for run in paragraph.runs:
                    run.font.name = 'Arial'
                    run.font.size = Pt(11)

        doc.save(self.report_path)
        super().tearDown()

    # ---------- Тесты ----------

    def test_blog_model_creation(self):
        self.assertEqual(self.blog.title, 'Тестовый заголовок')
        self.assertEqual(str(self.blog), 'Тестовый заголовок')

    def test_blog_list_view(self):
        url = reverse('blog_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        # намеренно сломано — должно дать 'Ошибка'
        self.assertTemplateUsed(response, 'blog_list.html')

    def test_blog_detail_view(self):
        url = reverse('blog_detail', args=[self.blog.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog_detail.html')

    def test_blog_detail_not_found(self):
        url = reverse('blog_detail', args=[999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)