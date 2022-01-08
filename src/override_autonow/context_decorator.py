import functools
import inspect
import unittest
from typing import Callable, ContextManager, Set, Tuple, Type, Union
from django.db.models import Model
from django.db.models.fields import DateField, DateTimeField


def override_autonow(
        decorate_target=None,
        *,
        exclude_auto_now: bool = False,
        exclude_auto_now_add: bool = False,
        exclude_date_field: bool = False,
        exclude_datetime_field: bool = False,
        exclude_field_names: Set[str] = None,
        exclude_models: Tuple[Type[Model]] = None,
        override_field_names: Set[str] = None,
        override_models: Tuple[Type[Model]] = None,
) -> Union[ContextManager, Callable]:
    context_decorator = _ContextDecorator(
        exclude_auto_now=exclude_auto_now,
        exclude_auto_now_add=exclude_auto_now_add,
        exclude_date_field=exclude_date_field,
        exclude_datetime_field=exclude_datetime_field,
        exclude_field_names=exclude_field_names,
        exclude_models=exclude_models,
        override_field_names=override_field_names,
        override_models=override_models,
    )
    if decorate_target is not None:
        return context_decorator(decorate_target)
    return context_decorator


class _ContextDecorator:
    def __init__(
            self,
            *,
            exclude_auto_now: bool = False,
            exclude_auto_now_add: bool = False,
            exclude_date_field: bool = False,
            exclude_datetime_field: bool = False,
            exclude_field_names: Set[str] = None,
            exclude_models: Tuple[Type[Model]] = None,
            override_field_names: Set[str] = None,
            override_models: Tuple[Type[Model]] = None,
    ):
        self.exclude_auto_now = exclude_auto_now
        self.exclude_auto_now_add = exclude_auto_now_add
        self.exclude_date_field = exclude_date_field
        self.exclude_datetime_field = exclude_datetime_field
        self.exclude_field_names = set() if not exclude_field_names else set(exclude_field_names)
        self.exclude_models = tuple() if not exclude_models else tuple(exclude_models)
        self.override_field_names = override_field_names if override_field_names is None else set(override_field_names)
        self.override_models = override_models if override_models is None else tuple(override_models)
        self._original_date_field_pre_save = None
        self._original_datetime_field_pre_save = None

    def __call__(self, target):
        if inspect.isclass(target):
            return self.decorate_class(target)
        return self.decorate_callable(target)

    def __enter__(self):
        self.start()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()

    def start(self):
        if not self.exclude_date_field:
            self._original_date_field_pre_save = getattr(DateField, 'pre_save')
            date_field_pre_save_mock = get_pre_save_mock(
                context_decorator=self,
                original=self._original_date_field_pre_save,
            )
            setattr(DateField, 'pre_save', date_field_pre_save_mock)

        if not self.exclude_datetime_field:
            self._original_datetime_field_pre_save = getattr(DateTimeField, 'pre_save')
            datetime_field_pre_save_mock = get_pre_save_mock(
                context_decorator=self,
                original=self._original_datetime_field_pre_save,
            )
            setattr(DateTimeField, 'pre_save', datetime_field_pre_save_mock)

    def stop(self):
        if self._original_datetime_field_pre_save:
            setattr(DateTimeField, 'pre_save', self._original_datetime_field_pre_save)
            self._original_datetime_field_pre_save = None
        if self._original_date_field_pre_save:
            setattr(DateField, 'pre_save', self._original_date_field_pre_save)
            self._original_date_field_pre_save = None

    def decorate_class(self, _class):
        if issubclass(_class, unittest.TestCase):
            original_setup_class = _class.setUpClass
            original_teardown_class = _class.tearDownClass

            @classmethod
            def setUpClass(cls):
                self.start()
                if original_setup_class is not None:
                    original_setup_class()

            @classmethod
            def tearDownClass(cls):
                if original_teardown_class is not None:
                    original_teardown_class()
                self.stop()

            _class.setUpClass = setUpClass
            _class.tearDownClass = tearDownClass

            return _class

        else:
            seen = set()
            classes = _class.mro()
            for base_class in classes:
                for (attr, attr_value) in base_class.__dict__.items():
                    if attr.startswith('_') or attr in seen:
                        continue
                    seen.add(attr)
                    if not callable(attr_value) or inspect.isclass(attr_value):
                        continue
                    try:
                        setattr(_class, attr, self(attr_value))
                    except (AttributeError, TypeError):
                        continue
            return _class

    def decorate_callable(self, func):
        def wrapper(*args, **kwargs):
            with self:
                result = func(*args, **kwargs)
            return result

        functools.update_wrapper(wrapper, func)
        return wrapper

    def should_override(
            self,
            add: bool,
            field_instance: Union[DateField, DateTimeField],
            model_instance: Model,
    ) -> bool:
        if field_instance.attname in self.exclude_field_names:
            return False

        if isinstance(model_instance, self.exclude_models):
            return False

        if self.override_field_names is not None and field_instance.attname not in self.override_field_names:
            return False

        if self.override_models is not None and not isinstance(model_instance, self.override_models):
            return False

        if field_instance.auto_now and self.exclude_auto_now:
            return False

        if add and field_instance.auto_now_add and self.exclude_auto_now_add:
            return False

        return True


def get_pre_save_mock(context_decorator: _ContextDecorator, original: Callable) -> Callable:
    def pre_save(self, model_instance, add):
        if context_decorator.should_override(add=add, field_instance=self, model_instance=model_instance):
            return super(DateField, self).pre_save(model_instance, add)
        return original(self, model_instance, add)

    return pre_save
