===========================
django-override-autonow
===========================

.. image:: https://img.shields.io/pypi/v/django-override-autonow.svg
    :target: https://pypi.org/project/django-override-autonow/
    :alt: PyPI Version

.. image:: https://github.com/yukihira1992/django-override-autonow/actions/workflows/test-package.yml/badge.svg
    :target: https://github.com/yukihira1992/django-override-autonow/actions
    :alt: Build status

``django-override-autonow`` is a testing tool for Django's project.
``django-override-autonow`` makes it easy to create model instance using ``DateField`` or ``DateTimeField`` with ``auto_now`` or ``auto_now_add`` options.

An example of django's model:

.. code-block:: python

    from django.db import models


    class Order(models.Model):
        amount = models.IntegerField()
        status = models.CharField(max_length=100)
        created_time = models.DateTimeField(auto_now_add=True)
        updated_time = models.DateTimeField(auto_now=True)

To test this model:

.. code-block:: python

    from unittest import mock

    from django.test import TestCase
    from django.utils import timezone
    from override_autonow import override_autonow

    from .models import Order


    class TestOrder(TestCase):

        @override_autonow
        def test_with_django_override_autonow(self):
            # We need a order with desired created_time and updated_time for test
            order = Order.objects.create(
                amount=200,
                status='PAID',
                created_time=timezone.datetime(year=2022, month=1, day=1, hour=23, minute=59, second=59),
                updated_time=timezone.datetime(year=2022, month=1, day=2, hour=0, minute=0, second=0),
            )

            # test order

        def test_without_django_override_autonow(self):
            # Django's standard way is to mock timezone.now and save the model.

            # First, create object with mocking timezone.now and set desired value to created_time field
            with mock.patch('django.db.models.fields.timezone') as mock_timezone:
                mock_timezone.now.return_value = timezone.datetime(year=2022, month=1, day=1, hour=23, minute=59, second=59)
                order = Order.objects.create(
                    amount=200,
                    status='PAID',
                )

            # Second, save object again with mocking timezone.now and set desired value to updated_time field
            with mock.patch('django.db.models.fields.timezone') as mock_timezone:
                mock_timezone.now.return_value = timezone.datetime(year=2022, month=1, day=2, hour=0, minute=0, second=0)
                order.save()

            # test order

Features
========

- Support Django 2.2+ and Python 3.7+
- Compatible with major testing packages
    - `pytest <https://docs.pytest.org/en/6.2.x/>`_'s class based test and function based test with `pytest-django <https://pytest-django.readthedocs.io/en/latest/>`_
    - `factory-boy <https://factoryboy.readthedocs.io/en/stable/>`_'s model factory
- Choose suitable style for your situation
    - Method decorator
    - Class decorator
    - Context manager
- Flexible override target selection
    - Affects only specified field names and exclude specified field names
    - Affects only specified models and exclude specified field names
    - Affects only ``auto_now`` option or ``auto_now_add`` option
    - Affects only ``DateField`` or ``DateTimeField``

Installation
============

Installing from PyPI::

    pip install django-override-autonow

Use Cases
=========

Test with Django's TestCase:

.. code-block:: python

    from django.test import TestCase

    from override_autonow import override_autonow

    from .models import Order


    class TestOrder(TestCase):

        # as method decorator

        @override_autonow
        def test_with_method_decorator(self):
            order = Order.objects.create(
                amount=200,
                status='PAID',
                created_time=timezone.datetime(year=2022, month=1, day=1, hour=23, minute=59, second=59),
                updated_time=timezone.datetime(year=2022, month=1, day=2, hour=0, minute=0, second=0),
            )

            # test order

        def test_with_context_manager(self):

            # as context manager

            with override_autonow():
                order_with_override = Order.objects.create(
                    amount=200,
                    status='PAID',
                    created_time=timezone.datetime(year=2022, month=1, day=1, hour=23, minute=59, second=59),
                    updated_time=timezone.datetime(year=2022, month=1, day=2, hour=0, minute=0, second=0),
                )

            order_without_override = Order.objects.create(
                amount=200,
                status='PAID',
            )

            # test order


    # as class decorator

    @override_autonow
    class TestWithClassDecorator(TestCase):
        def test_with_class_decorator(self):
            order = Order.objects.create(
                amount=200,
                status='PAID',
                created_time=timezone.datetime(year=2022, month=1, day=1, hour=23, minute=59, second=59),
                updated_time=timezone.datetime(year=2022, month=1, day=2, hour=0, minute=0, second=0),
            )

            # test order

Test with pytest(pytest-django):

.. code-block:: python

    import pytest

    from override_autonow import override_autonow

    from .models import Order


    @pytest.mark.django_db
    class TestOrder:

        # as method decorator

        @override_autonow
        def test_with_method_decorator(self):
            order = Order.objects.create(
                amount=200,
                status='PAID',
                created_time=timezone.datetime(year=2022, month=1, day=1, hour=23, minute=59, second=59),
                updated_time=timezone.datetime(year=2022, month=1, day=2, hour=0, minute=0, second=0),
            )

            # test order

        def test_with_context_manager(self):

            # as context manager

            with override_autonow():
                order_without_autonow = Order.objects.create(
                    amount=200,
                    status='PAID',
                    created_time=timezone.datetime(year=2022, month=1, day=1, hour=23, minute=59, second=59),
                    updated_time=timezone.datetime(year=2022, month=1, day=2, hour=0, minute=0, second=0),
                )

            order_with_autonow = Order.objects.create(
                amount=200,
                status='PAID',
            )

            # test order


    # as class decorator

    @override_autonow
    @pytest.mark.django_db
    class TestWithClassDecorator:
        def test_with_class_decorator(self):
            order = Order.objects.create(
                amount=200,
                status='PAID',
                created_time=timezone.datetime(year=2022, month=1, day=1, hour=23, minute=59, second=59),
                updated_time=timezone.datetime(year=2022, month=1, day=2, hour=0, minute=0, second=0),
            )

            # test order

Override specific targets:

.. code-block:: python

    from django.test import TestCase

    from override_autonow import override_autonow

    from .models import Order


    class TestOrder(TestCase):
        @override_autonow(exclude_auto_now=True)
        def test_exclude_auto_now_option(self):
            # Override only auto_now_add option
            ...

        @override_autonow(exclude_auto_now_add=True)
        def test_exclude_auto_now_add_option(self):
            # Override only auto_now option
            ...

        @override_autonow(exclude_date_field=True)
        def test_exclude_date_field(self):
            # Override only DateTimeField
            ...

        @override_autonow(exclude_datetime_field=True)
        def test_exclude_datetime_field(self):
            # Override only DateField
            ...

        @override_autonow(exclude_field_names={'created_time'})
        def test_exclude_field_names(self):
            # Override except fields named created_time
            ...

        @override_autonow(exclude_models=(Order,))
        def test_exclude_models(self):
            # Override except the Order model
            ...

        @override_autonow(override_field_names={'created_time'})
        def test_override_field_names(self):
            # Override only fields named created_time
            ...

        @override_autonow(override_models=(Order,))
        def test_override_models(self):
            # Override only the Order model
            ...

Test with factory-bot:

.. code-block:: python

    from django.test import TestCase
    from django.utils import timezone
    from factory.django import DjangoModelFactory

    from override_autonow import override_autonow

    from .models import Order


    class OrderFactory:
        class Meta:
            model = Order

        amount = 200,
        status = 'PAID',
        created_time = timezone.datetime(year=2022, month=1, day=1, hour=23, minute=59, second=59)
        updated_time = timezone.datetime(year=2022, month=1, day=2, hour=0, minute=0, second=0)


    class TestOrder(TestCase):
        @override_autonow
        def test_with_method_decorator(self):

            # Override created_time and updated_time with factory

            order = OrderFactory()

            # test order
