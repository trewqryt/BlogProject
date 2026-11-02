
from pathlib import Path
from datetime import datetime

from django.conf import settings
from django.test.runner import DiscoverRunner
from docx import Document
from docx.shared import Pt, Cm


class WordReportTestRunner(DiscoverRunner):
    def run_suite(self, suite, **kwargs):
        self.test_names = []

        def collect(test_suite):
            for item in test_suite:
                if hasattr(item, "__iter__"):
                    collect(item)
                else:
                    self.test_names.append(item.id())

        collect(suite)
        return super().run_suite(suite, **kwargs)

    def suite_result(self, suite, result, **kwargs):
        self.create_word_report(result)
        return super().suite_result(suite, result, **kwargs)

    def create_word_report(self, result):
        document = Document()

        section = document.sections[0]
        section.top_margin = Cm(2)
        section.bottom_margin = Cm(2)

        normal = document.styles["Normal"]
        normal.font.name = "Times New Roman"
        normal.font.size = Pt(12)

        document.add_heading(
            "Отчёт по тестированию Django CRUD", 0
        )

        document.add_paragraph(
            "Проект: BlogProject\n"
            "Приложение: crud\n"
            "Дата: " + datetime.now().strftime("%d.%m.%Y %H:%M")
        )

        document.add_heading("Цель работы", level=1)
        document.add_paragraph(
            "Проверить корректность работы CRUD-приложения "
            "с помощью автоматических тестов Django."
        )

        document.add_heading("Результаты тестирования", level=1)

        failures = {
            test.id(): message
            for test, message in result.failures
        }
        errors = {
            test.id(): message
            for test, message in result.errors
        }
        skipped = {
            test.id(): reason
            for test, reason in result.skipped
        }

        table = document.add_table(rows=1, cols=3)
        table.style = "Table Grid"

        headers = table.rows[0].cells
        headers[0].text = "№"
        headers[1].text = "Название теста"
        headers[2].text = "Результат"

        for index, name in enumerate(self.test_names, 1):
            if name in failures or name in errors:
                status = "FAILED"
            elif name in skipped:
                status = "SKIPPED"
            else:
                status = "PASSED"

            cells = table.add_row().cells
            cells[0].text = str(index)
            cells[1].text = name.split(".")[-1]
            cells[2].text = status

        document.add_heading("Общая статистика", level=1)

        passed = (
            result.testsRun
            - len(result.failures)
            - len(result.errors)
            - len(result.skipped)
        )

        document.add_paragraph(
            f"Всего тестов: {result.testsRun}\n"
            f"Успешно: {passed}\n"
            f"Ошибок: {len(result.errors)}\n"
            f"Не пройдено: {len(result.failures)}\n"
            f"Пропущено: {len(result.skipped)}"
        )

        if failures or errors:
            document.add_heading("Подробности ошибок", level=1)
            for name, message in {**failures, **errors}.items():
                document.add_heading(name, level=2)
                document.add_paragraph(message)

        document.add_heading("Вывод", level=1)

        if failures or errors:
            document.add_paragraph(
                "Во время тестирования обнаружены ошибки, "
                "которые необходимо исправить."
            )
        else:
            document.add_paragraph(
                "Все выполненные тесты завершились успешно. "
                "Проверенные функции CRUD работают корректно."
            )

        report_dir = Path(settings.BASE_DIR) / "reports"
        report_dir.mkdir(exist_ok=True)

        filename = report_dir / "CRUD_Test_Report.docx"
        document.save(filename)

        print(f"\nWord-отчёт создан: {filename}")
