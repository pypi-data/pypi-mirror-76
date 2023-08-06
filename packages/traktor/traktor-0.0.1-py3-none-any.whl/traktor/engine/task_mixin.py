from typing import List, Optional

from sqlalchemy import orm

from traktor import errors
from traktor.models import DB, RGB, Task
from traktor.engine.project_mixin import ProjectMixin


class TaskMixin(ProjectMixin):
    @classmethod
    def task_list(cls, session: orm.Session, project: str) -> List[Task]:
        """List all tasks in a project.

        Args:
            session (orm.Session): SQLAlchemy session.
            project (str): Project name.
        """
        project = cls.project_get(session=session, name=project)

        return DB.filter(
            session=session,
            model=Task,
            filters=[Task.project_id == project.id],
        )

    @classmethod
    def task_get(cls, session: orm.Session, project: str, name: str) -> Task:
        project = cls.project_get(session=session, name=project)
        return DB.get(
            session=session,
            model=Task,
            filters=[Task.project_id == project.id, Task.name == name],
        )

    @classmethod
    def task_get_or_create(
        cls,
        session: orm.Session,
        project: str,
        name: str,
        color: Optional[RGB] = None,
    ) -> Task:
        project = cls.project_get(session=session, name=project)
        try:
            obj = cls.task_get(
                session=session, project=project.name, name=name
            )
            if color is not None:
                if obj.color != color:
                    obj.color = color
                    DB.save(session=session, obj=obj)

        except errors.ObjectNotFound:
            obj = Task(
                project_id=project.id,
                name=name,
                color_hex=(color or RGB()).hex,
            )
            DB.save(session=session, obj=obj)

        return obj

    @classmethod
    def task_rename(
        cls, session: orm.Session, project: str, name: str, new_name: str
    ) -> Task:
        task = cls.task_get(session=session, project=project, name=name)
        task.name = new_name
        DB.save(session=session, obj=task)
        return task

    @staticmethod
    def task_delete(session: orm.Session, task: Task):
        DB.delete(session=session, obj=task)
