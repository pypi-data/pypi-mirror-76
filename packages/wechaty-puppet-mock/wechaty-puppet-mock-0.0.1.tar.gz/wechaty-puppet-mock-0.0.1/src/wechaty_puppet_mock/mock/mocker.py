"""
Code Generator - https://github.com/wj-Mcat/python-wechaty-puppet-mock

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
from typing import (
    Optional,
    Dict,
    Type,
    List,
    Union,
    TYPE_CHECKING
)
from uuid import uuid4
from collections import defaultdict
from pyee import AsyncIOEventEmitter    # type: ignore
import json
from datetime import datetime
from dataclasses import dataclass
from wechaty_puppet import (    # type: ignore
    ContactPayload,
    RoomPayload,
    MessagePayload,
    Puppet,
    get_logger,
    EventType,
    FileBox,
    MessageType
)
from wechaty import (   # type: ignore
    Contact,
    Room,
    Message
)

if TYPE_CHECKING:
    from wechaty import Contact, Wechaty

from wechaty_puppet_mock.mock.environment import EnvironmentMock
from wechaty_puppet_mock.exceptions import WechatyPuppetMockError

log = get_logger('Mocker')


@dataclass
class MockerResponse:
    """this is the common data-structure for mocker"""
    type: int
    payload: str


class Mocker(AsyncIOEventEmitter):
    """mock fake data"""
    def __init__(self):
        super().__init__()
        self.id: str = str(uuid4())

        # login user is set when the method login
        self._login_user: Optional[Contact] = None
        self.has_login: bool = False

        self._contact_payload_pool: Dict[str, ContactPayload] = \
            defaultdict(ContactPayload)
        self._room_payload_pool: Dict[str, RoomPayload] = \
            defaultdict(RoomPayload)
        self._message_payload_pool: Dict[str, MessagePayload] = \
            defaultdict(MessagePayload)

        self._environment: Optional[EnvironmentMock] = None
        self.Contact: Type[Contact] = Contact
        self.Room: Type[Room] = Room
        self.Message: Type[Message] = Message

    @property
    def login_user(self) -> Contact:
        """get the login user contact"""
        if not self._login_user:
            raise WechatyPuppetMockError('please login before get login user')
        return self._login_user

    def init(self, puppet: Puppet, wechaty):
        """init the puppet """

        log.info('init the abstract')
        self.Contact.abstract = False
        self.Room.abstract = False
        self.Message.abstract = False

        log.info('init puppet for mocker')
        self.Contact.set_puppet(puppet)
        self.Room.set_puppet(puppet)
        self.Message.set_puppet(puppet)

        log.info('init wechaty for mocker')
        self.Contact.set_wechaty(wechaty)
        self.Room.set_wechaty(wechaty)
        self.Message.set_wechaty(wechaty)

    @property
    def environment(self) -> EnvironmentMock:
        """get the environment for mocker"""
        # log.info('use the environment')
        if not self._environment:
            raise WechatyPuppetMockError('environment not found')
        return self._environment

    def use(self, environment: EnvironmentMock):
        """use the environment to support rooms contacts"""
        log.info('use the environment <{%s}>', environment)
        self._environment = environment

    def new_room(self) -> Room:
        """create random room"""
        payload = self.environment.new_room_payload()
        room = self.Room.load(payload.id)
        room.payload = payload

        log.info('create random room <%s>', room)
        return room

    def new_contact(self) -> Contact:
        """create random contact"""
        payload = self.environment.new_contact_payload()
        contact = self.Contact.load(payload.id)
        contact.payload = contact

        log.info('create random contact <%s>')
        return contact

    def scan(self, scan_code: str):
        """emit the scan event"""
        log.info('emit the scan event')
        scan_event_payload = {
            'qrcode': scan_code,
            'status': 3
        }
        response = MockerResponse(
            type=int(EventType.EVENT_TYPE_SCAN),
            payload=json.dumps(scan_event_payload)
        )
        self.emit('stream', response)

    def login(self, user_id: str):
        """emit the login user event"""
        log.info('mock the user <%s> login event', user_id)
        login_event_payload = {
            'contactId': user_id
        }
        response = MockerResponse(
            type=int(EventType.EVENT_TYPE_LOGIN),
            payload=json.dumps(login_event_payload)
        )
        self.emit('stream', response)

    def logout(self):
        """emit the logout user event"""
        log.info(f'mock the user <{self.login_user}> logout event')
        response = MockerResponse(
            type=int(EventType.EVENT_TYPE_LOGOUT),
            payload=json.dumps({
                'contactId': self.login_user.contact_id
            })
        )
        self._login_user = None
        self.emit('stream', response)

    def send_message(self,
                     talker: Contact,
                     conversation: Union[Contact, Room],
                     msg: Union[str, FileBox],
                     msg_type: MessageType = MessageType.MESSAGE_TYPE_TEXT
                     ) -> str:
        """mock the talker send message event

        In this version, we will only support str and FileBox message type
        """
        log.info('mock send message event')
        message_payload = MessagePayload(
            id=str(uuid4()),
            from_id=talker.contact_id,
            timestamp=int(datetime.now().timestamp() * 1000),
            type=msg_type
        )
        if isinstance(conversation, Contact):
            message_payload.to_id = conversation.contact_id
        else:
            message_payload.room_id = conversation.room_id

        if isinstance(msg, str):
            message_payload.text = msg
        else:
            message_payload.filename = msg.name

        # save the message payload to environment
        self.environment.add_message_payload(message_payload)

        response = MockerResponse(
            type=int(EventType.EVENT_TYPE_MESSAGE),
            payload=json.dumps({
                'messageId': message_payload.id
            })
        )
        self.emit('stream', response)
        return message_payload.id

    def add_contact_to_room(self, contact_ids: Union[str, List[str]],
                            room_id: str, inviter_id: Optional[str] = None):
        """add contact to the room"""

        if not inviter_id:
            inviter_id = self.login_user.contact_id

        room_payload = self.environment.get_room_payload(room_id)

        if isinstance(contact_ids, str):
            contact_ids = [contact_ids]

        for contact_id in contact_ids:
            if contact_id in room_payload.member_ids:
                continue
            room_payload.member_ids.append(contact_id)

        self.environment.update_room_payload(room_payload)

        response = MockerResponse(
            type=int(EventType.EVENT_TYPE_ROOM_JOIN),
            payload=json.dumps({
                'roomId': room_payload.id,
                'inviterId': inviter_id,
                'timestamp': datetime.now().timestamp() * 1000,
                'inviteeIdList': contact_ids
            })
        )

        self.emit('stream', response)
