from datetime import datetime
import sys
from traceback import format_tb

from django.conf import settings
from django.db.utils import OperationalError

from .models import Exc


class Task:
    model = None

    @classmethod
    def get_task_name(cls):
        return cls.model.get_task_name()

    @classmethod
    def as_func(cls):
        def func(*args, **kwargs):
            task = cls()
            for k, v in kwargs.items():
                setattr(task, k, v)
            task.is_canceled = False
            task.started_at = datetime.now()
            try:
                task.init_task()
                if task.is_canceled:
                    return
                task.run_task()
                if task.is_canceled:
                    return
                task.complete_task()
            # except OperationalError as e:
                # if 'deadlock' in str(e).lower():  # deadlock. shit happens
                #    task.restart_task()
                #    return
            #    task.save_exc()
            #    task.disable_task()
            except Exception:
                task.save_exc()
                task.disable_task()
        return func

    def init_task(self):
        pass

    def run_task(self):
        raise NotImplementedError(
            '%s.run_task NOT IMPLEMENTED' % self.__class__.__name__)

    def delete_task(self):
        self.model.objects.filter(id=self.id).delete()
        self.is_canceled = True

    def complete_task(self, **kwargs):
        kwargs.update(
            is_completed=True,
            is_disabled=False,
            is_enqueued=False,
            is_restarted=False,
            completed_at=datetime.now(),
            disabled_at=None,
            restarted_at=None,
            started_at=self.started_at,
            updated_at=datetime.now()
        )
        self.model.objects.filter(id=self.id).update(**kwargs)
        self.is_canceled = True

    def disable_task(self):
        self.model.objects.filter(id=self.id).update(
            is_disabled=True,
            is_enqueued=False,
            is_restarted=False,
            completed_at=None,
            disabled_at=datetime.now(),
            enqueued_at=None,
            restarted_at=None,
            started_at=None,
            updated_at=datetime.now()
        )
        self.is_canceled = True

    def restart_task(self, priority=None):
        self.model.objects.filter(id=self.id).update(
            is_disabled=False,
            is_enqueued=False,
            is_restarted=True,
            disabled_at=None,
            enqueued_at=None,
            restarted_at=datetime.now(),
            started_at=None,
            updated_at=datetime.now(),
            priority=priority if priority is not None else self.priority
        )
        self.is_canceled = True

    def save_exc(self):
        exc, exc_value, tb = sys.exc_info()
        Exc(
            db_table=self.model._meta.db_table,
            task_id=self.id,
            exc_type=exc.__module__ + '.' + exc.__name__ if exc.__module__ else exc.__name__,
            exc_value=exc_value if exc_value else '',
            exc_traceback='\n'.join(format_tb(tb))
        ).save()
