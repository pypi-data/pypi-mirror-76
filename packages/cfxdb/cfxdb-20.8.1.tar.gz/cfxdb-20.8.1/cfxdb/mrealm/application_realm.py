##############################################################################
#
#                        Crossbar.io FX
#     Copyright (C) Crossbar.io Technologies GmbH. All rights reserved.
#
##############################################################################

from typing import Optional, List
from uuid import UUID
import pprint

from cfxdb.common import ConfigurationElement
from cfxdb.gen.arealm.ApplicationRealmStatus import ApplicationRealmStatus


class ApplicationRealm(ConfigurationElement):
    """
    Application realm database configuration object.
    """

    STATUS_BY_CODE = {
        ApplicationRealmStatus.NONE: 'NONE',
        ApplicationRealmStatus.STOPPED: 'STOPPED',
        ApplicationRealmStatus.STARTING: 'STARTING',
        ApplicationRealmStatus.RUNNING: 'RUNNING',
        ApplicationRealmStatus.PAUSED: 'PAUSED',
        ApplicationRealmStatus.STOPPING: 'STOPPING',
        ApplicationRealmStatus.ERROR: 'ERROR',
        ApplicationRealmStatus.DEGRADED: 'DEGRADED',
    }

    STATUS_BY_NAME = {
        'NONE': ApplicationRealmStatus.NONE,
        'STOPPED': ApplicationRealmStatus.STOPPED,
        'STARTING': ApplicationRealmStatus.STARTING,
        'RUNNING': ApplicationRealmStatus.RUNNING,
        'PAUSED': ApplicationRealmStatus.PAUSED,
        'STOPPING': ApplicationRealmStatus.STOPPING,
        'ERROR': ApplicationRealmStatus.ERROR,
        'DEGRADED': ApplicationRealmStatus.DEGRADED,
    }

    STATUS_STOPPED = ApplicationRealmStatus.STOPPED
    STATUS_STARTING = ApplicationRealmStatus.STARTING
    STATUS_RUNNING = ApplicationRealmStatus.RUNNING
    STATUS_PAUSED = ApplicationRealmStatus.PAUSED
    STATUS_STOPPING = ApplicationRealmStatus.STOPPING
    STATUS_ERROR = ApplicationRealmStatus.ERROR
    STATUS_DEGRADED = ApplicationRealmStatus.DEGRADED

    def __init__(self,
                 oid: Optional[UUID] = None,
                 label: Optional[str] = None,
                 description: Optional[str] = None,
                 tags: Optional[List[str]] = None,
                 name: Optional[str] = None,
                 status: Optional[int] = None,
                 workergroup_oid: Optional[UUID] = None,
                 webcluster_oid: Optional[UUID] = None,
                 changed: Optional[int] = None,
                 owner: Optional[UUID] = None,
                 _unknown=None):
        """

        :param oid: Object ID of application realm

        :param label: Optional user label of application realm

        :param description: Optional user description of application realm

        :param tags: Optional list of user tags on application realm

        :param name: Name of application realm

        :param status: Status of application realm.

        :param workergroup_oid: When running, router cluster worker group this application realm is running on.

        :param webcluster_oid: When running, the web cluster to serve as a frontend layer for the application realm.

        :param changed: Timestamp when the application realm was last changed
        :param owner: Owning user (object ID)
        """
        ConfigurationElement.__init__(self, oid=oid, label=label, description=description, tags=tags)
        self.name = name
        self.status = status
        self.workergroup_oid = workergroup_oid
        self.webcluster_oid = webcluster_oid
        self.changed = changed
        self.owner = owner

        # private member with unknown/untouched data passing through
        self._unknown = _unknown

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if not ConfigurationElement.__eq__(self, other):
            return False
        if other.name != self.name:
            return False
        if other.status != self.status:
            return False
        if other.workergroup_oid != self.workergroup_oid:
            return False
        if other.webcluster_oid != self.webcluster_oid:
            return False
        if other.changed != self.changed:
            return False
        if other.owner != self.owner:
            return False
        return True

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return pprint.pformat(self.marshal())

    def copy(self, other, overwrite=False):
        """
        Copy over other object.

        :param other: Other application realm to copy data from.
        :type other: instance of :class:`ManagementRealm`
        :return:
        """
        ConfigurationElement.copy(self, other, overwrite=overwrite)

        if (not self.name and other.name) or overwrite:
            self.name = other.name
        if (not self.status and other.status) or overwrite:
            self.status = other.status
        if (not self.workergroup_oid and other.workergroup_oid) or overwrite:
            self.workergroup_oid = other.workergroup_oid
        if (not self.webcluster_oid and other.webcluster_oid) or overwrite:
            self.webcluster_oid = other.webcluster_oid
        if (not self.changed and other.changed) or overwrite:
            self.changed = other.changed
        if (not self.owner and other.owner) or overwrite:
            self.owner = other.owner

        # _unknown is not copied!

    def marshal(self):
        """
        Marshal this object to a generic host language object.

        :return: dict
        """
        assert self.oid is None or isinstance(self.oid, UUID)
        assert self.name is None or type(self.name) == str
        assert self.status is None or type(self.status) == int
        assert self.workergroup_oid is None or isinstance(self.workergroup_oid, UUID)
        assert self.webcluster_oid is None or isinstance(self.webcluster_oid, UUID)
        assert self.changed is None or type(self.changed) == int
        assert self.owner is None or isinstance(self.owner, UUID)

        obj = ConfigurationElement.marshal(self)

        obj.update({
            'oid': str(self.oid) if self.oid else None,
            'name': self.name,
            'status': self.STATUS_BY_CODE.get(self.status, None),
            'workergroup_oid': str(self.workergroup_oid) if self.workergroup_oid else None,
            'webcluster_oid': str(self.webcluster_oid) if self.webcluster_oid else None,
            'changed': self.changed,
            'owner': str(self.owner) if self.owner else None,
        })

        if self._unknown:
            # pass through all attributes unknown
            obj.update(self._unknown)

        return obj

    @staticmethod
    def parse(data):
        """
        Parse generic host language object into an object of this class.

        :param data: Generic host language object
        :type data: dict

        :return: instance of :class:`ApplicationRealm`
        """
        assert type(data) == dict

        obj = ConfigurationElement.parse(data)
        data = obj._unknown

        # future attributes (yet unknown) are not only ignored, but passed through!
        _unknown = {}
        for k in data:
            if k not in ['oid', 'name', 'status', 'workergroup_oid', 'webcluster_oid', 'owner', 'created']:
                _unknown[k] = data[k]

        name = data.get('name', 'arealm-{}'.format(str(obj.oid)[:8]))
        assert type(name) == str

        status = data.get('status', None)
        assert status is None or (type(status) == str)
        status = ApplicationRealm.STATUS_BY_NAME.get(status, None)

        workergroup_oid = None
        if 'workergroup_oid' in data and data['workergroup_oid'] is not None:
            assert type(
                data['workergroup_oid']) == str, 'workergroup_oid must be a string, but was {}'.format(
                    type(data['workergroup_oid']))
            workergroup_oid = UUID(data['workergroup_oid'])

        webcluster_oid = None
        if 'webcluster_oid' in data and data['webcluster_oid'] is not None:
            assert type(data['webcluster_oid']) == str, 'webcluster_oid must be a string, but was {}'.format(
                type(data['webcluster_oid']))
            webcluster_oid = UUID(data['webcluster_oid'])

        owner = None
        if 'owner' in data and data['owner'] is not None:
            assert type(data['owner']) == str, 'owner must be a string, but was {}'.format(type(
                data['owner']))
            owner = UUID(data['owner'])

        changed = data.get('changed', None)
        assert changed is None or type(changed) == int

        obj = ApplicationRealm(oid=obj.oid,
                               label=obj.label,
                               description=obj.description,
                               tags=obj.tags,
                               name=name,
                               workergroup_oid=workergroup_oid,
                               webcluster_oid=webcluster_oid,
                               status=status,
                               owner=owner,
                               changed=changed,
                               _unknown=_unknown)

        return obj
