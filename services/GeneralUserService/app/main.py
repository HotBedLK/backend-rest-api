from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from services.GeneralUserService.app.exceptions.generalUserEXceptions import GeneralUserExceptions
from .api.FetchLandingDemoPosts import router as FetchLandingDemoPostsRouter 
from .api.SinglePropertyDetails import router as SinglePropertyDetailsRouter 
from .api.LandingPagePostDetails import router as LandingPagePostDetails 

app = FastAPI(title="Generaluser Service")

app.include_router(FetchLandingDemoPostsRouter)
app.include_router(SinglePropertyDetailsRouter)
app.include_router(LandingPagePostDetails)

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "user"}





@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
):
    messages = []
    for error in exc.errors():
        messages.append(error["msg"])

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        content={
            "error_code": "VALIDATION_ERROR",
            "error_message": messages[0],
            "status_code": status.HTTP_422_UNPROCESSABLE_CONTENT,
        },
    )

#services wise exception handlers
@app.exception_handler(GeneralUserExceptions)
async def app_exception_handler(request: Request, exc: GeneralUserExceptions):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error_code": exc.error_code,
            "error_message": exc.error_message,
            "status_code": exc.status_code,
        },
    )


