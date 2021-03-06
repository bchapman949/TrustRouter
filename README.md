TrustRouter
===========

TrustRouter is an implementation of the Secure Neighbor Discovery Protocol (SEND, [RFC 3971](http://tools.ietf.org/html/rfc3971)). Its focus is on securing router advertisements in IPv6 networks. Even though it is specified in the SEND RFC, TrustRouter does not implement CGAs and does not secure neighbor advertisements as of yet.
TrustRouter will be available as a one-click solution that can be installed on clients running Linux, Mac OS X, and Windows. In addition to that, TrustRouter will also be integrated in the router advertisement daemon radvd.

Downloads
---------
Please refer to the [Download](https://github.com/TrustRouter/TrustRouter/downloads) section for the most recent version of TrustRouter for your operating system.

The Team
--------
TrustRouter is a project developed by the following five master students of IT-Systems Engineering at [Hasso-Plattner-Institute](http://www.hpi.uni-potsdam.de) Potsdam, Germany: Robert Aschenbrenner, Michael Goderbauer, Martin Hanysz, Martin Krüger, and Thomas Zimmermann. The project is supervised by Dr. Martin von Löwis.

Do you have comments, questions, or remarks? Contact us at team@trustrouter.net. 

Version History
---------------
**v1.1 (April 18, 2012)**<br/>
- set the hop limit of CPS messages to the correct value of 255<br/>
- Windows: correctly join solicited-node multi-cast groups<br/>
- Mac: added configuration option to disable NDProtector compatibility mode

**v1.0 (March 16, 2012)**<br/>
- initial release


Configuration
-------------
On Mac OS X you can configure the following options in the configuration file located at */Library/TrustRouter/config.py*. The other operating systems will use the default values.

**MODE** - valid options are: 
*"mixedMode"* (default, process secured and unsecured RAs, but unsecured RAs cannot overwrite secured RAs), 
*"onlySend"* (process only secured RAs, unsecured RAs will be blocked), 
*"noUnsecuredAfterSecured"* (reject all unsecured RAs after receiving the first secured RA), 
*"noSend"* (process all RAs)

**ADDITIONAL_TRUST_ANCHORS**: 
list of paths to DER encoded certificates that should be used as trust anchors in addition to the standard trust anchors that ship with TrustRouter (default: empty list)

**NDPROTECTOR_COMPATIBILITY**:
boolean to enable compatibility mode for [NDprotecotor](http://amnesiak.org/NDprotector/)

Documentation
-------------
Please refer to our [wiki](https://github.com/TrustRouter/TrustRouter/wiki). It contains background information about, router advertisements, SEND, and certificate paths. In addition to that, the wiki also explains our TrustRouter implementation in greater detail and we point out some of the quirks we encountered while implementing the SEND protocol on various platforms.

Do you have more questions or comments? Do not hesitate to contact us at team@trustrouter.net.
