# Copyright (C) 2019 Philipp Hörist <philipp AT hoerist.com>
#
# This file is part of nbxmpp.
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 3
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; If not, see <http://www.gnu.org/licenses/>.

from nbxmpp.namespaces import Namespace
from nbxmpp.protocol import Iq
from nbxmpp.protocol import Node
from nbxmpp.protocol import isResultNode
from nbxmpp.protocol import JID
from nbxmpp.structs import AnnotationNote
from nbxmpp.structs import CommonResult
from nbxmpp.modules.date_and_time import parse_datetime
from nbxmpp.util import call_on_response
from nbxmpp.util import callback
from nbxmpp.util import raise_error
from nbxmpp.modules.base import BaseModule


class Annotations(BaseModule):
    def __init__(self, client):
        BaseModule.__init__(self, client)

        self._client = client
        self.handlers = []

    @property
    def domain(self):
        return self._client.get_bound_jid().getDomain()

    @call_on_response('_annotations_received')
    def request_annotations(self):
        self._log.info('Request annotations for %s', self.domain)
        payload = Node('storage', attrs={'xmlns': Namespace.ROSTERNOTES})
        return Iq(typ='get', queryNS=Namespace.PRIVATE, payload=payload)

    @callback
    def _annotations_received(self, stanza):
        if not isResultNode(stanza):
            return raise_error(self._log.info, stanza)

        storage = stanza.getQueryChild('storage')
        if storage is None:
            return raise_error(self._log.warning, stanza, 'stanza-malformed',
                               'No annotations found')

        notes = []
        for note in storage.getTags('note'):
            try:
                jid = JID(note.getAttr('jid'))
            except Exception as error:
                self._log.warning('Invalid JID: %s, %s',
                                  note.getAttr('jid'), error)
                continue

            cdate = note.getAttr('cdate')
            if cdate is not None:
                cdate = parse_datetime(cdate, epoch=True)

            mdate = note.getAttr('mdate')
            if mdate is not None:
                mdate = parse_datetime(mdate, epoch=True)

            data = note.getData()
            notes.append(AnnotationNote(jid=jid, cdate=cdate,
                                        mdate=mdate, data=data))

        self._log.info('Received annotations from %s:', self.domain)
        for note in notes:
            self._log.info(note)
        return notes

    @call_on_response('_default_response')
    def set_annotations(self, notes):
        self._log.info('Set annotations for %s:', self.domain)
        for note in notes:
            self._log.info(note)
        storage = Node('storage', attrs={'xmlns': Namespace.ROSTERNOTES})
        for note in notes:
            node = Node('note', attrs={'jid': note.jid})
            node.setData(note.data)
            if note.cdate is not None:
                node.setAttr('cdate', note.cdate)
            if note.mdate is not None:
                node.setAttr('mdate', note.mdate)
            storage.addChild(node=node)
        return Iq(typ='set', queryNS=Namespace.PRIVATE, payload=storage)

    @callback
    def _default_response(self, stanza):
        if not isResultNode(stanza):
            return raise_error(self._log.info, stanza)
        return CommonResult(jid=stanza.getFrom())
