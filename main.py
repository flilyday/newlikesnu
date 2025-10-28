import uvicorn
from fastapi import FastAPI, Request, Response
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import httpx

# FastAPI 앱 인스턴스 생성
app = FastAPI()

# HTML 템플릿을 위한 디렉토리 설정
templates = Jinja2Templates(directory="templates")

@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return Response(status_code=204)

async def get_books():
    async with httpx.AsyncClient() as client:
        response = await client.get("http://likesnuapi.snu.ac.kr:9797/recommend/B111675/book?cnt=30")
        if response.status_code == 200:
            books = response.json()
            # thumb_url이 /image로 시작하는 항목 필터링
            filtered_books = [book for book in books if not book.get('thumb_url', '').startswith('/image')]
            return filtered_books
        return None

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/{filename}", response_class=HTMLResponse)
async def read_item(request: Request, filename: str):
    if filename == "1.knowledge-books.html":
        books = await get_books()
        return templates.TemplateResponse(filename, {"request": request, "books": books})
    if filename == "4.knowledge-empty-class.html":
        books = await get_books()
        return templates.TemplateResponse(filename, {"request": request, "books": books})
    return templates.TemplateResponse(filename, {"request": request})


# 이 파일이 직접 실행될 때 FastAPI 서버를 시작합니다.
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)