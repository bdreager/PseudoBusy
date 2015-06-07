#!/bin/bash

APP=PseudoBusy
MAIN=__main__.py
if [ -f $APP ] || [ -d $APP ] 
then
	echo "$APP already exists. Stopping."
	exit 1
fi
mkdir $APP
cp *.py $APP
cd $APP
touch $MAIN
printf 'import pseudoBusy\nif __name__ == "__main__":\n    pseudoBusy.PseudoBusy(packaged=True).run()' >> $MAIN
python -m compileall .
rm *.py
zip -r ../$APP *
cd ..
rm -rf $APP
mv $APP.zip $APP
echo '#!/usr/bin/env python' | cat - $APP > $APP.temp && mv $APP.temp $APP
chmod +x $APP
echo "$APP done."