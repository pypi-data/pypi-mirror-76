########################
USPS Address Validation
########################

``pyUSPS`` provides a simple client and interface for validating addresses
using the USPS API. It is mostly taken from 
https://github.com/BuluBox/usps-api/ 

The only reason this package exists is that not all environment can build
(or be made to build, or successfully install dated wheels for) ``lxml``.
So this version uses the native ElementTree implementation in the 
standard library - no compilation required.
