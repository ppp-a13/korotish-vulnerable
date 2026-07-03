from fastapi import FastAPI

app = FastAPI(title='korotish')


@app.get('/health')
async def health():
    return {'status': 'ok'}
