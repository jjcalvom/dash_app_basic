# the 0 indicates that apt-buildpack is the first in the list
#  if you change the order of buildpacks you need to update this too
export PATH=$PATH:/home/vcap/deps/0/apt/opt/mssql-tools/bin/

# point to the odbcinst.ini file
#  that file needs to have the correct path to the ODBC driver shared library
#  it should be right, but if you change the order of the buildpacks then that
#  would need updated too
export ODBCSYSINI=$HOME/odbc-cfg/
