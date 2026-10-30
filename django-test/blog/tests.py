import os
from django.test import TestCase, Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from blog.models import Blog


class BlogTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.report_path = 'Test_Report3.docx'

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

    def _make_image(self):
        return SimpleUploadedFile(
            name='test_blog_image.jpg',
            content=b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\xff\xff\xff\x21\xf9\x04\x01\x00\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x4c\x01\x00\x3b',
            content_type='image/jpeg'
        )

    def setUp(self):
        self.blog = Blog.objects.create(
            title='Тестовый заголовок',
            description='Тестовое описание',
            image=self._make_image(),
            author='Ivanov',
        )

    def tearDown(self):
        result = self._outcome.result
        has_failed = any(t == self for t, _ in result.failures + result.errors)
        status_text = "Ошибка!" if has_failed else "Успешно!"

        doc = Document(self.report_path)
        table = doc.tables[0]

        row_cells = table.add_row().cells
        row_cells[0].text = str(self._testMethodName)
        row_cells[1].text = status_text

        for cell in row_cells:
            for paragraph in cell.paragraphs:
                for run in paragraph.runs:
                    run.font.name = 'Arial'
                    run.font.size = Pt(11)

        doc.save(self.report_path)

    def test_blog_model_creation(self):
        self.assertEqual(self.blog.title, 'Тестовый заголовок')

    def test_blog_list_view(self):
        url = reverse('blog_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_blog_detail_view(self):
        url = reverse('blog_detail', args=[self.blog.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_blog_detail_not_found(self):
        url = reverse('blog_detail', args=[999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    ## Новые тесты

    def test_create_blog_view_get(self):
        url = reverse('create_blog')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create_blog.html')

    def test_create_blog_view_post(self):
        url = reverse('create_blog')
        form_data = {
            'title': 'Новый блог',
            'description': 'Описание блога новое',
            'author': 'Петров Иван',
            'image': self._make_image(),
        }

        response = self.client.post(url, data=form_data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/blog_list/')

        self.assertTrue(Blog.objects.filter(title='Новый блог').exists())

    def test_update_blog_view_post(self):
        url = reverse('update_blog', args=[self.blog.id])

        updated_data = {
            'title': 'Обновление данных',
            'description': 'Обновление описания',
            'author': 'Qwertis Qwertu',
            'image': self._make_image(),
        }

        response = self.client.post(url, data=updated_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/blog_list/')
        self.blog.refresh_from_db()
        self.assertEqual(self.blog.title, 'Обновление данных')

    def test_delete_blog_view(self):
        inital_count = Blog.objects.count()
        url = reverse('delete_blog', args=[self.blog.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/blog_list/')

        self.assertEqual(Blog.objects.count(), inital_count - 1)
        self.assertFalse(Blog.objects.filter(id=self.blog.id).exists())



#         #Что	Было	Стало
# Создание картинки	self.test_image = SimpleUploadedFile(...) в setUp, переиспользовался	Хелпер _make_image(), каждый раз новый объект
# setUp	image=self.test_image	image=self._make_image()
# test_create_blog_view_post	'image': self.test_image (уже прочитан)	'image': self._make_image()
# test_update_blog_view_post	'image': self.test_image (уже прочитан)	'image': self._make_image()
# tearDown	self._outcome.errors (нет в Django 5)	self._outcome.result.failures + .errors