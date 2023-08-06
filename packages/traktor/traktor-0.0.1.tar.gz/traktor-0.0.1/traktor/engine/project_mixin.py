from typing import List, Optional


from sqlalchemy import orm

from traktor import errors
from traktor.models import DB, RGB, Project


class ProjectMixin:
    @staticmethod
    def project_list(session: orm.Session) -> List[Project]:
        return DB.all(session=session, model=Project)

    @staticmethod
    def project_get(session: orm.Session, name: str) -> Project:
        return DB.get(
            session=session, model=Project, filters=[Project.name == name]
        )

    @classmethod
    def project_get_or_create(
        cls, session: orm.Session, name: str, color: Optional[RGB] = None
    ) -> Project:
        try:
            obj = cls.project_get(session=session, name=name)
            if color is not None:
                if obj.color != color:
                    obj.color = color
                    DB.save(session=session, obj=obj)
        except errors.ObjectNotFound:
            obj = Project(name=name, color_hex=(color or RGB()).hex)
            DB.save(session=session, obj=obj)

        return obj

    @classmethod
    def project_rename(
        cls, session: orm.Session, name: str, new_name: str
    ) -> Project:
        project = cls.project_get(session=session, name=name)
        project.name = new_name
        DB.save(session=session, obj=project)
        return project

    @classmethod
    def project_delete(cls, session: orm.Session, project: Project):
        DB.delete(session=session, obj=project)
