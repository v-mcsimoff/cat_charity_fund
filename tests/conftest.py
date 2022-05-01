from datetime import datetime

import uuid
import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from fastapi_users import models
from fastapi_users.password import PasswordHelper
from mixer.backend.sqlalchemy import Mixer as _mixer
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

try:
    from app.core.db import Base, get_async_session
except (NameError, ImportError):
    raise AssertionError(
        'Не обнаружены объекты `Base, get_async_session`. '
        'Создайте эти объекты по пути `app.core.db`',
    )

try:
    from app.core.user import current_superuser, current_user
except (NameError, ImportError):
    raise AssertionError(
        'Не обнаружены объекты `current_superuser, current_user`.'
        'Создайте эти объекты по пути `app.code.user`',
    )

try:
    from app.main import app
except (NameError, ImportError):
    raise AssertionError(
        'Не обнаружен объект приложения `app`.'
        'Создайте эти объекты по пути `app.main`',
    )


SQLALCHEMY_DATABASE_URL = 'sqlite+aiosqlite:///./test.db'


engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)
TestingSessionLocal = sessionmaker(
    class_=AsyncSession, autocommit=False, autoflush=False, bind=engine,
)


password_helper = PasswordHelper()
password_hash = password_helper.hash('chimichangas4life')


class User(models.BaseUser):
    pass


class UserDB(User, models.BaseUserDB):
    pass


user_uuid4 = uuid.uuid4()
user = UserDB(
    id=user_uuid4,
    email='dead@pool.com',
    hashed_password=str(password_hash),
    is_active=True,
    is_verified=True,
    is_superuser=False,
)

superuser_uuid4 = uuid.uuid4()
superuser = UserDB(
    id=superuser_uuid4,
    email='superdead@pool.com',
    hashed_password=str(password_hash),
    is_active=True,
    is_verified=True,
    is_superuser=True,
)


async def override_db():
    async with TestingSessionLocal() as session:
        yield session


@pytest_asyncio.fixture(autouse=True)
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
def user_client():
    app.dependency_overrides = {}
    app.dependency_overrides[get_async_session] = override_db
    app.dependency_overrides[current_user] = lambda: user
    with TestClient(app) as client:
        yield client


@pytest.fixture
def superuser_client():
    app.dependency_overrides = {}
    app.dependency_overrides[get_async_session] = override_db
    app.dependency_overrides[current_superuser] = lambda: superuser
    with TestClient(app) as client:
        yield client


@pytest.fixture
def mixer():
    engine = create_engine('sqlite:///./test.db')
    session = sessionmaker(bind=engine)
    return _mixer(session=session(), commit=True)


@pytest.fixture
def charity_project(mixer):
    return mixer.blend(
        'app.models.charity_project.CharityProject',
        name='chimichangas4life',
        user_email='dead@pool.com',
        description='Huge fan of chimichangas. Wanna buy a lot',
        full_amount=1000000,
        close_date=datetime.strptime('2019-08-24T14:15:22Z', '%Y-%m-%dT%H:%M:%SZ'),
        create_date=datetime.strptime('2019-08-24T14:15:22Z', '%Y-%m-%dT%H:%M:%SZ'),
    )


@pytest.fixture
def charity_project_nunchaku(mixer):
    return mixer.blend(
        'app.models.charity_project.CharityProject',
        name='nunchaku',
        user_email='evil@pool.com',
        description='Nunchaku is better',
        full_amount=5000000,
        close_date=datetime.strptime('2019-08-24T14:15:22Z', '%Y-%m-%dT%H:%M:%SZ'),
        create_date=datetime.strptime('2019-08-24T14:15:22Z', '%Y-%m-%dT%H:%M:%SZ'),
    )


@pytest.fixture
def small_fully_charity_project(mixer):
    return mixer.blend(
        'app.models.charity_project.CharityProject',
        name='1M$ for u project',
        user_email='elon@tusk.com',
        description='Wanna buy you project',
        full_amount=100,
        fully_invested=True,
        close_date=datetime.strptime('2019-08-24T14:15:22Z', '%Y-%m-%dT%H:%M:%SZ'),
        create_date=datetime.strptime('2019-08-24T14:15:22Z', '%Y-%m-%dT%H:%M:%SZ'),
    )


@pytest.fixture
def donation(mixer):
    return mixer.blend(
        'app.models.donation.Donation',
        full_amount=1000000,
        comment='To you for chimichangas',
        create_date=datetime.strptime('2019-09-24T14:15:22Z', '%Y-%m-%dT%H:%M:%SZ'),
        user_id=superuser_uuid4,
        invest_amount=100,
        fully_invested=False,
        close_date=datetime.strptime('2019-08-24T14:15:22Z', '%Y-%m-%dT%H:%M:%SZ'),
    )


@pytest.fixture
def dead_pool_donation(mixer):
    return mixer.blend(
        'app.models.donation.Donation',
        full_amount=1000000,
        comment='To you for chimichangas',
        create_date=datetime.strptime('2019-09-24T14:15:22Z', '%Y-%m-%dT%H:%M:%SZ'),
        user_id=user_uuid4,
        invest_amount=100,
        fully_invested=False,
        close_date=datetime.strptime('2019-08-24T14:15:22Z', '%Y-%m-%dT%H:%M:%SZ'),
    )


@pytest.fixture
def small_donation(mixer):
    return mixer.blend(
        'app.models.donation.Donation',
        comment='To you for chimichangas',
        create_date=datetime.strptime('2019-09-24T14:15:22Z', '%Y-%m-%dT%H:%M:%SZ'),
        user_email='evil@pool.com',
        full_amount=50,
        fully_invested=False,
        close_date=datetime.strptime('2019-08-24T14:15:22Z', '%Y-%m-%dT%H:%M:%SZ'),
    )
