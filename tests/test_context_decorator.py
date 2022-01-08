import pytest
from django.test import TestCase
from override_autonow import override_autonow

from .testapp.models import AutoFieldsModel, AutoFieldsModel2


class TestOverrideMixin(TestCase):
    def assertIsOverridden(self, *args, **kwargs):
        self.assertIsNone(*args, **kwargs)

    def assertIsNotOverridden(self, *args, **kwargs):
        self.assertIsNotNone(*args, **kwargs)


def assert_is_overridden(value):
    assert value is None


def assert_is_not_overridden(value):
    assert value is not None


class TestContextManager(TestOverrideMixin, TestCase):
    def test_context_manager(self):
        with override_autonow():
            obj = AutoFieldsModel.objects.create()

        self.assertIsOverridden(obj.date_auto_now)
        self.assertIsOverridden(obj.date_auto_now_add)
        self.assertIsOverridden(obj.datetime_auto_now)
        self.assertIsOverridden(obj.datetime_auto_now_add)

    def test_before_context_manager(self):
        obj = AutoFieldsModel.objects.create()
        with override_autonow():
            pass

        self.assertIsNotOverridden(obj.date_auto_now)
        self.assertIsNotOverridden(obj.date_auto_now_add)
        self.assertIsNotOverridden(obj.datetime_auto_now)
        self.assertIsNotOverridden(obj.datetime_auto_now_add)

    def test_after_context_manager(self):
        with override_autonow():
            pass
        obj = AutoFieldsModel.objects.create()

        self.assertIsNotOverridden(obj.date_auto_now)
        self.assertIsNotOverridden(obj.date_auto_now_add)
        self.assertIsNotOverridden(obj.datetime_auto_now)
        self.assertIsNotOverridden(obj.datetime_auto_now_add)

    def test_exclude_auto_now(self):
        with override_autonow(exclude_auto_now=True):
            obj = AutoFieldsModel.objects.create()

        self.assertIsNotOverridden(obj.date_auto_now)
        self.assertIsOverridden(obj.date_auto_now_add)
        self.assertIsNotOverridden(obj.datetime_auto_now)
        self.assertIsOverridden(obj.datetime_auto_now_add)

    def test_exclude_auto_now_add(self):
        with override_autonow(exclude_auto_now_add=True):
            obj = AutoFieldsModel.objects.create()

        self.assertIsOverridden(obj.date_auto_now)
        self.assertIsNotOverridden(obj.date_auto_now_add)
        self.assertIsOverridden(obj.datetime_auto_now)
        self.assertIsNotOverridden(obj.datetime_auto_now_add)

    def test_exclude_date_field(self):
        with override_autonow(exclude_date_field=True):
            obj = AutoFieldsModel.objects.create()

        self.assertIsNotOverridden(obj.date_auto_now)
        self.assertIsNotOverridden(obj.date_auto_now_add)
        self.assertIsOverridden(obj.datetime_auto_now)
        self.assertIsOverridden(obj.datetime_auto_now_add)

    def test_exclude_datetime_field(self):
        with override_autonow(exclude_datetime_field=True):
            obj = AutoFieldsModel.objects.create()

        self.assertIsOverridden(obj.date_auto_now)
        self.assertIsOverridden(obj.date_auto_now_add)
        self.assertIsNotOverridden(obj.datetime_auto_now)
        self.assertIsNotOverridden(obj.datetime_auto_now_add)

    def test_exclude_field_names(self):
        with override_autonow(exclude_field_names={'date_auto_now', 'datetime_auto_now_add'}):
            obj = AutoFieldsModel.objects.create()

        self.assertIsNotOverridden(obj.date_auto_now)
        self.assertIsOverridden(obj.date_auto_now_add)
        self.assertIsOverridden(obj.datetime_auto_now)
        self.assertIsNotOverridden(obj.datetime_auto_now_add)

    def test_exclude_models(self):
        with override_autonow(exclude_models=(AutoFieldsModel2,)):
            obj1 = AutoFieldsModel.objects.create()
            obj2 = AutoFieldsModel2.objects.create()

        self.assertIsOverridden(obj1.date_auto_now)
        self.assertIsOverridden(obj1.date_auto_now_add)
        self.assertIsOverridden(obj1.datetime_auto_now)
        self.assertIsOverridden(obj1.datetime_auto_now_add)

        self.assertIsNotOverridden(obj2.date_auto_now)
        self.assertIsNotOverridden(obj2.date_auto_now_add)
        self.assertIsNotOverridden(obj2.datetime_auto_now)
        self.assertIsNotOverridden(obj2.datetime_auto_now_add)

    def test_override_field_names(self):
        with override_autonow(override_field_names={'date_auto_now', 'datetime_auto_now_add'}):
            obj = AutoFieldsModel.objects.create()

        self.assertIsOverridden(obj.date_auto_now)
        self.assertIsNotOverridden(obj.date_auto_now_add)
        self.assertIsNotOverridden(obj.datetime_auto_now)
        self.assertIsOverridden(obj.datetime_auto_now_add)

    def test_override_models(self):
        with override_autonow(override_models=(AutoFieldsModel2,)):
            obj1 = AutoFieldsModel.objects.create()
            obj2 = AutoFieldsModel2.objects.create()

        self.assertIsNotOverridden(obj1.date_auto_now)
        self.assertIsNotOverridden(obj1.date_auto_now_add)
        self.assertIsNotOverridden(obj1.datetime_auto_now)
        self.assertIsNotOverridden(obj1.datetime_auto_now_add)

        self.assertIsOverridden(obj2.date_auto_now)
        self.assertIsOverridden(obj2.date_auto_now_add)
        self.assertIsOverridden(obj2.datetime_auto_now)
        self.assertIsOverridden(obj2.datetime_auto_now_add)

    def test_nested_context_managers(self):
        with override_autonow(override_models=(AutoFieldsModel,)):
            with override_autonow(override_models=(AutoFieldsModel2,)):
                obj1 = AutoFieldsModel.objects.create()
                obj2 = AutoFieldsModel2.objects.create()

        self.assertIsOverridden(obj1.date_auto_now)
        self.assertIsOverridden(obj1.date_auto_now_add)
        self.assertIsOverridden(obj1.datetime_auto_now)
        self.assertIsOverridden(obj1.datetime_auto_now_add)

        self.assertIsOverridden(obj2.date_auto_now)
        self.assertIsOverridden(obj2.date_auto_now_add)
        self.assertIsOverridden(obj2.datetime_auto_now)
        self.assertIsOverridden(obj2.datetime_auto_now_add)


class TestDjangoTestCaseMethodDecorator(TestOverrideMixin, TestCase):

    @override_autonow
    def test_method_decorator(self):
        obj = AutoFieldsModel.objects.create()

        self.assertIsOverridden(obj.date_auto_now)
        self.assertIsOverridden(obj.date_auto_now_add)
        self.assertIsOverridden(obj.datetime_auto_now)
        self.assertIsOverridden(obj.datetime_auto_now_add)

    def test_without_method_decorator(self):
        obj = AutoFieldsModel.objects.create()

        self.assertIsNotOverridden(obj.date_auto_now)
        self.assertIsNotOverridden(obj.date_auto_now_add)
        self.assertIsNotOverridden(obj.datetime_auto_now)
        self.assertIsNotOverridden(obj.datetime_auto_now_add)

    @override_autonow(exclude_auto_now=True)
    def test_exclude_auto_now(self):
        obj = AutoFieldsModel.objects.create()

        self.assertIsNotOverridden(obj.date_auto_now)
        self.assertIsOverridden(obj.date_auto_now_add)
        self.assertIsNotOverridden(obj.datetime_auto_now)
        self.assertIsOverridden(obj.datetime_auto_now_add)

    @override_autonow(exclude_auto_now_add=True)
    def test_exclude_auto_now_add(self):
        obj = AutoFieldsModel.objects.create()

        self.assertIsOverridden(obj.date_auto_now)
        self.assertIsNotOverridden(obj.date_auto_now_add)
        self.assertIsOverridden(obj.datetime_auto_now)
        self.assertIsNotOverridden(obj.datetime_auto_now_add)

    @override_autonow(exclude_date_field=True)
    def test_exclude_date_field(self):
        obj = AutoFieldsModel.objects.create()

        self.assertIsNotOverridden(obj.date_auto_now)
        self.assertIsNotOverridden(obj.date_auto_now_add)
        self.assertIsOverridden(obj.datetime_auto_now)
        self.assertIsOverridden(obj.datetime_auto_now_add)

    @override_autonow(exclude_datetime_field=True)
    def test_exclude_datetime_field(self):
        obj = AutoFieldsModel.objects.create()

        self.assertIsOverridden(obj.date_auto_now)
        self.assertIsOverridden(obj.date_auto_now_add)
        self.assertIsNotOverridden(obj.datetime_auto_now)
        self.assertIsNotOverridden(obj.datetime_auto_now_add)

    @override_autonow(exclude_field_names={'date_auto_now', 'datetime_auto_now_add'})
    def test_exclude_field_names(self):
        obj = AutoFieldsModel.objects.create()

        self.assertIsNotOverridden(obj.date_auto_now)
        self.assertIsOverridden(obj.date_auto_now_add)
        self.assertIsOverridden(obj.datetime_auto_now)
        self.assertIsNotOverridden(obj.datetime_auto_now_add)

    @override_autonow(exclude_models=(AutoFieldsModel2,))
    def test_exclude_models(self):
        obj1 = AutoFieldsModel.objects.create()
        obj2 = AutoFieldsModel2.objects.create()

        self.assertIsOverridden(obj1.date_auto_now)
        self.assertIsOverridden(obj1.date_auto_now_add)
        self.assertIsOverridden(obj1.datetime_auto_now)
        self.assertIsOverridden(obj1.datetime_auto_now_add)

        self.assertIsNotOverridden(obj2.date_auto_now)
        self.assertIsNotOverridden(obj2.date_auto_now_add)
        self.assertIsNotOverridden(obj2.datetime_auto_now)
        self.assertIsNotOverridden(obj2.datetime_auto_now_add)

    @override_autonow(override_field_names={'date_auto_now', 'datetime_auto_now_add'})
    def test_override_field_names(self):
        obj = AutoFieldsModel.objects.create()

        self.assertIsOverridden(obj.date_auto_now)
        self.assertIsNotOverridden(obj.date_auto_now_add)
        self.assertIsNotOverridden(obj.datetime_auto_now)
        self.assertIsOverridden(obj.datetime_auto_now_add)

    @override_autonow(override_models=(AutoFieldsModel2,))
    def test_override_models(self):
        obj1 = AutoFieldsModel.objects.create()
        obj2 = AutoFieldsModel2.objects.create()

        self.assertIsNotOverridden(obj1.date_auto_now)
        self.assertIsNotOverridden(obj1.date_auto_now_add)
        self.assertIsNotOverridden(obj1.datetime_auto_now)
        self.assertIsNotOverridden(obj1.datetime_auto_now_add)

        self.assertIsOverridden(obj2.date_auto_now)
        self.assertIsOverridden(obj2.date_auto_now_add)
        self.assertIsOverridden(obj2.datetime_auto_now)
        self.assertIsOverridden(obj2.datetime_auto_now_add)

    @override_autonow(override_models=(AutoFieldsModel,))
    @override_autonow(override_models=(AutoFieldsModel2,))
    def test_nested_method_decorators(self):
        obj1 = AutoFieldsModel.objects.create()
        obj2 = AutoFieldsModel2.objects.create()

        self.assertIsOverridden(obj1.date_auto_now)
        self.assertIsOverridden(obj1.date_auto_now_add)
        self.assertIsOverridden(obj1.datetime_auto_now)
        self.assertIsOverridden(obj1.datetime_auto_now_add)

        self.assertIsOverridden(obj2.date_auto_now)
        self.assertIsOverridden(obj2.date_auto_now_add)
        self.assertIsOverridden(obj2.datetime_auto_now)
        self.assertIsOverridden(obj2.datetime_auto_now_add)


@pytest.mark.django_db
class TestPytestMethodDecorator:

    @override_autonow
    def test_method_decorator(self):
        obj = AutoFieldsModel.objects.create()

        assert_is_overridden(obj.date_auto_now)
        assert_is_overridden(obj.date_auto_now_add)
        assert_is_overridden(obj.datetime_auto_now)
        assert_is_overridden(obj.datetime_auto_now_add)

    def test_without_method_decorator(self):
        obj = AutoFieldsModel.objects.create()

        assert_is_not_overridden(obj.date_auto_now)
        assert_is_not_overridden(obj.date_auto_now_add)
        assert_is_not_overridden(obj.datetime_auto_now)
        assert_is_not_overridden(obj.datetime_auto_now_add)

    @override_autonow(exclude_auto_now=True)
    def test_exclude_auto_now(self):
        obj = AutoFieldsModel.objects.create()

        assert_is_not_overridden(obj.date_auto_now)
        assert_is_overridden(obj.date_auto_now_add)
        assert_is_not_overridden(obj.datetime_auto_now)
        assert_is_overridden(obj.datetime_auto_now_add)

    @override_autonow(exclude_auto_now_add=True)
    def test_exclude_auto_now_add(self):
        obj = AutoFieldsModel.objects.create()

        assert_is_overridden(obj.date_auto_now)
        assert_is_not_overridden(obj.date_auto_now_add)
        assert_is_overridden(obj.datetime_auto_now)
        assert_is_not_overridden(obj.datetime_auto_now_add)

    @override_autonow(exclude_date_field=True)
    def test_exclude_date_field(self):
        obj = AutoFieldsModel.objects.create()

        assert_is_not_overridden(obj.date_auto_now)
        assert_is_not_overridden(obj.date_auto_now_add)
        assert_is_overridden(obj.datetime_auto_now)
        assert_is_overridden(obj.datetime_auto_now_add)

    @override_autonow(exclude_datetime_field=True)
    def test_exclude_datetime_field(self):
        obj = AutoFieldsModel.objects.create()

        assert_is_overridden(obj.date_auto_now)
        assert_is_overridden(obj.date_auto_now_add)
        assert_is_not_overridden(obj.datetime_auto_now)
        assert_is_not_overridden(obj.datetime_auto_now_add)

    @override_autonow(exclude_field_names={'date_auto_now', 'datetime_auto_now_add'})
    def test_exclude_field_names(self):
        obj = AutoFieldsModel.objects.create()

        assert_is_not_overridden(obj.date_auto_now)
        assert_is_overridden(obj.date_auto_now_add)
        assert_is_overridden(obj.datetime_auto_now)
        assert_is_not_overridden(obj.datetime_auto_now_add)

    @override_autonow(exclude_models=(AutoFieldsModel2,))
    def test_exclude_models(self):
        obj1 = AutoFieldsModel.objects.create()
        obj2 = AutoFieldsModel2.objects.create()

        assert_is_overridden(obj1.date_auto_now)
        assert_is_overridden(obj1.date_auto_now_add)
        assert_is_overridden(obj1.datetime_auto_now)
        assert_is_overridden(obj1.datetime_auto_now_add)

        assert_is_not_overridden(obj2.date_auto_now)
        assert_is_not_overridden(obj2.date_auto_now_add)
        assert_is_not_overridden(obj2.datetime_auto_now)
        assert_is_not_overridden(obj2.datetime_auto_now_add)

    @override_autonow(override_field_names={'date_auto_now', 'datetime_auto_now_add'})
    def test_override_field_names(self):
        obj = AutoFieldsModel.objects.create()

        assert_is_overridden(obj.date_auto_now)
        assert_is_not_overridden(obj.date_auto_now_add)
        assert_is_not_overridden(obj.datetime_auto_now)
        assert_is_overridden(obj.datetime_auto_now_add)

    @override_autonow(override_models=(AutoFieldsModel2,))
    def test_override_models(self):
        obj1 = AutoFieldsModel.objects.create()
        obj2 = AutoFieldsModel2.objects.create()

        assert_is_not_overridden(obj1.date_auto_now)
        assert_is_not_overridden(obj1.date_auto_now_add)
        assert_is_not_overridden(obj1.datetime_auto_now)
        assert_is_not_overridden(obj1.datetime_auto_now_add)

        assert_is_overridden(obj2.date_auto_now)
        assert_is_overridden(obj2.date_auto_now_add)
        assert_is_overridden(obj2.datetime_auto_now)
        assert_is_overridden(obj2.datetime_auto_now_add)

    @override_autonow(override_models=(AutoFieldsModel,))
    @override_autonow(override_models=(AutoFieldsModel2,))
    def test_nested_method_decorators(self):
        obj1 = AutoFieldsModel.objects.create()
        obj2 = AutoFieldsModel2.objects.create()

        assert_is_overridden(obj1.date_auto_now)
        assert_is_overridden(obj1.date_auto_now_add)
        assert_is_overridden(obj1.datetime_auto_now)
        assert_is_overridden(obj1.datetime_auto_now_add)

        assert_is_overridden(obj2.date_auto_now)
        assert_is_overridden(obj2.date_auto_now_add)
        assert_is_overridden(obj2.datetime_auto_now)
        assert_is_overridden(obj2.datetime_auto_now_add)


@pytest.mark.django_db
@override_autonow
def test_pytest_function_with_decorator():
    obj = AutoFieldsModel.objects.create()

    assert_is_overridden(obj.date_auto_now)
    assert_is_overridden(obj.date_auto_now_add)
    assert_is_overridden(obj.datetime_auto_now)
    assert_is_overridden(obj.datetime_auto_now_add)


@pytest.mark.django_db
def test_pytest_function_without_decorator():
    obj = AutoFieldsModel.objects.create()

    assert_is_not_overridden(obj.date_auto_now)
    assert_is_not_overridden(obj.date_auto_now_add)
    assert_is_not_overridden(obj.datetime_auto_now)
    assert_is_not_overridden(obj.datetime_auto_now_add)


@override_autonow(override_models=(AutoFieldsModel,))
@override_autonow(override_models=(AutoFieldsModel2,))
@pytest.mark.django_db
def test_pytest_function_with_nested_decorators():
    obj1 = AutoFieldsModel.objects.create()
    obj2 = AutoFieldsModel2.objects.create()

    assert_is_overridden(obj1.date_auto_now)
    assert_is_overridden(obj1.date_auto_now_add)
    assert_is_overridden(obj1.datetime_auto_now)
    assert_is_overridden(obj1.datetime_auto_now_add)

    assert_is_overridden(obj2.date_auto_now)
    assert_is_overridden(obj2.date_auto_now_add)
    assert_is_overridden(obj2.datetime_auto_now)
    assert_is_overridden(obj2.datetime_auto_now_add)


@override_autonow
class TestDjangoTestCaseClassDecorator(TestOverrideMixin, TestCase):

    def test_class_decorator(self):
        obj = AutoFieldsModel.objects.create()

        self.assertIsOverridden(obj.date_auto_now)
        self.assertIsOverridden(obj.date_auto_now_add)
        self.assertIsOverridden(obj.datetime_auto_now)
        self.assertIsOverridden(obj.datetime_auto_now_add)


@override_autonow(override_models=(AutoFieldsModel,))
@override_autonow(override_models=(AutoFieldsModel2,))
class TestDjangoTestCaseWithNestedClassDecorators(TestOverrideMixin, TestCase):
    def test_nested_class_decorators(self):
        obj1 = AutoFieldsModel.objects.create()
        obj2 = AutoFieldsModel2.objects.create()

        self.assertIsOverridden(obj1.date_auto_now)
        self.assertIsOverridden(obj1.date_auto_now_add)
        self.assertIsOverridden(obj1.datetime_auto_now)
        self.assertIsOverridden(obj1.datetime_auto_now_add)

        self.assertIsOverridden(obj2.date_auto_now)
        self.assertIsOverridden(obj2.date_auto_now_add)
        self.assertIsOverridden(obj2.datetime_auto_now)
        self.assertIsOverridden(obj2.datetime_auto_now_add)


@pytest.mark.django_db
@override_autonow
class TestPytestClassDecorator:

    def test_class_decorator(self):
        obj = AutoFieldsModel.objects.create()

        assert_is_overridden(obj.date_auto_now)
        assert_is_overridden(obj.date_auto_now_add)
        assert_is_overridden(obj.datetime_auto_now)
        assert_is_overridden(obj.datetime_auto_now_add)


@override_autonow(override_models=(AutoFieldsModel,))
@override_autonow(override_models=(AutoFieldsModel2,))
@pytest.mark.django_db
class TestPytestWithNestedClassDecorators:
    def test_nested_class_decorators(self):
        obj1 = AutoFieldsModel.objects.create()
        obj2 = AutoFieldsModel2.objects.create()

        assert_is_overridden(obj1.date_auto_now)
        assert_is_overridden(obj1.date_auto_now_add)
        assert_is_overridden(obj1.datetime_auto_now)
        assert_is_overridden(obj1.datetime_auto_now_add)

        assert_is_overridden(obj2.date_auto_now)
        assert_is_overridden(obj2.date_auto_now_add)
        assert_is_overridden(obj2.datetime_auto_now)
        assert_is_overridden(obj2.datetime_auto_now_add)
