# coding: utf-8

import pprint
import re

import six





class BucketAuthorizedReq:


    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """

    sensitive_list = []

    openapi_types = {
        'bucket': 'str',
        'operation': 'str',
        'project_id': 'str'
    }

    attribute_map = {
        'bucket': 'bucket',
        'operation': 'operation',
        'project_id': 'project_id'
    }

    def __init__(self, bucket=None, operation=None, project_id=None):
        """BucketAuthorizedReq - a model defined in huaweicloud sdk"""
        
        

        self._bucket = None
        self._operation = None
        self._project_id = None
        self.discriminator = None

        self.bucket = bucket
        self.operation = operation
        if project_id is not None:
            self.project_id = project_id

    @property
    def bucket(self):
        """Gets the bucket of this BucketAuthorizedReq.

        桶名 

        :return: The bucket of this BucketAuthorizedReq.
        :rtype: str
        """
        return self._bucket

    @bucket.setter
    def bucket(self, bucket):
        """Sets the bucket of this BucketAuthorizedReq.

        桶名 

        :param bucket: The bucket of this BucketAuthorizedReq.
        :type: str
        """
        self._bucket = bucket

    @property
    def operation(self):
        """Gets the operation of this BucketAuthorizedReq.

        操作标记，取值[0,1]，0表示取消授权，1表示授权 

        :return: The operation of this BucketAuthorizedReq.
        :rtype: str
        """
        return self._operation

    @operation.setter
    def operation(self, operation):
        """Sets the operation of this BucketAuthorizedReq.

        操作标记，取值[0,1]，0表示取消授权，1表示授权 

        :param operation: The operation of this BucketAuthorizedReq.
        :type: str
        """
        self._operation = operation

    @property
    def project_id(self):
        """Gets the project_id of this BucketAuthorizedReq.

        租户Id

        :return: The project_id of this BucketAuthorizedReq.
        :rtype: str
        """
        return self._project_id

    @project_id.setter
    def project_id(self, project_id):
        """Sets the project_id of this BucketAuthorizedReq.

        租户Id

        :param project_id: The project_id of this BucketAuthorizedReq.
        :type: str
        """
        self._project_id = project_id

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                if attr in self.sensitive_list:
                    result[attr] = "****"
                else:
                    result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, BucketAuthorizedReq):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
