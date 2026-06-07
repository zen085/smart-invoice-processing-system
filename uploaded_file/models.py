from django.db import models
from core.models import TimeStampModel
from django.conf import settings
import uuid
# Create your models here.

class UploadedFile(TimeStampModel):
    
    class UploadStatus(models.TextChoices):
        PENDING = "pending","pending"
        PROCESSING = "processing","processing"
        PROCESSED = "processed","processed"
        FAILED = "failed","failed"

    uuid = models.UUIDField(default=uuid.uuid4,editable=False,unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="uploads")
    file = models.FileField(upload_to="uploads/")
    invoice_archive = models.FileField(upload_to="invoice_archives/",blank=True,null=True)
    status = models.CharField(max_length=20,choices=UploadStatus.choices,default=UploadStatus.PENDING)
    error_message = models.TextField()
    is_hidden = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.file.name}"

