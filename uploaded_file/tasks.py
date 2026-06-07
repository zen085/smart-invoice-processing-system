from celery import shared_task
from .models import UploadedFile
from .services import UploadedFileProcessingService

import logging

logger = logging.getLogger(__name__)



@shared_task(autoretry_for=(ConnectionError,),retry_backoff=True,max_retries=5,)
def process_uploaded_file_task(uploaded_file_id):

    try:

        logger.info(
            f"Starting processing for "
            f"uploaded file ID: "
            f"{uploaded_file_id}"
        )

        uploaded_file = UploadedFile.objects.get(id=uploaded_file_id)

    except UploadedFile.DoesNotExist:

        logger.error(
            f"Uploaded file with ID {uploaded_file_id} does not exist"
        )

        return

    try:

        uploaded_file.status = UploadedFile.UploadStatus.PROCESSING

        uploaded_file.save(update_fields=["status"])

        UploadedFileProcessingService.process_uploaded(uploaded_file)

        uploaded_file.status = UploadedFile.UploadStatus.PROCESSED
        uploaded_file.error_message = ""

        uploaded_file.save(update_fields=["status","error_message"])
        

        logger.info(
            f"Completed processing for "
            f"uploaded file ID: "
            f"{uploaded_file_id}"
        )

    except Exception as error:

        logger.exception(  
            f"Task failed for file ID: {uploaded_file_id}., Error:{error}"
            )           
           
        user_error = "The uploaded file could not be processed.Please verify the file format and contents."
         
        try:

            uploaded_file.status = UploadedFile.UploadStatus.FAILED
            uploaded_file.error_message = user_error

            uploaded_file.save(
                update_fields=["status","error_message"]
            )

        except Exception:

            logger.exception(
                "Failed updating upload status and error_message"
            )

        raise
