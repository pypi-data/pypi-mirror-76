"""Safe in Cloud dabase decryption"""
import struct
import io
import zlib

from Crypto.Cipher import AES
from passlib.utils import pbkdf2


def read_sic_db(filename, password):
    """Read the database and return the XML content."""
    with open(filename, 'rb') as db_file:
        db_file.seek(3)  # skip magic + version

        # Get salt and iv
        salt = __get_array(db_file)
        init_vector = __get_array(db_file)

        __skip_array(db_file)  # skip salt 2

        # decrypt iv and password block
        skey = pbkdf2.pbkdf2(password, salt, 10000, 32)
        cipher = AES.new(skey, AES.MODE_CBC, init_vector)
        iv_pw_block = cipher.decrypt(__get_array(db_file))

        # extract iv and password from block
        byte_buffer = io.BytesIO(iv_pw_block)
        iv2 = __get_array(byte_buffer)
        pass2 = __get_array(byte_buffer)

        __skip_array(byte_buffer)  # skip check

        # decrypt data
        cipher = AES.new(pass2, AES.MODE_CBC, iv2)
        data = cipher.decrypt(db_file.read())

        # decompress data
        decompressor = zlib.decompressobj()
        return decompressor.decompress(data) + decompressor.flush()


def __get_byte(file):
    return ord(file.read(1))


def __get_short(file):
    return int.from_bytes(file.read(2), byteorder='big')


def __get_array(file):
    size = ord(file.read(1))
    return struct.unpack("%ds" % size, file.read(size))[0]


def __skip_array(file):
    file.seek(ord(file.read(1)), 1)
