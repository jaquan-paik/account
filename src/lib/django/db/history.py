import json

from django.core.serializers.json import DjangoJSONEncoder
from django.db import Error, connections, models
from django.db.models.fields.files import ImageFieldFile
from django.forms import model_to_dict
from threadlocals.threadlocals import get_current_request

from infra.configure.config import GeneralConfig
from infra.configure.constants import SiteType


class ModelHistory:
    def contribute_to_class(self, cls, name) -> None:
        def _contribute(sender, **kwargs) -> None:
            _create_history_table_if_not_exists(cls)
            model = _create_history_model(sender)

            def _write_save_history(sender, instance, created, **kwargs) -> None:
                if not instance.need_to_record_history:
                    return

                _write_history('save', instance, model)

            def _write_delete_history(sender, instance, **kwargs) -> None:
                if not instance.need_to_record_history:
                    return

                _write_history('delete', instance, model)

            models.signals.post_save.connect(_write_save_history, sender=cls, weak=False)

            models.signals.post_delete.connect(_write_delete_history, sender=cls, weak=False)

        models.signals.class_prepared.connect(_contribute, sender=cls, weak=False)


class HistoryMixin:
    _need_to_record_history = True

    @property
    def need_to_record_history(self):
        return self._need_to_record_history

    @need_to_record_history.setter
    def need_to_record_history(self, value):
        self._need_to_record_history = value


class CustomDjangoJSONEncoder(DjangoJSONEncoder):
    """
    기존 DjangoJSONEncoder 에서 TypeError: not serialzable 에러나는 부분을 최대한 serialize 하기 위해 상속
    """

    def default(self, o) -> str:  # pylint: disable=E0202
        if isinstance(o, ImageFieldFile):
            return str(o)
        else:
            try:
                return super().default(o)
            except TypeError:
                return str(o)


def _write_history(action, instance, model):
    """
    django model의 json 변환을 위해 기존 django에서 기본으로 제공하는 serializer.serialize 를 사용하면
    exclude password 같은 옵션이 없음. 이에 django model을 dict로 변환하면서 exclude 옵션을 사용하고
    이를 다시 json으로 변환하는 방법을 사용.
    """
    instance_dict = model_to_dict(instance, exclude=['password'])
    history_dict = {
        'action': action,
        'instance': instance_dict
    }
    history_json = json.dumps(history_dict, cls=CustomDjangoJSONEncoder)

    request = get_current_request()
    actor = None
    if request and request.user:
        actor = '%s : %s' % (GeneralConfig.get_site(), request.user.id)

    try:
        model._default_manager.create(row_id=instance.pk, json=history_json, actor=actor)  # pylint: disable=protected-access
    except Error:
        pass


def _get_history_table_name(cls) -> str:
    return '{}_history'.format(cls._meta.db_table)  # pylint: disable=protected-access


def _create_history_table_if_not_exists(cls) -> None:
    # 여러 사이트에서 뜨면서 동시에 같은 테이블을 만들기 때문에 테이블 생성은 admin 사이트에서만
    if GeneralConfig.get_site() is not SiteType.ADMIN:
        return

    table_name = _get_history_table_name(cls)
    current_tables = connections['log'].introspection.table_names()
    if table_name not in current_tables:
        cursor = connections['log'].cursor()
        cursor.execute('''
            CREATE TABLE %s (
                `id` int(11) NOT NULL AUTO_INCREMENT,
                `row_id` int(11) NOT NULL,
                `reg_date` datetime(6) NOT NULL,
                `json` text,
                `actor` varchar(30) DEFAULT NULL,
                PRIMARY KEY (`id`),
                KEY `row_id` (`row_id`)
            ) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;
        ''' % table_name)


def _create_history_model(cls):
    name = cls.__name__ + 'History'

    class Meta:
        db_table = '{}_history'.format(cls._meta.db_table)  # pylint: disable=protected-access
        app_label = cls._meta.app_label  # pylint: disable=protected-access
        verbose_name_plural = '%s history' % cls._meta.verbose_name  # pylint: disable=protected-access

    attrs = {
        '__module__': cls.__module__,
        'Meta': Meta,
        'id': models.AutoField(primary_key=True),
        'row_id': models.IntegerField(db_index=True, null=False),
        'json': models.TextField(help_text='히스토리'),
        'reg_date': models.DateTimeField(auto_now_add=True, editable=False, help_text='등록일'),
        'actor': models.CharField(max_length=20, help_text='액터'),
    }

    return type(name, (models.Model,), attrs)
