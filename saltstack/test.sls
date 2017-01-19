
one:
  file.managed:
    - source: salt://app/one/two.war
    - name: /usr/local/appname4/tomcat-1/two.war
    - user: appname
    - group: appname
    - mode: 755
  cmd.run:
    - name: |
        source /etc/profile
        time=`date +%Y%m%d%M`
        if [ ! -d /usr/local/appname4/backup ];then
               mkdir /usr/local/appname4/backup
        fi
        /etc/init.d/tomcat-1 stop
        mv /usr/local/appname4/tomcat-1/webapps/two.war /usr/local/appname4/backup/two-$time.war
        rm -rf /usr/local/appname4/tomcat-1/webapps/two
        mv /usr/local/appname4/tomcat-1/two.war /usr/local/appname4/tomcat-1/webapps/two.war
        nohup sh /etc/init.d/tomcat-1 start 2>1&>/tmp/nohup.log &
    - requrie:
      - file: /usr/local/appname4/tomcat-1/two.war
