from aiohttp import web, log
import zerorpc


client = zerorpc.Client()
client.connect('tcp://127.0.0.1:9000')


async def get_agents_handler(request: web.Request):
    """获取已注册agent列表"""
    txt = client.get_agents()
    return web.json_response(txt)


async def commit_task(request: web.Request):
    """任务提交
    {
    "script":"echo hello.",
    "timeout":30,
    "targets":["d2c920a93371414fa66388ef3dbc710e"]
    }
    """
    body: dict = await request.json()
    txt = client.add_task(body)
    return web.json_response(text=txt, status=201)


app = web.Application()
app.router.add_get('/task/agents', get_agents_handler)
app.router.add_post('/task', commit_task)
web.run_app(app, host='0.0.0.0', port=9900)



