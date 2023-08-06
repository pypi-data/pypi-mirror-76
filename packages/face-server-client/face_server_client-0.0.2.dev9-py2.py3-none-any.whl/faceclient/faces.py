import cv2
import numpy as np

from faceclient import base


class Face(base.Resource):
    resource_name = 'Face'


class FacesManager(base.ResourceManager):
    resource_class = Face

    def create(self, image, align=True):
        if isinstance(image, np.ndarray):
            # Convert to byte string
            image = cv2.imencode('.jpg', image)[1].tostring()
        if isinstance(image, str):
            # Convert to bytes
            image = image.encode()
        if not isinstance(image, bytes):
            raise RuntimeError(
                'Input type is not recognized. '
                'It should be either 3D numpy array, string or bytes'
            )

        resp = self.http_client.post(
            '/faces',
            image,
            headers={'content-type': 'image/jpeg', 'X-Face-Align': str(align)}
        )

        if resp.status_code >= 400:
            self._raise_api_exception(resp)

        return [self.resource_class(self, resource_data)
                for resource_data in base.extract_json(resp, 'faces')]

    def reassign(self, old_id, new_id):
        resp = self.http_client.put(f'/faces/{old_id}/reassign/{new_id}', '{}')

        if resp.status_code >= 400:
            self._raise_api_exception(resp)

        return resp.json()

    def list(self):
        return self._list('/faces', response_key='faces')

    def get(self, id):
        return self._get(f'/faces/{id}')

    def delete(self, id):
        self._ensure_not_empty(id=id)

        self._delete(f'/faces/{id}')
