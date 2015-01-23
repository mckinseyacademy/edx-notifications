"""
Unit tests to exercise code implemented in data.py
"""

from django.test import TestCase

from notifications.base_data import (
    BaseDataObject,
    TypedField,
)

from notifications.data import (
    NotificationMessage,
)


class DataObject(BaseDataObject):
    """
    Sample very simple test data object
    """

    test_variable = None


class DataObjectWithTypedFields(BaseDataObject):
    """
    More sophisticated DataObject
    """

    test_int_field = TypedField(int)
    test_dict_field = TypedField(dict)
    test_class_field = TypedField(NotificationMessage)


class BaseDataObjectTests(TestCase):
    """
    Go through data.py and exercise some tests
    """

    def test_base_data_object(self):
        """
        Assert proper behavior with BaseDataObject
        """

        test_class = DataObject(test_variable='foo')
        self.assertEquals(test_class.test_variable, 'foo')

        with self.assertRaises(ValueError):
            DataObject(doesnt_exist='bar')

        # make sure we are not allowed to add on new
        # attributes after initialization
        obj = DataObject(test_variable='foo')
        with self.assertRaises(ValueError):
            obj.blow_up_now = True  # pylint: disable=attribute-defined-outside-init

    def test_typed_fields(self):
        """
        Assert proper behavior with TypedFields inside of BaseDataObjects
        """

        # make sure we can make proper assignments on initialization
        obj = DataObjectWithTypedFields(
            id=1,
            test_int_field=100,
            test_dict_field={
                'foo': 'bar'
            },
            test_class_field=NotificationMessage()
        )

        self.assertTrue(isinstance(obj.test_int_field, int))
        self.assertTrue(isinstance(obj.test_dict_field, dict))
        self.assertTrue(isinstance(obj.test_class_field, NotificationMessage))

        # make sure we can set fields after initialization

        obj = DataObjectWithTypedFields()
        obj.test_int_field = 100
        obj.test_dict_field = {
            'foo': 'bar'
        }
        obj.test_class_field = NotificationMessage()

        self.assertTrue(isinstance(obj.test_int_field, int))
        self.assertTrue(isinstance(obj.test_dict_field, dict))
        self.assertTrue(isinstance(obj.test_class_field, NotificationMessage))

        # make sure we can set typed fields as None
        obj = DataObjectWithTypedFields(
            test_int_field=None,
            test_dict_field=None,
            test_class_field=None,
        )

        self.assertTrue(isinstance(obj.test_int_field, type(None)))
        self.assertTrue(isinstance(obj.test_dict_field, type(None)))
        self.assertTrue(isinstance(obj.test_class_field, type(None)))

    def test_type_fields_bad(self):
        """
        Asserts that TypeErrors are raised when we try to assign
        fields with the incorrect types
        """

        # assert that we can't set wrong types on initialization

        with self.assertRaises(TypeError):
            DataObjectWithTypedFields(
                id=1,
                test_int_field='wrong type',
                test_dict_field=11,
                test_class_field={'wrong': True},
            )

        # assert that we can't set wrong types post initialization

        obj = DataObjectWithTypedFields()

        with self.assertRaises(TypeError):
            obj.test_int_field = 'wrong type'

    def test_illegal_type_change(self):
        """
        Assert that we cannot change types of a DataObject after we already
        set it
        """

        obj = DataObjectWithTypedFields(
            id=1,
            test_int_field=100,
            test_dict_field={
                'foo': 'bar'
            },
            test_class_field=NotificationMessage()
        )

        with self.assertRaises(TypeError):
            obj.test_int_field = "wrong type"

        # however, we should be able to change to/from None

        obj.test_int_field = None
        obj.test_int_field = 200