"""
Code Generator - https://github.com/wj-Mcat/code-generator

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
from __future__ import annotations

from typing import List, Optional, Union
from dataclasses import dataclass
import json
from pyee import AsyncIOEventEmitter    # type: ignore

from wechaty import Contact, Room   # type: ignore

from wechaty_puppet import (    # type: ignore
    Puppet, FileBox, RoomQueryFilter,
    MiniProgramPayload, UrlLinkPayload, MessageQueryFilter,
    PuppetOptions, EventType,
    get_logger,
    EventMessagePayload)
from wechaty_puppet.schemas.types import (  # type: ignore
    MessagePayload,
    ContactPayload,
    FriendshipPayload,
    ImageType,
    RoomInvitationPayload,
    RoomPayload,
    RoomMemberPayload
)
from wechaty_puppet_mock.exceptions import WechatyPuppetMockError
from wechaty_puppet_mock.mock.mocker import Mocker, MockerResponse


log = get_logger('PuppetMock')


@dataclass
class PuppetMockOptions(PuppetOptions):
    """options for puppet mock"""
    mocker: Optional[Mocker] = None


# pylint: disable=too-many-public-methods
class PuppetMock(Puppet):
    """mock for puppet"""
    def __init__(self, options: PuppetMockOptions, name: str = 'puppet-mock'):
        super().__init__(options, name)

        if not options.mocker:
            raise WechatyPuppetMockError('mocker in options is required')
        self.mocker: Mocker = options.mocker

        self.started: bool = False
        self.emitter = AsyncIOEventEmitter()

    async def message_image(self, message_id: str,
                            image_type: ImageType) -> FileBox:
        """get image from message"""

    async def ding(self, data: Optional[str] = None):
        pass

    def on(self, event_name: str, caller):
        """listen event"""
        self.emitter.on(event_name, caller)

    def listener_count(self, event_name: str) -> int:
        """get the event count of the specific event"""
        listeners = self.emitter.listeners(event=event_name)
        return len(listeners)

    async def start(self) -> None:
        """star the account"""
        self.started = True
        if not self.mocker:
            raise WechatyPuppetMockError(
                'PuppetMock should not start without mocker'
            )

        def _emit_events(response: MockerResponse):
            """emit the events from the mocker"""
            payload_data = json.loads(response.payload)

            if response.type == int(EventType.EVENT_TYPE_MESSAGE):
                log.debug('receive message info <%s>', payload_data)
                event_message_payload = EventMessagePayload(
                    message_id=payload_data['messageId'])
                self.emitter.emit('message', event_message_payload)

        self.mocker.on('stream', _emit_events)

    async def stop(self):
        """stop the account"""
        self.started = False

    async def contact_list(self) -> List[str]:
        """get all of the contact"""
        return self.mocker.get_contact_ids()

    async def tag_contact_delete(self, tag_id: str) -> None:
        pass

    async def tag_favorite_delete(self, tag_id: str) -> None:
        pass

    async def tag_contact_add(self, tag_id: str, contact_id: str):
        pass

    async def tag_favorite_add(self, tag_id: str, contact_id: str):
        pass

    async def tag_contact_remove(self, tag_id: str, contact_id: str):
        pass

    async def tag_contact_list(self,
                               contact_id: Optional[str] = None) -> List[str]:
        pass

    async def message_send_text(self, conversation_id: str, message: str,
                                mention_ids: List[str] = None) -> str:
        """send the text message to the specific contact/room"""

        conversation: Union[Room, Contact]
        if conversation_id.startswith('room-'):
            conversation = self.mocker.Room.load(conversation_id)
        else:
            conversation = self.mocker.Contact.load(conversation_id)
        message_id = self.mocker.send_message(
            talker=self.mocker.login_user,
            conversation=conversation,
            msg=message
        )
        return message_id

    async def message_send_contact(self, contact_id: str,
                                   conversation_id: str) -> str:
        pass

    async def message_send_file(self, conversation_id: str,
                                file: FileBox) -> str:
        pass

    async def message_send_url(self, conversation_id: str, url: str) -> str:
        pass

    async def message_send_mini_program(self,
                                        conversation_id: str,
                                        mini_program: MiniProgramPayload
                                        ) -> str:
        pass

    async def message_search(self, query: Optional[MessageQueryFilter] = None
                             ) -> List[str]:
        pass

    async def message_recall(self, message_id: str) -> bool:
        pass

    async def message_payload(self, message_id: str) -> MessagePayload:
        """get the message payload"""
        return self.mocker.environment.get_message_payload(
            message_id=message_id)

    async def message_forward(self, to_id: str, message_id: str):
        pass

    async def message_file(self, message_id: str) -> FileBox:
        """get the file-box from message instance

        save the file-box data in message_payload.text field to avoid creating a
        new structure to support this feature
        """
        message_payload = self.mocker.environment.get_message_payload(
            message_id=message_id
        )
        return FileBox.from_json(message_payload.text)

    async def message_contact(self, message_id: str) -> str:
        """get the message Contact id info

            text field save the message contact_id info
        """
        message_payload = self.mocker.environment.get_message_payload(
            message_id=message_id
        )
        return message_payload.text

    async def message_url(self, message_id: str) -> UrlLinkPayload:
        """get the url link """

    async def message_mini_program(self, message_id: str) -> MiniProgramPayload:
        pass

    async def contact_alias(self, contact_id: str,
                            alias: Optional[str] = None) -> str:
        """get/save the contact alias"""
        contact_payload = self.mocker.environment.\
            get_contact_payload(contact_id)
        if not alias:
            return contact_payload.alias
        contact_payload.alias = alias
        self.mocker.environment.update_contact_payload(contact_payload)
        return alias

    async def contact_payload_dirty(self, contact_id: str):
        pass

    async def contact_payload(self, contact_id: str) -> ContactPayload:
        """get the contact payload"""
        return self.mocker.environment.get_contact_payload(contact_id)

    async def contact_avatar(self, contact_id: str,
                             file_box: Optional[FileBox] = None) -> FileBox:
        """get the contact avatar"""
        contact_payload = self.mocker.environment.\
            get_contact_payload(contact_id)
        if not file_box:
            return FileBox.from_base64(
                contact_payload.avatar,
                name=f'{contact_payload.name}.png'
            )
        contact_payload.avatar = file_box.base64
        self.mocker.environment.update_contact_payload(contact_payload)

    async def contact_tag_ids(self, contact_id: str) -> List[str]:
        pass

    def self_id(self) -> str:
        return self.mocker.login_user.contact_id

    async def friendship_search(self, weixin: Optional[str] = None,
                                phone: Optional[str] = None) -> Optional[str]:
        pass

    async def friendship_add(self, contact_id: str, hello: str):
        pass

    async def friendship_payload(self, friendship_id: str,
                                 payload: Optional[FriendshipPayload] = None
                                 ) -> FriendshipPayload:
        pass

    async def friendship_accept(self, friendship_id: str):
        pass

    async def room_list(self) -> List[str]:
        """get the room id list"""
        rooms = self.mocker.environment.get_room_payloads()
        return [room.id for room in rooms]

    async def room_create(self, contact_ids: List[str],
                          topic: str = None) -> str:
        """create the room"""
        room_payload = self.mocker.environment.new_room_payload(
            member_ids=contact_ids,
            topic=topic
        )
        return room_payload.id

    async def room_search(self, query: RoomQueryFilter = None) -> List[str]:
        pass

    async def room_invitation_payload(self,
                                      room_invitation_id: str,
                                      payload: Optional[
                                          RoomInvitationPayload] = None
                                      ) -> RoomInvitationPayload:
        pass

    async def room_invitation_accept(self, room_invitation_id: str):
        pass

    async def contact_self_qr_code(self) -> str:
        pass

    async def contact_self_name(self, name: str):
        pass

    async def contact_signature(self, signature: str):
        pass

    async def room_payload(self, room_id: str) -> RoomPayload:
        """get the room payload"""
        return self.mocker.environment.get_room_payload(room_id)

    async def room_members(self, room_id: str) -> List[str]:
        """get the room member ids from environment

        Args:
            room_id (str): the union identification for room

        Returns:
            List[str]: room member ids
        """
        room_payload: RoomPayload = self.mocker.environment.get_room_payload(
            room_id)
        return room_payload.member_ids

    async def room_add(self, room_id: str, contact_id: str):
        """add a contact to a room"""
        self.mocker.add_contact_to_room(
            contact_ids=[contact_id],
            room_id=room_id
        )

    async def room_delete(self, room_id: str, contact_id: str):
        pass

    async def room_quit(self, room_id: str):
        pass

    async def room_topic(self, room_id: str, new_topic: str):
        pass

    async def room_announce(self, room_id: str,
                            announcement: str = None) -> str:
        pass

    async def room_qr_code(self, room_id: str) -> str:
        pass

    async def room_member_payload(self, room_id: str,
                                  contact_id: str) -> RoomMemberPayload:
        pass

    async def room_avatar(self, room_id: str) -> FileBox:
        pass

    async def logout(self):
        pass

    async def login(self, user_id: str):
        """login the user data"""
        self.mocker.login(user_id=user_id)
