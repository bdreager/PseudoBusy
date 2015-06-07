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
python -m compileall .
rm *.py
touch $MAIN
> $MAIN
printf '#!/usr/bin/env python\nimport pseudoBusy\nif __name__ == "__main__":\n    main=pseudoBusy.PseudoBusy()\n    main.run()' >> $MAIN
zip -r ../$APP *
cd ..
rm -rf $APP
mv $APP.zip $APP
echo '#!/usr/bin/env python' | cat - $APP > $APP.temp && mv $APP.temp $APP
chmod +x $APP
echo "$APP done."