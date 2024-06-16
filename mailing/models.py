from django.conf import settings
from django.db import models

from client.models import Client
from users.models import User

NULLABLE = {"null": True, "blank": True}
FREQUENCY_CHOICES = [
    ("Daily", "Раз в день"),
    ("Weekly", "Раз в неделю"),
    ("Monthly", "раз в месяц"),
]
STATUS_OF_NEWSLETTER = [
    ("Create", "Создана"),
    ("Started", "Запущена"),
    ("Done", "Завершена"),
]
LOGS_STATUS_CHOICES = [
    ("Success", "Успешно"),
    ("Fail", "Не успешно"),
]


class MailingMessage(models.Model):
    """Модель для сообщения"""

    title = models.CharField(max_length=100, verbose_name="Тема письма")
    content = models.TextField(verbose_name="Тело письма")
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Автор", **NULLABLE
    )

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"

    def __str__(self):
        return self.title


class MailingSettings(models.Model):
    """Модель для рассылки"""

    first_datetime = models.DateTimeField(
        auto_now_add=True, verbose_name="Начало рассылки"
    )
    end_time = models.DateTimeField(verbose_name="Конец рассылки", **NULLABLE)
    sending = models.CharField(
        max_length=50, choices=FREQUENCY_CHOICES, verbose_name="Период рассылки"
    )
    message = models.ForeignKey(
        MailingMessage, on_delete=models.CASCADE, verbose_name="Сообщение"
    )
    setting_status = models.CharField(
        max_length=50,
        choices=STATUS_OF_NEWSLETTER,
        verbose_name="Статус рассылки",
        default="Create",
    )
    clients = models.ManyToManyField(Client, verbose_name="Получатели")
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Автор", **NULLABLE
    )

    class Meta:
        verbose_name = "Настройка рассылки"
        verbose_name_plural = "Настройки рассылки"
        permissions = [
            ("can_change_setting_status", "Может отключать рассылку"),
        ]

    def __str__(self):
        return (
            f"{self.message} отправляется каждый {self.sending} с {self.first_datetime}"
        )


class MailingStatus(models.Model):
    """Модель для статуса рассылки"""

    last_datetime = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата и время последней рассылки"
    )
    status = models.CharField(
        max_length=50,
        choices=LOGS_STATUS_CHOICES,
        default="",
        verbose_name="Статус попытки",
    )
    mailing_response = models.TextField(verbose_name="Ответ почтового сервера")
    mailing = models.ForeignKey(
        MailingSettings, on_delete=models.CASCADE, verbose_name="Рассылка"
    )
    client = models.ForeignKey(
        Client, on_delete=models.CASCADE, verbose_name="Клиент рассылки", **NULLABLE
    )
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Автор", **NULLABLE
    )

    class Meta:
        verbose_name = "Статус отправки"
        verbose_name_plural = "Статусы отправки"

    def __str__(self):
        return f"{self.status} в {self.last_datetime}, ответ сервера: {self.mailing_response}"
