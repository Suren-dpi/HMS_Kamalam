from fastapi import Depends, FastAPI, HTTPException, status, Request, Form, File, UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse,JSONResponse
import uvicorn

app = FastAPI()

####Test#####
@app.get('/get_token', response_class=JSONResponse)
async def get_token(request: Request):
    tk = {"accesstoken":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTcwMTE1ODQ2N30.MY1NHU_N6t5X6HhUfPgcKF60tntL-9MTrV8oSymvE1k"}
    return tk

@app.get('/si', response_class=JSONResponse)
async def get_token(request: Request):
    tk = { "mid": "CFE907", "rrn": "332030118231","tid": "27273919","acquirerBank": "HDFC BANK","acquirerBankID": "52","address": " TH94 KHORI HOUSE DEVIPURA NEAR BAJAJ CIRCLE OPP BANK OF BARODA SIKAR RAJASTHAN PIN NO 332001TH94 KHORI HOUSE DEVIPURA NEAR BAJAJ CIRCLE OPP BA TH94 KHORI HOUSE DEVIPURA NEAR BAJAJ CIRCLE OPP BA","amount": "1206.00","authCode": "NA","batchNo": "000164","grabUniqueIdentifier":"101150969571700115579","invoiceNo": "000972", "issuerBank": "", "merchantVPA":"TH94RELIANCEFRESHREL.27273919@hdfcbank", "payeeVPA": "9887554557@ybl", "paymentMode": "UPI", "primeID": "R179152220231116115030721172025021100","responseCode": "00","responseDate": "2023-11-16 11:50:30.722","responseMessage": "APPROVED", "responseTime": "2023-11-16 11:50:30.722","upi_txn_id": "R17915223320114941264GRA"}
    return tk


if __name__ == "__main__":
    #uvicorn.run("web_app:app", host=conn['host'], port=int(conn['port']), log_level="info",reload=True,ssl_keyfile=conn['ssl_keyfile'], ssl_certfile=conn['ssl_certfile'])
    uvicorn.run("app:app", host="127.0.0.1", port=5008, log_level="info", reload=True)
