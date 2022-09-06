===========================================================================
django-mrrt: IHE Management of Radiology Report Templates (MRRT) for Django
===========================================================================

Management of Radiology Report Templates (MRRT) is an `IHE <https://www.ihe.net/>`_
standard for storing and retrieving templates in a standardized format.
django-mrrt is a re-usable Djano app supports the MRRT Retrieve [RAD-103],
Store [RAD-104], and Query [RAD-105] transactions.

Can act as "Report Template Manager"

**Security Warning**

* By default the views are unauthenticated. A swappable model is defined,
  and the urls should be wrapped to enforce some type of authentication
  (OAuth, etc)
* MRRT templates if rendered as HTML can contain unsafe content (e.g. event
  listeners, remote script/link loading).  django-mrrt plans to implement
  CSP headers and template validation in the future, but does not at present.

Usage
=====

::

   GET /IHETemplateService/
   GET /IHETemplateService/<templateUID>
   PUT /IHETemplateService/<templateUID>


References
==========

* http://www.ihe.net/uploadedFiles/Documents/Radiology/IHE_RAD_Suppl_MRRT.pdf
* https://pubmed.ncbi.nlm.nih.gov/27137649/
* https://www.radreport.org/about

