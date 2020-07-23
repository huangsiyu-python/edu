from my_task.main import app

@app.task(name="upload_file")
def upload_file():
    print("上传文件的方法")
    return "file"