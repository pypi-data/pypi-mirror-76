"""
python wechaty - https://github.com/wj-Mcat/python-wechaty-puppet-mock

Authors:    Jingjing WU (吴京京) <https://github.com/wj-Mcat>

2020-now @ Copyright wj-Mcat

Licensed under the Apache License, Version 2.0 (the 'License');
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an 'AS IS' BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import os
from collections import defaultdict
from typing import (
    Dict,
    Optional,
    List
)
import random
from wechaty_puppet import (    # type: ignore
    ContactPayload,
    ContactGender,
    ContactType,

    RoomPayload,
    MessagePayload
)
from chatie_grpc.wechaty import MessageFileResponse     # type: ignore

from wechaty_puppet_mock.config import get_image_base64_data
from wechaty_puppet_mock.exceptions import MockEnvironmentError
from faker import Faker     # type: ignore

faker = Faker('zh_CN')

BASE_URL = os.path.abspath(os.path.basename(__file__))


class EnvironmentMock:
    """get the simple mock environment"""

    def __init__(self,
                 room_num: int = 3,
                 contact_num: int = 30,
                 message_num: int = 10):
        """init the environment for mocker"""
        self._contact_payload_pool: Dict[str, ContactPayload] = \
            defaultdict(ContactPayload)
        self._room_payload_pool: Dict[str, RoomPayload] = \
            defaultdict(RoomPayload)
        self._message_payload_pool: Dict[str, MessagePayload] = \
            defaultdict(MessagePayload)

        self._message_file_payload_ppol: Dict[str, MessageFileResponse] = \
            defaultdict(MessageFileResponse)

        self._login_user_payload = self._get_random_contact_payload()

        self._init_contacts(contact_num)

    @staticmethod
    def _get_random_contact_payload() -> ContactPayload:
        """get random contact payload"""
        temp_id = faker.uuid4()
        payload = ContactPayload(
            id=f'contact-{temp_id}',
            gender=ContactGender(faker.random.randint(0, 2)),
            type=ContactType(faker.random.randint(0, 2)),
            name=faker.name(),
            avatar=get_image_base64_data(),
            address=faker.address(),
            alias=faker.name(),
            city=faker.city(),
            friend=True,
            province=faker.province(),
            signature=faker.sentence(),
            star=(faker.random.randint(0, 1) % 2 == 0),
            weixin=f'weixin-{temp_id}'
        )
        return payload

    def _get_random_room_payload(self) -> RoomPayload:
        """get random room payload"""
        temp_id = faker.uuid4()
        contact_ids = list(self._contact_payload_pool.keys())
        if not contact_ids:
            raise MockEnvironmentError('there are no contacts in the '
                                       'environment, so, you can not '
                                       'create room')
        random_payload = RoomPayload(
            id=f'room-{temp_id}',
            topic=faker.sentence(),
            avatar=get_image_base64_data(),
            owner_id=self._login_user_payload.id,
            admin_ids=[],
            member_ids=random.sample(
                contact_ids,
                random.randint(0, len(contact_ids))
            )
        )
        return random_payload

    def _init_contacts(self, contact_num: int):
        """init contacts payload"""
        # read sample file content from FileBox
        for i in range(contact_num):
            random_payload = self._get_random_contact_payload()
            self._contact_payload_pool[random_payload.id] = random_payload

    def _init_rooms(self, room_num: int):
        """init rooms payload after contacts created"""
        for i in range(room_num):
            room_payload = self._get_random_room_payload()
            self._room_payload_pool[room_payload.id] = room_payload

    def new_room_payload(self,
                         member_ids: Optional[List[str]] = None,
                         topic: Optional[str] = None) -> RoomPayload:
        """create room payload"""
        random_room_payload = self._get_random_room_payload()

        if member_ids:
            random_room_payload.member_ids = member_ids

        if topic:
            random_room_payload.topic = topic

        self._room_payload_pool[random_room_payload.id] = random_room_payload
        return random_room_payload

    def new_contact_payload(self) -> ContactPayload:
        """create new random contact payload"""
        random_contact_paylaod = self._get_random_contact_payload()
        self._contact_payload_pool[random_contact_paylaod.id] = \
            random_contact_paylaod
        return random_contact_paylaod

    def get_room_payloads(self) -> List[RoomPayload]:
        """get fake room payloads"""
        return list(self._room_payload_pool.values())

    def get_room_payload(self, room_id: str) -> RoomPayload:
        """get room paylaod by room_id

        Args:
            room_id (str): the union identification for room

        Returns:
            RoomPayload: the payload data for room
        """
        if room_id not in self._room_payload_pool:
            raise MockEnvironmentError(
                f'room <{room_id}> not in environment'
            )
        return self._room_payload_pool[room_id]

    def update_room_payload(self, room_payload: RoomPayload):
        """update the room payload"""
        if room_payload.id not in self._room_payload_pool:
            raise MockEnvironmentError(
                f'room <{room_payload.id}> not in environment'
            )
        self._room_payload_pool[room_payload.id] = room_payload

    def get_contact_payloads(self) -> List[ContactPayload]:
        """get fake contact payloads"""
        return list(self._contact_payload_pool.values())

    def get_contact_payload(self, contact_id: str) -> ContactPayload:
        """get contact payload by id"""
        if contact_id not in self._contact_payload_pool:
            raise MockEnvironmentError(f'contact <{contact_id}> '
                                       f'not in environment')
        return self._contact_payload_pool[contact_id]

    def update_contact_payload(self, contact_payload: ContactPayload):
        """update the contact payload"""
        if contact_payload.id not in self._contact_payload_pool:
            raise MockEnvironmentError(f'contact <{contact_payload.id}> not '
                                       f'in environment')
        self._contact_payload_pool[contact_payload.id] = contact_payload

    def add_message_payload(self, message_payload: MessagePayload):
        """add a message payload to the pool"""
        self._message_payload_pool[message_payload.id] = message_payload

    def get_message_payload(self, message_id: str) -> MessagePayload:
        """get a message payload by message_id"""
        if message_id not in self._message_payload_pool:
            raise KeyError('message payload <%s> not in pool', message_id)

        return self._message_payload_pool[message_id]
