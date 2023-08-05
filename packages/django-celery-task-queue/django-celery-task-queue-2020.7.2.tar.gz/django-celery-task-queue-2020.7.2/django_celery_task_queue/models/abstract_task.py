from datetime import datetime

from django.db import models


IGNORED = [
    'is_completed',
    'is_disabled',
    'is_enqueued',
    'is_restarted',
    'disabled_at',
    'enqueued_at',
    'restarted_at',
    'updated_at'
]


def getfields(model):
    fields = list(filter(lambda f: f.name not in IGNORED, model._meta.fields))
    return list(map(lambda f: f.name, fields))


class AbstractTask(models.Model):
    activated_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True)
    disabled_at = models.DateTimeField(null=True)
    enqueued_at = models.DateTimeField(null=True)
    restarted_at = models.DateTimeField(null=True)
    started_at = models.DateTimeField(null=True)
    updated_at = models.DateTimeField(null=True)

    is_completed = models.BooleanField(default=False)
    is_disabled = models.BooleanField(default=False)
    is_enqueued = models.BooleanField(default=False)
    is_restarted = models.BooleanField(default=False)

    priority = models.IntegerField(default=0, null=False)

    task_name = None

    class Meta:
        abstract = True

    def get_db_table(self):
        return self._meta.db_table

    @classmethod
    def get_task_name(model):
        return model.task_name if model.task_name else model._meta.db_table

    @classmethod
    def send_tasks(model, app, enqueued_limit):
        count = enqueued_limit - model.objects.filter(is_enqueued=True).count()
        if count <= 0:
            return
        qs = model.objects.filter(
            is_completed=False, is_enqueued=False, is_disabled=False
        ).only(*getfields(model)).order_by('-priority')
        ids = []
        task_name = model.get_task_name()
        enqueued_at = datetime.now()
        for r in qs[0:count]:
            ids.append(r.id)
            kwargs = dict(enqueued_at=enqueued_at)
            for f in getfields(model):
                kwargs[f] = getattr(r, f)
            app.send_task(task_name, args=[], kwargs=kwargs)
        if ids:
            model.objects.filter(id__in=ids).update(
                is_enqueued=True, enqueued_at=enqueued_at
            )
