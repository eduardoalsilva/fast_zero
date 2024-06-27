from sqlalchemy import select

from fast_zero.models import User


def test_create_user(session):
    user = User(username='Eduardo',
                email='eduardo@email.com',
                password='123A'
            )

    session.add(user)
    session.commit()
    result = session.scalar(
        select(User).where(User.email == 'eduardo@email.com')
    )

    assert result.username == 'Eduardo'
