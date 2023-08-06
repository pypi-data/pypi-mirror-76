import os
import unittest

import pbtools


class ParserTest(unittest.TestCase):

    def test_int32(self):
        parsed = pbtools.parse_file('tests/files/int32.proto')

        self.assertEqual(parsed.package, 'int32')
        self.assertTrue(os.path.isabs(parsed.abspath))
        self.assertTrue(
            parsed.abspath.endswith(os.path.join('tests', 'files', 'int32.proto')))
        self.assertEqual(parsed.imports, [])
        self.assertEqual(parsed.options, [])
        self.assertEqual(len(parsed.messages), 2)

        message = parsed.messages[0]
        self.assertEqual(len(message.fields), 1)
        self.assertEqual(len(message.enums), 0)
        self.assertEqual(len(message.messages), 0)

        field = message.fields[0]
        self.assertEqual(field.type, 'int32')
        self.assertEqual(field.name, 'value')
        self.assertEqual(field.field_number, 1)
        self.assertFalse(field.repeated)

        message = parsed.messages[1]
        self.assertEqual(len(message.fields), 1)
        self.assertEqual(len(message.enums), 0)
        self.assertEqual(len(message.messages), 0)

        field = message.fields[0]
        self.assertEqual(field.type, 'int32')
        self.assertEqual(field.name, 'value')
        self.assertEqual(field.field_number, 16)
        self.assertFalse(field.repeated)

    def test_repeated(self):
        parsed = pbtools.parse_file('tests/files/repeated.proto')

        self.assertEqual(parsed.package, 'repeated')
        self.assertEqual(len(parsed.messages), 6)

        # Message.
        message = parsed.messages[0]
        self.assertEqual(len(message.fields), 4)
        self.assertEqual(len(message.enums), 0)
        self.assertEqual(len(message.messages), 0)

        field = message.fields[0]
        self.assertEqual(field.type, 'int32')
        self.assertEqual(field.name, 'int32s')
        self.assertEqual(field.field_number, 1)
        self.assertTrue(field.repeated)

        field = message.fields[1]
        self.assertEqual(field.type, 'Message')
        self.assertEqual(field.name, 'messages')
        self.assertEqual(field.field_number, 2)
        self.assertTrue(field.repeated)

        field = message.fields[2]
        self.assertEqual(field.type, 'string')
        self.assertEqual(field.name, 'strings')
        self.assertEqual(field.field_number, 3)
        self.assertTrue(field.repeated)

        field = message.fields[3]
        self.assertEqual(field.type, 'bytes')
        self.assertEqual(field.name, 'bytes')
        self.assertEqual(field.field_number, 4)
        self.assertTrue(field.repeated)

    def test_address_book(self):
        parsed = pbtools.parse_file('tests/files/address_book.proto')

        self.assertEqual(parsed.package, 'address_book')
        self.assertEqual(len(parsed.messages), 2)

        # Person.
        message = parsed.messages[0]
        self.assertEqual(message.name, 'Person')
        self.assertEqual(len(message.fields), 4)
        self.assertEqual(len(message.enums), 1)
        self.assertEqual(len(message.messages), 1)
        self.assertEqual(message.namespace, ['address_book'])
        self.assertEqual(message.full_name, 'address_book.Person')
        self.assertEqual(message.full_name_snake_case, 'address_book_person')

        field = message.fields[0]
        self.assertEqual(field.type, 'string')
        self.assertEqual(field.name, 'name')
        self.assertEqual(field.field_number, 1)
        self.assertFalse(field.repeated)
        self.assertEqual(field.namespace, [])
        self.assertEqual(field.full_type, 'string')
        self.assertEqual(field.full_type_snake_case, 'string')

        field = message.fields[1]
        self.assertEqual(field.type, 'int32')
        self.assertEqual(field.name, 'id')
        self.assertEqual(field.field_number, 2)
        self.assertFalse(field.repeated)
        self.assertEqual(field.namespace, [])

        field = message.fields[2]
        self.assertEqual(field.type, 'string')
        self.assertEqual(field.name, 'email')
        self.assertEqual(field.field_number, 3)
        self.assertFalse(field.repeated)
        self.assertEqual(field.namespace, [])

        field = message.fields[3]
        self.assertEqual(field.type, 'PhoneNumber')
        self.assertEqual(field.name, 'phones')
        self.assertEqual(field.field_number, 4)
        self.assertTrue(field.repeated)
        self.assertEqual(field.namespace, ['address_book', 'Person'])
        self.assertEqual(field.full_type, 'address_book.Person.PhoneNumber')
        self.assertEqual(field.full_type_snake_case, 'address_book_person_phone_number')

        # Person.PhoneType
        enum = message.enums[0]
        self.assertEqual(enum.name, 'PhoneType')
        self.assertEqual(len(enum.fields), 3)
        self.assertEqual(enum.namespace, ['address_book', 'Person'])

        field = enum.fields[0]
        self.assertEqual(field.name, 'MOBILE')
        self.assertEqual(field.field_number, 0)

        field = enum.fields[1]
        self.assertEqual(field.name, 'HOME')
        self.assertEqual(field.field_number, 1)

        field = enum.fields[2]
        self.assertEqual(field.name, 'WORK')
        self.assertEqual(field.field_number, 2)

        # Person.PhoneNumber
        inner_message = message.messages[0]
        self.assertEqual(inner_message.name, 'PhoneNumber')
        self.assertEqual(len(inner_message.fields), 2)
        self.assertEqual(len(inner_message.enums), 0)
        self.assertEqual(len(inner_message.messages), 0)
        self.assertEqual(inner_message.namespace, ['address_book', 'Person'])

        field = inner_message.fields[0]
        self.assertEqual(field.type, 'string')
        self.assertEqual(field.name, 'number')
        self.assertEqual(field.field_number, 1)
        self.assertFalse(field.repeated)
        self.assertEqual(field.namespace, [])

        field = inner_message.fields[1]
        self.assertEqual(field.type, 'PhoneType')
        self.assertEqual(field.name, 'type')
        self.assertEqual(field.field_number, 2)
        self.assertFalse(field.repeated)
        self.assertEqual(field.namespace, ['address_book', 'Person'])

        # AddressBook.
        message = parsed.messages[1]
        self.assertEqual(message.name, 'AddressBook')
        self.assertEqual(len(message.fields), 1)
        self.assertEqual(message.namespace, ['address_book'])

        field = message.fields[0]
        self.assertEqual(field.type, 'Person')
        self.assertEqual(field.name, 'people')
        self.assertEqual(field.field_number, 1)
        self.assertTrue(field.repeated)
        self.assertEqual(field.namespace, ['address_book'])

    def test_service(self):
        parsed = pbtools.parse_file('tests/files/service.proto')

        self.assertEqual(parsed.package, 'service')
        self.assertEqual(len(parsed.messages), 2)
        self.assertEqual(len(parsed.services), 1)

        service = parsed.services[0]
        self.assertEqual(len(service.rpcs), 6)

        rpc = service.rpcs[0]
        self.assertEqual(rpc.name, 'Foo')
        self.assertEqual(rpc.request_type, 'Request')
        self.assertFalse(rpc.request_stream)
        self.assertEqual(rpc.response_type, 'Response')
        self.assertFalse(rpc.response_stream)

        rpc = service.rpcs[1]
        self.assertEqual(rpc.name, 'Bar')
        self.assertEqual(rpc.request_type, 'Request')
        self.assertFalse(rpc.request_stream)
        self.assertEqual(rpc.response_type, 'Response')
        self.assertFalse(rpc.response_stream)

        rpc = service.rpcs[4]
        self.assertEqual(rpc.name, 'Fam')
        self.assertEqual(rpc.request_type, 'Request')
        self.assertTrue(rpc.request_stream)
        self.assertEqual(rpc.response_type, 'Response')
        self.assertTrue(rpc.response_stream)

    def test_oneof(self):
        parsed = pbtools.parse_file('tests/files/oneof.proto')

        self.assertEqual(parsed.package, 'oneof')
        self.assertEqual(len(parsed.messages), 3)

        # Message.
        message = parsed.messages[0]
        self.assertEqual(len(message.oneofs), 1)
        oneof = message.oneofs[0]
        self.assertEqual(oneof.name, 'value')
        self.assertEqual(len(oneof.fields), 2)
        self.assertEqual(oneof.namespace, ['oneof', 'Message'])
        self.assertEqual(oneof.full_name, 'oneof.Message.value')
        self.assertEqual(oneof.full_name_snake_case, 'oneof_message_value')

        field = oneof.fields[0]
        self.assertEqual(field.type, 'int32')
        self.assertEqual(field.name, 'v1')
        self.assertEqual(field.field_number, 1)
        self.assertEqual(field.namespace, [])
        self.assertEqual(field.full_type, 'int32')
        self.assertEqual(field.full_type_snake_case, 'int32')

        field = oneof.fields[1]
        self.assertEqual(field.type, 'string')
        self.assertEqual(field.name, 'v2')
        self.assertEqual(field.field_number, 2)
        self.assertEqual(field.namespace, [])
        self.assertEqual(field.full_type, 'string')
        self.assertEqual(field.full_type_snake_case, 'string')

        # Message2.
        message = parsed.messages[1]
        self.assertEqual(len(message.oneofs), 2)

        # Message2.oneof1.
        oneof = message.oneofs[0]
        self.assertEqual(oneof.name, 'oneof1')
        self.assertEqual(len(oneof.fields), 3)
        self.assertEqual(oneof.namespace, ['oneof', 'Message2'])
        self.assertEqual(oneof.full_name, 'oneof.Message2.oneof1')
        self.assertEqual(oneof.full_name_snake_case, 'oneof_message2_oneof1')

        field = oneof.fields[0]
        self.assertEqual(field.type, 'Foo')
        self.assertEqual(field.name, 'v4')
        self.assertEqual(field.field_number, 4)
        self.assertEqual(field.namespace, ['oneof', 'Message2'])
        self.assertEqual(field.full_type, 'oneof.Message2.Foo')
        self.assertEqual(field.full_type_snake_case, 'oneof_message2_foo')

        field = oneof.fields[1]
        self.assertEqual(field.type, 'bytes')
        self.assertEqual(field.name, 'v5')
        self.assertEqual(field.field_number, 5)
        self.assertEqual(field.namespace, [])
        self.assertEqual(field.full_type, 'bytes')
        self.assertEqual(field.full_type_snake_case, 'bytes')

        field = oneof.fields[2]
        self.assertEqual(field.type, 'Enum')
        self.assertEqual(field.name, 'v6')
        self.assertEqual(field.field_number, 6)
        self.assertEqual(field.namespace, ['oneof'])
        self.assertEqual(field.full_type, 'oneof.Enum')
        self.assertEqual(field.full_type_snake_case, 'oneof_enum')

        # Message2.oneof2.
        oneof = message.oneofs[1]
        field = oneof.fields[0]
        self.assertEqual(field.type, 'bool')
        self.assertEqual(field.name, 'v1')
        self.assertEqual(field.field_number, 1)
        self.assertEqual(field.namespace, [])
        self.assertEqual(field.full_type, 'bool')
        self.assertEqual(field.full_type_snake_case, 'bool')

        field = oneof.fields[1]
        self.assertEqual(field.type, 'Foo')
        self.assertEqual(field.name, 'v2')
        self.assertEqual(field.field_number, 2)
        self.assertEqual(field.namespace, ['oneof', 'Message2'])
        self.assertEqual(field.full_type, 'oneof.Message2.Foo')
        self.assertEqual(field.full_type_snake_case, 'oneof_message2_foo')

        field = oneof.fields[2]
        self.assertEqual(field.type, 'Message')
        self.assertEqual(field.name, 'v3')
        self.assertEqual(field.field_number, 3)
        self.assertEqual(field.namespace, ['oneof'])
        self.assertEqual(field.full_type, 'oneof.Message')
        self.assertEqual(field.full_type_snake_case, 'oneof_message')

        # Message3.
        message = parsed.messages[2]
        self.assertEqual(len(message.oneofs), 1)

        # Message3.Foo.
        inner_message = message.messages[0]
        self.assertEqual(inner_message.name, 'Foo')
        self.assertEqual(len(inner_message.fields), 0)
        self.assertEqual(len(inner_message.oneofs), 1)
        self.assertEqual(inner_message.namespace, ['oneof', 'Message3'])
        self.assertEqual(inner_message.full_name, 'oneof.Message3.Foo')
        self.assertEqual(inner_message.full_name_snake_case, 'oneof_message3_foo')

        # Message3.Foo.inner_message.
        oneof = inner_message.oneofs[0]
        field = oneof.fields[0]
        self.assertEqual(field.type, 'bool')
        self.assertEqual(field.name, 'v1')
        self.assertEqual(field.field_number, 1)
        self.assertEqual(field.namespace, [])
        self.assertEqual(field.full_type, 'bool')
        self.assertEqual(field.full_type_snake_case, 'bool')

        field = oneof.fields[1]
        self.assertEqual(field.type, 'bytes')
        self.assertEqual(field.name, 'v2')
        self.assertEqual(field.field_number, 2)
        self.assertEqual(field.namespace, [])
        self.assertEqual(field.full_type, 'bytes')
        self.assertEqual(field.full_type_snake_case, 'bytes')

        # Message3.Bar.
        inner_message = message.messages[1]
        self.assertEqual(inner_message.name, 'Bar')
        self.assertEqual(len(inner_message.fields), 1)
        self.assertEqual(inner_message.namespace, ['oneof', 'Message3'])
        self.assertEqual(inner_message.full_name, 'oneof.Message3.Bar')
        self.assertEqual(inner_message.full_name_snake_case, 'oneof_message3_bar')

        field = inner_message.fields[0]
        self.assertEqual(field.type, 'Foo')
        self.assertEqual(field.name, 'foo')
        self.assertEqual(field.field_number, 1)
        self.assertEqual(field.namespace, ['oneof', 'Message3'])
        self.assertEqual(field.full_type, 'oneof.Message3.Foo')
        self.assertEqual(field.full_type_snake_case, 'oneof_message3_foo')
        self.assertTrue(field.repeated)

    def test_enum(self):
        parsed = pbtools.parse_file('tests/files/enum.proto')

        self.assertEqual(parsed.package, 'enum')
        self.assertEqual(len(parsed.messages), 4)
        self.assertEqual(len(parsed.enums), 1)

        enum = parsed.enums[0]
        self.assertEqual(enum.name, 'Enum')
        self.assertEqual(len(enum.fields), 2)

        field = enum.fields[0]
        self.assertEqual(field.name, 'C')
        self.assertEqual(field.field_number, 0)

        field = enum.fields[1]
        self.assertEqual(field.name, 'D')
        self.assertEqual(field.field_number, 1)

        message = parsed.messages[0]
        enum = message.enums[0]
        self.assertEqual(enum.name, 'Enum')
        self.assertEqual(len(enum.fields), 2)

        field = enum.fields[0]
        self.assertEqual(field.name, 'A')
        self.assertEqual(field.field_number, 0)

        field = enum.fields[1]
        self.assertEqual(field.name, 'B')
        self.assertEqual(field.field_number, 1)

        message = parsed.messages[1]
        enum = message.enums[0]
        self.assertEqual(enum.name, 'InnerEnum')
        self.assertEqual(len(enum.fields), 2)

        field = enum.fields[0]
        self.assertEqual(field.name, 'E')
        self.assertEqual(field.field_number, 0)

        field = enum.fields[1]
        self.assertEqual(field.name, 'F')
        self.assertEqual(field.field_number, 1)

        # Limits.
        message = parsed.messages[2]
        enum = message.enums[0]
        self.assertEqual(enum.name, 'Enum')
        self.assertEqual(len(enum.fields), 3)

        field = enum.fields[0]
        self.assertEqual(field.name, 'G')
        self.assertEqual(field.field_number, 0)

        field = enum.fields[1]
        self.assertEqual(field.name, 'H')
        self.assertEqual(field.field_number, -2147483648)

        field = enum.fields[2]
        self.assertEqual(field.name, 'I')
        self.assertEqual(field.field_number, 2147483647)

        # AllowAlias.
        message = parsed.messages[3]
        enum = message.enums[0]
        self.assertEqual(enum.name, 'Enum')
        self.assertEqual(len(enum.fields), 3)

        field = enum.fields[0]
        self.assertEqual(field.name, 'A')
        self.assertEqual(field.field_number, 0)

        field = enum.fields[1]
        self.assertEqual(field.name, 'B')
        self.assertEqual(field.field_number, 1)

        field = enum.fields[2]
        self.assertEqual(field.name, 'C')
        self.assertEqual(field.field_number, 1)

    def test_options(self):
        parsed = pbtools.parse_file('tests/files/options.proto')

        self.assertEqual(parsed.package, 'options')
        self.assertEqual(len(parsed.options), 2)

        option = parsed.options[0]
        self.assertEqual(option.name, 'foo')
        self.assertEqual(option.kind, 'bool')
        self.assertEqual(option.value, True)

        option = parsed.options[1]
        self.assertEqual(option.name, '(bar).fie')
        self.assertEqual(option.kind, 'bool')
        self.assertEqual(option.value, True)

    def test_message(self):
        parsed = pbtools.parse_file('tests/files/message.proto')

        self.assertEqual(parsed.package, 'message')
        self.assertEqual(len(parsed.messages), 4)

        # message.Foo.
        message = parsed.messages[0]
        self.assertEqual(message.name, 'Foo')
        self.assertEqual(message.namespace, ['message'])
        self.assertEqual(message.full_name, 'message.Foo')

        # message.Bar.
        message = parsed.messages[1]
        self.assertEqual(message.name, 'Bar')
        self.assertEqual(message.namespace, ['message'])
        self.assertEqual(message.full_name, 'message.Bar')

        field = message.fields[0]
        self.assertEqual(field.type, 'int32')
        self.assertEqual(field.name, 'fie')
        self.assertEqual(field.namespace, [])
        self.assertEqual(field.full_type, 'int32')
        self.assertEqual(field.full_type_snake_case, 'int32')
        self.assertEqual(field.type_kind, 'scalar-value-type')

        # message.Message.
        message = parsed.messages[2]
        self.assertEqual(message.name, 'Message')
        self.assertEqual(message.namespace, ['message'])
        self.assertEqual(message.full_name, 'message.Message')

        field = message.fields[0]
        self.assertEqual(field.type, 'Foo')
        self.assertEqual(field.name, 'foo')
        self.assertEqual(field.namespace, ['message', 'Message'])
        self.assertEqual(field.full_type, 'message.Message.Foo')
        self.assertEqual(field.full_type_snake_case, 'message_message_foo')
        self.assertEqual(field.type_kind, 'enum')

        field = message.fields[1]
        self.assertEqual(field.type, 'Bar')
        self.assertEqual(field.name, 'bar')
        self.assertEqual(field.namespace, ['message'])
        self.assertEqual(field.full_type, 'message.Bar')
        self.assertEqual(field.full_type_snake_case, 'message_bar')
        self.assertEqual(field.type_kind, 'message')

        field = message.fields[2]
        self.assertEqual(field.type, 'Fie')
        self.assertEqual(field.name, 'fie')
        self.assertEqual(field.namespace, ['message', 'Message'])
        self.assertEqual(field.full_type, 'message.Message.Fie')
        self.assertEqual(field.full_type_snake_case, 'message_message_fie')
        self.assertEqual(field.type_kind, 'message')

        # message.Message.Foo.
        enum = message.enums[0]
        self.assertEqual(enum.name, 'Foo')
        self.assertEqual(enum.namespace, ['message', 'Message'])
        self.assertEqual(enum.full_name, 'message.Message.Foo')

        # message.Message.Fie.
        fie_message = message.messages[0]
        self.assertEqual(fie_message.name, 'Fie')
        self.assertEqual(fie_message.namespace, ['message', 'Message'])
        self.assertEqual(fie_message.full_name, 'message.Message.Fie')

        field = fie_message.fields[0]
        self.assertEqual(field.type, 'Foo')
        self.assertEqual(field.name, 'foo')
        self.assertEqual(field.namespace, ['message', 'Message', 'Fie'])
        self.assertEqual(field.full_type, 'message.Message.Fie.Foo')
        self.assertEqual(field.full_type_snake_case, 'message_message_fie_foo')
        self.assertEqual(field.type_kind, 'message')

        # message.Message.Fie.Foo.
        fie_foo_message = fie_message.messages[0]
        self.assertEqual(fie_foo_message.name, 'Foo')
        self.assertEqual(fie_foo_message.namespace, ['message', 'Message', 'Fie'])
        self.assertEqual(fie_foo_message.full_name, 'message.Message.Fie.Foo')

        field = fie_foo_message.fields[0]
        self.assertEqual(field.type, 'bool')
        self.assertEqual(field.name, 'value')
        self.assertEqual(field.namespace, [])
        self.assertEqual(field.full_type, 'bool')
        self.assertEqual(field.full_type_snake_case, 'bool')
        self.assertEqual(field.type_kind, 'scalar-value-type')

        field = fie_foo_message.fields[1]
        self.assertEqual(field.type, 'Bar')
        self.assertEqual(field.name, 'bar')
        self.assertEqual(field.namespace, ['message'])
        self.assertEqual(field.full_type, 'message.Bar')
        self.assertEqual(field.full_type_snake_case, 'message_bar')
        self.assertEqual(field.type_kind, 'message')

    def test_benchmark(self):
        parsed = pbtools.parse_file('tests/files/benchmark.proto')

        self.assertEqual(parsed.package, 'benchmark')
        self.assertEqual(len(parsed.messages), 5)
        self.assertEqual(len(parsed.options), 3)

        # Options.
        option = parsed.options[0]
        self.assertEqual(option.name, 'java_package')
        self.assertEqual(option.kind, 'string')
        self.assertEqual(option.value, 'com.google.protobuf.benchmarks')

        option = parsed.options[1]
        self.assertEqual(option.name, 'optimize_for')
        self.assertEqual(option.kind, 'ident')
        self.assertEqual(option.value, 'SPEED')

        option = parsed.options[2]
        self.assertEqual(option.name, 'cc_enable_arenas')
        self.assertEqual(option.kind, 'bool')
        self.assertEqual(option.value, True)

    def test_no_package(self):
        parsed = pbtools.parse_file('tests/files/no_package.proto')

        self.assertEqual(parsed.package, None)
        self.assertEqual(len(parsed.messages), 1)

        # M0.
        message = parsed.messages[0]
        self.assertEqual(len(message.fields), 3)
        self.assertEqual(message.name, 'M0')
        self.assertEqual(message.full_name, 'M0')
        self.assertEqual(message.full_name_snake_case, 'm0')

        field = message.fields[0]
        self.assertEqual(field.type, 'M1')
        self.assertEqual(field.name, 'v1')
        self.assertEqual(field.field_number, 1)
        self.assertEqual(field.namespace, ['M0'])

        field = message.fields[1]
        self.assertEqual(field.type, 'M1')
        self.assertEqual(field.name, 'v2')
        self.assertEqual(field.field_number, 2)
        self.assertEqual(field.namespace, ['M0'])

        field = message.fields[2]
        self.assertEqual(field.type, 'E1')
        self.assertEqual(field.name, 'v3')
        self.assertEqual(field.field_number, 3)
        self.assertEqual(field.namespace, ['M0'])

    def test_importing(self):
        parsed = pbtools.parse_file('tests/files/importing.proto',
                                    [
                                        'tests/files',
                                        'tests/files/imports'
                                    ])

        self.assertEqual(len(parsed.imports), 3)

        imported = parsed.imports[0]
        self.assertEqual(imported.path, 'imported.proto')
        self.assertEqual(imported.package, 'imported')
        self.assertTrue(
            imported.abspath.endswith(os.path.join('tests', 'files', 'imported.proto')))
        self.assertEqual(imported.enums, ['ImportedEnum'])
        self.assertEqual(imported.messages, ['ImportedMessage'])

        imported = parsed.imports[1]
        self.assertEqual(imported.path, 'imported_duplicated_package.proto')
        self.assertEqual(imported.package, 'imported')
        self.assertTrue(
            imported.abspath.endswith(
                os.path.join('tests', 'files', 'imports', 'imported_duplicated_package.proto')))
        self.assertEqual(imported.enums, ['ImportedDuplicatedPackageEnum'])
        self.assertEqual(imported.messages,
                         ['Imported2Message', 'ImportedDuplicatedPackageMessage'])

        imported = parsed.imports[2]
        self.assertEqual(imported.path, 'imported2.proto')
        self.assertEqual(imported.package, 'imported2.foo.bar')
        self.assertTrue(
            imported.abspath.endswith(
                os.path.join('tests', 'files', 'imports', 'imported2.proto')))
        self.assertEqual(imported.enums, ['Imported2Enum'])
        self.assertEqual(imported.messages,
                         ['Imported2Message', 'Imported3Message'])

        self.assertEqual(len(parsed.messages), 3)

        # Message.
        message = parsed.messages[0]
        self.assertEqual(len(message.fields), 2)

        field = message.fields[0]
        self.assertEqual(field.type, 'ImportedEnum')
        self.assertEqual(field.type_kind, 'enum')
        self.assertEqual(field.name, 'v1')
        self.assertEqual(field.field_number, 1)
        self.assertEqual(field.package, 'imported')

        field = message.fields[1]
        self.assertEqual(field.type, 'ImportedMessage')
        self.assertEqual(field.type_kind, 'message')
        self.assertEqual(field.name, 'v2')
        self.assertEqual(field.field_number, 2)
        self.assertEqual(field.package, 'imported')

        # Message2.
        message = parsed.messages[1]
        self.assertEqual(len(message.fields), 2)

        field = message.fields[0]
        self.assertEqual(field.type, 'Message')
        self.assertEqual(field.type_kind, 'message')
        self.assertEqual(field.name, 'v1')
        self.assertEqual(field.field_number, 1)
        self.assertEqual(field.package, 'importing')

        field = message.fields[1]
        self.assertEqual(field.type, 'Imported2Message')
        self.assertEqual(field.type_kind, 'message')
        self.assertEqual(field.name, 'v2')
        self.assertEqual(field.field_number, 2)
        self.assertEqual(field.package, 'imported2.foo.bar')

        # Message3.
        message = parsed.messages[2]
        self.assertEqual(len(message.fields), 2)

        field = message.fields[0]
        self.assertEqual(field.type, 'ImportedDuplicatedPackageEnum')
        self.assertEqual(field.type_kind, 'enum')
        self.assertEqual(field.name, 'v1')
        self.assertEqual(field.field_number, 1)
        self.assertEqual(field.package, 'imported')

        field = message.fields[1]
        self.assertEqual(field.type, 'ImportedDuplicatedPackageMessage')
        self.assertEqual(field.type_kind, 'message')
        self.assertEqual(field.name, 'v2')
        self.assertEqual(field.field_number, 2)
        self.assertEqual(field.package, 'imported')

    def test_no_package_importing(self):
        parsed = pbtools.parse_file('tests/files/no_package_importing.proto',
                                    ['tests/files'])

        self.assertEqual(len(parsed.messages), 1)

        message = parsed.messages[0]
        self.assertEqual(len(message.fields), 1)

        field = message.fields[0]
        self.assertEqual(field.type, 'NoPackageImportedMessage')
        self.assertEqual(field.type_kind, 'message')
        self.assertEqual(field.name, 'v3')
        self.assertEqual(field.field_number, 1)
        self.assertEqual(field.package, None)

    def test_missing_type(self):
        with self.assertRaises(pbtools.Error) as cm:
            pbtools.parse_file('tests/files/missing_type.proto')

        self.assertEqual(str(cm.exception), "'MissingType' is not defined.")

    def test_comments(self):
        # Ok.
        parsed = pbtools.parse_file('tests/files/comments.proto')
        self.assertEqual(len(parsed.messages), 1)

        # Missing multi line end.
        with self.assertRaises(pbtools.Error) as cm:
            pbtools.parse_file('tests/files/comments_missing_multi_line_end.proto')

        self.assertEqual(str(cm.exception),
                         'Invalid syntax at line 5, column 1: ">>!<</*"')

        # Nested multi line comments are not allowed.
        with self.assertRaises(pbtools.Error) as cm:
            pbtools.parse_file('tests/files/comments_nested_multi_line.proto')

        self.assertEqual(str(cm.exception),
                         'Invalid syntax at line 3, column 1: ">>!<</*"')

    def test_reserved(self):
        pbtools.parse_file('tests/files/reserved.proto')

    def test_field_names(self):
        parsed = pbtools.parse_file('tests/files/field_names.proto')

        self.assertEqual(parsed.package, 'field_names')
        self.assertEqual(len(parsed.messages), 6)

        message = parsed.messages[0]
        self.assertEqual(len(message.fields), 1)
        self.assertEqual(len(message.enums), 0)
        self.assertEqual(len(message.messages), 0)

        field = message.fields[0]
        self.assertEqual(field.type, 'bool')
        self.assertEqual(field.name, 'MyValue')
        self.assertEqual(field.name_snake_case, 'my_value')

        message = parsed.messages[1]
        self.assertEqual(len(message.fields), 17)
        self.assertEqual(message.fields[0].name, 'myInt32')
        self.assertEqual(message.fields[0].name_snake_case, 'my_int32')
        self.assertEqual(message.fields[1].name, 'myInt64')
        self.assertEqual(message.fields[1].name_snake_case, 'my_int64')
        self.assertEqual(message.fields[2].name, 'mySint32')
        self.assertEqual(message.fields[2].name_snake_case, 'my_sint32')
        self.assertEqual(message.fields[3].name, 'mySint64')
        self.assertEqual(message.fields[3].name_snake_case, 'my_sint64')
        self.assertEqual(message.fields[4].name, 'myUint32')
        self.assertEqual(message.fields[4].name_snake_case, 'my_uint32')
        self.assertEqual(message.fields[5].name, 'myUint64')
        self.assertEqual(message.fields[5].name_snake_case, 'my_uint64')
        self.assertEqual(message.fields[6].name, 'myFixed32')
        self.assertEqual(message.fields[6].name_snake_case, 'my_fixed32')
        self.assertEqual(message.fields[7].name, 'myFixed64')
        self.assertEqual(message.fields[7].name_snake_case, 'my_fixed64')
        self.assertEqual(message.fields[8].name, 'mySfixed32')
        self.assertEqual(message.fields[8].name_snake_case, 'my_sfixed32')
        self.assertEqual(message.fields[9].name, 'mySfixed64')
        self.assertEqual(message.fields[9].name_snake_case, 'my_sfixed64')
        self.assertEqual(message.fields[10].name, 'myFloat')
        self.assertEqual(message.fields[10].name_snake_case, 'my_float')
        self.assertEqual(message.fields[11].name, 'myDouble')
        self.assertEqual(message.fields[11].name_snake_case, 'my_double')
        self.assertEqual(message.fields[12].name, 'myBool')
        self.assertEqual(message.fields[12].name_snake_case, 'my_bool')
        self.assertEqual(message.fields[13].name, 'myString')
        self.assertEqual(message.fields[13].name_snake_case, 'my_string')
        self.assertEqual(message.fields[14].name, 'myBytes')
        self.assertEqual(message.fields[14].name_snake_case, 'my_bytes')
        self.assertEqual(message.fields[15].name, 'myEnum')
        self.assertEqual(message.fields[15].name_snake_case, 'my_enum')
        self.assertEqual(message.fields[16].name, 'myMessage')
        self.assertEqual(message.fields[16].name_snake_case, 'my_message')

        message = parsed.messages[2]
        self.assertEqual(len(message.fields), 17)
        self.assertEqual(message.fields[0].name, 'MyInt32')
        self.assertEqual(message.fields[0].name_snake_case, 'my_int32')
        self.assertEqual(message.fields[1].name, 'MyInt64')
        self.assertEqual(message.fields[1].name_snake_case, 'my_int64')
        self.assertEqual(message.fields[2].name, 'MySint32')
        self.assertEqual(message.fields[2].name_snake_case, 'my_sint32')
        self.assertEqual(message.fields[3].name, 'MySint64')
        self.assertEqual(message.fields[3].name_snake_case, 'my_sint64')
        self.assertEqual(message.fields[4].name, 'MyUint32')
        self.assertEqual(message.fields[4].name_snake_case, 'my_uint32')
        self.assertEqual(message.fields[5].name, 'MyUint64')
        self.assertEqual(message.fields[5].name_snake_case, 'my_uint64')
        self.assertEqual(message.fields[6].name, 'MyFixed32')
        self.assertEqual(message.fields[6].name_snake_case, 'my_fixed32')
        self.assertEqual(message.fields[7].name, 'MyFixed64')
        self.assertEqual(message.fields[7].name_snake_case, 'my_fixed64')
        self.assertEqual(message.fields[8].name, 'MySfixed32')
        self.assertEqual(message.fields[8].name_snake_case, 'my_sfixed32')
        self.assertEqual(message.fields[9].name, 'MySfixed64')
        self.assertEqual(message.fields[9].name_snake_case, 'my_sfixed64')
        self.assertEqual(message.fields[10].name, 'MyFloat')
        self.assertEqual(message.fields[10].name_snake_case, 'my_float')
        self.assertEqual(message.fields[11].name, 'MyDouble')
        self.assertEqual(message.fields[11].name_snake_case, 'my_double')
        self.assertEqual(message.fields[12].name, 'MyBool')
        self.assertEqual(message.fields[12].name_snake_case, 'my_bool')
        self.assertEqual(message.fields[13].name, 'MyString')
        self.assertEqual(message.fields[13].name_snake_case, 'my_string')
        self.assertEqual(message.fields[14].name, 'MyBytes')
        self.assertEqual(message.fields[14].name_snake_case, 'my_bytes')
        self.assertEqual(message.fields[15].name, 'MyEnum')
        self.assertEqual(message.fields[15].name_snake_case, 'my_enum')
        self.assertEqual(message.fields[16].name, 'MyMessage')
        self.assertEqual(message.fields[16].name_snake_case, 'my_message')

        message = parsed.messages[3]
        self.assertEqual(len(message.fields), 17)
        self.assertEqual(message.fields[0].name, 'myInt32')
        self.assertEqual(message.fields[0].name_snake_case, 'my_int32')
        self.assertEqual(message.fields[1].name, 'myInt64')
        self.assertEqual(message.fields[1].name_snake_case, 'my_int64')
        self.assertEqual(message.fields[2].name, 'mySint32')
        self.assertEqual(message.fields[2].name_snake_case, 'my_sint32')
        self.assertEqual(message.fields[3].name, 'mySint64')
        self.assertEqual(message.fields[3].name_snake_case, 'my_sint64')
        self.assertEqual(message.fields[4].name, 'myUint32')
        self.assertEqual(message.fields[4].name_snake_case, 'my_uint32')
        self.assertEqual(message.fields[5].name, 'myUint64')
        self.assertEqual(message.fields[5].name_snake_case, 'my_uint64')
        self.assertEqual(message.fields[6].name, 'myFixed32')
        self.assertEqual(message.fields[6].name_snake_case, 'my_fixed32')
        self.assertEqual(message.fields[7].name, 'myFixed64')
        self.assertEqual(message.fields[7].name_snake_case, 'my_fixed64')
        self.assertEqual(message.fields[8].name, 'mySfixed32')
        self.assertEqual(message.fields[8].name_snake_case, 'my_sfixed32')
        self.assertEqual(message.fields[9].name, 'mySfixed64')
        self.assertEqual(message.fields[9].name_snake_case, 'my_sfixed64')
        self.assertEqual(message.fields[10].name, 'myFloat')
        self.assertEqual(message.fields[10].name_snake_case, 'my_float')
        self.assertEqual(message.fields[11].name, 'myDouble')
        self.assertEqual(message.fields[11].name_snake_case, 'my_double')
        self.assertEqual(message.fields[12].name, 'myBool')
        self.assertEqual(message.fields[12].name_snake_case, 'my_bool')
        self.assertEqual(message.fields[13].name, 'myString')
        self.assertEqual(message.fields[13].name_snake_case, 'my_string')
        self.assertEqual(message.fields[14].name, 'myBytes')
        self.assertEqual(message.fields[14].name_snake_case, 'my_bytes')
        self.assertEqual(message.fields[15].name, 'myEnum')
        self.assertEqual(message.fields[15].name_snake_case, 'my_enum')
        self.assertEqual(message.fields[16].name, 'myMessage')
        self.assertEqual(message.fields[16].name_snake_case, 'my_message')

        message = parsed.messages[4]
        self.assertEqual(len(message.fields), 17)
        self.assertEqual(message.fields[0].name, 'MyInt32')
        self.assertEqual(message.fields[0].name_snake_case, 'my_int32')
        self.assertEqual(message.fields[1].name, 'MyInt64')
        self.assertEqual(message.fields[1].name_snake_case, 'my_int64')
        self.assertEqual(message.fields[2].name, 'MySint32')
        self.assertEqual(message.fields[2].name_snake_case, 'my_sint32')
        self.assertEqual(message.fields[3].name, 'MySint64')
        self.assertEqual(message.fields[3].name_snake_case, 'my_sint64')
        self.assertEqual(message.fields[4].name, 'MyUint32')
        self.assertEqual(message.fields[4].name_snake_case, 'my_uint32')
        self.assertEqual(message.fields[5].name, 'MyUint64')
        self.assertEqual(message.fields[5].name_snake_case, 'my_uint64')
        self.assertEqual(message.fields[6].name, 'MyFixed32')
        self.assertEqual(message.fields[6].name_snake_case, 'my_fixed32')
        self.assertEqual(message.fields[7].name, 'MyFixed64')
        self.assertEqual(message.fields[7].name_snake_case, 'my_fixed64')
        self.assertEqual(message.fields[8].name, 'MySfixed32')
        self.assertEqual(message.fields[8].name_snake_case, 'my_sfixed32')
        self.assertEqual(message.fields[9].name, 'MySfixed64')
        self.assertEqual(message.fields[9].name_snake_case, 'my_sfixed64')
        self.assertEqual(message.fields[10].name, 'MyFloat')
        self.assertEqual(message.fields[10].name_snake_case, 'my_float')
        self.assertEqual(message.fields[11].name, 'MyDouble')
        self.assertEqual(message.fields[11].name_snake_case, 'my_double')
        self.assertEqual(message.fields[12].name, 'MyBool')
        self.assertEqual(message.fields[12].name_snake_case, 'my_bool')
        self.assertEqual(message.fields[13].name, 'MyString')
        self.assertEqual(message.fields[13].name_snake_case, 'my_string')
        self.assertEqual(message.fields[14].name, 'MyBytes')
        self.assertEqual(message.fields[14].name_snake_case, 'my_bytes')
        self.assertEqual(message.fields[15].name, 'MyEnum')
        self.assertEqual(message.fields[15].name_snake_case, 'my_enum')
        self.assertEqual(message.fields[16].name, 'MyMessage')
        self.assertEqual(message.fields[16].name_snake_case, 'my_message')

        message = parsed.messages[5]
        self.assertEqual(len(message.oneofs), 1)
        oneof = message.oneofs[0]
        self.assertEqual(oneof.name, 'OneOf')
        self.assertEqual(oneof.name_snake_case, 'one_of')
        self.assertEqual(oneof.fields[0].name, 'camelCaseMessage')
        self.assertEqual(oneof.fields[0].name_snake_case, 'camel_case_message')
        self.assertEqual(oneof.fields[1].name, 'PascalCaseMessage')
        self.assertEqual(oneof.fields[1].name_snake_case, 'pascal_case_message')
        self.assertEqual(oneof.fields[2].name, 'camelCaseMessageRepeated')
        self.assertEqual(
            oneof.fields[2].name_snake_case, 'camel_case_message_repeated')
        self.assertEqual(oneof.fields[3].name, 'PascalCaseMessageRepeated')
        self.assertEqual(
            oneof.fields[3].name_snake_case, 'pascal_case_message_repeated')
        self.assertEqual(oneof.fields[4].name, 'myInt32')
        self.assertEqual(oneof.fields[4].name_snake_case, 'my_int32')
        self.assertEqual(oneof.fields[5].name, 'myString')
        self.assertEqual(oneof.fields[5].name_snake_case, 'my_string')
        self.assertEqual(oneof.fields[6].name, 'myBytes')
        self.assertEqual(oneof.fields[6].name_snake_case, 'my_bytes')

    def test_public_import(self):
        parsed = pbtools.parse_file('tests/files/public_importing.proto',
                                    [
                                        'tests/files',
                                        'tests/files/imports'
                                    ])

    def test_optional_fields(self):
        parsed = pbtools.parse_file('tests/files/optional_fields.proto')

        message = parsed.messages[0]

        field = message.fields[0]
        self.assertEqual(field.type, 'int32')
        self.assertEqual(field.name, 'v1')
        self.assertTrue(field.optional)

        field = message.fields[3]
        self.assertEqual(field.type, 'int32')
        self.assertEqual(field.name, 'v4')
        self.assertFalse(field.optional)


if __name__ == '__main__':
    unittest.main()
