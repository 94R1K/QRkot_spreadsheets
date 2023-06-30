from copy import deepcopy
from datetime import datetime
from typing import List

from aiogoogle import Aiogoogle

from app.core.config import settings
from app.models import CharityProject

FORMAT = "%Y/%m/%d %H:%M:%S"
ROW_COUNT = 100
COLUMN_COUNT = 100
SHEETS_VERSION = 'v4'
DRIVE_VERSION = 'v3'
SPREADSHEET_TITLE = 'Отчет на {date}'
SPREADSHEET_BODY = dict(
    properties=dict(
        title=SPREADSHEET_TITLE.format(date=datetime.now().strftime(FORMAT)),
        locale='ru_RU',
    ),
    sheets=[dict(properties=dict(
        sheetType='GRID',
        sheetId=0,
        title='Лист1',
        gridProperties=dict(
            rowCount=ROW_COUNT,
            columnCount=COLUMN_COUNT,
        )
    ))]
)
TABLE_HEADER = [
    ['Отчет от', datetime.now().strftime(FORMAT)],
    ['Количество по скорости закрытия'],
    ['Название проекта', 'Время сбора', 'Описание']
]


async def spreadsheets_create(
        wrapper_services: Aiogoogle,
        spreadsheet_body=None
) -> str:
    if spreadsheet_body is None:
        spreadsheet_body = deepcopy(SPREADSHEET_BODY)
        spreadsheet_body['properties']['title'] = SPREADSHEET_TITLE.format(
            date=datetime.now().strftime(FORMAT)
        )
    service = await wrapper_services.discover('sheets', SHEETS_VERSION)
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    spreadsheet_id = response['spreadsheetId']
    return spreadsheet_id


async def set_user_permissions(
        spreadsheetid: str,
        wrapper_services: Aiogoogle
) -> None:
    permissions_body = {
        'type': 'user',
        'role': 'writer',
        'emailAddress': settings.email
    }
    service = await wrapper_services.discover('drive', DRIVE_VERSION)
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheetid,
            json=permissions_body,
            fields='id'
        )
    )


async def spreadsheets_update_value(
        spreadsheetid: str,
        projects: List[CharityProject],
        wrapper_services: Aiogoogle
) -> None:
    service = await wrapper_services.discover('sheets', SHEETS_VERSION)
    table_header = deepcopy(TABLE_HEADER)
    table_header[0][1] = datetime.now().strftime(FORMAT)
    table_values = [
        *table_header,
        *[list(map(str, [
            attr.name, attr.close_date - attr.create_date, attr.description
        ])) for attr in projects],
    ]
    rows = len(table_values)
    cols = max(map(len, table_values))
    if rows > ROW_COUNT or cols > COLUMN_COUNT:
        raise ValueError(
            'Превышены габариты таблицы. '
            f'Сформированно строк {rows}. Допустимо {ROW_COUNT}. '
            f'Сформированно столбцов {cols}. Допустимо {COLUMN_COUNT}. '
        )
    update_body = {
        'majorDimension': 'ROWS',
        'values': table_values
    }
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheetid,
            range=f'R1C1:R{rows}C{cols}',
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )
