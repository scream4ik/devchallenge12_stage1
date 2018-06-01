from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from .models import TmpChunkedUpload, Server, Replica
from core.tests import SetUpUserMixin, generate_image_file

from unittest import mock
import hashlib


class TmpChunkedUploadViewTest(SetUpUserMixin, APITestCase):
    """
    Tests for TmpChunkedUploadView
    """

    def test_upload(self):
        """
        test for put and post request to tmp_upload and tmp_upload_detail
        :return: 200
        """
        image = generate_image_file()
        image_size = 315
        data = {
            'filename': 'test.png',
            'file': image
        }
        response = self.client.put(
            reverse('tmp_upload'),
            data=data,
            HTTP_CONTENT_RANGE='bytes 1-{}/{}'.format(image_size, image_size),
            format='multipart'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 1)
        self.assertEqual(response.data['filename'], 'test.png')
        chunked = TmpChunkedUpload.objects.get(id=response.data['id'])
        self.assertEqual(chunked.file.name.split('.')[-1], 'part')

        data = {
            'md5': self.md5(image)
        }
        response = self.client.post(
            reverse('tmp_upload_detail', args=[chunked.id]), data=data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 2)
        chunked = TmpChunkedUpload.objects.get(id=response.data['id'])
        self.assertEqual(chunked.file.name.split('.')[-1], 'png')

    @staticmethod
    def md5(f):
        """md5 checksum (hex) of the entire file"""
        m = hashlib.md5()
        with f as memf:
            data = memf.getvalue()
            m.update(data)
        return m.hexdigest()


class UserFilesListViewTest(SetUpUserMixin, APITestCase):
    """
    Tests for UserFilesListView
    """

    def setUp(self):
        super().setUp()
        self.upload = TmpChunkedUpload(filename='test.png', user=self.user)
        self.upload.file.save('test.png', generate_image_file(), save=False)
        self.upload.save()

    def test_get(self):
        """
        test for get request to user_files_list
        :return: 200
        """
        response = self.client.get(reverse('user_files_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(response.data, {})
        self.assertTrue(isinstance(response.data, dict))
        self.assertTrue('results' in response.data)


class ChunkedDownloadViewTest(SetUpUserMixin, APITestCase):
    """
    Tests for ChunkedDownloadView
    """

    def setUp(self):
        super().setUp()
        self.upload = TmpChunkedUpload(filename='test.png', user=self.user)
        self.upload.file.save('test.png', generate_image_file(), save=False)
        self.upload.save()

        self.server = Server.objects.create(
            public_domain='example.com',
            public_port=80,
            status='online',
            ssh_host='example.com',
            ssh_user='root',
            ssh_password='root'
        )

        self.replica = Replica.objects.create(
            chunked=self.upload, server=self.server
        )

    def test_get(self):
        """
        test for get request to download
        :return: 302
        """
        ping = {self.server.pk: {'public_ip': '216.58.209.78'}}
        with mock.patch('storage.views.ping', return_value=ping):
            response = self.client.get(
                reverse('download', args=[self.upload.pk])
            )
            self.assertEqual(response.status_code, status.HTTP_302_FOUND)
