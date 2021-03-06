# -*- coding: utf-8 -*-

# Note: the tests depend on the certificates, which makes them time-dependent, because the certificates will expire at some point

import sys
import os
import os.path
from unittest import TestCase, TestSuite, TextTestRunner
from security import verify_prefix_with_cert, verify_cert, verify_signature

class TestRAVerification(TestCase):

    module_path = os.path.abspath(__file__)
    module_directory = os.path.split(module_path)[0]
    upper_directory = os.path.split(module_directory)[0]

    o_data_directory = os.path.join(module_directory, "example_data", "only_one_block")
    m_data_directory = os.path.join(module_directory, "example_data", "multiple_blocks")

    ripe_o_pem_path = os.path.join(o_data_directory, "ripe", "ripe.cer")
    dfn_o_pem_path = os.path.join(o_data_directory, "dfn", "dfn.cer")
    uni_o_pem_path = os.path.join(o_data_directory, "uni_potsdam", "uni_potsdam.cer")
    hpi_o_pem_path = os.path.join(o_data_directory, "hpi", "hpi.cer")
    router0_o_pem_path = os.path.join(o_data_directory, "router0", "router0.cer")
    router1_o_pem_path = os.path.join(o_data_directory, "router1_correct", "router1.cer")
    router2_o_pem_path = os.path.join(o_data_directory, "router2_faulty_range", "router2.cer")
    router3_o_pem_path = os.path.join(o_data_directory, "router3_faulty_selfsigned", "router3.cer")

    ripe_o_der_path = os.path.join(o_data_directory, "ripe", "ripe.der")
    dfn_o_der_path = os.path.join(o_data_directory, "dfn", "dfn.der")
    uni_o_der_path = os.path.join(o_data_directory, "uni_potsdam", "uni_potsdam.der")
    hpi_o_der_path = os.path.join(o_data_directory, "hpi", "hpi.der")
    router0_o_der_path = os.path.join(o_data_directory, "router0", "router0.der")
    router1_o_der_path = os.path.join(o_data_directory, "router1_correct", "router1.der")
    router2_o_der_path = os.path.join(o_data_directory, "router2_faulty_range", "router2.der")
    router3_o_der_path = os.path.join(o_data_directory, "router3_faulty_selfsigned", "router3.der")

    ripe_m_pem_path = os.path.join(m_data_directory, "ripe", "ripe.cer")
    dfn_m_pem_path = os.path.join(m_data_directory, "dfn", "dfn.cer")
    uni_m_pem_path = os.path.join(m_data_directory, "uni_potsdam", "uni_potsdam.cer")
    hpi_m_pem_path = os.path.join(m_data_directory, "hpi", "hpi.cer")
    router0_m_pem_path = os.path.join(m_data_directory, "router0", "router0.cer")

    ripe_m_der_path = os.path.join(m_data_directory, "ripe", "ripe.der")
    dfn_m_der_path = os.path.join(m_data_directory, "dfn", "dfn.der")
    uni_m_der_path = os.path.join(m_data_directory, "uni_potsdam", "uni_potsdam.der")
    hpi_m_der_path = os.path.join(m_data_directory, "hpi", "hpi.der")
    router0_m_der_path = os.path.join(m_data_directory, "router0", "router0.der")

    signed_ra_path = os.path.join(o_data_directory, "router0", "signed_data")
    ra_signature_path = os.path.join(o_data_directory, "router0", "signature")

    fh = open(signed_ra_path, "rb")
    signed_ra = fh.read()
    fh.close()
    fh = open(ra_signature_path, "rb")
    ra_signature = fh.read()
    fh.close()

    fh = open(ripe_o_der_path, "rb")
    ripe_o_der = fh.read()
    fh.close()
    fh = open(dfn_o_der_path, "rb")
    dfn_o_der = fh.read()
    fh.close()
    fh = open(uni_o_der_path, "rb")
    uni_o_der = fh.read()
    fh.close()
    fh = open(hpi_o_der_path, "rb")
    hpi_o_der = fh.read()
    fh.close()
    fh = open(router0_o_der_path, "rb")
    router0_o_der = fh.read()
    fh.close()
    fh = open(router1_o_der_path, "rb")
    router1_o_der = fh.read()
    fh.close()
    fh = open(router2_o_der_path, "rb")
    router2_o_der = fh.read()
    fh.close()
    fh = open(router3_o_der_path, "rb")
    router3_o_der = fh.read()
    fh.close()
    fh = open(ripe_m_der_path, "rb")
    ripe_m_der = fh.read()
    fh.close()
    fh = open(dfn_m_der_path, "rb")
    dfn_m_der = fh.read()
    fh.close()
    fh = open(uni_m_der_path, "rb")
    uni_m_der = fh.read()
    fh.close()
    fh = open(hpi_m_der_path, "rb")
    hpi_m_der = fh.read()
    fh.close()
    fh = open(router0_m_der_path, "rb")
    router0_m_der = fh.read()
    fh.close()

    prefix_b = bytearray(b'\x20\x01\x06\x38\x08\x07\x02\x1d\x00\x00\x00\x00\x00\x00\x00\x00')
    prefix_bad = bytearray(b'\x20\x03\x06\x38\x08\x07\x02\x1d\x00\x00\x00\x00\x00\x00\x00\x00')
    prefix_length = 64
    prefix_ext_0 = "IPv6:2001:638:807:21d::/64"
    prefix_ext_1 = "IPv6:2001:0638::/32"

    def setUp(self):
        self.ripe_o_der = TestRAVerification.ripe_o_der
        self.ripe_m_der = TestRAVerification.ripe_m_der
        self.dfn_o_der = TestRAVerification.dfn_o_der
        self.dfn_m_der = TestRAVerification.dfn_m_der
        self.uni_o_der = TestRAVerification.uni_o_der
        self.uni_m_der = TestRAVerification.uni_m_der
        self.hpi_o_der = TestRAVerification.hpi_o_der
        self.hpi_m_der = TestRAVerification.hpi_m_der
        self.router0_o_der = TestRAVerification.router0_o_der
        self.router0_m_der = TestRAVerification.router0_m_der
        self.router1_o_der = TestRAVerification.router1_o_der
        self.router2_o_der = TestRAVerification.router2_o_der
        self.router3_o_der = TestRAVerification.router3_o_der
        self.prefix_b = TestRAVerification.prefix_b
        self.prefix_length = TestRAVerification.prefix_length
        self.prefix_bad = TestRAVerification.prefix_bad
        self.signed_ra = TestRAVerification.signed_ra
        self.ra_signature = TestRAVerification.ra_signature

    def test_verify_prefix(self):
        self.assertTrue(
            verify_prefix_with_cert(
                [self.ripe_o_der],
                [],
                self.dfn_o_der,
                self.prefix_b,
                self.prefix_length
            )
        ) 
        self.assertTrue(
            verify_prefix_with_cert(
                [self.ripe_o_der],
                [self.dfn_o_der],
                self.uni_o_der,
                self.prefix_b,
                self.prefix_length
            )
        ) 
        self.assertFalse(
            verify_prefix_with_cert(
                [self.ripe_o_der],
                [],
                self.uni_o_der,
                self.prefix_b,
                self.prefix_length
            )
        )
        self.assertTrue(
            verify_prefix_with_cert(
                [self.ripe_o_der],
                [self.dfn_o_der, self.uni_o_der, self.hpi_o_der],
                self.router1_o_der,
                self.prefix_b,
                self.prefix_length
            )
        ) 
        self.assertFalse(
            verify_prefix_with_cert(
                [self.ripe_o_der],
                [self.dfn_o_der, self.uni_o_der, self.hpi_o_der],
                self.router2_o_der,
                self.prefix_b,
                self.prefix_length
            )
        )
        self.assertFalse(
            verify_prefix_with_cert(
                [self.ripe_o_der],
                [self.dfn_o_der, self.uni_o_der, self.hpi_o_der],
                self.router3_o_der,
                self.prefix_b,
                self.prefix_length
            )
        )
        self.assertFalse(
            verify_prefix_with_cert(
                [self.ripe_o_der],
                [self.dfn_o_der, self.uni_o_der, self.hpi_o_der],
                self.router1_o_der,
                self.prefix_b,
                self.prefix_length - 1
            )
        )
        self.assertFalse(
            verify_prefix_with_cert(
                [self.ripe_o_der],
                [],
                self.dfn_o_der,
                self.prefix_bad,
                self.prefix_length
            )
        )
        self.assertFalse(
            verify_prefix_with_cert(
                [self.ripe_o_der],
                [self.dfn_o_der, self.uni_o_der, self.hpi_o_der],
                self.router1_o_der,
                self.prefix_bad,
                self.prefix_length
            )
        )
        self.assertTrue(
            verify_prefix_with_cert(
                [self.ripe_m_der],
                [],
                self.dfn_m_der,
                self.prefix_b,
                self.prefix_length
            )
        ) 
        self.assertTrue(
            verify_prefix_with_cert(
                [self.ripe_m_der],
                [self.dfn_m_der],
                self.uni_m_der,
                self.prefix_b,
                self.prefix_length
            )
        ) 
        self.assertFalse(
            verify_prefix_with_cert(
                [self.ripe_m_der],
                [],
                self.uni_m_der,
                self.prefix_b,
                self.prefix_length
            )
        )
        self.assertTrue(
            verify_prefix_with_cert(
                [self.ripe_m_der],
                [self.dfn_m_der, self.uni_m_der, self.hpi_m_der],
                self.router0_m_der,
                self.prefix_b,
                self.prefix_length
            )
        )
        self.assertTrue(
            verify_prefix_with_cert(
                [self.ripe_m_der],
                [self.dfn_m_der, self.uni_m_der, self.hpi_m_der],
                self.router0_m_der + b'\x00',
                self.prefix_b,
                self.prefix_length
            )
        )
        self.assertTrue(
            verify_prefix_with_cert(
                [self.ripe_m_der],
                [self.dfn_m_der + b'\x00', self.uni_m_der, self.hpi_m_der],
                self.router0_m_der,
                self.prefix_b,
                self.prefix_length
            )
        )
        self.assertTrue(
            verify_prefix_with_cert(
                [self.ripe_m_der],
                [self.dfn_m_der, self.uni_m_der + b'\x00', self.hpi_m_der],
                self.router0_m_der,
                self.prefix_b,
                self.prefix_length
            )
        )
        self.assertTrue(
            verify_prefix_with_cert(
                [self.ripe_m_der],
                [self.dfn_m_der, self.uni_m_der, self.hpi_m_der + b'\x00'],
                self.router0_m_der,
                self.prefix_b,
                self.prefix_length
            )
        )
        self.assertFalse(
            verify_prefix_with_cert(
                [self.ripe_m_der],
                [self.dfn_m_der, self.uni_m_der, self.hpi_m_der],
                self.router0_m_der,
                self.prefix_b,
                self.prefix_length - 1
            )
        )
        self.assertFalse(
            verify_prefix_with_cert(
                [self.ripe_m_der],
                [],
                self.dfn_m_der,
                self.prefix_bad,
                self.prefix_length
            )
        )

    def test_verify_cert(self):
        self.assertTrue(verify_cert([self.ripe_o_der], [], self.dfn_o_der))
        self.assertTrue(verify_cert([self.ripe_o_der], [self.dfn_o_der], self.uni_o_der))
        self.assertFalse(verify_cert([self.ripe_o_der], [], self.uni_o_der))
        self.assertTrue(
            verify_cert(
                [self.ripe_o_der],
                [self.dfn_o_der, self.uni_o_der, self.hpi_o_der],
                self.router1_o_der
            )
        )
        self.assertTrue(
            verify_cert(
                [self.ripe_o_der],
                [self.dfn_o_der + b'\x00', self.uni_o_der, self.hpi_o_der],
                self.router1_o_der
            )
        )
        self.assertTrue(
            verify_cert(
                [self.ripe_o_der],
                [self.dfn_o_der, self.uni_o_der + b'\x00', self.hpi_o_der],
                self.router1_o_der
            )
        )
        self.assertTrue(
            verify_cert(
                [self.ripe_o_der],
                [self.dfn_o_der, self.uni_o_der, self.hpi_o_der + b'\x00'],
                self.router1_o_der
            )
        )
        self.assertTrue(
            verify_cert(
                [self.ripe_o_der],
                [self.dfn_o_der, self.uni_o_der, self.hpi_o_der],
                self.router1_o_der + b'\x00'
            )
        )
        self.assertFalse(
            verify_cert(
                [self.ripe_o_der],
                [self.dfn_o_der, self.uni_o_der, self.hpi_o_der],
                self.router2_o_der
            )
        )
        self.assertFalse(
            verify_cert(
                [self.ripe_o_der],
                [self.dfn_o_der, self.uni_o_der, self.hpi_o_der],
                self.router3_o_der
            )
        )
        self.assertTrue(
            verify_cert(
                [self.ripe_m_der],
                [self.dfn_m_der, self.uni_m_der, self.hpi_m_der],
                self.router0_m_der
            )
        )

    def test_verify_signature(self):
        self.assertTrue(verify_signature(self.router0_o_der, self.signed_ra, self.ra_signature))
        self.assertTrue(verify_signature(self.router0_o_der + b'\x00', self.signed_ra, self.ra_signature))
        self.assertFalse(verify_signature(self.router1_o_der, self.signed_ra, self.ra_signature))
        self.assertFalse(verify_signature(self.router2_o_der, self.signed_ra, self.ra_signature))
        self.assertFalse(verify_signature(self.router3_o_der, self.signed_ra, self.ra_signature))

def run_tests():
    suite = TestSuite()
    suite.addTest(TestRAVerification('test_verify_prefix'))
    suite.addTest(TestRAVerification('test_verify_cert'))
    suite.addTest(TestRAVerification('test_verify_signature'))
    runner = TextTestRunner()
    runner.run(suite)