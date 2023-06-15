from typing import List

from fastapi import APIRouter, Depends
from fastapi import Body

from models.mongo import BookmarksModel
from services.bookmarks import BookmarksService, get_bookmarks_service

router = APIRouter()


@router.get(
    '/bookmarks',
    description='Метод возвращает информацию по закладкам',
)
async def get_document_bookmarks(
        user_id: str,
        bookmarks_service: BookmarksService = Depends(get_bookmarks_service),
) -> List[BookmarksModel]:

    response = await bookmarks_service.get_data_by_user(
        query={'user_id': user_id},
    )

    return response


@router.post(
    '/bookmarks',
    description='Метод сохраняет ифнормацию по закладкам',
)
async def set_document_bookmarks(
        document: BookmarksModel = Body(),
        bookmarks_service: BookmarksService = Depends(get_bookmarks_service),
) -> None:

    await bookmarks_service.set_data_by_user(
        document=document
    )


@router.delete(
    '/bookmarks',
    description='Метод удаляет документ из базы'
)
async def delete_document_bookmarks(
        user_id: str,
        bookmarks_service: BookmarksService = Depends(get_bookmarks_service),
) -> None:

    await bookmarks_service.delete_document(
        query={'user_id': user_id}
    )
