from fastapi.responses import JSONResponse
from src.services.fewshot_service import few_shot_body_template
from src.services.noshot_service import no_shot_body_template
from src.schemas.users import *
import uuid
from src.config.logger_config import new_logger as logger
from src.utils.constants import *
from src.services.subject_service import subject_generator

async def generate_email(response: any,llm_id, trace_id : str = None):
    if(not trace_id):
        trace_id = str(uuid.uuid4())
    try:
        validated_item =  response["validated_item"]
        reference =  response["reference_list"]

        if(len(reference)==0):
            # no shot
            mail_subject = subject_generator(validated_item.ticket_id,validated_item.requestor_name,validated_item.description,validated_item.priority,validated_item.severity,trace_id)

            mail_body =  no_shot_body_template(validated_item.ticket_id,validated_item.requestor_name,validated_item.description,validated_item.priority,validated_item.severity,trace_id)

            logger.info(f"{trace_id}: Response sent sucessfully")
            return JSONResponse(content={
                "subject":mail_subject,
                "body": mail_body,
                "llm_id": llm_id
            }, status_code = OK)

        else: #Fewshot
            mail_subject = subject_generator(validated_item.ticket_id,validated_item.requestor_name,validated_item.description,validated_item.priority,validated_item.severity,trace_id)

            mail_body =  few_shot_body_template(validated_item.ticket_id, validated_item.requestor_name, validated_item.priority, validated_item.severity, validated_item.description, reference, trace_id)
            
            logger.info(f"{trace_id}: Response sent sucessfully")
            return JSONResponse(content={
                "subject":mail_subject,
                "body": mail_body,
                "llm_id": llm_id
            }, status_code = OK)

    except Exception as e:
        logger.error(f"{trace_id}: {e}")
        error_msg = f"Error in user_data function: {str(e)}"
        return JSONResponse(content={"message": error_msg}, status_code = INTERNAL_SERVER_ERROR)
    

