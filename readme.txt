Use REMOTE_USER authentification in Airflow behind an Apache proxy for SSO Login

* Put file customesecurity.py into /home/airflow

* Add these lines in webserver_config.py

AUTH_TYPE = AUTH_REMOTE_USER
import sys
sys.path.append('/home/airflow')
FAB_SECURITY_MANAGER_CLASS = 'customsecurity.CustomAirflowSecurityManager'

* Configure Apache with SSL, GSS API and rewrite header rules :

<VirtualHost *:443>
  ServerName airflow.recb.fr
  ErrorLog /var/log/apache2/airflow_error.log
  CustomLog /var/log/apache2/airflow_access.log combined
  SSLEngine on
  SSLCipherSuite ALL:!aNULL:!ADH:!eNULL:!LOW:!EXP:RC4+RSA:+HIGH:+MEDIUM:+SSLv3
  SSLCertificateFile /etc/letsencrypt/live/recb.fr/cert.pem
  SSLCertificateKeyFile /etc/letsencrypt/live/recb.fr/privkey.pem
  SSLCertificateChainFile /etc/letsencrypt/live/recb.fr/fullchain.pem
  SSLCACertificateFile /etc/letsencrypt/live/recb.fr/chain.pem
  <Proxy *>
     AllowOverride None
     AuthType GSSAPI
     AuthName "GSSAPI Single Sign On Login"
     GssapiCredStore keytab:/etc/apache2/httpd.keytab
     GssapiBasicAuth On
     GssapiBasicAuthMech krb5
     GssapiAllowedMech krb5
     GssapiLocalName On
     <RequireAll>
        Require ip 10.11.12.0/24 192.168.11.0/24
        Require valid-user
     </RequireAll>
     RewriteEngine on
     RewriteCond %{REMOTE_USER} (.*)
     RewriteRule .* - [E=X_REMOTE_USER:%1]
     RequestHeader set REMOTE_USER %{X_REMOTE_USER}e
  </Proxy>
  ProxyPreserveHost On
  ProxyRequests Off
  ProxyPass / http://localhost:9666/
  ProxyPassReverse / http://localhost:9666
</VirtualHost>


