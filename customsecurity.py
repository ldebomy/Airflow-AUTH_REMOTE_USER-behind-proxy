from urllib.parse import urlencode
from urllib.parse import urljoin

import requests,logging

from flask import flash, g, redirect, request
from flask_appbuilder.baseviews import expose
from flask_appbuilder.security.views import AuthRemoteUserView
from werkzeug.wrappers import Response as WerkzeugResponse
from flask_login import login_user



__version__ = "0.1.0"
log=logging.getLogger(__name__)

class CustomAuthRemoteUserView(AuthRemoteUserView):

   @expose("/login/")
   def login(self) -> WerkzeugResponse:
      username = request.headers.get("REMOTE_USER")
      log.info(f"REMOTE_USER={username}")
      if g.user is not None and g.user.is_authenticated:
         return redirect(self.appbuilder.get_url_for_index)
      if username:
         user = self.appbuilder.sm.auth_user_remote_user(username)
         if user is None:
            flash(as_unicode(self.invalid_login_message), "warning")
         else:
            login_user(user)
      else:
         flash(as_unicode(self.invalid_login_message), "warning")
      return redirect(self.appbuilder.get_url_for_index)
                                                                           

try:
   from airflow.www.security import AirflowSecurityManager
except ImportError:
   AirflowSecurityManager = None 

class CustomAirflowSecurityManager(AirflowSecurityManager):
   authremoteuserview = CustomAuthRemoteUserView
