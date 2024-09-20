from unittest.mock import ANY
from uuid import uuid4

from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_204_NO_CONTENT,
)

from .models.task import Task


class TaskApiTests(APITestCase):
    def setUp(self):
        self.id1 = str(uuid4())
        self.id2 = str(uuid4())
        Task.objects.bulk_create([
            Task(
                id=self.id1,
                title='test title1',
                description='test description1',
            ),
            Task(
                id=self.id2,
                title='test title2',
                description='test description2',
            ),
        ])

    def test_list(self):
        response = self.client.get(reverse('tasks'))
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.json(), [
            {
                'id': self.id1,
                'title': 'test title1',
                'description': 'test description1',
                'completed': False,
            },
            {
                'id': self.id2,
                'title': 'test title2',
                'description': 'test description2',
                'completed': False,
            },
        ])

    def test_list_wrong_order(self):
        response = self.client.get(reverse('tasks'))
        self.assertNotEqual(response.json(), [
            {
                'id': self.id2,
                'title': 'test title2',
                'description': 'test description2',
                'completed': False,
            },
            {
                'id': self.id1,
                'title': 'test title1',
                'description': 'test description1',
                'completed': False,
            },
        ])

    def test_retrieve(self):
        response = self.client.get(reverse(
            'task',
            kwargs={'pk': self.id1},
        ))
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.json(), {
            'id': self.id1,
            'title': 'test title1',
            'description': 'test description1',
            'completed': False,
        })

    def test_create_valid_data(self):
        input_data = {
            'title': 'test title1',
            'description': 'test description1',
            'completed': False,
        }
        response = self.client.post(reverse('tasks'), input_data)
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertEqual(response.json(), {
            'id': ANY,
            **input_data,
        })

    def test_create_invalid_data(self):
        invalid_data = {
            'title': 123,
            'completed': 'completed',
        }
        response = self.client.post(reverse('tasks'), invalid_data)
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

    def test_partial_update(self):
        task = Task.objects.create(
            title='test title1',
            description='test description1',
            completed=False,
        )
        response = self.client.patch(
            reverse(
                'task',
                kwargs={'pk': task.id},
            ),
            {'completed': True},
        )
        response_data = response.json()

        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response_data['completed'], True)
        self.assertNotEqual(response_data['completed'], task.completed)

    def test_update_with_required_fields(self):
        task = Task.objects.create(
            title='test title1',
            description='test description1',
            completed=False,
        )
        response = self.client.put(
            reverse(
                'task',
                kwargs={'pk': task.id},
            ),
            {'title': 'new title'},
        )
        response_data = response.json()

        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response_data['title'], 'new title')
        self.assertNotEqual(task.title, response_data['title'])

    def test_update_only_optional_fields(self):
        response = self.client.put(
            reverse(
                'task',
                kwargs={'pk': self.id1},
            ),
            {'completed': True},
        )
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

    def test_destroy(self):
        task = Task.objects.create(title='title')
        response = self.client.delete(reverse(
            'task',
            kwargs={'pk': task.id},
        ))
        self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)
