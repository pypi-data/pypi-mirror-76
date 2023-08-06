# define Python user-defined exceptions

# Exceptions for Mail.py library ===============================
class Error(Exception):
   """Base class for other exceptions"""
   pass
class ValueIsNone(Error):
   """Raised when this value is None"""
   pass

class EMailIsNone(Error):
   """Raised EMail value is None"""
   pass

class PasswordIsNone(Error):
   """Raised password value is None"""
   pass
class ToEMailIsNone(Error):
   """Raised ToEMail value is None"""
   pass
class SubjectIsNone(Error):
   """Raised subject value is None"""
   pass
class MessageIsNone(Error):
   """Raised EMail value is None"""
   pass
class FileLocationIsNone(Error):
   """Raised FileLocation_location value is None"""
   pass
class SMTPServerNotRegister(Error):
   """Raised SMTP Server Not Register"""
   pass
# =================================================================