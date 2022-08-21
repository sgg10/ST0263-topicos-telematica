from fastapi import APIRouter
from fastapi import Path, Body
from fastapi import Response, status, HTTPException
from app.exceptions import HTTPAppException

from app.redis import connect
from app.models.users import User, Users
from app.cruds.users import CRUDUsers

router = APIRouter(prefix="/users", tags=["Users"])

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

@router.get("/", response_model=Users)
def get_users():
    response = execute_task("get_users")
    return Users(users=response)

@router.post("/")
def create_user(user: User = Body(...)):
    user = user.dict()
    response = execute_task("create_user", **user)
    return User(**response)


@router.get("/{nickname}")
def get_user(nickname: str = Path(...)):
    response = execute_task("get_user", nickname=nickname)
    return User(**response)

@router.put("/{nickname}")
def full_update_user(
    nickname: str = Path(...),
    first_name: str = Body(...),
    last_name: str = Body(...)
):
    user_data = {"nickname": nickname, "first_name": first_name, "last_name": last_name}
    response = execute_task("update_user", **user_data)
    return User(**response)

@router.patch("/{nickname}")
def full_update_user(
    nickname: str = Path(...),
    first_name: str = Body(default=None),
    last_name: str = Body(default=None)
):
    user_data = {"nickname": nickname, "first_name": first_name, "last_name": last_name}
    if not user_data["first_name"] and not user_data["last_name"]:
        pass
    response = execute_task("update_user", **user_data)
    return User(**response)

@router.delete("/{nickname}")
def delete_user(nickname: str = Path(...)):
    execute_task("delete_user", nickname=nickname)
    return Response(status_code=status.HTTP_204_NO_CONTENT)