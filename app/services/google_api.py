from datetime import datetime
from copy import deepcopy

from aiogoogle import Aiogoogle

from app.core.config import settings

FORMAT = "%Y/%m/%d %H:%M:%S"

NOW_DATE_TIME = datetime.now().strftime(FORMAT)

SPREADSHEET_BODY = {
    'properties': {'title': f'Report on {NOW_DATE_TIME}',
                   'locale': 'en_US'},
    'sheets': [{'properties': {'sheetType': 'GRID',
                               'sheetId': 0,
                               'title': 'Sheet1',
                               'gridProperties': {'rowCount': 100,
                                                  'columnCount': 11}}}]
}

TABLE_HEADER = [
    ['Report on', NOW_DATE_TIME],
    ['Top projects by speed of completion'],
    ['Project name', 'Completion time', 'Description']
]


async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
    service = await wrapper_services.discover('sheets', 'v4')

    spreadsheet_body = deepcopy(SPREADSHEET_BODY)
    spreadsheet_body['properties']['title'] = f'Report on {NOW_DATE_TIME}'

    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )

    spreadsheet_id = response['spreadsheetId']
    return spreadsheet_id


async def set_user_permissions(spreadsheet_id: str, wrapper_services: Aiogoogle) -> None:
    permissions_body = {'type': 'user',
                        'role': 'writer',
                        'emailAddress': settings.email}
    service = await wrapper_services.discover('drive', 'v3')
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheet_id,
            json=permissions_body,
            fields="id"
        ))


async def spreadsheets_update_value(spreadsheet_id: str, projects: list, wrapper_services: Aiogoogle) -> None:
    service = await wrapper_services.discover('sheets', 'v4')

    table_values = deepcopy(TABLE_HEADER)

    for project in projects:
        new_row = [
            str(project['name']),
            str(project["close_date"] - project["create_date"]),
            str(project['description']),
        ]
        table_values.append(new_row)

    update_body = {
        'majorDimension': 'ROWS',
        'values': table_values
    }

    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range='Sheet1!A1:C30',
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )
