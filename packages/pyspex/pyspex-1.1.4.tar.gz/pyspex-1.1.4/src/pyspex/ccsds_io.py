"""
This file is part of pyspex

https://github.com/rmvanhees/pyspex.git

Class to read SPEXone ICU packages

Copyright (c) 2019-2020 SRON - Netherlands Institute for Space Research
   All Rights Reserved

License:  BSD-3-Clause
"""
from pathlib import Path
import argparse

import numpy as np

from pyspex.lib.tmtc_def import tmtc_def

# - global parameters ------------------------------


# - local functions --------------------------------


# - class CCSDSio -------------------------
class CCSDSio:
    """
    Defines SPEXone L0 data package

    Doc: TMTC handbook (SPX1-TN-005), issue 12, 2020-05-15
    """
    def __init__(self, flname, tmtc_issue=12, verbose=False):
        """
        Parameters
        ----------
        flname: str
           Name of the file with SPEXone ICU packages
        tmtc_issue: int
           Issue of the TMTC handbook which contains the definition of the
           Science Data Header format. Default: 12
        verbose: bool
           Be verbose. Default: be not verbose
        """
        # initialize class attributes
        self.filename = flname
        self.offset = 0
        self.__hdr = None
        self.tmtc_issue = tmtc_issue
        self.verbose = verbose

    @staticmethod
    def __hdr1_def():
        """
        Defines parameters of Primary header
        - Packet type     (3 bits): Version No.
                                    Indicates this is a CCSDS version 1 packet
                           (1 bit): Type indicator
                                    Indicates this is a telemetery packet
                           (1 bit): Secondary flag
                                    Indicate presence of Secondary header
                         (11 bits): ApID
                                    SPEXone ApID [0x320 - 0x351] or 2047

        - Packet Sequence (2 bits): Grouping flag
                                    00 continuation packet-data segment
                                    01 first packet-data segment
                                    10 last packet-data segment
                                    11 packet-data unsegmented
                         (14 bits): Counter per ApID, rollover to 0 at 0x3FFF
        - Packet length  (16 bits): size of packet data in bytes (always odd)
                                    (secondary header + User data) - 1
        """
        return [
            ('type', '>u2'),         # 0x000
            ('sequence', '>u2'),     # 0x002
            ('length', '>u2')        # 0x004
        ]

    @staticmethod
    def __timestamp():
        """
        Defines parameters of a timestamp
        - Seconds     (32 bits): seconds (TAI)
        - Sub-seconds (16 bits): sub-seconds (1/2 ** 16)
        """
        return [
            ('tai_sec', '>u4'),      # 0x006
            ('sub_sec', '>u2')       # 0x00A
        ]

    @property
    def version_no(self):
        """
        Returns CCSDS version number
        """
        if self.__hdr is None:
            return None

        return (self.__hdr['type'] >> 13) & 0x7

    @property
    def type_indicator(self):
        """
        Returns type of telemetry packet
        """
        if self.__hdr is None:
            return None

        return (self.__hdr['type'] >> 12) & 0x1

    @property
    def secnd_hdr_flag(self):
        """
        Returns flag indicating presence of a secondary header
        """
        if self.__hdr is None:
            return None

        return (self.__hdr['type'] >> 11) & 0x1

    @property
    def ap_id(self):
        """
        Returns SPEXone ApID
        """
        if self.__hdr is None:
            return None

        return self.__hdr['type'] & 0x7FF

    @property
    def grouping_flag(self):
        """
        Returns grouping flag

        Possible values:
          00 continuation packet-data segment
          01 first packet-data segment
          10 last packet-data segment
          11 packet-data unsegmented
        """
        if self.__hdr is None:
            return None

        return (self.__hdr['sequence'] >> 14) & 0x3

    @property
    def sequence_count(self):
        """
        Returns sequence counter, rollover to zero at 0x3FFF
        """
        if self.__hdr is None:
            return None

        return self.__hdr['sequence'] & 0x3FFF

    @property
    def packet_length(self):
        """
        Returns size of packet data in bytes
          Value equals secondary header + user data (always odd)
        """
        if self.__hdr is None:
            return None

        return self.__hdr['length']

    def __tm(self, num_data):
        """
        Return empty telemetry packet
        """
        return np.zeros(1, dtype=np.dtype([
            ('primary_header', np.dtype(self.__hdr1_def())),
            ('secondary_header', np.dtype(self.__timestamp())),
            ('mps', np.dtype(tmtc_def(0x350))),
            ('icu_time', np.dtype(self.__timestamp())),
            ('image_data', 'u2', (num_data,))]))

    def __rd_tm_packet(self):
        """
        Read next telemetry packet

        Parameters
        ----------
        None

        Returns
        -------
        TM packet: primary & secondary header, MPS and image-data
        """
        hdr1_dtype = np.dtype(self.__hdr1_def())
        hdr2_dtype = np.dtype(self.__timestamp())
        mps_dtype = np.dtype(tmtc_def(0x350))

        # read parts of one telemetry packet data
        with open(self.filename, 'rb') as fp:
            hdr_one = np.fromfile(fp, dtype=hdr1_dtype,
                                  count=1, offset=self.offset)
            if hdr_one.size == 0:
                self.offset = 0
                return None

            self.__hdr = hdr_one[0]
            if self.verbose:
                print('ApID: ', self.ap_id,
                      self.secnd_hdr_flag, self.grouping_flag,
                      self.sequence_count, self.packet_length)
            if self.ap_id != 0x350:
                return None

            hdr_two = None
            mps = None
            icu_time = None
            num_bytes = self.packet_length + 1
            if self.secnd_hdr_flag == 1:
                hdr_two = np.fromfile(fp, dtype=hdr2_dtype, count=1)[0]
                num_bytes -= hdr2_dtype.itemsize

            # MPS is provided in first segement or unsegmented data packet
            mps = None
            if self.grouping_flag in (1, 3):
                mps = np.fromfile(fp, dtype=mps_dtype, count=1)[0]
                num_bytes -= mps_dtype.itemsize
                if self.tmtc_issue == 12:
                    icu_time = np.fromfile(fp, dtype=hdr2_dtype, count=1)[0]
                    num_bytes -= hdr2_dtype.itemsize

                # Correct 32-bit integers which originate from 24-bit
                # Necessary due to an allignment problem, in addition,
                # the 4 bytes of DET_CHENA also contain DET_ILVDS
                key_list = ['DET_EXPTIME', 'DET_EXPSTEP', 'DET_KP1',
                            'DET_KP2', 'DET_EXPTIME2', 'DET_EXPSTEP2',
                            'DET_CHENA']
                mps['DET_ILVDS'] = mps['DET_CHENA'] & 0xf
                for key in key_list:
                    mps[key] = mps[key] >> 8

            # remainder is image data
            data = np.fromfile(fp, dtype='>u2', count=num_bytes // 2)
            if self.verbose:
                if mps is None:
                    print(self.secnd_hdr_flag, self.grouping_flag,
                          self.ap_id, hdr_two['tai_sec'], hdr_two['sub_sec'],
                          fp.tell() - self.offset, data.nbytes,
                          self.packet_length, fp.tell())
                else:
                    print(self.secnd_hdr_flag, self.grouping_flag,
                          self.ap_id, hdr_two['tai_sec'], hdr_two['sub_sec'],
                          fp.tell() - self.offset, data.nbytes,
                          self.packet_length,
                          mps['MPS_ID'], mps['IMRLEN'], fp.tell())

        # combine parts to telemetry packet
        tm_packet = self.__tm(data.size)
        tm_packet[0]['primary_header'] = self.__hdr
        if hdr_two is not None:
            tm_packet[0]['secondary_header'] = hdr_two
        if mps is not None:
            tm_packet[0]['mps'] = mps
        if icu_time is not None:
            tm_packet[0]['icu_time'] = icu_time
        tm_packet[0]['image_data'] = data

        # move offset to next telemetry packet
        self.offset += self.__hdr.nbytes + self.packet_length + 1
        return tm_packet[0]

    def read(self, raw=False):
        """
        Read Telemetry packages

        Parameters
        ----------
        raw : boolean
          raw=True: return all TM packets
          raw=False: combine packages using grouping flags (default)
        """
        # We should check that segmented packages consist of a sequence
        # with grouping flags {1, N * 0, 2}. I need to clean-up this code!
        group_flag = None
        packets = ()
        while True:
            try:
                buff = self.__rd_tm_packet()
            except (IOError, EOFError) as msg:
                print(msg)
                return None

            # end of loop
            if buff is None:
                break

            # raw processing of packages
            if raw:
                packets += (buff,)
                continue

            # get grouping flag of current package
            flag = (buff['primary_header']['sequence'] >> 14) & 0x0003

            # handle special case of the first telemetry packet
            if group_flag is None:
                if flag == 1:
                    group_flag = 2
                elif flag == 3:
                    group_flag = 3
                else:
                    print('Warning first grouping flag not equal to 1 or 3')
                    continue

            # handle unsegmented data
            if flag == 3:
                if group_flag != 3:
                    print('Warning mix of segmented and unsegmented packages')
                    continue
                packets += (buff,)
                continue

            # handle unsegmented data
            if flag == 1:
                # group_flag should be 2
                if group_flag != 2:
                    print('Warning first segment, but previous not closed?')

                data = buff['image_data']
                buff0 = self.__tm(buff['mps']['IMRLEN'] // 2)[0]
                buff0['primary_header'] = buff['primary_header']
                buff0['secondary_header'] = buff['secondary_header']
                buff0['mps'] = buff['mps']
                # buff0['image_data'][0:data.size] = data
                packets += (buff0,)
            elif flag in (0, 2):
                # group_flag should be 0 or 1
                if group_flag not in (0, 1):
                    print('Warning previous packet not closed?')

                if flag == 2:
                    data = np.concatenate((data, buff['image_data']))
                    packets[-1]['image_data'] = data
                else:
                    data = np.concatenate((data, buff['image_data']))

            # keep current grouping-flag for next read
            group_flag = flag

        return packets


# -------------------------
def main():
    """
    main function
    """
    # parse command-line parameters
    parser = argparse.ArgumentParser(
        description='Read CCSDS product (SPEXone level 0)')
    parser.add_argument('l0_product', default=None,
                        help='name of SPEXone DEM L0 product')
    parser.add_argument('--combine_segemented', action='store_true',
                        default=False)
    parser.add_argument('--verbose', action='store_true', default=False)
    args = parser.parse_args()
    if args.verbose:
        print(args)

    if not Path(args.l0_product).is_file():
        raise FileNotFoundError(
            'File {} does not exist'.format(args.l0_product))

    ccsds = CCSDSio(args.l0_product, verbose=args.verbose)
    packets = ccsds.read(raw=(not args.combine_segemented))

    if args.verbose:
        print('Number of TM packages: ', len(packets))
        mps = packets[0]['mps']
        for key in mps.dtype.names:
            print('MPS [{}] = 0x{:04X}'.format(key, mps[key]))


# --------------------------------------------------
if __name__ == '__main__':
    main()
