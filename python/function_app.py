import azure.functions as func
import logging

from app.service import process_users

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)


@app.route(route="process-licenses", methods=["POST"])
def process_licenses(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Starting license assignment process")

    try:
        process_users()

        return func.HttpResponse(
            "License processing completed successfully.",
            status_code=200,
        )

    except Exception as e:
        logging.exception("Processing failed")

        return func.HttpResponse(
            f"Error: {str(e)}",
            status_code=500,
        )