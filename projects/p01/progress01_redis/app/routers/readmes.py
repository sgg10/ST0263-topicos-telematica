from fastapi import APIRouter, Path
from fastapi.responses import HTMLResponse
from fastapi import Response, status, HTTPException

from app.redis import connect
from app.cruds.users import CRUDUsers
from app.exceptions import HTTPAppException

router = APIRouter(prefix="/readme", tags=["Reads me"])

def execute_task(task_name: str, *args, **kwargs):
    try:
        redis = connect()
        users = CRUDUsers(redis)
        task = getattr(users, task_name)
        response = task(*args, **kwargs)
        redis.close()
        return response
    except HTTPAppException as error:
        raise HTTPException(
            detail=error.message,
            status_code=error.status_code
        )
    except Exception as e:
        raise HTTPException(
            detail=f"Error: {e}",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@router.get("/{nickname}")
def get_user_readme(nickname: str = Path(...)):
    content, _status = execute_task("get_readme", nickname=nickname)

    if _status:
        return HTMLResponse(content, status_code=status.HTTP_200_OK)
    return {"message": content}

@router.post("/{nickname}")
def create_user_readme(nickname: str = Path(...)):
    execute_task("create_readme", nickname=nickname)
    return {"message": f"{nickname}'s readme will be created in a few seconds :)"}