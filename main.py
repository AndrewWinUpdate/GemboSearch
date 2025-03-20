from fastapi import FastAPI, UploadFile, File
import shutil
import func

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello, World!"}

@app.post("/index_clip/")
async def upload_clip(movie_id: str, clip_id: str, file: UploadFile = File(...)):
    file_path = f"temp_{clip_id}.srt"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    func.index_clip(movie_id, clip_id, file_path)
    return {"status": "indexed", "clip_id": clip_id}

@app.get("/search/")
async def search_clip(query: str):
    results = func.search_clips(query)
    return {"results": results}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
