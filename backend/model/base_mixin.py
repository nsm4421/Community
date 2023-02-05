from database.connection import custom_database

from sqlalchemy import Column, Integer, DateTime, func
from sqlalchemy.orm import Session

class BaseMixin:
    """
        - 객체 id
        - 생성시간
        - 수정시간
        - 삭제시간
        TODO : 인증기능 구현 후 생성한 사람, 수정한 사람 추가 컬럼
    """
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, nullable=False, default=func.utc_timestamp())
    updated_at = Column(DateTime, nullable=False, default=func.utc_timestamp(), onupdate=func.utc_timestamp())
    removed_at = Column(DateTime, nullable=True)

    def __init__(cls):
        cls._q = None
        cls._session = None

    @classmethod
    def __hash__(cls):
        return hash(cls.id)

    @classmethod
    def columns(cls, exclude_meta=True):
        """
            모든 컬럼명 가져오기
            - exclude_meta = True → 메타데이터(id, create, updated_at, removed_at) 제외
            - exclude_meta = False → 모든 컬럼명 return
        """
        if exclude_meta:
            return [c for c in cls.__table__.columns if (c.name not in ['id','created_at','updated_at','removed_at'])]
        return cls.__table__.columns

    @classmethod
    def create(cls, session:Session, auto_commit=False, **kds):
        """
            객체를 생성하는 메써드
            Ex) User.create(session, name="Karma", age=29)
        """
        obj = cls()
        for col in obj.columns():   
            if col.name in kds:
                setattr(obj, col.name, kds.get(col.name))
        session.add(obj)
        session.flush()
        if auto_commit:
            session.commit()
        return obj
    
    @classmethod
    def get_first(cls, session: Session = None, **kds):
        """
            한개만 조회
        """
        s = next(custom_database.session()) if not session else session
        q = s.query(cls)
        for k, v in kds.items():
            q = q.filter(getattr(cls, k) == v)
        if not s:
            session.close()
        return q.first()

    @classmethod
    def get(cls, session: Session = None, **kds):
        """
            전체 조회
        """
        s = next(custom_database.session()) if not session else session
        q = s.query(cls)
        for k, v in kds.items():
            q = q.filter(getattr(cls, k) == v)
        if not s:
            session.close()
        return q.all()

    @classmethod
    def get_page(cls, session: Session = None, unit_per_page:int=10, page:int=0, **kds):
        """
            페이지 형태로 반환
            - unit_per_page : 페이지 당 반환 개수 (default 10)
            - page : 페이지수 (default 0)
        """
        s = next(custom_database.session()) if not session else session
        q = s.query(cls)
        for k, v in kds.items():
            q = q.filter(getattr(cls, k) == v)
        q = q.order_by(cls.created_at.desc)
        q.offset(unit_per_page*page).limit(unit_per_page).all()
        if not s:
            session.close()
        return q.all()
    
    @classmethod
    def delete(cls, session: Session = None):
        s = next(custom_database.session()) if not session else session
        q = s.query(cls)
        q.delete()